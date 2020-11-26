import datetime

import airflow
from airflow.operators import bash_operator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule


default_args = {
    'owner': 'Composer Example',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': datetime.datetime(2017, 1, 1),
}

def process_data(**kwargs):

    run_configs = (kwargs['dag_run'].conf)
    file_loc = "gs://" + "/".join(run_configs['id'].split('/')[:-1])
    print(file_loc)

with airflow.DAG(
        'composer_sample_trigger_response_dag',
        default_args=default_args,
        # Not scheduled, trigger only
        schedule_interval=None) as dag:

    # Print the dag_run's configuration, which includes information about the
    # Cloud Storage object change.
    print_gcs_info = bash_operator.BashOperator(
        task_id='print_gcs_info', bash_command='echo {{ dag_run.conf }}')

    get_file_metadata = PythonOperator(
        task_id="get_metadata",
        python_callable=process_data,
        provide_context=True
    )


    print_gcs_info>>get_file_metadata

