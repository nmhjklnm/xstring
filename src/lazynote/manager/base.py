import inspect
import textwrap
from abc import ABC, abstractmethod
from typing import Optional

import libcst as cst
from pydantic import BaseModel, Field

from lazynote.parser import BaseParser
from lazynote.schema import MemberType, get_member_type


class BaseManager(BaseModel, ABC):
    """
    执行器，用于修改模块的文档字符串，目前只支持模块级别或文件级别。

    子类需要重写 gen_docstring 方法以生成自定义的文档字符串。
    """

    parser: Optional[BaseParser] = Field(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.parser is None:
            self.parser = BaseParser(skip_modules=kwargs.get('skip_modules', []))

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
    
    @abstractmethod
    def modify_docstring(self, module):
        pass

    def _write_code_to_file(self, module, code: str):
        # 获取模块文件的路径
        module_file_path = inspect.getfile(module)

        # 将修改后的代码写回文件
        with open(module_file_path, 'w', encoding='utf-8') as file:
            file.write(code)

    def traverse(self, obj, skip_modules=None):
        if skip_modules is None:
            skip_modules = []

        member_type = get_member_type(obj)
        module = inspect.getmodule(obj)

        if module and module.__name__ in skip_modules:
            print(f"Skipping module: {module.__name__}")
            return

        # 直接使用 BaseParser 作为工具类
        self.parser.parse(obj, module, self,skip_modules=skip_modules)

        if member_type in (MemberType.PACKAGE):
            for name, member in inspect.getmembers(obj):
                if self.is_defined_in_module(member, module):
                    self.traverse(member, skip_modules=skip_modules)
