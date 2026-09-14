from habitat.claims import Claim
from habitat.schema import Action, utcnow
from habitat.store import Store
from habitat.verify_api import proof_status, verify_and_prove


def _store(tmp_path):
    from habitat.schema import Habitat
    s = Store(tmp_path / 'habitat.db')
    now = utcnow()
    s.save_habitat(Habitat('h1', 'test', 'unknown', now, now))
    return s


def test_proof_status_is_machine_readable(tmp_path):
    s = _store(tmp_path)
    c = Claim.new('h1', 'job completed', 'j1', 'deploy', 'ok')
    c.run_id = 'run-1'
    s.save_claim(c)
    s.save_action(Action('a1', 'h1', utcnow(), 'agent', 'deploy', 'ok', 'j1', {'version': '1'}, 'run-1'))
    result = verify_and_prove(s, c.id)
    assert result['verdict'] == 'verified'
    assert result['proof']['content_sha256']
    assert result['proof']['ledger']['integrity'] == 'intact'
    s.close()


def test_tampered_ledger_yields_inconclusive_proof(tmp_path):
    s = _store(tmp_path)
    c = Claim.new('h1', 'job completed', 'j1', 'deploy', 'ok')
    c.run_id = 'run-1'
    s.save_claim(c)
    s.save_action(Action('a1', 'h1', utcnow(), 'agent', 'deploy', 'ok', 'j1', {}, 'run-1'))
    s.conn.execute("UPDATE action SET status='failed' WHERE id='a1'")
    s.conn.commit()
    result = proof_status(s, c.id)
    assert result['verdict'] == 'pending'
    assert result['ledger_integrity'] == 'failed'
    s.close()
