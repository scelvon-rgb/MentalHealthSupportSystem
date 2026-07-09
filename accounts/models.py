from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.role_name


class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20, blank=True)

    student_reg_no = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return self.user.username