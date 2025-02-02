from django.utils import timezone
import pandas as pd
def get_current_shift():
    current_hour = timezone.localtime().hour
    return 1 if 8 <= current_hour < 20 else 2


def process_list_field(value):
    """Convert string to cleaned, unique list of items"""
    if pd.isna(value) or value.strip() == '':
        return []
    return sorted(list(set(
        item.strip() 
        for item in str(value).split(',') 
        if item.strip()
    )))