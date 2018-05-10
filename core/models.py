from django.db import models
from django.contrib.auth.models import AbstractUser
from django_mysql.models import JSONField


# Create your models here.
class User(AbstractUser):
    """
    Extending the AbstractUser class, which works similar to User model class, but has to be extended to be used.
    """
    is_admin = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    position = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="uploads", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    skills = JSONField(default=list)
    interest = JSONField(default=list)

    def __repr__(self):
        return "%s" %self.username
