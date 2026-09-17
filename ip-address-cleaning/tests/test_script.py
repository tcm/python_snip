import subprocess
import json

def test_script_output():
    result = subprocess.run(
        ["python3", "my_script.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)

    assert data["status"] == "ok"