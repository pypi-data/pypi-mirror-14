from datetime import datetime


def load_data(apps, schema_editor):
    HolidayType = apps.get_model("acp_calendar", "HolidayType")
    for holiday_type in get_holiday_type_list():
        HolidayType.objects.create(**holiday_type)

    ACPHoliday = apps.get_model("acp_calendar", "ACPHoliday")
    for holiday_data in get_holidays_list():
        holiday_type = HolidayType.objects.get(name=holiday_data['holiday_type'])
        holiday_data['holiday_type'] = holiday_type
        ACPHoliday.objects.create(**holiday_data)


def get_holiday_type_list():
    holiday_types = [{'name': 'Año Nuevo'},
                     {'name': 'Día de los Mártires'},
                     {'name': 'Martes Carnaval'},
                     {'name': 'Viernes Santo'},
                     {'name': 'Día del Trabajador'},
                     {'name': 'Día de la Separación de Panamá de Colombia'},
                     {'name': 'Día de Colón'},
                     {'name': 'Primer Grito de Independencia'},
                     {'name': 'Independencia de Panamá de España'},
                     {'name': 'Día de la Madre'},
                     {'name': 'Navidad'},
                     ]
    return holiday_types


def get_holidays_list():
    holidays_16 = [{'date': datetime.strptime('2016-01-01', '%Y-%m-%d'), 'holiday_type': 'Año Nuevo'},
                   {'date': datetime.strptime('2016-01-08', '%Y-%m-%d'), 'holiday_type': 'Día de los Mártires'},
                   {'date': datetime.strptime('2016-02-09', '%Y-%m-%d'), 'holiday_type': 'Martes Carnaval'},
                   {'date': datetime.strptime('2016-03-25', '%Y-%m-%d'), 'holiday_type': 'Viernes Santo'},
                   {'date': datetime.strptime('2016-05-02', '%Y-%m-%d'), 'holiday_type': 'Día del Trabajador'},
                   {'date': datetime.strptime('2016-11-03', '%Y-%m-%d'),
                    'holiday_type': 'Día de la Separación de Panamá de Colombia'},
                   {'date': datetime.strptime('2016-11-04', '%Y-%m-%d'), 'holiday_type': 'Día de Colón'},
                   {'date': datetime.strptime('2016-11-10', '%Y-%m-%d'),
                    'holiday_type': 'Primer Grito de Independencia'},
                   {'date': datetime.strptime('2016-11-28', '%Y-%m-%d'),
                    'holiday_type': 'Independencia de Panamá de España'},
                   {'date': datetime.strptime('2016-12-08', '%Y-%m-%d'), 'holiday_type': 'Día de la Madre'},
                   {'date': datetime.strptime('2016-12-26', '%Y-%m-%d'), 'holiday_type': 'Navidad'},
                   ]
    return holidays_16
