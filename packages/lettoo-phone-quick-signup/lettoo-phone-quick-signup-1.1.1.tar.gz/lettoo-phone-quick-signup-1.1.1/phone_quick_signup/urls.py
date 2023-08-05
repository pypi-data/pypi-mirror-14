from django.conf.urls import url

from .views import RegisterView, VerifyPhoneView, ResendPhoneView

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='phone_quick_register'),
    url(r'^verify-phone/$', VerifyPhoneView.as_view(), name='phone_quick_verify'),
    url(r'^resend-phone/$', ResendPhoneView.as_view(), name='phone_quick_resend'),
]
