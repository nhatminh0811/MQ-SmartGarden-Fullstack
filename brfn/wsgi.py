"""
WSGI config for brfn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brfn.settings")

application = get_wsgi_application()

if os.getenv("CREATE_ADMIN_USER", "False").lower() in {"1", "true", "yes", "on"}:
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        username = os.getenv("ADMIN_USERNAME", "admin")
        email = os.getenv("ADMIN_EMAIL", "admin@localhost")
        password = os.getenv("ADMIN_PASSWORD", "admin123")

        admin_user, created = User.objects.get_or_create(username=username)
        if created:
            admin_user.email = email
            admin_user.role = "admin"
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password(password)
            admin_user.save()
        else:
            if not admin_user.is_superuser or not admin_user.is_staff:
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.role = "admin"
                admin_user.save()
    except Exception as exc:
        # If the database is not ready yet (migrations not applied), skip admin creation.
        print("CREATE_ADMIN_USER skipped:", exc)
