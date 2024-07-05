import allure
import requests
from data import UrlData
from data import DataExample
from data import DataAnswerMessage
import helper


class TestOrderCreation:
    @allure.title("Проверка создания заказа с существующими ингредиентами у авторизованного пользователя")
    def test_create_order_with_correct_ingredients_authorized_user_success(self):
        payload = helper.new_user_login()
        ingredients = helper.creation_list_of_ingredients()
        list_of_ingredient = [ingredients[0], ingredients[1], ingredients[2]]
        payload_order = {"ingredients": list_of_ingredient}
        response = requests.post(UrlData.MAIN_PAGE + UrlData.ORDER,
                                 data=payload_order,
                                 headers={'Authorization': payload["token"]})
        code = response.status_code
        order = response.json()["order"]
        helper.delete_user(payload["token"])
        assert code == 200 and "number" in order

    @allure.title("Проверка создания заказа с существующими ингредиентами у неавторизованного пользователя")
    def test_create_order_with_correct_ingredients_unauthorized_user_success(self):
        ingredients = helper.creation_list_of_ingredients()
        list_of_ingredient = [ingredients[0], ingredients[1], ingredients[2]]
        payload_order = {"ingredients": list_of_ingredient}
        response = requests.post(UrlData.MAIN_PAGE + UrlData.ORDER,
                                 data=payload_order)
        code = response.status_code
        order = response.json()["order"]
        assert code == 200 and "number" in order

    @allure.title("Проверка создания заказа без ингредиентов у авторизованного пользователя")
    def test_create_order_without_ingredients_authorized_user_impossible(self):
        payload = helper.new_user_login()
        response = requests.post(UrlData.MAIN_PAGE + UrlData.ORDER,
                                 headers={'Authorization': payload["token"]})
        code = response.status_code
        message = response.json()["message"]
        helper.delete_user(payload["token"])
        assert code == 400 and message == DataAnswerMessage.NEED_INGREDIENT_ID

    @allure.title("Проверка создания заказа без ингредиентов у неавторизованного пользователя")
    def test_create_order_without_ingredients_unauthorized_user_impossible(self):
        response = requests.post(UrlData.MAIN_PAGE + UrlData.ORDER)
        code = response.status_code
        message = response.json()["message"]
        assert code == 400 and message == DataAnswerMessage.NEED_INGREDIENT_ID

    @allure.title("Проверка создания заказа с неверным хэшем ингредиентов у авторизованного пользователя")
    def test_create_order_with_incorrect_ingredients_authorized_user_impossible(self):
        payload = helper.new_user_login()
        payload_order = {"ingredients": DataExample.WRONG_HASH_INGREDIENTS}
        response = requests.post(UrlData.MAIN_PAGE + UrlData.ORDER,
                                 data=payload_order,
                                 headers={'Authorization': payload["token"]})
        code = response.status_code
        helper.delete_user(payload["token"])
        assert code == 500

    @allure.title("Проверка создания заказа с неверным хэшем ингредиентов у неавторизованного пользователя")
    def test_create_order_with_incorrect_ingredients_unauthorized_user_success(self):
        payload_order = {"ingredients": DataExample.WRONG_HASH_INGREDIENTS}
        response = requests.post(UrlData.MAIN_PAGE + UrlData.ORDER,
                                 data=payload_order)
        code = response.status_code
        assert code == 500
