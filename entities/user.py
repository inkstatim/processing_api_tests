class User:

    def __init__(self, access_token, public_key):
        '''
        Example:
        {
            "id": 374586789,
            "firstName": "First name",
            "lastName": "Last name",
            "email": "supervasya@gmail.test",
            "role": "Administrator",
            "phone": "1231231231212",
            "lastUpdatePassword": 1172754000,
            "passwordActiveTill": 1172754000,
            "isTempPassword": true
        }
        '''
        self.access_token = access_token
        self.refresh_token = None
        self.public_key = public_key
        self.cookies = None
        self.signature = None
        self.id = None
        self.firstName = None
        self.lastName = None
        self.email = None
        self.role = None
        self.phone = None
        self.lastUpdatePassword = None
        self.passwordActiveTill = None
        self.isTempPassword = None

    def update_user_data(self, **kwargs):
        self.__dict__.update(kwargs)


class EmptyUser(User):

    def __init__(self):
        super().__init__("", "")
