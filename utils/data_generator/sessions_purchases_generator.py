import json
from utils import *
from collections import Counter

transaction_type_list = [
    'credit_card',
    'cash',
    'paypal'
]

def get_zipped_data(records, users):
    session_ids = (n for n in range(records))
    transaction_types = 
    amounts = 
    timestamps = 

    return zip(session_ids, user_ids)

def write_json(zipped, records, file_index):
    file_name = f'sessions_purchases/sessions_purchases_{file_index:03}.json'
    print(f'Creating file {file_name} with {records} records')

    try:
        with open(file_name, 'w+') as f:
            data = get_n_records_iter(zipped, records)
            written = 0
            for session_id, user_id in data:
                record = {i
                    'session_id': session_id,
                    'transaction_type': transaction_type,
                    'amount': amount,
                    'timestamp': timestamp,
                }
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
