# templatetags/roman_numerals.py
from django import template
from roman import toRoman

register = template.Library()

@register.filter(name='month_to_roman')
def month_to_roman(value):
    print('val', value)
    try:
        # Assuming value is a valid month number (1 to 12)
        return toRoman(int(value))
    except ValueError:
        return value

def conv_month_to_roman(value):
    try:
        return toRoman(int(value))
    except ValueError:
        return value

    