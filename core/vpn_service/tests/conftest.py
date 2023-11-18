import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory

from vpn_service.models import UserProfile, UserSite, SiteStatistic


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def user():
    return User.objects.create_user(username='Ivan', password='TzH7raBZ')


@pytest.fixture
def user_profile(user):
    return UserProfile.objects.create(
        user=user,
        data_of_birth='1972-02-12',
        phone_number='+380123456789',
    )


@pytest.fixture
def user_site(user):
    return UserSite.objects.create(
        user=user,
        user_site_name='testsite',
        original_site='https://testsite.com'
    )


@pytest.fixture
def site_statistic(user, user_site):
    return SiteStatistic.objects.create(
        user=user,
        site_name=user_site,
        clicks_count=2,
        data_sent=100,
        data_received=325,
    )
