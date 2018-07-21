from django.conf.urls import include, url

urlpatterns = [
    url(r'^search/', include('people.search.urls'))
]