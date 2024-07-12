import pytest

from xstring.manager import SimpleManager

# 定义模式列表
PATTERNS = ['clear','fill']

# 使用 params 创建 fixture
@pytest.fixture(params=PATTERNS)
def manager(request):
    return SimpleManager(pattern=request.param)

# 参数化测试用例
def test_traverse_components(lazyllm_package, manager):
    manager.traverse(lazyllm_package.components, skip_modules=[
        'lazyllm.components.deploy.relay.server',
        'lazyllm.components.deploy.lmdeploy',
        'lazyllm.components.deploy.relay.base',
        'lazyllm.components.finetune.easyllm'
    ])

def test_traverse_module(lazyllm_package, manager):
    manager.traverse(lazyllm_package.module, skip_modules=[
    ])

def test_traverse_tools(lazyllm_package, manager):
    manager.traverse(lazyllm_package.tools,skip_modules=[
        'lazyllm.tools.rag.component.bm25_retriever'
    ])

def test_traverse_configs(lazyllm_package, manager):
    manager.traverse(lazyllm_package.configs)

def test_traverse_flow(lazyllm_package, manager):
    manager.traverse(lazyllm_package.flow,skip_modules=[
    ])
