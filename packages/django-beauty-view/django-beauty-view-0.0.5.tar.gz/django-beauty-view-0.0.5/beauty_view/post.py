# -*- coding: utf-8 -*-
from django.http import Http404


class OnlyPostMixin(object):
    def get(self, request, *args, **kwargs):
        raise Http404
