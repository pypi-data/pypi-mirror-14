# -*- coding: utf-8 -*-
import django
from hijack.tests.utils import SettingsOverride

if django.VERSION < (1, 7):
    pass
else:
    from django.conf import settings
    from django.core.checks import Error, Warning
    from django.test import TestCase

    from hijack import settings as hijack_settings

    from hijack_admin import checks
    from hijack_admin.apps import HijackAdminConfig


    class ChecksTests(TestCase):

        def test_check_get_requests_allowed(self):

            self.assertTrue(hijack_settings.HIJACK_ALLOW_GET_REQUESTS)
            errors = checks.check_get_requests_allowed(HijackAdminConfig)
            self.assertFalse(errors)

            with SettingsOverride(hijack_settings, HIJACK_ALLOW_GET_REQUESTS=False):
                errors = checks.check_get_requests_allowed(HijackAdminConfig)
                expected_errors = [
                    Error(
                        'Hijack GET requests must be allowed for django-hijack-admin to work.',
                        hint='Set HIJACK_ALLOW_GET_REQUESTS to True.',
                        obj=None,
                        id='hijack_admin.E001',
                    )
                ]
                self.assertEqual(errors, expected_errors)

        def test_check_custom_user_model(self):
            warnings = checks.check_custom_user_model(HijackAdminConfig)
            self.assertFalse(warnings)

            with self.settings(AUTH_USER_MODEL='my_auth_user_model'):
                warnings = checks.check_custom_user_model(HijackAdminConfig)
                expected_warnings = [
                    Warning(
                        'django-hijack-admin does not work out the box with a custom user model.',
                        hint='Please mix HijackUserAdminMixin into your custom UserAdmin.',
                        obj=settings.AUTH_USER_MODEL,
                        id='hijack_admin.W001',
                    )
                ]
                self.assertEqual(warnings, expected_warnings)
