from datetime import datetime, timedelta
from dateutil import tz
import math
import argparse
import pandas as pd
import csv


def load_data(file):
    data = pd.read_csv(file)
    return data


def change_tz(x):
    if pd.isna(x['Submitted At']):
        return None

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    time_utc = x['Submitted At'].split(" UTC")[0]
    utc = datetime.strptime(time_utc, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    time_local = utc.astimezone(to_zone)
    return time_local


def lateness_function(x, deadline):
    submission_time = x['submission_time_local_tz']
    twelvelater = deadline + timedelta(hours=12)
    if (submission_time - twelvelater).total_seconds() > 0:
        return 100
    else:
        minutes_diff = (submission_time - deadline).total_seconds() / 60.0
        if minutes_diff <= 0:
            return 0
        else:
            return 100-math.pow(1-(10/72), minutes_diff)*100


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deadline', required=True, type=str,
                        help="assignment deadline in the format %Y-%m-%d %H:%M:%S, e.g. '2019-09-17 23:59:59'")
    parser.add_argument('--csv_path', required=True, type=str,
                        help="path to csv containing assignment grades downloaded from Crowdmark")

    args = parser.parse_args()

    deadline = datetime.strptime(args.deadline, '%Y-%m-%d %H:%M:%S').astimezone(tz=tz.tzlocal())
    data = load_data(args.csv_path)
    data['submission_time_local_tz'] = data.apply(lambda row: change_tz(row), axis=1)
    data['Penalty'] = data.apply(lambda row: lateness_function(row, deadline), axis=1)
    data['Total After Penalty'] = (data['Total'] - data['Penalty']).clip(lower=0)

    out_file = "{}_updated.csv".format(args.csv_path[:-4])
    data.to_csv(out_file, sep=',')

if __name__ == "__main__":
    main()