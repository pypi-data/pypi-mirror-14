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
from .utils import get_form_class, complete_signup, send_phone_confirmation
from .models import QuickPhoneConfirmation, QuickPhoneNumber
from .status import ApiStatus, PHONE_AND_KEY_REQUIRED, VERIFICATION_KEY_INVALID, VERIFICATION_KEY_VERIFIED, \
    PHONE_FIELD_REQUIRED, PHONE_NUMBER_DOES_NOT_EXIST, REFUSED_TO_RESEND_SMS, CONFIRMATION_DOES_NOT_EXIST


class RegisterView(APIView, FormView):
    """
    Accepts the credentials and creates a new user
    if user does not exist already
    Return the REST Token if the credentials are valid and authenticated.
    Calls allauth complete_signup method

    Accept the following POST parameters: username, phone, password
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
        return complete_signup(request, self.user)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RegisterView, self).get_form_kwargs(*args, **kwargs)
        kwargs['data'] = self.request.data
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'phone_quick_signup', self.form_class)

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
        return Response({'key': self.token.key, 'user': self.user.dict()}, status=status.HTTP_200_OK)

    def get_response_with_errors(self):
        return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    token_model = Token

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['phone'] = self.request.data.get('phone', '')
        self.kwargs['key'] = self.request.data.get('key', '')

        if not self.kwargs['phone'] or not self.kwargs['key']:
            return Response(ApiStatus(PHONE_AND_KEY_REQUIRED).get_json(), status=status.HTTP_400_BAD_REQUEST)

        confirmation = self.get_object()

        if not confirmation:
            return Response(ApiStatus(CONFIRMATION_DOES_NOT_EXIST).get_json(), status=status.HTTP_400_BAD_REQUEST)

        phone_number, result = confirmation.confirm(self.request)

        if result == 'invalid':
            if app_settings.INVALID_AUTO_RESEND_CONFIRMATION:
                send_phone_confirmation(request, phone_number.user, signup=True)
            return Response(ApiStatus(VERIFICATION_KEY_INVALID).get_json(), status=status.HTTP_400_BAD_REQUEST)
        elif result == 'verified':
            return Response(ApiStatus(VERIFICATION_KEY_VERIFIED).get_json(), status=status.HTTP_400_BAD_REQUEST)
        else:
            token = self.token_model.objects.get(user=phone_number.user)
            return Response({'key': token.key, 'user': phone_number.user.dict()}, status=status.HTTP_200_OK)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except QuickPhoneConfirmation.DoesNotExist:
            return None

    def get_queryset(self):
        qs = QuickPhoneConfirmation.objects.filter(phone_number__phone=self.kwargs["phone"])
        qs = qs.select_related("phone_number__user")
        return qs


class ResendPhoneView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    token_model = Token

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['phone'] = self.request.data.get('phone', '')

        if not self.kwargs['phone']:
            return Response(ApiStatus(PHONE_FIELD_REQUIRED).get_json(), status=status.HTTP_400_BAD_REQUEST)

        phone_number = self.get_object()

        if not phone_number:
            return Response(ApiStatus(PHONE_NUMBER_DOES_NOT_EXIST).get_json(), status=status.HTTP_400_BAD_REQUEST)

        send_sms = send_phone_confirmation(request, phone_number.user, signup=True)

        if send_sms:
            token = self.token_model.objects.get(user=phone_number.user)
            return Response({'key': token.key, 'user': phone_number.user.dict()}, status=status.HTTP_200_OK)
        else:
            return Response(ApiStatus(REFUSED_TO_RESEND_SMS).get_json(), status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if queryset and len(queryset) > 0:
            return queryset[0]
        else:
            return None

    def get_queryset(self):
        qs = QuickPhoneNumber.objects.filter(phone=self.kwargs["phone"])
        return qs
