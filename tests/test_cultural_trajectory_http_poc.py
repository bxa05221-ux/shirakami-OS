"""Contract checks for the local-only observation HTTP PoC."""
import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from runtime.cultural_trajectory_http_poc import ObservationHandler, project_payload


SYNTHETIC = {"messages": [
    {"id": "synthetic:001", "text": "原文  \nそのまま"},
    {"id": "synthetic:002", "text": "別の見方"},
]}


def test_projection_contract():
    result = project_payload(SYNTHETIC)
    assert result["status"] == "candidate_only"
    assert result["verification"] == "unverified"
    assert result["evidence_resolution"] == "not_implemented"
    assert result["posts"][0]["original_text"] == "原文  \nそのまま"
    assert result["relations"][0]["assertion"]["verification"] == "unverified"


@pytest.mark.parametrize("payload", [{}, {"messages": []}, {"messages": [{"id": "x", "text": "a"}]}, {"messages": [{"id": "x", "text": "a"}, {"id": "y", "text": "b", "verified": True}]}])
def test_reject_invalid(payload):
    with pytest.raises(ValueError):
        project_payload(payload)


def test_real_loopback_http():
    server = ThreadingHTTPServer(("127.0.0.1", 0), ObservationHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        endpoint = f"http://127.0.0.1:{server.server_port}/v0/observe"
        request = Request(endpoint, json.dumps(SYNTHETIC).encode(), {"Content-Type": "application/json"}, method="POST")
        with urlopen(request, timeout=2) as response:
            result = json.load(response)
        assert result == project_payload(SYNTHETIC)
        assert result["verification"] == "unverified"
        invalid = Request(endpoint, b'{"messages":[]}', {"Content-Type": "application/json"}, method="POST")
        with pytest.raises(HTTPError) as exc:
            urlopen(invalid, timeout=2)
        assert exc.value.code == 400
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
