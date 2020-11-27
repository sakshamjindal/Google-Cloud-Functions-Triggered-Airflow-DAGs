
## Cloud Functions Triggered DAGs

The following guide walks through the entire worflow on how to trigger a dag using Cloud Functions

#### Step 1. Make a Cloud Composer Environment [(link)](https://cloud.google.com/composer/docs/how-to/using/managing-dags#gcloud)

Spin up a Google Cloud Compose Environment [(link)](https://cloud.google.com/composer/docs/how-to/managing/creating#creating_a_new_environment)

```
gcloud composer environments create composer1 \
    --location euope-west2
```


Determine the storage bucker assosciated with the environment [(link)](https://cloud.google.com/composer/docs/how-to/using/managing-dags#gcloud)
```
gcloud composer environments describe compose 1 \
  --location europe-west2 \
  --format="get(config.dagGcsPrefix)"
```

#### Step 2. Set up Google Cloud Functions to trigger dags [(link)](https://cloud.google.com/composer/docs/how-to/using/triggering-with-gcf)

The google cloud functions needs to be deployed to trigger the dags on any changes in the environment. We create a cloud function called `gcs-dag-trigger-function` on using the above mentioned guide. 

For creating the function, we need the following parameters from the composer environment
- `client_id` :  Client id (can be fetched by running the scrip `get_client.py` in the main directory)
- `webserver_id` : URL of the web server on which airflow is currently running [(here)](https://cloud.google.com/composer/docs/how-to/accessing/airflow-web-interface)
- `dag_name`: The name of the dag which is triggered (discussed below; here it is called ` composer_sample_trigger_response_dag
schedule`)

#### Step 3. Putting together the DAG definition

Once the above steps are done, the entire dag configuration is defined in the main folder in the file `trigger_dag.py` with the dag named as `composer_sample_trigger_response_dag
schedule`

To push the latest version of the dag to the composer environment, run the following command in the main folder containing the dag file:
```
gcloud composer environments storage dags import \
                            --environment composer1 \
                            --location europe-west2 \
                            --source trigger_dag.py 
```