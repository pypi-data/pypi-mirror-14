# -*- coding: utf-8 -*-
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.db import models

class HolidayType(models.Model):
    name = models.CharField(_('Holiday name'), max_length=60)

    def __str__(self):
        return self.name


class ACPHoliday(models.Model):
    date = models.DateField(_('Date'), unique=True)
    holiday_type = models.ForeignKey(HolidayType, verbose_name=_('Holiday type'))

    def __str__(self):
        return '%s %s' % (self.date.strptime('%Y-%m-%d'), self.holiday_type)

    class Meta:
        ordering = ('date',)

    @staticmethod
    def validate_dates(start_date, end_date):
        last_holiday = ACPHoliday.objects.all().last()
        if end_date > last_holiday.date:
            raise ValueError(_('End date exceed the last registered holiday'))
        first_holiday = ACPHoliday.objects.all().first()
        if start_date < first_holiday.date:
            raise ValueError(_('Start date precedes the first registered holiday'))

    @staticmethod
    def get_working_days(start_date, end_date, **kwargs):
        ACPHoliday.validate_dates(start_date, end_date)
        day_generator = ACPHoliday.days_in_range_generator(start_date, end_date)
        holidays_in_range = ACPHoliday.objects.filter(date__gte=start_date, date__lte=end_date).count()
        working_days = sum(1 for day in day_generator if day.weekday() < 5)
        return working_days - holidays_in_range


    @staticmethod
    def days_in_range_generator(start_date, end_date):
        start_date = start_date - timedelta(1)
        day_generator = (start_date + timedelta(x + 1) for x in range((end_date - start_date).days))
        return day_generator


