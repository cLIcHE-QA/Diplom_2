import allure
import requests

from data import UrlData
from data import DataExample
from data import DataAnswerMessage
import helper


class TestGetUserOrder:
    @allure.title("Проверка получения заказа у авторизованного пользователя")
    def test_get_order_authorized_user(self):
        payload = helper.new_user_login()
        for i in range(DataExample.QUANTITY_ORDERS):
            helper.creation_order_authorized_user(payload["token"])
        response = requests.get(UrlData.MAIN_PAGE + UrlData.ORDER,
                                headers={'Authorization': payload["token"]})
        code = response.status_code
        orders = response.json()["orders"]
        helper.delete_user(payload["token"])
        assert code == 200 and len(orders) == DataExample.QUANTITY_ORDERS

    @allure.title("Проверка получения заказа у неавторизованного пользователя")
    def test_get_order_unauthorized_user(self):
        response = requests.get(UrlData.MAIN_PAGE + UrlData.ORDER)
        code = response.status_code
        orders = response.json()["message"]
        assert code == 401 and orders == DataAnswerMessage.UNAUTHORISED_USER
