from django.conf.urls import include, url
from .views import reservations_botview

urlpatterns = [
                  url(r'^fburl2/?$', reservations_botview.as_view())
               ]