from django.http import HttpRequest
from django.http.response import Http404
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from . import app_settings
from .forms import SignupForm
from .utils import get_form_class, complete_signup, send_email_confirmation
from .models import QuickEmailConfirmation


class RegisterView(APIView, FormView):
    """
    Accepts the credentials and creates a new user
    if user does not exist already
    Return the REST Token if the credentials are valid and authenticated.
    Calls allauth complete_signup method

    Accept the following POST parameters: username, email, password
    Return the REST Framework Token Object's key.
    """

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    token_model = Token
    form_class = SignupForm

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def form_valid(self, form):
        self.user = form.save(self.request)
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user
        )
        if isinstance(self.request, HttpRequest):
            request = self.request
        else:
            request = self.request._request
        return complete_signup(request, self.user, app_settings.EMAIL_VERIFICATION)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RegisterView, self).get_form_kwargs(*args, **kwargs)
        kwargs['data'] = self.request.data
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'email_quick_signup', self.form_class)

    def post(self, request, *args, **kwargs):
        self.initial = {}
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form_valid(self.form)
            return self.get_response()
        else:
            return self.get_response_with_errors()

    def get_response(self):
        return Response({'message': _('ok')}, status=status.HTTP_200_OK)

    def get_response_with_errors(self):
        return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    token_model = Token

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['email'] = self.request.data.get('email', '')
        self.kwargs['key'] = self.request.data.get('key', '')

        if not self.kwargs['email'] or not self.kwargs['key']:
            return Response({'message': _('email and key parameters required')}, status=status.HTTP_400_BAD_REQUEST)

        confirmation = self.get_object()
        email_address, result = confirmation.confirm(self.request)

        if result == 'invalid':
            send_email_confirmation(request, email_address.user, signup=True)
            return Response({'message': _('invalid')}, status=status.HTTP_200_OK)
        elif result == 'verified':
            return Response({'message': _('verified')}, status=status.HTTP_200_OK)
        else:
            token = self.token_model.objects.get(user=email_address.user)
            return Response({'message': _('ok'), 'token': token.key}, status=status.HTTP_200_OK)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except QuickEmailConfirmation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        qs = QuickEmailConfirmation.objects.filter(email_address__email=self.kwargs["email"])
        qs = qs.select_related("email_address__user")
        return qs
