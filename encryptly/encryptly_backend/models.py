from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    private_key = models.CharField(max_length=4096)
    public_key = models.CharField(max_length=4096)
    mobile_number = models.CharField(max_length=15)
    two_factor = models.BooleanField(default=False)
    theme = models.IntegerField(default=0)
    online_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

