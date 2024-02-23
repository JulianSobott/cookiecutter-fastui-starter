import subprocess
from pathlib import Path
from pytest import fixture
import time
from cookiecutter.main import cookiecutter
import requests

temp_dir = Path("/tmp/fastui_starter_test")


@fixture
def create_repo():
    temp_dir.mkdir(parents=True, exist_ok=True)
    template_path = Path(__file__).parent.parent.absolute()
    cookiecutter(
        str(template_path), no_input=True, output_dir=str(temp_dir)
    )
    yield temp_dir


def test_app_works(create_repo):
    assert (create_repo / "fastui_starter" / "fastui_starter" / "main.py").exists()
    assert (create_repo / "fastui_starter" / "fastui_starter_app" / "src" / "App.tsx").exists()
    project = create_repo / "fastui_starter"
    res = subprocess.run(["poetry", "install"], cwd=project, capture_output=True)
    if res.returncode != 0:
        raise Exception(res.stdout.decode())
    assert res.returncode == 0
    res = subprocess.run(["npm", "install"], cwd=project / "fastui_starter_app", capture_output=True)
    if res.returncode != 0:
        raise Exception(res.stdout.decode())
    assert res.returncode == 0

    # TODO: this is a hack until the fastui-bootstrap package is fixed
    fix_fastui_bootstrap(project / "fastui_starter_app" / "node_modules")

    res = subprocess.run(["npm", "run", "build"], cwd=project / "fastui_starter_app", capture_output=True)
    if res.returncode != 0:
        raise Exception(res.stdout.decode())
    assert res.returncode == 0
    assert (project / "dist" / "index.html").exists()
    process = subprocess.Popen(["poetry", "run", "uvicorn", "fastui_starter.main:app"], cwd=project)
    process.poll()
    time.sleep(3)
    response = requests.get("http://127.0.0.1:8000/")
    assert "FastUI Starter" in response.text
    response = requests.get("http://127.0.0.1:8000/assets/index.css")
    assert response.status_code == 200
    # kill the server
    process.kill()


def fix_fastui_bootstrap(node_modules: Path):
    project_json = node_modules / "@pydantic" / "fastui-bootstrap" / "package.json"
    # replace: "main": "dist/index.js", with "main": "dist/npm-fastui-bootstrap/src/index.js",
    with open(project_json, "r") as f:
        text = f.read()
    text = text.replace("dist/index.d.ts", "dist/npm-fastui-bootstrap/src/index.d.ts")
    text = text.replace("dist/index.js", "dist/npm-fastui-bootstrap/src/index.js")
    with open(project_json, "w") as f:
        f.write(text)
