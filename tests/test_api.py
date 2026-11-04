from datetime import datetime

from backend.main import (
    health_check,
    register,
    login,
    RegisterRequest,
    LoginRequest,
)


def test_health_check_endpoint():
    res = health_check()
    assert res["status"] == "ok"


def test_api_registration_and_login():
    ts = datetime.utcnow().timestamp()
    username = f"api_test_{ts}"
    email = f"{username}@example.com"
    password = "SafePassword123!"

    reg_res = register(
        RegisterRequest(username=username, email=email, password=password)
    )
    assert "successfully" in reg_res["message"]

    login_res = login(
        LoginRequest(login_identifier=username, password=password)
    )
    assert login_res["username"] == username
    assert "user_id" in login_res
