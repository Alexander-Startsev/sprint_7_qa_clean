import allure

@allure.feature("Orders")
class TestOrdersList:

    @allure.title("Список заказов возвращается (200) и содержит массив orders")
    def test_list_contains_orders(self, orders_api):
        response = orders_api.list()
        assert response.status_code == 200
        response_body = response.json()
        assert isinstance(response_body, dict)
        assert isinstance(response_body.get("orders"), list)
