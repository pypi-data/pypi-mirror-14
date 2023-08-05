from django.conf.urls import url

from .views import RegisterView, VerifyPhoneView

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='phone_quick_register'),
    url(r'^verify-phone/$', VerifyPhoneView.as_view(), name='phone_quick_verify'),
]
