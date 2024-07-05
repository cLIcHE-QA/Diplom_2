import allure
import requests
import helper
from data import UrlData
from data import DataAnswerMessage


class TestUserLogin:

    @allure.title(
        "Проверка успешной авторизации существующего пользователя")
    def test_created_user_login_success(self):
        user = helper.new_user_creation()
        payload = {
            "email": user["email"],
            "password": user["password"]
        }
        response = requests.post(UrlData.MAIN_PAGE + UrlData.LOGIN, data=payload)
        code = response.status_code
        name = response.json()["user"]["name"]
        helper.delete_user(user["token"])
        assert code == 200 and name == user["name"]

    @allure.title(
        "Проверка авторизации с несуществующим паролем и логином")
    def test_login_with_wrong_password_and_login_impossible(self):
        payload = helper.get_random_user_payload()
        response = requests.post(UrlData.MAIN_PAGE + UrlData.LOGIN, data=payload)
        assert response.status_code == 401 and response.json()["message"] == DataAnswerMessage.INCORRECT_DATA
