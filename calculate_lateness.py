from datetime import datetime, timedelta
from dateutil import tz
import math
import argparse
import pandas as pd
import os


def load_data(file):
    data = pd.read_csv(file, sep='\t')
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
        return 1
    else:
        minutes_diff = (submission_time - deadline).total_seconds() / 60.0
        if minutes_diff <= 0:
            return 0
        else:
            return ((10/72) * minutes_diff)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_path', required=True, type=str, help="directory that stores Quercus spreadsheet, file lists, and CrowdMark spreadsheets")
    args = parser.parse_args()

    path_to_file_list = os.path.join(args.dir_path, "assignment_list.csv")
    file_list = pd.read_csv(path_to_file_list, sep='\t')
    quercus_filename = ""
    for dirpath, dirname, filenames in os.walk(args.dir_path):
        for filename in filenames:
            if "Grades" in filename and "updated" not in filename:

                #quercus_filename = os.path.join(args.dir_path, filename)

                quercus_filename = "ps/2019-12-18T1205_Grades-CSC263H1_F.csv"

    # quercus_df = load_data(quercus_filename)
    quercus_df = pd.read_csv(quercus_filename)
    quercus_df['SIS User ID'] = quercus_df['SIS User ID'].astype(float)

    for index, row in file_list.iterrows():
        deadline = datetime.strptime(row['Deadline'], '%Y-%m-%d %H:%M:%S').astimezone(tz=tz.tzlocal())
        crowdmark_data = load_data(os.path.join(args.dir_path, row['Crowdmark File']))


        quercus_column = row['Quercus Assignment']
        crowdmark_data['submission_time_local_tz'] = crowdmark_data.apply(lambda x: change_tz(x), axis=1)
        crowdmark_data['Penalty'] = crowdmark_data.apply(lambda x: lateness_function(x, deadline), axis=1)
        total_possible = float(quercus_df.iloc[1][quercus_column])
        crowdmark_data['Total After Penalty'] = (crowdmark_data['Total'] - (total_possible*crowdmark_data['Penalty'])).clip(lower=0)

        crowdmark_data.rename(columns={'Student ID': 'SIS User ID', 'Total After Penalty': quercus_column}, inplace=True)

        updated_crowdmark_marks = crowdmark_data[['SIS User ID', quercus_column]]
        quercus_df = quercus_df.drop([quercus_column], axis=1)

        updated_crowdmark_marks = updated_crowdmark_marks.dropna(subset=['SIS User ID'])
        updated_crowdmark_marks['SIS User ID'] = updated_crowdmark_marks['SIS User ID'].astype(float)


        quercus_df = quercus_df.merge(updated_crowdmark_marks, on=['SIS User ID'], how='left')


    out_file = "{}_updated.csv".format(quercus_filename[:-4])
    quercus_df.to_csv(out_file, sep=',', index=False)

if __name__ == "__main__":
    main()
