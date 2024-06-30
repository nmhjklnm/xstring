import pytest

from lazynote.manager import SimpleManager

# 定义模式列表
PATTERNS = ['clear', 'fill']

# 使用 params 创建 fixture
@pytest.fixture(params=PATTERNS)
def manager(request):
    return SimpleManager(pattern=request.param)

# 参数化测试用例
def test_traverse_components(lazyllm_package, manager):
    manager.traverse(lazyllm_package.components, skip_modules=['lazyllm.components.deploy.relay.server'])

def test_traverse_module(lazyllm_package, manager):
    manager.traverse(lazyllm_package.module)

def test_traverse_tools(lazyllm_package, manager):
    manager.traverse(lazyllm_package.tools)

def test_traverse_configs(lazyllm_package, manager):
    manager.traverse(lazyllm_package.configs)

def test_traverse_flow(lazyllm_package, manager):
    manager.traverse(lazyllm_package.flow)
