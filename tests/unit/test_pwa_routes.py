"""
PWA route tests.
"""

import json

import yaml

from lute.app_factory import create_app


def _write_config(tmp_path):
    "Write a temporary test config."
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        yaml.dump(
            {
                "ENV": "dev",
                "DBNAME": "test_lute.db",
                "DATAPATH": str(tmp_path / "data"),
            }
        ),
        encoding="utf-8",
    )
    return config_file


def _test_client(tmp_path):
    "Create a Flask test client."
    app = create_app(str(_write_config(tmp_path)), extra_config={"TESTING": True})
    return app.test_client()


def test_manifest_route_has_installable_fields(tmp_path):
    "Manifest route serves required PWA install metadata."
    client = _test_client(tmp_path)

    response = client.get("/manifest.webmanifest")

    assert response.status_code == 200
    assert response.mimetype == "application/manifest+json"

    manifest = json.loads(response.data)
    assert manifest["name"] == "Lute"
    assert manifest["short_name"] == "Lute"
    assert manifest["start_url"] == "/"
    assert manifest["scope"] == "/"
    assert manifest["display"] == "standalone"
    assert manifest["prefer_related_applications"] is False

    icon_sizes = {icon["sizes"] for icon in manifest["icons"]}
    assert "192x192" in icon_sizes
    assert "512x512" in icon_sizes


def test_service_worker_route_is_root_scoped_and_not_cached(tmp_path):
    "Service worker route is installable at root scope."
    client = _test_client(tmp_path)

    response = client.get("/service-worker.js")

    assert response.status_code == 200
    assert response.mimetype == "application/javascript"
    assert response.headers["Service-Worker-Allowed"] == "/"
    assert "no-store" in response.headers["Cache-Control"]

    script = response.data.decode("utf-8")
    assert "LUTE_OFFLINE_URL" in script
    assert "/static/js/never_cache/" in script


def test_offline_page_is_simple_fallback(tmp_path):
    "Offline page is available for the service worker fallback."
    client = _test_client(tmp_path)

    response = client.get("/offline")

    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert "Lute is offline" in body
    assert 'rel="manifest"' in body


def test_base_template_links_manifest_and_pwa_register(tmp_path):
    "Base pages expose the manifest and registration script."
    client = _test_client(tmp_path)

    response = client.get("/")

    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert 'rel="manifest" href="/manifest.webmanifest"' in body
    assert "/static/js/pwa-register.js" in body
