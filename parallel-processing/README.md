
# Parallel Processing

This demo shows how to use the Task Index and Task Count environment variables to allow parallel processing in Cloud Run Jobs


## Background

Typical batch processing systems would have a set of work being sent to a processing node, which would process the entire payload. By setting the `--tasks` in Cloud Run Jobs, you can have a number of tasks happening at once, but they would have the same input arguments, so batch separation needs to be determined by the task itself. 

The Task Index (`CLOUD_RUN_TASK_INDEX`) variable identifies the index of a worker, and the Task Count (`CLOUD_RUN_TASK_COUNT`) variable holds the value of `--tasks`. Using these two values, the data to be processed can be split into `task_count` chunks, with each worker performing the `task_index` element.  This ensures that the entire data set that needs to be processed is separated between all tasks, and no data is processed twice. 

In this sample, the data set is a single Cloud Storage object containing a list of inputs to be processed. Each task takes the index and count information, splits the contents of the object into chunks, and processes one chunk as determined by it's index.

You can adapt this model further, such as processing a chunk of Cloud Storage objects, a chunk of records in a Cloud SQL database, etc. 


## Before you begin



1. Install the <code>[gcloud](https://cloud.google.com/sdk/docs/install)</code> command line.
2. Create a Google Cloud project.
3. Set your current project in <code>gcloud</code>: 
    ```
    gcloud config set project PROJECT_ID
    ```


## Deploying the sample

Run `./deploy-parallel-job.sh` to setup and run a job that will parallel process a large Cloud Storage object. See [deploy-parallel-job.sh](deploy-parallel-job.sh) for details
