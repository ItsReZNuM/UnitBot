
import re
import math
import logging

logger = logging.getLogger(__name__)

UNITS = {
    'length': {
        'names': {
            'millimeter': 'mm', 'centimeter': 'cm', 'meter': 'm', 'kilometer': 'km', 'decimeter': 'dm',
            'inch': 'in', 'foot': 'ft', 'yard': 'yd', 'mile': 'mi',
            'mm': 'mm', 'cm': 'cm', 'm': 'm', 'km': 'km', 'dm': 'dm',
            'in': 'in', 'ft': 'ft', 'yd': 'yd', 'mi': 'mi'
        },
        'to_base': {
            'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000, 'dm': 0.1,
            'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
        },
        'base_unit': 'm',
        'emoji': '📏'
    },
    'weight': {
        'names': {
            'milligram': 'mg', 'gram': 'g', 'kilogram': 'kg', 'ton': 't', 'pound': 'lb',
            'mg': 'mg', 'g': 'g', 'kg': 'kg', 't': 't', 'lb': 'lb'
        },
        'to_base': {
            'mg': 0.000001, 'g': 0.001, 'kg': 1, 't': 1000, 'lb': 0.453592
        },
        'base_unit': 'kg',
        'emoji': '⚖️'
    },
    'area': {
        'names': {
            'centimeter square': 'cm2', 'meter square': 'm2', 'hectare': 'ha', 'inch square': 'in2', 'foot square': 'ft2', 'acre': 'acre',
            'cm2': 'cm2', 'm2': 'm2', 'ha': 'ha', 'in2': 'in2', 'ft2': 'ft2', 'acre': 'acre'
        },
        'to_base': {
            'cm2': 0.0001, 'm2': 1, 'ha': 10000, 'in2': 0.00064516, 'ft2': 0.092903, 'acre': 4046.86
        },
        'base_unit': 'm2',
        'emoji': '🏞️'
    },
    'volume': {
        'names': {
            'milliliter': 'ml', 'centimeter cubic': 'cm3', 'liter': 'l', 'meter cubic': 'm3', 'gallon': 'gal', 'barrel': 'bbl',
            'ml': 'ml', 'cm3': 'cm3', 'l': 'l', 'm3': 'm3', 'gal': 'gal', 'bbl': 'bbl', 'cc': 'cc'
        },
        'to_base': {
            'ml': 0.001, 'cm3': 0.001, 'l': 1, 'm3': 1000, 'gal': 3.78541, 'bbl': 158.987, 'cc': 0.001
        },
        'base_unit': 'l',
        'emoji': '🧴'
    },
    'time': {
        'names': {
            'second': 's', 'minute': 'min', 'hour': 'h', 'day': 'd', 'week': 'wk', 'month': 'mo', 'year': 'yr',
            's': 's', 'min': 'min', 'h': 'h', 'd': 'd', 'wk': 'wk', 'mo': 'mo', 'yr': 'yr'
        },
        'to_base': {
            's': 1, 'min': 60, 'h': 3600, 'd': 86400, 'wk': 604800, 'mo': 2.628e6, 'yr': 3.156e7
        },
        'base_unit': 's',
        'emoji': '⏱️'
    },
    'temperature': {
        'names': {
            'celsius': 'C', 'fahrenheit': 'F', 'kelvin': 'K',
            'C': 'C', 'F': 'F', 'K': 'K'
        },
        'to_base': {
            'C': lambda x: x, 'F': lambda x: (x - 32) * 5/9, 'K': lambda x: x - 273.15
        },
        'from_base': {
            'C': lambda x: x, 'F': lambda x: x * 9/5 + 32, 'K': lambda x: x + 273.15
        },
        'base_unit': 'C',
        'emoji': '🌡️'
    },
    'speed': {
        'names': {
            'meter per second': 'm/s', 'kilometer per hour': 'km/h', 'mile per hour': 'mph', 'mach': 'mach',
            'm/s': 'm/s', 'km/h': 'km/h', 'mph': 'mph', 'mach': 'mach'
        },
        'to_base': {
            'm/s': 1, 'km/h': 0.277778, 'mph': 0.44704, 'mach': 343
        },
        'base_unit': 'm/s',
        'emoji': '🚀'
    },
    'energy': {
        'names': {
            'joule': 'J', 'kilojoule': 'kJ', 'megajoule': 'MJ', 'watt hour': 'Wh', 'kilowatt hour': 'kWh', 'calorie': 'cal', 'kilocalorie': 'kcal',
            'J': 'J', 'kJ': 'kJ', 'MJ': 'MJ', 'Wh': 'Wh', 'kWh': 'kWh', 'cal': 'cal', 'kcal': 'kcal'
        },
        'to_base': {
            'J': 1, 'kJ': 1000, 'MJ': 1e6, 'Wh': 3600, 'kWh': 3.6e6, 'cal': 4.184, 'kcal': 4184
        },
        'base_unit': 'J',
        'emoji': '⚡️'
    },
    'pressure': {
        'names': {
            'pascal': 'Pa', 'kilopascal': 'kPa', 'atmosphere': 'atm', 'bar': 'bar', 'millimeter mercury': 'mmHg',
            'Pa': 'Pa', 'kPa': 'kPa', 'atm': 'atm', 'bar': 'bar', 'mmHg': 'mmHg'
        },
        'to_base': {
            'Pa': 1, 'kPa': 1000, 'atm': 101325, 'bar': 100000, 'mmHg': 133.322
        },
        'base_unit': 'Pa',
        'emoji': '🌬️'
    },
    'angle': {
        'names': {
            'degree': 'deg', 'radian': 'rad', 'gradian': 'grad',
            'deg': 'deg', 'rad': 'rad', 'grad': 'grad'
        },
        'to_base': {
            'deg': math.pi/180, 'rad': 1, 'grad': math.pi/200
        },
        'base_unit': 'rad',
        'emoji': '📐'
    },
    'digital': {
        'names': {
            'byte': 'B', 'kilobyte': 'KB', 'megabyte': 'MB', 'gigabyte': 'GB', 'terabyte': 'TB', 'petabyte': 'PB', 'exabyte': 'EB',
            'B': 'B', 'KB': 'KB', 'MB': 'MB', 'GB': 'GB', 'TB': 'TB', 'PB': 'PB', 'EB': 'EB'
        },
        'to_base': {
            'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4, 'PB': 1024**5, 'EB': 1024**6
        },
        'base_unit': 'B',
        'emoji': '💾'
    }
}


def persian_to_english_number(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(persian_digits, english_digits)
    return text.translate(translation_table)

def format_number(value):
    if value >= 100000:
        return f"{int(value):,}"
    elif value >= 1000:
        return f"{value:,.0f}"
    elif value < 0.01 and value > 0:
        return f"{value:.6f}".rstrip('0').rstrip('.')
    else:
        return f"{value:.2f}".rstrip('0').rstrip('.')

def convert_unit(value, from_unit, to_unit, category):
    try:
        if category == 'temperature':
            base_value = UNITS[category]['to_base'][from_unit](value)
            result = UNITS[category]['from_base'][to_unit](base_value)
        else:
            base_value = value * UNITS[category]['to_base'][from_unit]
            result = base_value / UNITS[category]['to_base'][to_unit]
        return format_number(result)
    except Exception as e:
        logger.error(f"Error in conversion from {from_unit} to {to_unit}: {str(e)}")
        raise

def find_unit(unit_str):
    if not unit_str:
        return None, None
    unit_str = unit_str.lower().strip()
    if unit_str == 'k':
        return 'K', 'temperature'
    for cat, data in UNITS.items():
        units = {k.lower(): v for k, v in data['names'].items()}
        if unit_str in units:
            return units[unit_str], cat
    return None, None

def parse_query(query):
    query = persian_to_english_number(query.strip())
    pattern = r'^(\d*\.?\d*)\s*([^\s]+)$'
    match = re.match(pattern, query)
    if not match:
        return None, None, None, "فرمت ورودی نادرست است. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nInvalid input format. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    value, from_unit_str = match.groups()
    try:
        value = float(value)
        if value == 0 and query.startswith('0'):
            return None, None, None, "عدد صفر معتبر نیست. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nZero value is not valid. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    except ValueError:
        return None, None, None, "عدد نامعتبر است. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nInvalid number. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    from_unit, category = find_unit(from_unit_str)
    if not from_unit:
        return None, None, None, f"واحد ({from_unit_str}) شناخته نشد. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nUnit ({from_unit_str}) not recognized. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    return value, from_unit, category, None