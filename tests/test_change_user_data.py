import allure
import pytest
import requests
from data import UrlData
import helper
from data import DataAnswerMessage


class TestChangeUserData:
    @allure.title("Проверка изменения почты и имени у авторизованного пользователя")
    @pytest.mark.parametrize('change_field', ["email", "name"])
    def test_change_authorized_user_name_email_success(self, change_field):
        payload = helper.new_user_login()
        changed_payload = {change_field: helper.get_random_email()}
        response = requests.patch(UrlData.MAIN_PAGE + UrlData.USER,
                                  data=changed_payload,
                                  headers={'Authorization': payload["token"]})
        code = response.status_code
        changed_data = response.json()["user"][change_field]
        helper.delete_user(payload["token"])
        assert code == 200 and changed_data == changed_payload[change_field]

    @allure.title("Проверка изменения пароля у авторизованного пользователя")
    def test_change_authorized_user_password_success(self):
        payload = helper.new_user_creation()
        changed_payload = {"password": helper.get_random_email()}
        requests.patch(UrlData.MAIN_PAGE + UrlData.USER,
                       data=changed_payload,
                       headers={'Authorization': payload["token"]})
        login_payload = {"email": payload["email"], "password": changed_payload["password"]}
        login_response = requests.post(UrlData.MAIN_PAGE + UrlData.LOGIN, data=login_payload)
        code = login_response.status_code
        name = login_response.json()["user"]["name"]
        helper.delete_user(payload["token"])
        assert code == 200 and name == payload["name"]

    @allure.title("Проверка изменения почты, пароля и имени у неавторизованного пользователя")
    @pytest.mark.parametrize('change_field', ["email", "password", "name"])
    def test_change_unauthorized_user_data_impossible(self, change_field):
        payload = helper.new_user_login()
        changed_payload = {change_field: helper.get_random_email()}
        response = requests.patch(UrlData.MAIN_PAGE + UrlData.USER,
                                  data=changed_payload, )
        code = response.status_code
        message = response.json()["message"]
        helper.delete_user(payload["token"])
        assert code == 401 and message == DataAnswerMessage.UNAUTHORISED_USER
