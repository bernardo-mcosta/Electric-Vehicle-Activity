# Electric Vehicle Activity Dashboard for Washington State, US

- [Electric Vehicle Activity Dashboard for Washington State, US](#electric-vehicle-activity-dashboard-for-washington-state-us)
  - [Scope](#scope)
  - [Data source](#data-source)
  - [Dashboard](#dashboard)
  - [Project Breakdown](#project-breakdown)
  - [How to reproduce](#how-to-reproduce)
    - [Pre-requisites](#pre-requisites)
    - [Steps to reproduce](#steps-to-reproduce)
  - [Improvements](#improvements)
  - [Linkedin](#linkedin)


## Scope

This project aims to develop a pipeline for extracting, transforming, and loading data to facilitate the creation of an interactive dashboard. The objective is to visualize trends in the evolving market of electric vehicle (EV) within the state of Washington and analyze EV adoption over time, as well as trends in the market such as leading automakers. 

Additionally, this project was also part of the [DataTalksClub's Engineering Zoomcamp Certification](https://github.com/DataTalksClub/data-engineering-zoomcamp).

## Data source 

The project utilizes data provided by the Washington State Department of Licensing at its  [official open data portal](https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2), specifically addressing electric vehicle title and registration activity.

The dataset contains 948k rows and 29 columns with data ranging from 2010 to 2024 (current date). Each rows is a transaction and the columns encompass information about the vehicle, transaction, fees and owner location. 

## Dashboard

The full dashboard built in Looker Studio can be accessed [here](https://lookerstudio.google.com/u/1/reporting/685d13cc-d55a-4133-a1c2-92caa371fb67/page/p_4lx3pm4dgd).

Please note that due to the GCP free-tier having a 90 day temporary access, the Looker Studio connection may be interrupted at the time of access. Below are the dashboard pages:

![Page 1](/assets/Electric_Vehicles_Activity_page-0001.jpg)
![Page 2](/assets/Electric_Vehicles_Activity_page-0002.jpg)

## Project Breakdown

![Architecture](/assets/architecture.jpg)

The project uses the following technologies:
  * Cloud Provider - Google Cloud Platform
  * Infrastructure as Code software - Terraform
  * Containerization - Docker
  * Workflow Orchestration - Mage
  * Data Transformation - dbt
  * Data Lake - Google Cloud Storage
  * Data Warehouse - BigQuery
  * Data Visualization - Looker Studio

The Google Cloud Platform (GCP) resources are provisioned using Terraform, which sets up a Google Cloud Storage bucket for a data lake and a BigQuery dataset for a data warehouse.

Two pipelines were created using Python and SQL and they were orchestrated by Mage, which runs through a Docker container.


1) The first one is called `api_to_gcp` and it extracts data from the Washington open data portal API, which is stored as .json, and loads it into a Google Cloud Storage bucket as partitioned .parquet files.
![pipeline 1](/assets/api_to_gcs.png)

1) The second pipeline is called `gcp_to_bigquery` and it reads data from the bucket and loads it into Bigquery as a partitioned external table. 
![pipeline 2](/assets/gcs_to_bigquery.png)

dbt is then used, pulling the source data stored in Bigquery to perform data transformations, such as casting data types and creating fact and dimension tables with SQL.
![pipeline 2](/assets/lineage.png)

Finally, Looker Studio imports the fact table created directly from Bigquery, and then the dashboard is created. 

## How to reproduce

### Pre-requisites
* Docker
* Terraform
* Optional: A GCP Virtual Machine setup with google cloud SDK

### Steps to reproduce
1) Setup a GCP account if you don't have one. A free account can be created and it has a 90 days trial. 
2) Create a new project and take note of its ID
3) Setup a GCP service account with the following roles:  Bigquery Admin, Storage Admin, Object Storage Admin. (note: this roles give broad permission and were listed here for simplicity)
4) Create an access key for this service account and save it as `keys.json`
5) Clone this repository
6) Create a folder called 'credentials'. Save `keys.json` in this folder. 
7) CD to the 01-terraform directory. 
8) Either set up the path to credentials in `main.tf` and `variables.tf` or use
``` 
export GOOGLE_APPLICATION_CREDENTIALS=credentials/keys.json
```
9) Edit `variables.tf` with your project ID and name the bucket and dataset. 
10) Run `terraform init` and then `terraform plan`
11) Run `terraform apply` and the GCP resources will be provisioned.
12) CD to the 02-mage directory
13) Rename `dev.env` to `.env`
14) Run `docker-compose build`. Docker will pull the contents of  /02-mage and ../credentials to the container, which means `keys.json` will be accessible there.
15) Run `docker-compose up` to initialize the container. 
16) Ensure the port 6789 described in `docker-compose.yml` is fowarded
17) Edit the code blocks to include the path to your credentials and with your GCP resources. The files you should edit are in the folders `data_loaders` and `data_exporters` :
    1)  `load_vehicles_gcs.py`
    2)  `evhicles_to_gcs.py`
18) Ensure the file `io_config.yaml` is pulling `keys.json`:
      ```
    # Google
    GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/credentials/keys.json"
    GOOGLE_LOCATION: southamerica-east1
19) Execute the pipelines. Watch this [video](https://www.youtube.com/watch?v=w0XmcASRUnc&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=24&pp=iAQB) fore more information.
20) Create a [dbt](https://www.getdbt.com/) free developer account
21) Create a new project and connect it to bigquery. Provide the `keys.json` file when asked for credentials. It's possible to load the content of a repository for simplicity. You can also replicate the contents of 03-dbt. 
22) Run `dbt build`. A green confirmation message will appear if it worked properly. 
23) Check if you are able to see the fact table created in your bigquery dataset. 
24) Connect this dataset to Looker Studio and build the dashboard.

## Improvements
A possible improvement would be to automatically import the GCP resources information to the container without the need to adjust the pipeline files manually using Terraform outputs. 

## Linkedin

Please reach out to me on [Linkedin](https://www.linkedin.com/in/bernardo-m-costa/
) if you found this project interesting and want to discuss!