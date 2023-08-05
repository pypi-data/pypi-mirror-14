from django.conf.urls import url

from .views import RegisterView, VerifyEmailView, ResendEmailView, PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='email_quick_register'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='email_quick_verify'),
    url(r'^resend-email/$', ResendEmailView.as_view(), name='email_quick_resend'),
    url(r'^password/reset/$', PasswordResetView.as_view(), name='email_quick_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='email_quick_password_reset_confirm'),
]
