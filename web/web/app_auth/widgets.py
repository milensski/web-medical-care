import datetime

from django import forms


class DatePickerInput(forms.DateInput):
    input_type = 'date'

    def format_value(self, value):
        if isinstance(value, datetime.date):
            value = value.strftime('%Y-%m-%d')
        return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['min'] = datetime.datetime.now().date().isoformat()
        # context['widget']['attrs']['disabled_dates'] = ['2023-07-01',
        #                                                 '2023-07-05']  # Add your list of disabled dates here
        return context

