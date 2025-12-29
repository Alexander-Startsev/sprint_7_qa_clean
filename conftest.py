import pytest, allure
from utils.clients import CourierApi, OrdersApi
from utils.generator import courier as gen_courier

@pytest.fixture(scope="session")
def courier_api():
    return CourierApi()

@pytest.fixture(scope="session")
def orders_api():
    return OrdersApi()

@pytest.fixture
def courier_data(courier_api: CourierApi):
    data = gen_courier()
    with allure.step("ПОДГОТОВКА: создать курьера"):
        courier_api.create(data)
    yield data
    with allure.step("ОЧИСТКА: удалить курьера, если удалось залогиниться"):
        lr = courier_api.login({"login": data["login"], "password": data["password"]})
        try:
            cid = lr.json().get("id")
        except Exception:
            cid = None
        if cid:
            courier_api.delete(cid)

@pytest.fixture
def created_order(orders_api: OrdersApi):
    tracks: list[int] = []
    yield tracks
    for t in tracks:
        orders_api.cancel(t)

@pytest.fixture
def created_couriers(courier_api: CourierApi):
    created: list[dict] = []
    yield created
    for courier_payload in created:
        login_response = courier_api.login({"login": courier_payload["login"], "password": courier_payload["password"]})
        try:
            courier_id = login_response.json().get("id")
        except Exception:
            courier_id = None
        if courier_id:
            courier_api.delete(courier_id)
