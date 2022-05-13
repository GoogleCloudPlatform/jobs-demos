# Cloud Run Jobs Demo Applications

[Cloud Run Jobs](https://cloud.google.com/run/docs/) allows you to run a container to completion without a server.

This repository contains a collection of samples for Jobs for various use cases.

**Note:** ⚠️ For preview, Cloud Run jobs are available only in the region **`europe-west9`**

## Samples

|          Sample                          |                     Description                                 |
| ---------------------------------------- | --------------------------------------------------------------- | 
| [Screenshot](./screenshot/)              | Create a Cloud Run job to take screenshots of web pages.        | 
| [User Journey Replayer](./user-journeys/)| Replay recorded user journeys of your website on Cloud Run jobs.| 
| [Invoice Processing](./invoice-processing-pipeline/)| Process invoices nightly from a GCS bucket.| 
| [Parallel Processing](./parallel-processing/) | Use the Task Index and Task Count environment variables to allow parallel processing in Cloud Run Jobs. |

## Contributing changes

Bug fixes are welcome, either as pull
requests or as GitHub issues.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## Licensing

Code in this repository is licensed under the Apache 2.0. See [LICENSE](LICENSE).

-------

This is not an official Google product.
