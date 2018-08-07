from django.conf.urls import url

from . import views

urlpatterns = [
    url('login', views.login, name='login'),
    url('resetPassword', views.reset_password, name='resetPassword'),
    url('logout', views.logout, name='logout'),
    url('register', views.register, name='register'),
    url('requestVerify', views.request_verify, name="requestVerify"),
    url('getVerifyStatus', views.get_verify_status, name="getVerifyStatus"),
    url('verifyUser', views.verify_user, name="verifyUser"),
    url('searchCompany', views.search_company, name="searchCompany"),
    url('searchUser', views.search_user, name="searchUser"),
    url('searchWorker', views.search_worker, name="searchWorker"),
    url('searchConnection', views.search_connection, name="searchConnection"),
]