from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from vpn_service.form import MyUserCreationForm, AddUserProfileForm, CreateSiteForm
from vpn_service.models import UserProfile, UserSite, SiteStatistic


def home(request):
    return render(request, 'home.html')


def register_user(request):
    if request.method == 'GET':
        return render(request, 'register_user.html', {'form1': MyUserCreationForm(), 'form2': AddUserProfileForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.save()
            userprofile = UserProfile(user=user, data_of_birth=request.POST['data_of_birth'],
                                      phone_number=request.POST['phone_number'])
            userprofile.save()
            login(request, user)
            return redirect('user_profile')
        else:
            return render(request, 'register_user.html')


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'sign_in.html', {'form': AuthenticationForm()})
    else:
        try:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('user_profile')
        except AttributeError:
            return render(request, 'sign_in.html', {'form': AuthenticationForm(), 'error': 'Password or username '
                                                                                           'is not corrected'})


def user_profile(request):
    user = request.user
    site = UserSite.objects.filter(user=user)
    statistic = SiteStatistic.objects.filter(user=user)
    return render(request, 'user_profile.html', {'user': request.user, 'usersite': site, 'statistics': statistic})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = AddUserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = AddUserProfileForm(instance=request.user.userprofile)
        return render(request, 'update_profile.html', {'form': form})


@login_required
def create_site(request):
    if request.method == 'GET':
        return render(request, 'create_site.html', {'form': CreateSiteForm})
    else:
        user_site = UserSite(user=request.user, user_site_name=request.POST['user_site_name'],
                             original_site=request.POST['original_site'])
        user_site.save()
        return redirect('user_profile')


def proxy_view(request, user_site_name, routes_on_original_site):
    original_url = routes_on_original_site
    response = requests.get(original_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    modify_content = replace_links(soup.prettify(), user_site_name, original_url)

    site_name = UserSite.objects.get(user=request.user, original_site=routes_on_original_site)
    site_statistic, created = SiteStatistic.objects.get_or_create(user=request.user, site_name=site_name)

    sent_data = len(response.request.body) + len(request.META) if response.request.body else 0
    received_data = len(HttpResponse(modify_content).content) if response.content else 0

    site_statistic.clicks_count += 1
    site_statistic.data_sent += sent_data
    site_statistic.data_received += received_data
    site_statistic.save()

    return render(request, 'vpn_page.html', {'content': modify_content})


def replace_links(parsed_content, user_site_name, original_url):
    soup = BeautifulSoup(parsed_content, 'html.parser')

    for a_tag in soup.find_all('a', href=True, src=True):

        if 'href' in a_tag.attrs and not a_tag['href'].startswith(('http:', 'https:')):
            a_tag['href'] = urljoin(user_site_name, original_url, a_tag["href"])

        if 'src' in a_tag.attrs and not a_tag['src'].startswith(('http:', 'https:')):
            a_tag['src'] = urljoin(user_site_name, original_url, a_tag["src"])

    return str(soup)