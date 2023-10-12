import time  # toDo del, mv all func to DateHelper
from typing import Union

import pytest
import requests

from clients.api_manager import ApiManager
from data.backoffice import Backoffice
from data.cards import Cards
from data.db.contract_db import ContractDb
from data.order import Order
from data.shop import Shops
from data.user_creds import UserCreds
from data.merchant import Merchant
from datetime import datetime, timedelta

from resources.user_creds import CommonUserCreds, AdminUserCreds, MerchantManagerCreds, OTPUserCreds, \
    MerchantAdminCreds, MerchantUserCreds
from utils.db.db_queries import Queries
from utils.random import RandomDataGenerator
from utils.str_formater import convert_camel_to_snake

from data.db.shop_db import ShopsDb
from utils.date_hepler import DateHelper


# toDo check sign "%_%" in data/*.py structures


@pytest.fixture(scope='class')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope='class')
def api_clients(session):
    return ApiManager(session)


@pytest.fixture
def user_creds():
    return UserCreds.CREDS(CommonUserCreds)


@pytest.fixture
def user_admin_creds():
    return UserCreds.CREDS(AdminUserCreds)


@pytest.fixture
def merchant_manager_creds():
    return UserCreds.CREDS(MerchantManagerCreds)


@pytest.fixture
def merchant_user_creds():
    return UserCreds.CREDS(MerchantUserCreds)


@pytest.fixture
def merchant_admin_creds():
    return UserCreds.CREDS(MerchantAdminCreds)


@pytest.fixture
def user_otp_creds():
    return UserCreds.OTP_CREDS(OTPUserCreds)


@pytest.fixture
def order():
    """
    Фикстура для получения json для создания заказа.

    Returns:
        dict: JSON с информацией о заказе.
    """
    min30_after_now = int(time.time()) + 1800
    return _fake_data(Order.ORDER(min30_after_now))


@pytest.fixture
def order_without_customer_data():
    """
    Фикстура для получения json для создания заказа.

    Returns:
        dict: JSON с информацией о заказе.
    """
    min30_after_now = int(time.time()) + 1800
    return Order.ORDER_WITH_EMPTY_CUSTOMER_DATA(min30_after_now)


@pytest.fixture
def order_without_time_limit():
    return Order.ORDER_WITHOUT_TIME_LIMIT


@pytest.fixture
def order_with_past_time_limit():
    """
    Фикстура для получения json для заказа с просроченным временным ограничением.
    Returns:
        dict: JSON с информацией о заказе с просроченным временным ограничением.
    """
    min60_before_now = (datetime.now() - timedelta(hours=1)).isoformat()
    return Order.ORDER(min60_before_now)


def order_cancelled(order_id: int):
    """
    Фикстура для получения json для отмены заказа.

    Returns:
        dict: JSON с информацией для отмены заказа.
    """
    return Order.ORDER_CANCELLED(order_id)


def order_search_data_by_id(order_number: str):
    return Merchant.ORDER_SEARCH(order_number)


@pytest.fixture
def order_with_empty_customer_data():
    min30_after_now = int(time.time()) + 1800
    return Order.ORDER_WITH_EMPTY_CUSTOMER_DATA(min30_after_now)


@pytest.fixture
def card():
    return Cards.SUCCESS_CARD(DateHelper.get_year(1))


@pytest.fixture
def card_expire():
    return Cards.EXPIRED_CARD(DateHelper.get_year(-1))


@pytest.fixture
def card_with_empty_cvv():
    return Cards.CARD_WITH_EMPTY_CVV(DateHelper.get_year(1))


@pytest.fixture
def refund_payment():
    return Cards.REFUND_PAYMENT


def shop(company_id: int):
    return _fake_data(Shops.SHOP(company_id))


@pytest.fixture
def order_list():
    return Merchant.ORDER_LIST


def shop_payment_type_db(shop_id: int):
    created_at = DateHelper.get_current_date_time('%Y-%m-%d %H:%M:%S.%f')
    return ShopsDb.SHOP_PAYMENT_TYPE(shop_id, created_at)


@pytest.fixture
def backoffice_company_db():
    return Backoffice.COMPANY


def contract_db(company_id: int):
    created_at = DateHelper.get_current_date_time('%Y-%m-%d %H:%M:%S.%f')
    year = DateHelper.get_year(1)
    return ContractDb.CONTRACT(created_at, year, company_id)


@pytest.fixture(scope="session")
def db_connector():
    db_instance = Queries()
    yield db_instance
    db_instance.db.close()


def _fake_data(data: Union[dict, list]) -> Union[dict, list]:  # noqa C901
    data_generator = RandomDataGenerator()
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = _fake_data(value)
            elif hasattr(data_generator, f"generate_random_{convert_camel_to_snake(key)}") and value != '':
                data[key] = getattr(data_generator, f"generate_random_{convert_camel_to_snake(key)}")()
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = _fake_data(item)
    return data
