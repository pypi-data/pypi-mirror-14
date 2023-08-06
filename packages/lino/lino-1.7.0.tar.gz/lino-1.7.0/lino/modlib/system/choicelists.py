# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Miscellaneous mixins for `lino.modlib.system`.

"""

from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from lino.core.choicelists import ChoiceList, Choice

from lino.utils import AttrDict


class YesNo(ChoiceList):
    """
    A choicelist with two values "Yes" and "No".

    .. django2rst::

        from lino.modlib.system.choicelists import YesNo
        rt.show(YesNo)

    Used e.g. to define parameter panel fields for BooleanFields::

      foo = dd.YesNo.field(_("Foo"), blank=True)


    """
    verbose_name_plural = _("Yes or no")
add = YesNo.add_item
add('y', _("Yes"), 'yes')
add('n', _("No"), 'no')


class Genders(ChoiceList):
    """
    Defines the two possible choices "male" and "female"
    for the gender of a person.

    .. django2rst::

            from lino.modlib.system.choicelists import Genders
            rt.show(Genders)


    See :ref:`lino.tutorial.human` for examples.
    See :doc:`/dev/choicelists`.
    """

    verbose_name = _("Gender")

add = Genders.add_item
add('M', _("Male"), 'male')
add('F', _("Female"), 'female')


class PeriodEvent(Choice):

    def add_filter(self, qs, obj):

        if isinstance(obj, datetime.date):
            obj = AttrDict(start_date=obj, end_date=obj)

        if obj.start_date is None or obj.end_date is None:
            return qs

        if self.name == 'started':
            qs = qs.filter(start_date__gte=obj.start_date)
            qs = qs.filter(start_date__lte=obj.end_date)
        elif self.name == 'ended':
            qs = qs.filter(end_date__isnull=False)
            qs = qs.filter(end_date__gte=obj.start_date)
            qs = qs.filter(end_date__lte=obj.end_date)
        elif self.name == 'active':
            qs = qs.filter(Q(start_date__isnull=True) |
                           Q(start_date__lte=obj.end_date))
            qs = qs.filter(Q(end_date__isnull=True) |
                           Q(end_date__gte=obj.start_date))
        return qs


class PeriodEvents(ChoiceList):
    """The list of things you can observe on a
    :class:`DatePeriod`. The default list has the following
    choices:

    .. django2rst::

        from lino.modlib.system.choicelists import PeriodEvents
        rt.show(PeriodEvents)

    """
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
    item_class = PeriodEvent


add = PeriodEvents.add_item
add('10', _("Starts"), 'started')
add('20', _("Is active"), 'active')
add('30', _("Ends"), 'ended')

