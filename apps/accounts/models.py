from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    WEBSITE_ADMIN = "WEBSITE_ADMIN", "Website Admin"
    CONTENT_MANAGER = "CONTENT_MANAGER", "Content Manager"
    MEMBER = "MEMBER", "Member"


ADMIN_ROLES = {UserRole.SUPER_ADMIN, UserRole.WEBSITE_ADMIN, UserRole.CONTENT_MANAGER}


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("role", UserRole.MEMBER)
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("role", UserRole.SUPER_ADMIN)
        extra["is_staff"] = True
        extra["is_superuser"] = True
        return self._create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, blank=True, db_index=True)
    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.MEMBER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return f"{self.full_name or self.email} ({self.role})"

    @property
    def is_admin_role(self) -> bool:
        return self.role in ADMIN_ROLES

    def save(self, *args, **kwargs):
        # Admin-role users get Django admin access.
        if self.is_admin_role:
            self.is_staff = True
        super().save(*args, **kwargs)
