"""Minimal settings needed for tests."""

import os

path_to_repo = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))

def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': 'sqlite.db'}},
        SECRET_KEY='Just a test key',
        JASMINE_TEST_DIRECTORY= '%s/%s' % (path_to_repo, 'example/jasmine/'),
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        INSTALLED_APPS=(
            'django_jasmine',
        ),
    )

    import django
    django.setup()
