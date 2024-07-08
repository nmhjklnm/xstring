"""Test config"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner


@pytest.fixture()
def clicker():
    """clicker fixture"""
    yield CliRunner()


REPO_URL = "https://github.com/LazyAGI/LazyLLM"
TARGET =None# "3998f72825d3022d67c3f543881259da4d768fbd"  # 这可以是提交哈希或标签名
REPO_DIR = Path("LazyLLM")

@pytest.fixture(scope="session", autouse=True)
def clone_repo():
    if not REPO_DIR.exists():
        try:
            # 执行克隆，获取最近的提交
            subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)], check=True, capture_output=True, text=True)
            # 切换到指定的提交或标签
            if TARGET:
                subprocess.run(["git", "checkout", TARGET], cwd=str(REPO_DIR), check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"操作出错: {e.stderr}")
            raise
    yield
    # 清理仓库
    # if REPO_DIR.exists():
    #     shutil.rmtree(REPO_DIR)

@pytest.fixture(scope="session")
def lazyllm_package():
    # 将仓库路径添加到 sys.path 以便导入
    project_root = Path(__file__).parent.parent.resolve()  # 获取项目根目录
    
    lazyllm_path = project_root / REPO_DIR
    
    docs_path = lazyllm_path / 'lazyllm' / 'docs'

    sys.path.append(str(docs_path))
    sys.path.append(str(lazyllm_path))

    import lazyllm
    return lazyllm
