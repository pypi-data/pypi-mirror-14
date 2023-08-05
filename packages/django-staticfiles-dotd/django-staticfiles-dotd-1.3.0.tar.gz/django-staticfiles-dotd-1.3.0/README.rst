django-staticfiles-dotd
=======================


    STATICFILES_FINDERS = (
        'staticfiles_dotd.finders.DotDFinder',
         'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

You probably want to use ``django-pipeline`` over this.
