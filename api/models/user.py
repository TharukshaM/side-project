import bcrypt
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model."""

    def create_user(self, username, email, password=None, address=""):
        """Creates a user with a hashed password."""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, address=address)
        if password:
            user.set_password(password)  # Hash password using bcrypt
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, address=""):
        """Creates a superuser with admin privileges."""
        user = self.create_user(username, email, password, address)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Extends Django's default User model to use bcrypt for password hashing."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Hashed with bcrypt
    address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin login
    is_superuser = models.BooleanField(default=False)  # Required for superuser privileges

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def set_password(self, raw_password):
        """Hashes the password using bcrypt before saving."""
        if raw_password:
            self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        """Checks if the provided password matches the stored bcrypt hash."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def __str__(self):
        return self.username
