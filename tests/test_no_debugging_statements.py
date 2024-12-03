import pytest

@pytest.fixture
def source_files(request):
    files = request.config.getoption("--file_path")
    return files.split()

def pytest_addoption(parser):
    parser.addoption("--file_path", action="store", default="")

@pytest.mark.parametrize("file_path", source_files())
def test_no_debugging_statements(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "ipdb.set_trace()" in line or "print(" in line:
                pytest.fail(f"Debugging statement found in {file_path} at line {i + 1}: {line.strip()}")
