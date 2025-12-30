import pytest
import allure
from utils.generator import courier as gen_courier


@allure.feature("Courier")
class TestCourierCreate:

    @allure.title("Можно создать курьера (201, ok=true)")
    def test_courier_can_be_created(self, courier_api, created_couriers):
        # Подготовка данных и действий
        courier_payload = gen_courier()
        created_couriers.append(courier_payload)

        response = courier_api.create(courier_payload)
        response_body = response.json()

        # Блок проверок — только assert'ы
        assert response.status_code == 201
        assert isinstance(response_body, dict)
        assert response_body.get("ok") is True

    @allure.title("Нельзя создать двух одинаковых курьеров (409, есть message)")
    def test_cannot_create_same_twice(self, courier_api, created_couriers):
        # Подготовка данных и действий
        courier_payload = gen_courier()
        created_couriers.append(courier_payload)

        first_response = courier_api.create(courier_payload)
        duplicate_response = courier_api.create(courier_payload)

        first_body = first_response.json()
        duplicate_body = duplicate_response.json()

        # Блок проверок — только assert'ы
        assert first_response.status_code == 201
        assert isinstance(first_body, dict)
        assert first_body.get("ok") is True

        assert duplicate_response.status_code == 409
        assert isinstance(duplicate_body, dict)
        assert "message" in duplicate_body

    @pytest.mark.parametrize("key", ["login", "password"], ids=["no_login", "no_password"])
    @allure.title("Создание курьера без обязательного поля: {key} → 400 + message")
    def test_required_fields(self, courier_api, key):
        # Подготовка
        courier_payload = gen_courier()
        courier_payload.pop(key)

        response = courier_api.create(courier_payload)
        response_body = response.json()

        # Проверки
        assert response.status_code == 400
        assert isinstance(response_body, dict)
        assert "message" in response_body

