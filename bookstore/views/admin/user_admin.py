from django.contrib import admin
from ...models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'role', 'email', 'address', 'phone', 'status', 'username', 'password']
    list_filter = ['id', 'role', 'status', 'full_name']

    def delete_User(self, request, obj=None):
        # Chỉ có tài khaongr superuser mới xóa được user
        return request.user.is_superuser