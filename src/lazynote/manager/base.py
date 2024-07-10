import inspect
import textwrap
from abc import ABC, abstractmethod
from typing import Optional

import libcst as cst
from pydantic import BaseModel, Field

from lazynote.parser import BaseParser
from lazynote.schema import MemberType, get_member_type
from lazynote.editor import BaseEditor  # Lazy import to avoid circular dependency
from enum import Enum
import importlib
import pkgutil
import asyncio
import traceback

class DocstringMode(str, Enum):
    TRANSLATE = "translate"
    POLISH = "polish"
    CLEAR = "clear"
    FILL = "fill"


class BaseManager(BaseModel, ABC):
    """
    执行器，用于修改模块的文档字符串，目前只支持模块级别或文件级别。

    子类需要重写 gen_docstring 方法以生成自定义的文档字符串。
    """

    parser: Optional[BaseParser] = Field(default_factory=BaseParser)
    pattern: DocstringMode
    skip_on_error: bool = False  # 添加类属性


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.parser is None:
            self.parser = BaseParser(skip_modules=kwargs.get('skip_modules', []))
        self.skip_on_error = kwargs.get('skip_on_error', self.skip_on_error)


    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def gen_docstring(self, old_docstring: Optional[str], node_code: str) -> str:
        """
        生成新的文档字符串。子类必须实现此方法以实现自定义逻辑。

        :param old_docstring: 旧的文档字符串
        :param node_code: 节点代码
        :return: 新的文档字符串
        """
        pass

    @staticmethod
    def is_defined_in_module(member, module):
        if hasattr(member, '__module__'):
            return member.__module__ == module.__name__
        elif isinstance(member, property):
            return member.fget.__module__ == module.__name__
        elif isinstance(member, staticmethod):
            return member.__func__.__module__ == module.__name__
        elif isinstance(member, classmethod):
            return member.__func__.__module__ == module.__name__
        elif hasattr(member, '__wrapped__'):
            return member.__wrapped__.__module__ == module.__name__
        return False


    def _write_code_to_file(self, module, code: str):
        # 获取模块文件的路径
        module_file_path = inspect.getfile(module)

        # 将修改后的代码写回文件
        with open(module_file_path, 'w', encoding='utf-8') as file:
            file.write(code)

    def traverse(self, obj, skip_modules=None):
        if skip_modules is None:
            skip_modules = []

        if get_member_type(obj) == MemberType.PACKAGE:
            # 遍历包中的所有模块和子包
            for importer, modname, ispkg in pkgutil.walk_packages(obj.__path__, obj.__name__ + "."):
                if any(modname.startswith(skip_mod) for skip_mod in skip_modules):
                    continue  # 跳过不需要处理的模块及其子模块
                if ispkg:
                    # 包级别docstrings暂不处理
                    continue

                try:
                    submodule = importlib.import_module(modname)
                    self.parser.parse(submodule, self)
                except Exception as e:
                    if self.skip_on_error:
                        print(f"Skipping {modname} due to import error: {e}")
                    else:
                        raise e

        elif get_member_type(obj) == MemberType.MODULE:
            # 处理单个模块或其他类型的对象
            try:
                self.parser.parse(obj, self)
            except Exception as e:
                if self.skip_on_error:
                    print(f"Skipping {obj.__name__} due to import error: {e}")
                else:
                    raise e

    async def atraverse(self, obj, skip_modules=None, max_concurrency=10):
        if skip_modules is None:
            skip_modules = []

        semaphore = asyncio.Semaphore(max_concurrency)

        async def sem_task(task):
            async with semaphore:
                try:
                    await task
                except Exception as e:
                    if self.skip_on_error:
                        print(f"Skipping task due to error: {e}")
                        traceback.print_exc()
                    else:
                        print(f"Task failed with error: {e}")
                        raise e

        loop = asyncio.get_event_loop()

        if get_member_type(obj) == MemberType.PACKAGE:
            tasks = []
            for importer, modname, ispkg in pkgutil.walk_packages(obj.__path__, obj.__name__ + "."):
                if any(modname.startswith(skip_mod) for skip_mod in skip_modules):
                    continue  # 跳过不需要处理的模块及其子模块
                if ispkg:
                    continue  # 包级别docstrings暂不处理

                try:
                    submodule = importlib.import_module(modname)
                    tasks.append(sem_task(loop.run_in_executor(None, self.parser.parse, submodule, self)))
                except Exception as e:
                    if self.skip_on_error:
                        traceback.print_exc()
                        print(f"Skipping {modname} due to import error: {e}")
                    else:
                        raise e
            await asyncio.gather(*tasks)

        elif get_member_type(obj) == MemberType.MODULE:
            try:
                task = loop.run_in_executor(None, self.parser.parse, obj, self)
                await sem_task(task)
            except Exception as e:
                if self.skip_on_error:
                    traceback.print_exc()
                    print(f"Skipping {obj.__name__} due to import error: {e}")
                else:
                    raise e


    def modify_docstring(self, module):

        try:
            source_code = inspect.getsource(module)
            source_code = textwrap.dedent(source_code)  # 去除多余的缩进
            tree = cst.parse_module(source_code)
            transformer = BaseEditor(
                gen_docstring=self.gen_docstring, pattern=self.pattern,module=module)
            modified_tree = tree.visit(transformer)
            self._write_code_to_file(module, modified_tree.code)
            return modified_tree.code
        except Exception as e:
            if self.skip_on_error:
                print(f"Skipping module {module.__name__} due to error: {e}")
                return None
            else:
                traceback.print_exc()  # 打印完整的堆栈跟踪
                raise e
