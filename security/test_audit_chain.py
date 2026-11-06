from dataclasses import replace

from security.audit_chain import LocalAuditChain

def test_chain_accepts_intact_entries():
    chain = LocalAuditChain()
    chain.append("p1", "r1", "alice", "write")
    chain.append("p1", "r1", "bob", "denied")
    assert LocalAuditChain.verify(chain.snapshot(), expected_head=chain.head_digest)

def test_chain_detects_modified_entry():
    chain = LocalAuditChain()
    chain.append("p1", "r1", "alice", "write")
    chain.append("p1", "r1", "bob", "denied")
    entries = list(chain.snapshot())
    entries[0] = replace(entries[0], action="read")
    assert not LocalAuditChain.verify(tuple(entries), expected_head=chain.head_digest)

def test_chain_detects_removed_entry_with_trusted_head():
    chain = LocalAuditChain()
    chain.append("p1", "r1", "alice", "write")
    chain.append("p1", "r1", "bob", "denied")
    assert not LocalAuditChain.verify(chain.snapshot()[:-1], expected_head=chain.head_digest)

def test_chain_detects_reordered_entries():
    chain = LocalAuditChain()
    chain.append("p1", "r1", "alice", "write")
    chain.append("p1", "r1", "bob", "denied")
    entries = chain.snapshot()
    assert not LocalAuditChain.verify((entries[1], entries[0]), expected_head=chain.head_digest)
