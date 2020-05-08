import csv
import pandas as pd
import itertools
from random import randint
from utils import *

cols = ['user_id', 'full_name', 'email', 'city']
email_extension = '@gmail.com'
cities_list = [
    'Mexicali',
    'Hermosillo',
    'Veracruz',
    'Guadalajara',
    'Monterrey',
    'Tampico',
    'CDMX',
    'Pachuca',
    'Tuxtla Gutierrez',
    'Cancun',
    'Colima',
    'Tepic'
]

def get_zipped_data(records):
    user_ids = (n for n in range(records))
    full_names = list(get_full_names(records))
    emails = (s.lower().replace(' ', '.') + email_extension for s in full_names)
    cities = (cities_list[randint(0, len(cities_list) - 1)] for _ in range(records))

    return zip(user_ids, full_names, emails, cities)

def write_csv(zipped, records, file_index, cols):
    file_name = f'users/users_{file_index:03}.csv'
    print(f'Creating file {file_name} with {records} records')

    try:
        with open(file_name, 'w+') as f:
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            data = get_n_records_iter(zipped, records)
            written = 0
            for user_id, full_name, email, city in data:
                record = {'user_id': user_id, 'full_name': full_name, 'email': email, 'city': city}
                writer.writerow(record)
                written += 1
            if written != records:
                print(f'ERROR: discrepancy between written {written} and expected {records}')
    except IOError:
        print('ERROR: Unable to write to file')

def get_full_names(records):
    last_names_df = pd.read_csv('sources/apellidos.csv', encoding='latin-1') 
    male_names_df = pd.read_csv('sources/nombres_hombre.csv', encoding='latin-1') 
    female_names_df = pd.read_csv('sources/nombres_mujer.csv', encoding='latin-1') 

    names = male_names_df.NOMBRE.tolist() + female_names_df.NOMBRE.tolist()
    last_names = last_names_df.apellido.tolist()

    full_names = (f'{str(n).lower()} {str(ln1).lower()} {str(ln2).lower()}' for n in names for ln1 in last_names for ln2 in last_names)
    return get_n_records_iter(full_names, records)

def main():
    records, files = get_records_files(2)

    records_per_file = int(records / files)

    zipped = get_zipped_data(records)
    for file_index in range(files):
        write_csv(zipped, records_per_file, file_index, cols)

if __name__ == '__main__':
    main()
