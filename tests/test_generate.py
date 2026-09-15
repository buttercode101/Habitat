from types import SimpleNamespace

from habitat.generate import render_dashboard, render_landing


def test_landing_page_has_real_navigation_and_no_fake_metrics():
    html = render_landing("Test Habitat")
    assert "Don't just log what an agent did" in html
    assert 'href="/dashboard"' in html
    assert "View source on GitHub" in html
    assert "10,000" not in html
    assert "99.9%" not in html


def test_dashboard_escapes_runtime_values_and_has_supervision_sections():
    habitat = SimpleNamespace(name="<Habitat>", status="healthy", model="model<&")
    jobs = [SimpleNamespace(name="job<&", enabled=True, last_status="ok", failure_streak=0, last_error=None)]
    signals = []
    actions = [SimpleNamespace(timestamp=__import__("datetime").datetime(2026, 1, 2, 3, 4), actor="agent<&", action="run", status="ok")]
    html = render_dashboard(habitat, jobs, signals, actions, habitat.name)
    assert "Jobs &amp; health" in html
    assert "&lt;Habitat&gt;" in html
    assert "job&lt;&amp;" in html
    assert "agent&lt;&amp;" in html
    assert "/dashboard" in html
