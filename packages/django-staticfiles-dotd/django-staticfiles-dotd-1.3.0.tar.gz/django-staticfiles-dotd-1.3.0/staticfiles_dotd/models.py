import monkeypatch

from .views import serve

monkeypatch.patch(serve, 'django.contrib.staticfiles.views', 'serve')
