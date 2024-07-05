class UrlData:
    MAIN_PAGE = 'https://stellarburgers.nomoreparties.site/'
    REGISTRATION = 'api/auth/register'
    USER = 'api/auth/user'
    LOGIN = 'api/auth/login'
    INGREDIENTS = 'api/ingredients'
    ORDER = 'api/orders'


class DataAnswerMessage:
    EXISTED_USER = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_DATA = "email or password are incorrect"
    UNAUTHORISED_USER = "You should be authorised"
    NEED_INGREDIENT_ID = "Ingredient ids must be provided"


class DataExample:
    WRONG_HASH_INGREDIENTS = ["1111111111", "2222222222222"]
    QUANTITY_ORDERS = 4
