from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.user.username


class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_site_name = models.CharField(max_length=120)
    original_site = models.URLField()

    def __str__(self):
        return self.original_site


class SiteStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    clicks_count = models.IntegerField(default=0)
    data_sent = models.BigIntegerField(default=0)
    data_received = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Statistic {self.site_name}"