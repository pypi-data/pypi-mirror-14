class AppSettings(object):
    class EmailVerificationMethod:
        # After signing up, keep the user account inactive until the email
        # address is verified
        MANDATORY = 'mandatory'
        # Allow login with unverified e-mail (e-mail verification is
        # still sent)
        OPTIONAL = 'optional'
        # Don't send e-mail verification mails during signup
        NONE = 'none'

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(settings,
                         'EMAIL_QUICK_SIGNUP_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, dflt))
        return getter(self.prefix + name, dflt)

    @property
    def EMAIL_CONFIRMATION_EXPIRE_DAYS(self):
        """
        Determines the expiration date of e-mail confirmation mails (#
        of days)
        """
        from django.conf import settings
        return self._setting("EMAIL_CONFIRMATION_EXPIRE_DAYS",
                             getattr(settings, "EMAIL_CONFIRMATION_DAYS", 3))

    @property
    def EMAIL_VERIFICATION(self):
        """
        See e-mail verification method
        """
        ret = self._setting("EMAIL_VERIFICATION",
                            self.EmailVerificationMethod.OPTIONAL)
        # Deal with legacy (boolean based) setting
        if ret is True:
            ret = self.EmailVerificationMethod.MANDATORY
        elif ret is False:
            ret = self.EmailVerificationMethod.OPTIONAL
        return ret

    @property
    def UNIQUE_EMAIL(self):
        """
        Enforce uniqueness of e-mail addresses
        """
        return self._setting("UNIQUE_EMAIL", True)

    @property
    def PASSWORD_MIN_LENGTH(self):
        """
        Minimum password Length
        """
        return self._setting("PASSWORD_MIN_LENGTH", 6)

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        """
        Subject-line prefix to use for email messages sent
        """
        return self._setting("EMAIL_SUBJECT_PREFIX", None)

    @property
    def SIGNUP_FORM_CLASS(self):
        """
        Signup form
        """
        return self._setting("SIGNUP_FORM_CLASS", None)

    @property
    def USERNAME_REQUIRED(self):
        """
        The user is required to enter a username when signing up
        """
        return self._setting("USERNAME_REQUIRED", True)

    @property
    def USERNAME_MIN_LENGTH(self):
        """
        Minimum username Length
        """
        return self._setting("USERNAME_MIN_LENGTH", 1)

    @property
    def USERNAME_BLACKLIST(self):
        """
        List of usernames that are not allowed
        """
        return self._setting("USERNAME_BLACKLIST", [])

    @property
    def PASSWORD_INPUT_RENDER_VALUE(self):
        """
        render_value parameter as passed to PasswordInput fields
        """
        return self._setting("PASSWORD_INPUT_RENDER_VALUE", False)

    @property
    def ADAPTER(self):
        return self._setting('ADAPTER',
                             'email_quick_signup.adapter.DefaultAccountAdapter')

    @property
    def USER_MODEL_USERNAME_FIELD(self):
        return self._setting('USER_MODEL_USERNAME_FIELD', 'username')

    @property
    def USER_MODEL_EMAIL_FIELD(self):
        return self._setting('USER_MODEL_EMAIL_FIELD', 'email')

    @property
    def FORMS(self):
        return self._setting('FORMS', {})

    @property
    def USER_MODEL(self):
        return self._setting('USER_MODEL', 'auth.User')


import sys

app_settings = AppSettings('EMAIL_QUICK_SIGNUP_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
