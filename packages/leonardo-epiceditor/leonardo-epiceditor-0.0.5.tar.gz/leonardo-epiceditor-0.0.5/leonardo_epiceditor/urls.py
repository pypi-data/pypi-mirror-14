
from django.conf.urls import url
from .views import EpicEditorView

from constance import config

urlpatterns = [
    url(r"^epiceditor/$",
        EpicEditorView.as_view(), name="epiceditor"),
]

if not config.LEONARDO_EPICEDITOR_PUBLIC:
    from leonardo.decorators import _decorate_urlconf
    _decorate_urlconf(urlpatterns)
