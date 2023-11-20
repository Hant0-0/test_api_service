import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from vpn_service.models import UserSite, SiteStatistic


@pytest.mark.django_db
def test_home(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_user_get(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_user_post(client):
    client = Client()
    url = reverse('register')
    valid_data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
        'data_of_birth': '1999-05-10',
        'phone_number': '1234567890',
    }

    response = client.post(url, data=valid_data)

    assert response.url == reverse('user_profile')
    assert User.objects.filter(username=valid_data['username']).exists()
    assert response.status_code == 302
    assert '_auth_user_id' in client.session

    """ Введення неправильних даних """

    invalid_data = {
        'username': 'testuser2',
        'password1': 'testpassword1',
        'password2': 'testpassword2',
        'data_of_birth': '1999-05-10',
        'phone_number': '1234567890',
    }

    response = client.post(url, data=invalid_data)
    assert not User.objects.filter(username=invalid_data['username']).exists()
    assert response.status_code == 200


@pytest.mark.django_db
def test_sign_in_get(client):
    url = reverse('sign_in')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_sign_in_post(client):
    valid_data = {
        'username': 'testuser',
        'password': 'testpassword',
    }
    user = User.objects.create_user(username=valid_data['username'], password=valid_data['password'])

    response = client.post(reverse('sign_in'), data=valid_data)
    assert response.status_code == 302
    assert response.url == reverse('user_profile')
    assert '_auth_user_id' in client.session

    invalid_data = {
        'username': 'testuser',
        'password': 'notestpassword',
    }
    response = client.post(reverse('sign_in'), data=invalid_data)
    assert response.status_code == 302
    user = authenticate(username=invalid_data['username'], password=invalid_data['password'])
    assert user is None


@pytest.mark.django_db
def test_user_profile(client):
    url = reverse('user_profile')
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_login(user)

    user_site = UserSite.objects.create(user=user, user_site_name='testsite', original_site='https://testsite.com/')
    statistic = SiteStatistic.objects.create(user=user, site_name=user_site, clicks_count=0, data_sent=0
                                             , data_received=0)

    response = client.get(url)
    assert response.status_code == 200
    assert 'user' in response.context







