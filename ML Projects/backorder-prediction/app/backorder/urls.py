from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import index, PredictView, about_us, contact_us

urlpatterns = [
                  path('', index, name='index'),
                  path('predict/', PredictView.as_view(), name='predict'),
                  path('about-us/', about_us, name='about_us'),
                  path('contact-us/', contact_us, name='contact_us'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
