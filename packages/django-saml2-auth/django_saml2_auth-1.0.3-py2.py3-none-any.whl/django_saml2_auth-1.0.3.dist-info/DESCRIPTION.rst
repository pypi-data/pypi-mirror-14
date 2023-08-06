=====================================
Django SAML2 Authentication Made Easy
=====================================

:Author: Fang Li
:Version: 1.0.3

.. image:: https://img.shields.io/pypi/pyversions/django-saml2-auth.svg
    :target: https://pypi.python.org/pypi/django-saml2-auth

.. image:: https://img.shields.io/pypi/v/django-saml2-auth.svg
    :target: https://pypi.python.org/pypi/django-saml2-auth

.. image:: https://img.shields.io/pypi/dm/django-saml2-auth.svg
        :target: https://pypi.python.org/pypi/django-saml2-auth

This project aim to provide a dead simple way to integrate your Django powered app with SAML2 Authentication.
Try it now, and get rid of the complicated configuration of saml.

Any SAML2 based SSO(Single-Sign-On) with dynamic metadata configuration was supported by this django plugin, Such as okta.



Dependencies
============

This plugin compatiable with Django 1.6/1.7/1.8/1.9, Python module `pysaml2` required.



Install
=======

You can install this plugin via `pip`:

.. code-block:: bash

    # pip install django_saml2_auth

or from source:

.. code-block:: bash

    # git clone https://github.com/fangli/django-saml2-auth
    # cd django-saml2-auth
    # python setup.py install



What does this plugin do?
=========================

This plugin takes over django's login page and redirect user to SAML2 SSO authentication service. While a user 
logged in and redirected back, it will check if this user is already in system. If not, it will create the user using django's default UserModel,
otherwise redirect the user to the last visited page.



How to use?
===========

#. Override the default login page in root urls.py, by adding these lines **BEFORE** any `urlpatterns`:

    .. code-block:: python

        # This is the SAML2 related URLs, you can change "^saml2_auth/" to any path you want, like "^sso_auth/", "^sso_login/", etc. (required)
        url(r'^saml2_auth/', include('django_saml2_auth.urls')),

        # If you want to replace the default user login with SAML2, just use the following line (optional)
        url(r'^accounts/login/$', 'django_saml2_auth.views.signin'),

        # If you want to replace the admin login with SAML2, use the following line (optional)
        url(r'^admin/login/$', 'django_saml2_auth.views.signin'),

#. Add 'django_saml2_auth' to INSTALLED_APPS

    .. code-block:: python

        INSTALLED_APPS = [
            '...',
            'django_saml2_auth',
        ]

#. In settings.py, add SAML2 related configuration.

    Please note only **METADATA_AUTO_CONF_URL** is required. The following block just shows the full featured configuration and their default values.

    .. code-block:: python

        SAML2_AUTH = {
            # Required
            'METADATA_AUTO_CONF_URL': '[The auto(dynamic) metadata configuration URL of SAML2]',

            # Following optional
            'NEW_USER_PROFILE': {
                'USER_GROUPS': [],  # The default group name when a new user logged in
                'ACTIVE_STATUS': True,  # The default active status of new user
                'STAFF_STATUS': True,  # The staff status of new user
                'SUPERUSER_STATUS': False,  # The superuser status of new user
            },
            'ATTRIBUTES_MAP': {  # Change Email/UserName/FirstName/LastName to corresponding SAML2 userprofile attributes.
                'email': 'Email',
                'username': 'UserName',
                'first_name': 'FirstName',
                'last_name': 'LastName',
            },
            'TRIGGER': {
                'CREATE_USER': 'path.to.your.new.user.hook.method',
                'BEFORE_LOGIN': 'path.to.your.login.hook.method',
            },
        }

#. In your SAML2 SSO service provider, set Single-sign-on URL and Audience URI(SP Entity ID) to http://your-domain/saml2_auth/acs/


Explanation
-----------

**METADATA_AUTO_CONF_URL** Auto SAML2 metadata configuration URL

**NEW_USER_PROFILE** Everytime when a new user login, we will create the user with this default options in system.

**ATTRIBUTES_MAP** map django user attributes to SAML2 user attributes.

**TRIGGER** If you want to do some additional actions, just use trigger.

**TRIGGER.CREATE_USER** Dot-separated style string, path to a method which receiving ONE dict parameter. This method will be triggered when a **new**
user login, before we logged in this user, after we created the user with default options. You may want to run some new-user-related tasks in this trigger.

**TRIGGER.BEFORE_LOGIN** Similar to CREATE_USER, but will be triggered only when an **existed** user login, before we logged in this user, after we got 
attributes from okta. You may want to update user information before a user logged-in in this trigger.




Customize
=========

You are allowed to override the default permission `denied` page and new user `welcome` page.

Just put a template named 'django_saml2_auth/welcome.html' or 'django_saml2_auth/denied.html' under your project's template folder.

In case of 'django_saml2_auth/welcome.html' existed, when a new user logged in, we'll show this template instead of redirecting user to the 
previous visited page. So you can have some first-visit notes and welcome words in this page. You can get user context in the template by 
using `user` context.

By the way, we have a built-in logout page as well, if you want to use it, just add the following lines into your urls.py, before any 
`urlpatterns`:

.. code-block:: python

    # If you want to replace the default user logout with plugin built-in page, just use the following line (optional)
    url(r'^accounts/logout/$', 'django_saml2_auth.views.signout'),

    # If you want to replace the admin logout with SAML2, use the following line (optional)
    url(r'^admin/logout/$', 'django_saml2_auth.views.signout'),

In a similar way, you can customize this logout template by added a template 'django_saml2_auth/signout.html'.


By default, we assume your SAML2 service provided user attribute Email/UserName/FirstName/LastName. Please change it to the correct 
user attributes mapping.



For okta Users
==============

I created this plugin original for okta.

You can find the METADATA_AUTO_CONF_URL under saml2 app's `Sign On` tab, in the Settings box, you will see 

`Identity Provider metadata is available if this application supports dynamic configuration.`

Just use the link in text "Identity Provider metadata".


How to Contribute
=================

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/fangli/django-saml2-auth
.. _AUTHORS: https://github.com/fangli/django-saml2-auth/blob/master/AUTHORS.rst


