import airflow
from airflow.operators import bash_operator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
import datetime

# definition of CONFIGS
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

BQ_PROJECT_NAME='proud-guide-296608'
BQ_DATASET_NAME='test_dataset'
BQ_TABLE_NAME='test_table1'

def get_metadata(**kwargs):

    run_configs = (kwargs['dag_run'].conf)
    file_location = "gs://" + "/".join(run_configs['id'].split('/')[:-1])
    file_name = "/".join(run_configs['id'].split('/')[1:-1])
    kwargs['task_instance'].xcom_push(key='file_name', value=file_name)

    return file_name

with airflow.DAG('composer_sample_trigger_response_dag',
        default_args=default_args,
        schedule_interval=None) as dag:

    # Step 1: 
    # Print the dag_run's configuration, which includes information about the
    # Cloud Storage object change.
    print_gcs_info = bash_operator.BashOperator(
        task_id='print_gcs_info', bash_command='echo {{ dag_run.conf }}')

    # Step 2:
    # Receives the metadata of the file uploaded from the dag's run configurations 
    # and pushes it using x-com
    get_file_metadata = PythonOperator(
        task_id="get_metadata",
        python_callable=get_metadata,
        provide_context=True
    )

    # Step 3:
    # Using xcom pull mechanism to get the filename to retrieve from the google cloud storage
    load_csv = GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq',
        bucket= 'my-test-bucker',
        source_objects=['{{  task_instance.xcom_pull(task_ids=["get_metadata"], key="file_name")[0]  }}'],
        destination_project_dataset_table= BQ_PROJECT_NAME + "." + BQ_DATASET_NAME + "." + BQ_TABLE_NAME,
        create_disposition='CREATE_IF_NEEDED',
        # write_disposition='WRITE_TRUNCATE',
        dag=dag)

    # DAG Task Dependency COnfiguration
    print_gcs_info>>get_file_metadata>>load_csv