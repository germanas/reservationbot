from django.conf.urls import include, url
from .views import reservations_botview

urlpatterns = [
                  url(r'^77d2b8f4a09cd35cb23076a1da5d51529136a3373fd570b122/?$', reservations_botview.as_view())
               ]