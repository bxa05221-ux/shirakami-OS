"""Executable checks for the v1.3.0 candidate bootstrap boundary."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_PATH = ROOT / "products" / "thread-rpg-v1.3.0" / "bootstrap.py"
SPEC = spec_from_file_location("thread_rpg_v130_bootstrap", BOOTSTRAP_PATH)
assert SPEC and SPEC.loader
BOOTSTRAP = module_from_spec(SPEC)
sys.modules[SPEC.name] = BOOTSTRAP
SPEC.loader.exec_module(BOOTSTRAP)


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _commit_fixture(repo: Path, version: str = "1.3.0-candidate") -> str:
    (repo / "products/thread-rpg-v1.3.0").mkdir(parents=True)
    (repo / "protocols").mkdir()
    (repo / BOOTSTRAP.ENTRY_PATH).write_text("# ThreadRPG v1.3.0 candidate — start guide\n", encoding="utf-8")
    (repo / BOOTSTRAP.DEPENDENCY_PATH).write_text(
        f"protocol:\n  version: {version}\n", encoding="utf-8"
    )
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "ThreadRPG test")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "fixture")
    return _git(repo, "rev-parse", "HEAD")


def test_bootstrap_reports_same_commit_blobs_and_declared_version(tmp_path):
    commit = _commit_fixture(tmp_path)

    report = BOOTSTRAP.verify_repository(tmp_path, commit)

    assert report.verified is True
    assert report.resolved_commit == commit
    assert report.protocol_version == "1.3.0-candidate"
    assert report.entry_blob_sha == _git(tmp_path, "rev-parse", f"{commit}:{BOOTSTRAP.ENTRY_PATH}")
    assert report.dependency_blob_sha == _git(tmp_path, "rev-parse", f"{commit}:{BOOTSTRAP.DEPENDENCY_PATH}")


def test_bootstrap_fails_closed_for_missing_dependency(tmp_path):
    _git(tmp_path, "init")
    _git(tmp_path, "config", "user.email", "test@example.invalid")
    _git(tmp_path, "config", "user.name", "ThreadRPG test")
    (tmp_path / "README").write_text("fixture", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-m", "fixture")

    report = BOOTSTRAP.verify_repository(tmp_path, _git(tmp_path, "rev-parse", "HEAD"))

    assert report.verified is False
    assert report.failure


def test_bootstrap_fails_closed_for_wrong_version(tmp_path):
    commit = _commit_fixture(tmp_path, version="1.2.1")

    report = BOOTSTRAP.verify_repository(tmp_path, commit)

    assert report.verified is False
    assert report.protocol_version is None
