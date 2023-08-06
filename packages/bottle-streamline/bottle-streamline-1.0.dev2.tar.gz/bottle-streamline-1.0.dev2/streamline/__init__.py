from .base import RouteBase
from .template import TemplateRoute, XHRPartialRoute, ROCARoute
from .forms import FormRoute, TemplateFormRoute, XHRPartialFormRoute


__version__ = '1.0.dev1'
__author__ = 'Outernet Inc'
__all__ = (
    RouteBase,
    TemplateRoute,
    XHRPartialRoute,
    ROCARoute,
    FormRoute,
    TemplateFormRoute,
    XHRPartialFormRoute,
)
