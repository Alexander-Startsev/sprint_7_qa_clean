import pytest, allure

@allure.feature("Courier")
class TestCourierLogin:

    @allure.title("Курьер может авторизоваться (200, ответ содержит id)")
    def test_login_returns_id(self, courier_api, courier_data):
        response = courier_api.login({"login": courier_data["login"], "password": courier_data["password"]})
        assert response.status_code == 200
        response_body = response.json()
        assert isinstance(response_body.get("id"), int)

    @pytest.mark.parametrize("missing_field", ["login", "password"], ids=["no_login","no_password"])
    @allure.title("Логин без обязательного поля: {missing_field} → 400 + message")
    def test_login_missing_field(self, courier_api, missing_field):
        login_payload = {"password": "x"} if missing_field == "login" else {"login": "x"}
        response = courier_api.login(login_payload)
        assert response.status_code == 400
        response_body = response.json()
        assert isinstance(response_body, dict) and "message" in response_body

    @allure.title("Логин с неверным паролем → 404 + message")
    def test_login_wrong_password(self, courier_api, courier_data):
        response = courier_api.login({"login": courier_data["login"], "password": "wrong"})
        assert response.status_code == 404
        response_body = response.json()
        assert isinstance(response_body, dict) and "message" in response_body

    @allure.title("Логин несуществующего пользователя → 404 + message")
    def test_login_nonexistent(self, courier_api):
        response = courier_api.login({"login": "ghost_user", "password": "x"})
        assert response.status_code == 404
        response_body = response.json()
        assert isinstance(response_body, dict) and "message" in response_body
