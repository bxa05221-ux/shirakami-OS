import runpy


def test_oppai_adapter_demo_uses_current_runtime_boundary(capsys):
    runpy.run_path("examples/oppai_adapter_demo.py", run_name="__main__")

    output = capsys.readouterr().out
    assert "local-demo" in output
    assert "received_prompt" in output
    assert "received_protocol" in output
