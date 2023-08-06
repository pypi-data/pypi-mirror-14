# -*- coding: utf-8 -*-

import calendar
import datetime
from collections import OrderedDict

from django.utils import timezone

from .models import Category, Event


class EventsMixin(object):
    def get_context_data(self, **kwargs):
        context = super(EventsMixin, self).get_context_data(**kwargs)
        context['events_categories'] = True
        context['categories'] = Category.objects.all()
        return context


class CategoryMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['current_category'] = self.category
        return context


class EventsQuerysetMixin(object):
    model = Event
    queryset = Event.objects.published()


class CalendarMixin(EventsQuerysetMixin):
    allow_future = True
    allow_empty = True
    month_format = '%m'
    date_field = 'date_url'

    def get_time_now(self):
        return timezone.now()

    def get_current_month(self):
        return datetime.date(year=int(self.get_year()), month=int(self.get_month()), day=1)

    def get_context_data(self, **kwargs):
        context = super(CalendarMixin, self).get_context_data(**kwargs)

        context['calendar_headings'] = self.get_calendar_day_names()
        context['calendar_events'] = self.get_events_list()

        return context

    def get_events_list(self):
        current_month = self.get_current_month()
        month_days = OrderedDict()

        cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
        for week in cal.monthdatescalendar(current_month.year, current_month.month):
            for i in week:
                month_days[i] = []

        for obj in self.object_list:
            event_date = obj.start.date()
            month_days[event_date].append(obj)

        return month_days.items()

    def get_calendar_day_names(self):
        calendar_days = []
        day_names = list(calendar.day_name)
        cal = calendar.Calendar(firstweekday=calendar.SUNDAY)

        for i in cal.iterweekdays():
            calendar_days.append(day_names[i])

        return calendar_days
