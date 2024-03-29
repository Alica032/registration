from django.contrib.auth.models import UserManager


class UserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, phone, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")

        if not phone:
            raise ValueError("The given phone number must be set")

        if not email:
            raise ValueError("The given email must be set")

        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, phone, password, **extra_fields)

    def create_superuser(self, username, email, phone, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, phone, password, **extra_fields)
