# User Journeys Replayer

This demo shows how to replay recorded user journeys of your website on Cloud Run jobs.

## Record your user journeys

1. Use [Chrome DevTools' Recorder](https://developer.chrome.com/docs/devtools/recorder/) to record critical user journeys for your publicly accessible website.
1. Export the replay using DevTools' Recorder [export feature](https://developer.chrome.com/docs/devtools/recorder/#edit-flows)
1. Save the exported `.js` file under the `journeys/` folder.

## Before you begin

1. Install the [`gcloud` command line](https://cloud.google.com/sdk/docs/install).
1. Create a Google Cloud project.
1. Set your current project in `gcloud`: 
```
gcloud config set project PROJECT_ID
```

## Replaying on Google Cloud

Run `./replay_on_gcp.sh` to setup and run a Cloud Run job to replay critical
user journeys. See [replay_on_gcp.sh](replay_on_gcp.sh) for details.

## Replaying every day

Run `./replay_every_day.sh` to create a Cloud Scheduler Job that will run the
Cloud Run Job every day. See [replay_every_day.sh](replay_every_day.sh) for
details.

## Testing locally

The following steps assume you have `docker` installed on your local machine. If you don't proceed to the next section to deploy to Google Cloud.

Build with:

```sh
docker build . -t user-journeys-demo
```

Run locally:

```sh
docker run --cap-add=SYS_ADMIN user-journeys-demo
```
