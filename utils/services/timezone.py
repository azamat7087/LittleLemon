from django.utils import timezone
import pytz


def convert_to_local_timezone(date):
    return timezone.localtime(date, pytz.timezone('Asia/Almaty'))
