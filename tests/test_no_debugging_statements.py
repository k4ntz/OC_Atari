import pytest
from pathlib import Path

# Define the root directory of the project
PROJECT_PATH = Path("./ocatari/")

# Collect all Python files recursively
PYTHON_FILES = [file for file in PROJECT_PATH.rglob("*.py")]

# Generate test IDs using the file names
TEST_IDS = [f"{file.parent}/{file.name}" for file in PYTHON_FILES]


@pytest.mark.parametrize("file_path", PYTHON_FILES, ids=TEST_IDS)
def test_no_ipdb_or_print(file_path):
    # Read the content of the file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Assert no `ipdb` breakpoints
    assert "ipdb.set_trace()" not in content, f"ipdb.set_trace() found in {file_path}"

    # Assert no `print` statements
    assert "print(" not in content, f"print() statement found in {file_path}"
