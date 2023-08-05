from django.conf import settings

RENDER_FN = getattr(
    settings,
    'STATICFILES_DOTD_RENDER_FN',
    'staticfiles_dotd.utils.render',
)
