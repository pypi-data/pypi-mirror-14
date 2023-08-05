# coding: utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


def openid_config(request):
    return {
        'openid_login_link': mark_safe(
            '<a href="%s?next=%s">Login with your PBS account</a>'
            % (reverse('login_begin'), request.get_full_path())
        )
    }
