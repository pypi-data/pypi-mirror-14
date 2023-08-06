# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import decorators, REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text


class LoginRequiredMixin(object):
    @method_decorator(decorators.login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class AccessMixin(object):
    login_url = None
    raise_exception = True
    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_unauthenticated_users = True

    def get_login_url(self):
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                'Define {0}.login_url or settings.LOGIN_URL or override '
                '{0}.get_login_url().'.format(self.__class__.__name__))

        return force_text(login_url)


class PermissionRequiredMixin(AccessMixin):
    permission_required = None

    def get_permission_required(self, request=None):
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} requires the "permission_required" attribute to be '
                'set.'.format(self.__class__.__name__))

        return self.permission_required

    def check_permissions(self, request):
        perms = self.get_permission_required(request)
        if isinstance(perms, list):
            result = False
            for permission in perms:
                if not result:
                    result = request.user.has_perm(permission)
            return result
        else:
            return request.user.has_perm(perms)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(self.get_login_url())
        has_permission = self.check_permissions(request)

        if not has_permission:
            raise PermissionDenied

        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)
