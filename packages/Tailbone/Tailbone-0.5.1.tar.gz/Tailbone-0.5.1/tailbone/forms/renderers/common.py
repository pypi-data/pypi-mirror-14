# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2014 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Common Field Renderers
"""

from __future__ import unicode_literals

import formalchemy
from formalchemy.fields import FieldRenderer, SelectFieldRenderer, CheckBoxFieldRenderer
from pyramid.renderers import render

from tailbone.util import pretty_datetime


class AutocompleteFieldRenderer(FieldRenderer):
    """
    Custom renderer for an autocomplete field.
    """

    service_route = None
    width = '300px'

    @property
    def focus_name(self):
        return self.name + '-textbox'

    @property
    def needs_focus(self):
        return not bool(self.value or self.field_value)

    @property
    def field_display(self):
        return self.raw_value

    @property
    def field_value(self):
        return self.value

    @property
    def service_url(self):
        return self.request.route_url(self.service_route)

    def render(self, **kwargs):
        kwargs.setdefault('field_name', self.name)
        kwargs.setdefault('field_value', self.field_value)
        kwargs.setdefault('field_display', self.field_display)
        kwargs.setdefault('service_url', self.service_url)
        kwargs.setdefault('width', self.width)
        return render('/forms/field_autocomplete.mako', kwargs)

    def render_readonly(self, **kwargs):
        value = self.field_display
        if value is None:
            return u''
        return unicode(value)


class DateTimeFieldRenderer(formalchemy.DateTimeFieldRenderer):
    """
    Custom date/time field renderer, which displays a "pretty" value in
    read-only mode, leveraging config to show the correct timezone.
    """

    def render_readonly(self, **kwargs):
        value = self.raw_value
        if not value:
            return ''
        return pretty_datetime(self.request.rattail_config, value)


class EnumFieldRenderer(SelectFieldRenderer):
    """
    Renderer for simple enumeration fields.
    """

    enumeration = {}

    def __init__(self, arg):
        if isinstance(arg, dict):
            self.enumeration = arg
        else:
            self(arg)

    def __call__(self, field):
        super(EnumFieldRenderer, self).__init__(field)
        return self

    def render_readonly(self, **kwargs):
        value = self.raw_value
        if value is None:
            return u''
        return self.enumeration.get(value, unicode(value))

    def render(self, **kwargs):
        opts = [(self.enumeration[x], x) for x in self.enumeration]
        return SelectFieldRenderer.render(self, opts, **kwargs)


class DecimalFieldRenderer(formalchemy.FieldRenderer):
    """
    Sort of generic field renderer for decimal values.  You must provide the
    number of places after the decimal (scale).  Note that this in turn relies
    on simple string formatting; the renderer does not attempt any mathematics
    of its own.
    """

    def __init__(self, scale):
        self.scale = scale

    def __call__(self, field):
        super(DecimalFieldRenderer, self).__init__(field)
        return self

    def render_readonly(self, **kwargs):
        value = self.raw_value
        if value is None:
            return ''
        fmt = '{{0:0.{0}f}}'.format(self.scale)
        return fmt.format(value)


class CurrencyFieldRenderer(formalchemy.FieldRenderer):
    """
    Sort of generic field renderer for currency values.
    """

    def __init__(self, field):
        super(CurrencyFieldRenderer, self).__init__(field)

    def render_readonly(self, **kwargs):
        value = self.raw_value
        if value is None:
            return ''
        # TODO: Add py2.6-compatible way to include thousands separator
        # (comma).  Apparently the ',' trick is py2.7+ only.
        return '$ {0:0.2f}'.format(value)


class YesNoFieldRenderer(CheckBoxFieldRenderer):

    def render_readonly(self, **kwargs):
        value = self.raw_value
        if value is None:
            return u''
        return u'Yes' if value else u'No'
