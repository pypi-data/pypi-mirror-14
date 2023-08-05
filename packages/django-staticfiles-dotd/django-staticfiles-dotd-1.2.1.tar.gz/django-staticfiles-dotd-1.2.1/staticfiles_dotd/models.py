import monkeypatch

from django.core.management.base import CommandError
from django.contrib.staticfiles.management.commands.collectstatic import Command

from .views import serve

def set_options(self, *args, **kwargs):
    set_options._set_options(self, *args, **kwargs)

    if self.symlink:
        raise CommandError(
            "--link is not yet supported with django-staticfiles-dotd"
        )

monkeypatch.patch(serve, 'django.contrib.staticfiles.views', 'serve')
monkeypatch.patch(set_options, Command, 'set_options')
