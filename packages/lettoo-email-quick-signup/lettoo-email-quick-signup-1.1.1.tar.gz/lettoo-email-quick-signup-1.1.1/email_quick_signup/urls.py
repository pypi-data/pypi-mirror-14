from django.conf.urls import url

from .views import RegisterView, VerifyEmailView, ResendEmailView

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='email_quick_register'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='email_quick_verify'),
    url(r'^resend-email/$', ResendEmailView.as_view(), name='email_quick_resend'),
]
