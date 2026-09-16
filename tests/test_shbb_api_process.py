"""Process-boundary verification for the external Shirakami API."""

import subprocess
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("uvicorn")


@pytest.fixture
def api_process():
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app:create_app",
            "--factory",
            "--host",
            "127.0.0.1",
            "--port",
            "8765",
        ],
        cwd="shbb-api",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.time() + 10
    while time.time() < deadline:
        if process.poll() is not None:
            pytest.fail("uvicorn process exited before the API became available")
        try:
            with urlopen("http://127.0.0.1:8765/docs", timeout=0.5) as response:
                if response.status == 200:
                    break
        except Exception:
            time.sleep(0.1)
    else:
        process.terminate()
        pytest.fail("API process did not become available within 10 seconds")

    try:
        yield process
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def test_observe_over_http_process(api_process):
    request = Request(
        "http://127.0.0.1:8765/observe",
        data=(
            b'{"landscape_id":"process-landscape",'
            b'"input":{"text":"process boundary"}}'
        ),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=5) as response:
        assert response.status == 200
        body = response.read().decode("utf-8")

    assert '"landscape_id":"process-landscape"' in body
    assert '"state":"observed"' in body
    assert '"evidence_id":null' in body
    assert '"transition":false' in body


def test_observe_http_rejects_invalid_input(api_process):
    request = Request(
        "http://127.0.0.1:8765/observe",
        data=b'{"landscape_id":"process-landscape","input":"invalid"}',
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with pytest.raises(HTTPError) as exc_info:
        urlopen(request, timeout=5)

    assert exc_info.value.code == 400
