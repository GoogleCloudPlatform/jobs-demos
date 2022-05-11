# Cloud Run Jobs Nightly Invoice Processing

This job uses [Document AI](https://cloud.google.com/document-ai)
the process data from human-readable invoices
in a variety of file formats stored in a
[Cloud Storage](https://cloud.google.com/storage) bucket,
and saves that data in a
[Cloud Firestore](https://cloud.google.com/firestore) database.

## The code

The job being executed is in `processor/main.py`. That program
calls code from the `processor/process.py` module to work with
the Document AI and Cloud Firestore client libraries.

The Dockerfile defines a basic container to run Python
programs.

## Prepare for the job

* Create a Google Cloud project using the console or command
line. 

* Enable the Cloud Run API, Firestore API, and Cloud Document API.

    ```
    gcloud services enable \
    firestore.googleapis.com \
    run.googleapis.com \
    documentai.googleapis.com
    ```

* Navigate the the
[Document AI](https://console.cloud.google.com/ai/document-ai)
section and create a new _Invoice Parser_ processor. Learn how to [Create a Document AI processor in the console](https://cloud.google.com/document-ai/docs/create-processor#create-processor).

* Create a bucket in the command line or the console to hold invoices to process. 

    ```
    gsutil mb -l us-central1 gs://$GOOGLE_CLOUD_PROJECT-invoices
    ```

* New invoices should be place in a bucket folder called `incoming/` and
the file names should start with a lower-case hex digit
(one of 0123456789abcdef). Naming them with UUID4 value
works well.

    ```
    # Copy provided example invoices to bucket
    gsutil cp -r incoming/*.pdf gs://$GOOGLE_CLOUD_PROJECT-invoices/incoming
    ```

* Note the Bucket name, Cloud Project ID, and the Document AI Processor ID
which will be used in the command to create the job.

    ```
    export PROCESSOR_ID=<>
    export GOOGLE_CLOUD_PROJECT=<>
    export BUCKET=$GOOGLE_CLOUD_PROJECT-invoices
    ```

## Create the Cloud Run Job

* Cloud Run Jobs can create a job from a container. The
container can be built with a variety of tools, including
Google Cloud Build with the command:

    ```
    gcloud builds submit --tag=gcr.io/$GOOGLE_CLOUD_PROJECT/invoice-processor
    ```

* Once a container is available in a container repository, create
the job with the command:

    ```
    gcloud run jobs create invoice-processing \
    --image gcr.io/$GOOGLE_CLOUD_PROJECT/invoice-processor
    --region europe-west9 \
    --set-env-vars BUCKET=$BUCKET \
    --set-env-vars PROCESSOR_ID=$PROCESSOR_ID
    ```
    
## Execute the job

* Execute the job from the command line with the command:

    ```
    gcloud run jobs execute invoice-processing
    ```

## The complete pipeline

### Create a Cloud Scheduler job
Run your job nightly with a cron job.

* Create new service account
  ```
  gcloud iam service-accounts create process-identity
  ```

* Give the service account access to invoke the `invoice-processing` job
  ```
  gcloud alpha run jobs add-iam-policy-binding invoice-processing \
    --member serviceAccount:process-identity@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role roles/run.invoker
  ```
  Note: The job does not have a publicly available endpoint; therefore must the Cloud Scheduler Job must have permissions to invoke.

* Create Cloud Scheduler Job for every day at midnight:
  ```
  gcloud scheduler jobs create http my-job \
    --schedule="0 0 * * *" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$GOOGLE_CLOUD_PROJECT/jobs/invoice-processing:run" \
    --http-method=POST \
    --oauth-service-account-email=process-identity@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
  ```

### Deploy supporting services
This repo also includes services for uploading and reviewing the processed invoices.

* Deploy the Uploader service:

    ```
    gcloud run deploy uploader \
        --source uploader/ \
        --set-env-vars BUCKET=$BUCKET \
        --allow-unauthenticated
    ```

* Deploy the Reviewer service:

    ```
    gcloud run deploy reviewer \
        --source reviewer/ \
        --set-env-vars BUCKET=$BUCKET \
        --allow-unauthenticated
    ```