# django-hijack-admin

Django admin integration for Django Hijack (https://github.com/arteria/django-hijack/)

[![Build Status](https://travis-ci.org/arteria/django-hijack-admin.svg?branch=master)](https://travis-ci.org/arteria/django-hijack-admin)
[![Coverage Status](https://coveralls.io/repos/arteria/django-hijack-admin/badge.svg?branch=master&service=github)](https://coveralls.io/github/arteria/django-hijack-admin?branch=master)

![Screenshot of django-hijack in action on the admin site.](docs/admin-screenshot.png)


## Installation

Follow the instructions on http://django-hijack.readthedocs.org/en/stable/#installation to install django-hijack.

Get the latest stable release from PyPi:

    pip install django-hijack-admin

In your ``settings.py``, add ``hijack_admin`` to your installed apps:

```python
INSTALLED_APPS = (
    ...,
    'hijack_admin',
)
```

For the admin integration to work, you must explicitly set `HIJACK_ALLOW_GET_REQUESTS = True` in your project settings.
Please be aware that users can now be hijacked not only using POST requests, but also using GET requests, which could facilitate CSRF attacks.

## Configuration

### `HIJACK_BUTTON_TEMPLATE`
Path to the template for the "Hijack" buttons. Default: `'hijack_admin/admin_button.html'`

### `HIJACK_REGISTER_ADMIN`
Whether the user model should be registered with `HijackUserAdmin` automatically. Default: `True`

## Custom user admins
Custom user admins are supported. Just set `HIJACK_REGISTER_ADMIN = False` and 
modify your custom admin class as shown in this example:

```python
# admin.py
from hijack.admin import HijackUserAdminMixin

class MyUserAdmin(UserAdmin, HijackUserAdminMixin):
    list_display = (
        ...
        'hijack_field',  # Hijack button
    )
```
