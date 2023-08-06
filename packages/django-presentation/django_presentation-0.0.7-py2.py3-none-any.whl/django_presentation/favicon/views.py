from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic.base import RedirectView


class Favicon(RedirectView):
    """A view that returns the path to the favicon for the particular environment that we're running in.
    `environmentMap` contains a dict mapping `settings.DJANGO_ENVIRONMENT` to a path that is passed to `static`.
    If `settings.DJANGO_ENVIRONMENT` is not in `environmentMap` or the path is None, uses the `defaultFavicon`."""
    permanent=True
    defaultFavicon='images/favicon.ico'
    environmentMap={
        'local':'images/favicon/favicon_local.ico',
        'dev':'images/favicon/favicon_dev.ico',
        'test':'images/favicon/favicon_test.ico',
    }


    def get_redirect_url(self,*args,**kwargs):
        path=self.environmentMap.get(settings.DJANGO_ENVIRONMENT,None)
        if path is None:
            path=self.defaultFavicon
        return static(path)
