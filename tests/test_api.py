from fastapi.testclient import TestClient
import sys
import os

# Ensure src is importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import app as application

client = TestClient(application.app)


def test_get_activities():
    res = client.get('/activities')
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Expect some known activities from the seed data
    assert 'Chess Club' in data


def test_signup_and_unregister_flow():
    activity = 'Chess Club'
    test_email = 'test_student@example.com'

    # Ensure cleanup: try to unregister if exists
    client.delete(f"/activities/{activity}/unregister?email={test_email}")

    # Signup
    res = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert res.status_code == 200
    assert 'Signed up' in res.json().get('message', '')

    # Signup again should fail (already registered)
    res2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert res2.status_code == 400

    # Now unregister
    res3 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert res3.status_code == 200
    assert 'Unregistered' in res3.json().get('message', '')

    # Unregister again should 404 (not registered)
    res4 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert res4.status_code == 404
