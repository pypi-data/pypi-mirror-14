# Lettoo phone quick signup documents

------

Lettoo Phone Quick Signup is an easy to setup authentication/registration mechanism for Django projects.

> * Requirements
> * Installation
> * API endpoints
> * Configuration
> * Licenses

------

[TOC]

------

## Requirements

> Python (2.7, 3.2, 3.3, 3.4, 3.5)
> Django (1.7+, 1.8, 1.9)
> Django REST framework (3.3.2+)

------

## Installation

### 1. Install package

From pypi

```
$ pip install lettoo-phone-quick-signup
```

or

```
$ easy_install lettoo-phone-quick-signup
```

### 2. Add phone_quick_signup app to INSTALLED_APPS in your django settings.py

```
INSTALLED_APPS = (
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    ...,
    'phone_quick_signup'
)
```

*This project depends on `django-rest-framework` library, so install it if you haven’t done yet. Make sure also you have installed `rest_framework` and `rest_framework.authtoken` apps*

### 3. Add phone_quick_signup urls

```
urlpatterns = patterns('',
    ...,
    url(r'^api/v1/phone-quick/', include('phone_quick_signup.urls'))
)
```

------

## API endpoints

> After successful registration will send a mail contains 6 digit verification code

- /api/v1/phone-quick/ (POST)
    - phone

```
POST /api/v1/phone-quick/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Cache-Control: no-cache

{"phone":"123456789"}
```

- /api/v1/phone-quick/verify-phone/ (POST)
    - phone
    - key

```
POST /api/v1/phone-quick/verify-phone/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Cache-Control: no-cache

{"phone": "test1@test.com", "key": "597510"}
```

------

## Configuration

- PHONE_QUICK_SIGNUP_PHONE_CONFIRMATION_EXPIRE_DAYS = 3

- PHONE_QUICK_SIGNUP_PHONE_VERIFICATION = 'optional'

- PHONE_QUICK_SIGNUP_UNIQUE_PHONE = True

- PHONE_QUICK_SIGNUP_SIGNUP_FORM_CLASS = None

- PHONE_QUICK_SIGNUP_USER_MODEL = 'auth.User'

- PHONE_QUICK_SIGNUP_USER_MODEL_USERNAME_FIELD = 'username'

- PHONE_QUICK_SIGNUP_USER_MODEL_PHONE_FIELD = 'phone'

------

## Licenses

```
Copyright (c) 2016 Lettoo Software Technology, and contributors.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
```

