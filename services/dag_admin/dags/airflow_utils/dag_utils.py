from airflow.utils.dates import days_ago
from datetime import timedelta

def get_airflow_defaults(cron_expr):
    return {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': days_ago(1),
        'email': ['airflow@airflow.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
        'schedule_interval': cron_expr
    }
