from django.utils import timezone
import pandas as pd

def get_current_shift():
    current_hour = timezone.localtime().hour
    return 1 if 8 <= current_hour < 20 else 2

# def get_current_shift_with_date():
#     current_time = timezone.localtime()
#     current_hour = current_time.hour
#     current_date = current_time.date()
    
#     if 8 <= current_hour < 20:
#         # Shift 1 belongs to the current date
#         return {
#             'shift': 1,
#             'shift_date': current_date
#         }
#     else:
#         # Shift 2 belongs to the current date if it's after 20:00,
#         # otherwise it belongs to the previous date
#         if current_hour >= 20:
#             return {
#                 'shift': 2,
#                 'shift_date': current_date
#             }
#         else:  # current_hour < 8
#             # For hours 0-7, it's the previous day's shift 2
#             previous_date = current_date - timezone.timedelta(days=1)
#             return {
#                 'shift': 2,

#             }

def process_list_field(value):
    """Convert string to cleaned, unique list of items"""
    if pd.isna(value) or value.strip() == '':
        return []
    return sorted(list(set(
        item.strip() 
        for item in str(value).split(',') 
        if item.strip()
    )))
    