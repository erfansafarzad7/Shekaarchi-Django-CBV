from django.contrib.auth.backends import BaseBackend
from .models import User, Otp


class MyBackend(BaseBackend):

    def custom_auth(self, phone=None, password=None, otp_code=None):
        """
        Get users info and authenticate with password or otp.
        return a user if exists.
        """
        if phone and (password or otp_code):
            # find user and otp
            user = User.objects.get(phone__exact=phone)
            otp_obj = Otp.objects.get(code__exact=otp_code)
            check_pass = user.check_password(password)
            if user and (check_pass or (otp_obj.phone == phone)):
                return user
            return None


authenticate = MyBackend()
