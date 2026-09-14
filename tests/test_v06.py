import json, subprocess, sys
from habitat.schema import Habitat, Action, Job, utcnow
from habitat.store import Store
from habitat.claims import Claim
from habitat.verify import verify_claim
from habitat.runtime import due, run_once
from habitat.adapters import JSONFileEvidenceAdapter


def setup(tmp_path):
    s=Store(tmp_path/'h.db'); now=utcnow(); s.save_habitat(Habitat('h','H')); s.save_job(Job('j','h','J','every 1 sec',True,'echo ok')); return s


def test_run_id_prevents_stale_claim_match(tmp_path):
    s=setup(tmp_path); s.save_action(Action('old','h',utcnow(),'agent','run_job','ok','j',{},'run-old'))
    c=Claim.new('h','new run','j','run_job','ok'); c.run_id='run-new'; s.save_claim(c); assert verify_claim(s,c).status=='rejected'; s.close()


def test_signal_resolves_after_recovery(tmp_path):
    s=setup(tmp_path); j=s.jobs()[0]; j.command='python -c "import sys; sys.stderr.write(\'auth failed\'); sys.exit(1)"'; s.save_job(j); run_once(s); run_once(s); run_once(s); assert s.habitat().status=='needs_attention'
    j=s.jobs()[0]; j.command='echo recovered'; s.save_job(j); run_once(s); assert s.active_signals()==[]; assert s.habitat().status=='healthy'; s.close()


def test_simple_schedule_due(tmp_path):
    s=setup(tmp_path); assert due(s.jobs()[0]); s.close()


def test_external_evidence_predicate(tmp_path):
    f=tmp_path/'e.json'; f.write_text(json.dumps({'result':{'status':'ok','id':'42'}})); s=setup(tmp_path); c=Claim.new('h','external'); s.save_claim(c); out=verify_claim(s,c,JSONFileEvidenceAdapter(f),'result',{'status':'ok','id':'42'}); assert out.status=='verified'; c=Claim.new('h','external'); s.save_claim(c); out=verify_claim(s,c,JSONFileEvidenceAdapter(f),'result',{'status':'failed'}); assert out.status=='rejected'; s.close()


def test_package_metadata_and_entrypoint():
    import tomllib
    data=tomllib.loads(open('pyproject.toml','rb').read().decode())
    assert data['project']['version']=='1.2.0'
    assert data['project']['scripts']['habitat']=='habitat.__main__:main'
