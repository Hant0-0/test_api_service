import datetime

import pytest
from django.contrib.auth.models import User

from vpn_service.models import UserProfile, UserSite, SiteStatistic


@pytest.mark.django_db
def test_user(user):
    user_test = User.objects.first()
    assert user == user_test


@pytest.mark.django_db
def test_user_profile(user_profile, user):
    user_profile_test = UserProfile.objects.first()
    assert UserProfile.objects.count() == 1
    assert user_profile_test.user == user
    assert str(user_profile_test.data_of_birth) == user_profile.data_of_birth
    assert user_profile_test.phone_number == user_profile.phone_number


@pytest.mark.django_db
def test_user_site(user, user_site):
    user_site_test = UserSite.objects.first()
    assert UserSite.objects.count() == 1
    assert user_site_test.user == user
    assert user_site_test.user_site_name == user_site.user_site_name
    assert user_site_test.original_site == user_site.original_site


@pytest.mark.django_db
def test_site_statistic(user, user_site, site_statistic):
    site_statistic_t = SiteStatistic.objects.first()
    assert SiteStatistic.objects.count() == 1
    assert site_statistic_t.user == user
    assert site_statistic_t.site_name == user_site
    assert site_statistic_t.clicks_count == site_statistic.clicks_count
    assert site_statistic_t.data_sent == site_statistic.data_sent
    assert site_statistic_t.data_received == site_statistic.data_received

