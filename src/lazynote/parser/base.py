import importlib
import pkgutil
from typing import Callable, Dict

from lazynote.schema import MemberType, get_member_type


class BaseParser:
    def __init__(self, skip_modules):
        self.parsers: Dict[MemberType, Callable] = {
            MemberType.PACKAGE: self.parse_package,
            MemberType.MODULE: self.parse_module,
            MemberType.CLASS: self.parse_class,
            MemberType.METHOD: self.parse_method,
            MemberType.FUNCTION: self.parse_function,
            MemberType.PROPERTY: self.parse_property,
            MemberType.ATTRIBUTE: self.parse_attribute
        }

    def parse(self, member, module, manager, **kwargs):
        member_type = get_member_type(member)
        parser = self.parsers.get(member_type)
        if parser:
            parser(member, module, manager, **kwargs)

    def parse_package(self, package, module, manager, **kwargs):
        skip_modules = kwargs.get('skip_modules', [])
        print(f"Package: {package.__name__}")
        for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            if modname in skip_modules:
                print(f"Skipping module: {modname}")
                continue
            try:
                submodule = importlib.import_module(modname)
                manager.traverse(submodule, skip_modules)
            except Exception as e:
                print(f"Error importing {modname}: {e}")

    def parse_module(self, module, parent_module, manager,**kwargs):
        print(f"--Module: {module.__name__}--")
        new_code = manager.modify_docstring(module)
        print(new_code[:20])

    def parse_class(self, cls, module, manager,**kwargs):
        print(f"Class: {cls.__name__}")

    def parse_method(self, method, module, manager,**kwargs):
        print(f"  Method: {method.__name__}")

    def parse_function(self, func, module, manager,**kwargs):
        print(f"Function: {func.__name__}")

    def parse_property(self, prop, module, manager,**kwargs):
        print(f"  Property: {prop}")

    def parse_attribute(self, attr, module, manager,**kwargs):
        print(f"  Attribute: {attr}")
