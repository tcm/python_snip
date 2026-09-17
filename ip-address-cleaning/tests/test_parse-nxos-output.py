import subprocess
import json
from pathlib import Path


def run_script(filename):
    
    basepath = Path(__file__).parent
    inputfile = basepath / "data" / filename

    return subprocess.run(
        ["python3", "parse-nxos-output.py", "--file", inputfile, "--json"],
        capture_output=True,
        text=True
    )


def test_script_returns_valid_json():
    result = run_script("input.txt")

    assert result.returncode == 0, f"Script failed: {result.stderr}"

    # Validate JSON
    data = json.loads(result.stdout)

    assert isinstance(data, dict)
    assert "linecount" in data
    assert "id" in data
    assert "macaddress" in data
    assert "ipaddress" in data
    assert "vlan" in data
    assert "timestamp" in data


def test_script_output_ok():
    result = run_script("input1.txt")
    data = json.loads(result.stdout)

    assert data["linecount"] == 28
    assert data ["id"] == "5a693341c87555687079ccb08c4c3026458cc69f"
    assert data ["ipaddress"] == "128.85.3.41"
    assert data ["macaddress"] == "0000.1c9f.f4cd"
    assert data ["vlan"] == "vlan1220"