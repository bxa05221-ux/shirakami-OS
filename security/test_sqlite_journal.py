"""Synthetic-only atomic persistence and restart tests."""
import sqlite3

import pytest

from security.sqlite_journal import AtomicEvaluationJournal

def test_encrypted_record_and_audit_survive_restart(tmp_path):
    path = tmp_path / "journal.sqlite3"
    journal = AtomicEvaluationJournal(path)
    head = journal.append_encrypted_record(
        record_id="r1", project_id="p1", owner_id="alice",
        ciphertext=b"encrypted-fixture", key_version="v1",
        occurred_at="2026-11-06T09:00:00+00:00",
    )
    reopened = AtomicEvaluationJournal(path)
    assert reopened.load_encrypted_record("r1", "p1") == (b"encrypted-fixture", "v1")
    assert reopened.load_encrypted_record("r1", "p2") is None
    assert reopened.verify(expected_head=head)
    assert not reopened.verify(expected_head="0" * 64)

def test_duplicate_record_rolls_back_audit_and_record(tmp_path):
    journal = AtomicEvaluationJournal(tmp_path / "journal.sqlite3")
    args = dict(record_id="r1", project_id="p1", owner_id="alice",
                ciphertext=b"encrypted-fixture", key_version="v1",
                occurred_at="2026-11-06T09:00:00+00:00")
    head = journal.append_encrypted_record(**args)
    with pytest.raises(sqlite3.IntegrityError):
        journal.append_encrypted_record(**args)
    assert journal.verify(expected_head=head)

def test_modified_audit_is_detected_and_blocks_next_write(tmp_path):
    path = tmp_path / "journal.sqlite3"
    journal = AtomicEvaluationJournal(path)
    head = journal.append_encrypted_record(
        record_id="r1", project_id="p1", owner_id="alice",
        ciphertext=b"encrypted-fixture", key_version="v1",
        occurred_at="2026-11-06T09:00:00+00:00",
    )
    with sqlite3.connect(path) as db:
        db.execute("UPDATE audit SET action='altered' WHERE sequence=1")
    assert not journal.verify(expected_head=head)
    from security.sqlite_journal import PersistenceIntegrityError
    with pytest.raises(PersistenceIntegrityError):
        journal.append_encrypted_record(
            record_id="r2", project_id="p1", owner_id="alice",
            ciphertext=b"encrypted-fixture-2", key_version="v1",
            occurred_at="2026-11-06T09:01:00+00:00",
        )
    assert journal.load_encrypted_record("r2", "p1") is None

def test_ciphertext_tampering_is_detected_before_read(tmp_path):
    path = tmp_path / "journal.sqlite3"
    journal = AtomicEvaluationJournal(path)
    head = journal.append_encrypted_record(
        record_id="r1", project_id="p1", owner_id="alice",
        ciphertext=b"encrypted-fixture", key_version="v1",
        occurred_at="2026-11-06T09:00:00+00:00",
    )
    with sqlite3.connect(path) as db:
        db.execute("UPDATE records SET ciphertext=? WHERE record_id='r1'", (b"tampered",))
    assert not journal.verify(expected_head=head)
    from security.sqlite_journal import PersistenceIntegrityError
    with pytest.raises(PersistenceIntegrityError):
        journal.load_encrypted_record("r1", "p1", expected_head=head)

def test_deleted_record_is_detected(tmp_path):
    path = tmp_path / "journal.sqlite3"
    journal = AtomicEvaluationJournal(path)
    head = journal.append_encrypted_record(
        record_id="r1", project_id="p1", owner_id="alice",
        ciphertext=b"encrypted-fixture", key_version="v1",
        occurred_at="2026-11-06T09:00:00+00:00",
    )
    with sqlite3.connect(path) as db:
        db.execute("DELETE FROM records WHERE record_id='r1'")
    assert not journal.verify(expected_head=head)

def test_read_without_independently_trusted_head_fails_closed(tmp_path):
    journal = AtomicEvaluationJournal(tmp_path / "journal.sqlite3")
    journal.append_encrypted_record(
        record_id="r1", project_id="p1", owner_id="alice",
        ciphertext=b"encrypted-fixture", key_version="v1",
        occurred_at="2026-11-06T09:00:00+00:00",
    )
    from security.sqlite_journal import PersistenceIntegrityError
    with pytest.raises(PersistenceIntegrityError, match="trusted external audit head"):
        journal.load_encrypted_record("r1", "p1")

def test_key_version_tampering_is_detected(tmp_path):
    path = tmp_path / "journal.sqlite3"
    journal = AtomicEvaluationJournal(path)
    head = journal.append_encrypted_record(
        record_id="r1", project_id="p1", owner_id="alice",
        ciphertext=b"encrypted-fixture", key_version="v1",
        occurred_at="2026-11-06T09:00:00+00:00",
    )
    with sqlite3.connect(path) as db:
        db.execute("UPDATE records SET key_version='v2' WHERE record_id='r1'")
    assert not journal.verify(expected_head=head)
