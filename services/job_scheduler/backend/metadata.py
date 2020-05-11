from pyspark.sql import SparkSession
from os import path
from collections import Counter

class Metadata():
    def __init__(self, source_type, database=None, table=None, filename=None):
        if source_type is None:
            extensions = [f.split('.')[1] for f in listdir(filename) if isfile(join(filename, f))]
            cntr = Counter(extensions)
            sorted_extensions = {k: v for k, v in sorted(cntr.items(), key=lambda item: item[1])}
            source_type = sorted_extensions.keys()[0]
        spark = (
            SparkSession.builder
                      .appName('Metadata extractor')
                      .config('spark.jars.packages', 'com.crealytics:spark-excel_2.11:0.11.1')
                      .config('spark.sql.shuffle.partitions', '10')
                         # Allows quicker transformations between pandas and spark dataframes
                      .config('spark.sql.execution.arrow.enabled', 'true')
                      .getOrCreate()
        )
        switcher = {
            'csv': self.get_csv,
            'xlsx': self.get_excel,
            'json': self.get_json,
            'mysql': self.get_mysql
        }
        f = switcher.get(source_type, 'Invalid option')
        source_path = ''
        if f is not None:
            if source_type == 'mysql':
                df = f(database, table, spark)
                source_path = '{}.{}'.format(database, table)
            else:
                df = f(filename, spark)
                source_path = filename
        else:
            raise Exception('Unable to find option {}'.format(input_type))

        # TODO: get the real size from mysql
        self.size = 0 if source_type == 'mysql' else path.getsize(filename)
        self.source_type = source_type

    def get_csv(self, file_name, spark):
        df = spark.read.option('header', 'true').csv(file_name)
        return df

    def get_excel(self, file_name, spark, sheet_name='Sheet1'):
        data_address = f"'{sheet_name}'!A1"

        df = (
            spark.read
                .format('com.crealytics.spark.excel')
                .option('dataAddress', data_address)
                .option('useHeader', True)
                .option('multiline', True)
                .option('inferSchema', True)
                .load(filename)
        )

        return df

    def get_json(self, file_name, spark):
        df = spark.read.json(file_name)
        return df

    def get_mysql(self, database, table, spark):
        url = f'jdbc:mysql://{host}:{port}/{database}?useUnicode=true'

        properties = {'user' : 'user',
                      'password' : 'password',
                      'driver' : 'com.mysql.cj.jdbc.Driver',
                      'autoReconnect' : 'true',
                      'useSSL' : 'false',
                      'serverTimezone' : 'UTC'}

        df = spark.read.jdbc(url=url, table=table, properties=properties)
        return df

