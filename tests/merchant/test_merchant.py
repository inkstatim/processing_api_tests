import allure
import pytest
from jsonschema.validators import validate

from conftest import shop_payment_type_db, contract_db, shop
from enums.db_tables import Tables
from json_resp_schemes.merchant import MerchantSchema


# toDo add postfix "TestMerchantCreate" after test_merchant_details refactoring
class TestMerchant:

    @allure.description("Получение информации о магазинах мерчанта")
    @pytest.mark.case("QA-T172 (1.0)")
    def test_merchant_details(self, user_admin_creds, backoffice_company_db, api_clients, db_connector):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_admin_creds)
        with allure.step("create company"):
            company_id = api_clients.backoffice_api.create_and_get_id_backoffice_company(user, backoffice_company_db)
        with allure.step("create contract"):
            db_connector.insert(Tables.CONTRACT, contract_db(company_id))
        with allure.step("create shop"):
            shop_expected = shop(company_id)
            shop_id = api_clients.backoffice_api.create_and_get_id_shop(user, shop_expected)
        # toDO now ids hardcode in data/*.py:
        # with allure.step("create acquirer"):
        # with allure.step("create merchant_settings"):
        with allure.step("set payment type for shop"):
            payment_type_expected = shop_payment_type_db(shop_id)
            db_connector.insert(Tables.SHOP_PAYMENT_TYPE, payment_type_expected)
        with allure.step("getting information about shops for user"):
            shops_resp = api_clients.merchant_api.get_shops_details(user)
            validate(shops_resp, MerchantSchema.GET)
        with allure.step("checking availability of shops"):
            shop_actual = [shop for shop in shops_resp if shop['id'] == shop_id][0]
            shop_actual_name = shop_actual['name']
            shop_actual_payment_types = shop_actual['paymentTypes'][0]
            assert shop_expected.get('name', {}) == shop_actual_name
            assert payment_type_expected.get('instrument_type', {}) == shop_actual_payment_types
