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
REPO_DIR = Path("LazyLLM")  # 相对路径到项目根目录下的 LazyLLM 目录

@pytest.fixture(scope="session", autouse=True)
def clone_repo():
    if not REPO_DIR.exists():
        try:
            result = subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"克隆仓库出错: {e.stderr}")
            raise
    yield
    # 清理仓库
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)

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
