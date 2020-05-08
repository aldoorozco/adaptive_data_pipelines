import json
from utils import *
from collections import Counter

def get_zipped_data(records, users):
    session_ids = (n for n in range(records))
    user_ids = get_normal_dist(users, users/2, records)

    #cntr = Counter(sorted(user_ids))
    #srted = {k: v for k, v in sorted(cntr.items(), key=lambda item: item[1])}

    return zip(session_ids, user_ids)

def write_json(zipped, records, file_index):
    file_name = f'sessions_users/sessions_users_{file_index:03}.json'
    print(f'Creating file {file_name} with {records} records')

    try:
        with open(file_name, 'w+') as f:
            data = get_n_records_iter(zipped, records)
            written = 0
            for session_id, user_id in data:
                record = {'session_id': int(session_id), 'user_id': int(user_id)}
                f.write(json.dumps(record) + '\n')
                written += 1
            if written != records:
                print(f'ERROR: discrepancy between written {written} and expected {records}')
    except IOError:
        print('ERROR: Unable to write to file')

def main():
    records, files, users = get_records_files(3)

    records_per_file = int(records / files)

    zipped = get_zipped_data(records, users)
    for file_index in range(files):
        write_json(zipped, records_per_file, file_index)

if __name__ == '__main__':
    main()
