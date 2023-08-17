from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model, admin as auth
from XroutS.core.models import UserProfile, AppUser
from XroutS.core.views import RegisterUserForm



# Register your models here.
User = get_user_model()
class ProfileInline(admin.StackedInline):
    model = UserProfile

@admin.register(User)
class AppUserAdmin(auth.UserAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request,obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['email'].disabled = True

        return form
    # readonly_fields = ['email','is_staff']
    ordering = ['email']
    list_display = ['id','email','is_staff']
    list_filter = ('is_staff',)
    add_form = RegisterUserForm
    inlines = auth_admin.UserAdmin = (ProfileInline,)
    search_fields = ('email',)
    fieldsets = (
        (None, {"fields": ("email",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("User dates information", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_per_page = 10
    readonly_fields = ['date_joined', 'last_login']
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'city', 'age',]
    list_filter = ['city', 'age']


