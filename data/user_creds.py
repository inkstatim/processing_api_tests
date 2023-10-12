class UserCreds:
    CREDS = lambda user_abstract: {
        "email": user_abstract.EMAIL.value,
        "password": user_abstract.PASSWORD.value

    }

    OTP_CREDS = lambda user_abstract: {
        "email": user_abstract.EMAIL.value,
        "password": user_abstract.PASSWORD.value,
        "otp_secret": user_abstract.OTP_SECRET.value
    }
