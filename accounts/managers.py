from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, email, password):
        if not phone_number:
            raise ValueError("Enter Your Phone Number..")
        if not username:
            raise ValueError("Enter Your Username..")
        if not email:
            raise ValueError("Enter Your Email..")

        user = self.model(phone_number=phone_number, username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, email, password):
        user = self.create_user(phone_number, username, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

