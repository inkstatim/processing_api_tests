import os
from enum import Enum


class CommonUserCreds(Enum):
    EMAIL = os.getenv('USER_CREDS_EMAIL')
    PASSWORD = os.getenv('USER_CREDS_PASSWORD')


class AdminUserCreds(Enum):
    EMAIL = os.getenv('USER_ADMIN_CREDS_EMAIL')
    PASSWORD = os.getenv('USER_ADMIN_CREDS_PASSWORD')


class MerchantManagerCreds(Enum):
    EMAIL = os.getenv('MERCHANT_MANAGER_CREDS_EMAIL')
    PASSWORD = os.getenv('MERCHANT_MANAGER_CREDS_PASSWORD')


class MerchantUserCreds(Enum):
    EMAIL = os.getenv('MERCHANT_USER_CREDS_EMAIL')
    PASSWORD = os.getenv('MERCHANT_USER_CREDS_PASSWORD')


class MerchantAdminCreds(Enum):
    EMAIL = os.getenv('MERCHANT_ADMIN_CREDS_EMAIL')
    PASSWORD = os.getenv('MERCHANT_ADMIN_CREDS_PASSWORD')


class OTPUserCreds(Enum):
    EMAIL = os.getenv('OTP_USER_CREDS_EMAIL')
    PASSWORD = os.getenv('OTP_USER_CREDS_PASSWORD')
    OTP_SECRET = os.getenv('OTP_USER_SECRET')
