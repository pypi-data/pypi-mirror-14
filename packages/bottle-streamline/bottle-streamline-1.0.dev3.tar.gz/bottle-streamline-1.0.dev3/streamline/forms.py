"""
This module contains mixins and classes for working with forms.
"""

from .base import RouteBase
from .template import TemplateRoute, XHRPartialRoute


class FormAdaptor(object):
    """
    This class servers as an adaptor for 3rd party form APIs that works with
    the default form-handling API in this module. It can also be used on its
    own as it provides basic means of performing validation of form data.

    The adaptor is instantiated with a dict-like object (usually
    :py:class:`~bottle.FormsDict`).
    """

    #: Mapping of fields names to validator functions. Validator functions are
    #: expected to take the field value as single positional argument, and
    #: return a boolean result of validation.
    validators = {}

    def __init__(self, data={}):
        self.data = data

    def is_valid(self):
        """
        Perform validation and return a boolean result.
        """
        for field, validator in self.validators.items():
            if not validator(self.data.get(field)):
                return False
        return True


class FormMixin(object):
    """
    Mixin that provides form-related functionality. The methods and properties
    in this class are implemented in a way that allows easy customization for
    any form API by focusing on the workflow rather than concreate APIs.
    """

    #: Form factory function or class. By default, the value of this property
    #: is used to construct form objects. Default form factory is
    #: :py:class:`~streamline.forms.FormAdaptor`.
    form_factory = FormAdaptor

    def get_form_factory(self):
        """
        Return form factory function/class. Default behvarior is to return the
        :py:attr:`~FormMixin.form_factory` property.
        """
        return self.form_factory

    def get_unbound_form(self):
        """
        Return unbound form object.
        """
        form_factory = self.get_form_factory()
        return form_factory()

    def get_bound_form(self):
        """
        Return bound form object.
        """
        form_factory = self.get_form_factory()
        return form_factory(self.request.forms)

    def get_form(self):
        """
        Return form object. Depending on the HTTP verb, this method returns
        either an unbound (GET) or a bound (all other verbs) form. Once a form
        object is created, this method will keep returning the previously
        created instance.
        """
        if hasattr(self, 'form'):
            return self.form
        if self.method == 'get':
            return self.get_unbound_form()
        return self.get_bound_form()

    def validate_form(self, form):
        """
        Perform validation and return the results of validation.
        """
        return form.is_valid()

    def show_form(self, *args, **kwargs):
        """
        Prepare for rendering a blank, unbound form.
        """
        return {}

    def validate(self, *args, **kwargs):
        """
        Branch to one of the outcome methods depending on form validation
        result. The business logic should be writen in the outcome methods
        :py:meth:`~form_valid` and :py:meth:`~form_invalid`.

        .. warning::
            An object that includes this mixin **must** set its ``form``
            property to a form object before this method is invoked. Failure to
            do this will result in ``AttributeError``. This is automatically
            handled in classes that include the
            :py:class:`~streamline.forms.FormBase` mixin.
        """
        if self.validate_form(self.form):
            return self.form_valid(*args, **kwargs)
        return self.form_invalid(*args, **kwargs)

    def form_valid(self, *args, **kwargs):
        """
        Handle positive form validation outcome.
        """
        pass

    def form_invalid(self, *args, **kwargs):
        """
        Handle negative form validation outcome.
        """
        pass


class FormBase(object):
    """
    Base mixin for form-related CBRH.
    """

    def get(self, *args, **kwargs):
        """
        Delegate to :py:meth:`~streamline.forms.FormMixin.show_form`.
        """
        return self.show_form(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Delegate to :py:meth:`~streamline.forms.FormMixin.validate`.
        """
        return self.validate(*args, **kwargs)


class FormRoute(FormMixin, FormBase, RouteBase):
    """
    Class for form handling without templates.

    :subclasses: :py:class:`~streamline.base.RouteBase`
    :includes: :py:class:`~streamline.forms.FormMixin`,
               :py:class:`~streamline.forms.FormBase`
    """

    def create_response(self):
        self.form = self.get_form()
        super(FormRoute, self).create_response()


class TemplateFormRoute(FormMixin, FormBase, TemplateRoute):
    """
    Class for form handling with template rendering.

    :subclasses: :py:class:`~streamline.template.TemplateRoute`
    :includes: :py:class:`~streamline.forms.FormMixin`,
               :py:class:`~streamline.forms.FormBase`
    """

    def get_context(self):
        ctx = super(TemplateFormRoute, self).get_context()
        ctx['form'] = self.get_form()
        return ctx

    def create_response(self):
        self.form = self.get_form()
        super(TemplateFormRoute, self).create_response()


class XHRPartialFormRoute(FormMixin, FormBase, XHRPartialRoute):
    """
    Class for form handling with XHR partial rendering support.

    :subclasses: :py:class:`~streamline.template.XHRPartialRoute`
    :includes: :py:class:`~streamline.forms.FormMixin`
               :py:class:`~streamline.forms.FormBase`
    """

    def get_context(self):
        ctx = super(XHRPartialFormRoute, self).get_context()
        ctx['form'] = self.get_form()
        return ctx

    def create_response(self):
        self.form = self.get_form()
        super(XHRPartialFormRoute, self).create_response()

ROCAFormRoute = XHRPartialFormRoute
