import random

from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.template.defaultfilters import slugify
from django.utils import timezone

from XroutS.core.utils import generate_random_number
from XroutS.core.validators import validate_file_size,validate_only_characters


class UserManager(auth_models.BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Create the user using the _create_user method
        user = self._create_user(email, password, **extra_fields)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AppUser(auth_models.AbstractBaseUser,auth_models.PermissionsMixin):
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    objects = UserManager()





UserModel = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        validators=(
            validate_only_characters,
        )
    )

    last_name = models.CharField(
        max_length=50,
        blank=False,
        null=True,
    )

    age = models.PositiveIntegerField(
        blank=False,
        null=True,
    )

    city = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )

    profile_picture = models.ImageField(
        validators=(validate_file_size,),
        upload_to='user_picture/',
        blank=True,
        null=False
    )

    slug = models.SlugField(unique=True, editable=False)

    followers = models.ManyToManyField(UserModel, related_name='followers', blank=True)
    following = models.ManyToManyField(UserModel, related_name='following', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.user_id}{generate_random_number()}')
            return super().save(*args, **kwargs)

    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()


    objects = models.Manager()

