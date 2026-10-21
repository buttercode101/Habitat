import copy
import json
from pathlib import Path

from habitat.proof_verify import verify_proof

ROOT = Path(__file__).parents[1]


def test_shared_browser_demo_has_valid_digest_but_does_not_claim_external_truth():
    proof = json.loads((ROOT / 'web/lib/demo-proof.json').read_text())
    result = verify_proof(proof)
    assert result['valid'], result['errors']
    assert result['verdict'] == 'unverified'
    assert result['assurance']['external_truth'] == 'not-established'
    changed = copy.deepcopy(proof)
    changed['claim']['evidence']['details']['summary'] = 'Changed after the proof was generated.'
    assert not verify_proof(changed)['valid']


def test_public_proof_paths_match_their_payload_and_manifest():
    public = ROOT / 'web/public'
    manifest = json.loads((public / 'proofs-manifest.json').read_text())
    listed = {run['run_id'] for runs in manifest['projects'].values() for run in runs}
    files = list((public / 'proofs').rglob('proof.json'))
    assert {p.parent.name for p in files} == listed
    for path in files:
        proof = json.loads(path.read_text())
        assert proof['claim']['run_id'] == path.parent.name
        result = verify_proof(proof)
        assert result['valid'], result['errors']
