from pydantic import BaseModel, Field, AliasPath


EXPECTED_GET_OTP_USER_RESPONSE = {
    'email': 'pp@test.pp',
    'firstName': 'PP guy',
    'id': 43,
    'isTempPassword': False,
    'lastName': 'PPP',
    'lastUpdatePassword': 1694464058,
    'passwordActiveTill': 1702240057,
    'phone': '123123213',
    'role': 'admin',
    'twoFactor': ['TOTP']}


class GetUserResponse(BaseModel):
    email: str
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    phone: str
    role: str
    is_temp_password: bool = Field(alias="isTempPassword")
    two_factor: str = Field(validation_alias=AliasPath('twoFactor', 0))
