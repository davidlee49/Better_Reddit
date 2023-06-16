import datetime
import pytz
import calendar
import json
import os


def get_date(epoch):
    # Convert epoch to datetime
    # dt = datetime.datetime.fromtimestamp(epoch)
    dt = datetime.datetime.fromtimestamp(epoch, pytz.timezone('utc'))

    # Format datetime as a string
    # formatted_datetime = dt.strftime('%Y-%m-%d')
    #
    # return formatted_datetime

    formatted_datetime = dt.strftime('%Y-%m-%d')
    # print(formatted_datetime)
    return formatted_datetime

def get_days_in_month(item_path):
    file = item_path.split('\\')
    date = file[-1].split('_')
    year, month = date[1].split('-')

    # Create a datetime object for the specified month and year
    # date = datetime.datetime(int(year), int(month), 1)

    # Get the number of days in the specified month
    return calendar.monthrange(int(year), int(month))[1]


def log_event(file_path, completion_status, skipped_posts, error=None):
    cur_file = os.path.basename(file_path)
    log_path = r"C:\Users\ryu28\PycharmProjects\BetterReddit\error_report.json"

    log_event = {
        'completed': completion_status,
        'last_line_added': skipped_posts,
        'error': error
    }

    with open(log_path, 'r') as log:
        log_json = json.load(log)

    if cur_file not in log_json:
        log_json[cur_file] = [log_event]
    else:
        log_json[cur_file].append(log_event)

    with open(log_path, 'w') as log:
        json.dump(log_json, log, indent=4)