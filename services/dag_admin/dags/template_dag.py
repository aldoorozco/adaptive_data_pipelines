from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow_utils.dag_utils import get_airflow_defaults
from cluster import Cluster

template_dag = True

dag_name = 'placeholder_dag'
cron_expr = 'placeholder_cron'
task_name = 'placeholder_task'
sql_query = '''
placeholder_sql
'''
template_file = 'placeholder_template'
partitions = 'placeholder_partitions'
public_subnet = 'placeholder_public_subnet'
private_subnet = 'placeholder_private_subnet'
security_group = 'placeholder_security_group'
destination_table = 'placeholder_table'
logs_path = 'placeholder_logs_path'
master_sg = 'placeholder_master_sg'
slave_sg = 'placeholder_slave_sg'
destination_path = 'placeholder_destination_path'
service_access_sg = 'placeholder_service_access_sg'

sql_query = sql_query.strip()

args = [
    dag_name,
    template_file,
    sql_query,
    partitions,
    private_subnet,
    destination_table,
    logs_path,
    master_sg,
    slave_sg,
    destination_path,
    service_access_sg
]

if not template_dag:
    dag = DAG(dag_name, default_args=get_airflow_defaults(cron_expr))

    t1 = PythonOperator(
        task_id=task_name,
        python_callable=Cluster.create,
        op_args=args,
        dag=dag
    )
