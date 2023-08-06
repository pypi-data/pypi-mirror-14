from datetime import datetime

from jsonview.decorators import json_view

from .models import ACPHoliday


@json_view
def working_days(request, start_date, end_date):
    d_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    d_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    results = {'start_date': start_date,
               'end_date': end_date,
               'days': -1,
               }
    try:
        days = ACPHoliday.get_working_days(d_start_date, d_end_date)
        results['days'] = days
    except ValueError as e:
        results['error'] = str(e)
    return results
