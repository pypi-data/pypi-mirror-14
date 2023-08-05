# ~*~ coding: utf-8 ~*~
from django import __version__

if float(__version__[:3]) >= 1.9:
    import urls_new
    urlpatterns = urls_new.urlpatterns
else:
    import urls_old
    urlpatterns = urls_old.urlpatterns
