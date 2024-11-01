# Data Warehouse and ETL Pipeline for Music Streaming Analytics on AWS with Redshift

## Introduction

This project involves building an ETL pipeline that extracts data from Amazon S3, stages them in Amazon Redshift, and transforms data into a set of dimensional tables for Sparkify, a music streaming startup. The goal is to enable the analytics team to find insights into what songs their users are listening to.

## Project Description

You'll build an ETL pipeline for a database hosted on Amazon Redshift. Data from S3 is loaded into staging tables on Redshift and then transformed into a star schema optimized for queries on song play analysis.

### Datasets

- **Song Data**: `s3://udacity-dend/song_data`
- **Log Data**: `s3://udacity-dend/log_data`
- **Log Data JSON Path**: `s3://udacity-dend/log_json_path.json`

## Database Schema Design

A star schema optimized for song play queries includes the following tables:

### Fact Table

- **fact_songplays**: Records in event data associated with song plays.

  - `songplay_id` (INT) PRIMARY KEY
  - `start_time` (TIMESTAMP) NOT NULL
  - `user_id` (INT) NOT NULL
  - `level` (VARCHAR)
  - `song_id` (VARCHAR)
  - `artist_id` (VARCHAR)
  - `session_id` (INT)
  - `location` (VARCHAR)
  - `user_agent` (VARCHAR)

### Dimension Tables

- **dim_users**: Users in the app.

  - `user_id` (INT) PRIMARY KEY
  - `first_name` (VARCHAR)
  - `last_name` (VARCHAR)
  - `gender` (CHAR)
  - `level` (VARCHAR)

- **dim_songs**: Songs in the music database.

  - `song_id` (VARCHAR) PRIMARY KEY
  - `title` (VARCHAR)
  - `artist_id` (VARCHAR)
  - `year` (INT)
  - `duration` (FLOAT)

- **dim_artists**: Artists in the music database.

  - `artist_id` (VARCHAR) PRIMARY KEY
  - `name` (VARCHAR)
  - `location` (VARCHAR)
  - `latitude` (FLOAT)
  - `longitude` (FLOAT)

- **dim_time**: Timestamps of records in `fact_songplays` broken down into specific units.

  - `start_time` (TIMESTAMP) PRIMARY KEY
  - `hour` (INT)
  - `day` (INT)
  - `week` (INT)
  - `month` (INT)
  - `year` (INT)
  - `weekday` (VARCHAR)

## Project Structure

    .
    ├── README.md
    ├── create_tables.py
    ├── dwh.cfg
    ├── etl.py
    ├── sql_queries.py
    └── terraform
        ├── dwh_cfg.tmpl
        ├── iam.tf
        ├── main.tf
        ├── networking.tf
        ├── outputs.tf
        ├── provider.tf
        ├── redshift.tf
        ├── security_groups.tf
        ├── terraform.tfvars
        └── variables.tf

- **create_tables.py**: Drops and creates tables. Run this file to reset the tables before each ETL run.
- **etl.py**: Loads data from S3 into staging tables on Redshift and then processes that data into the analytics tables.
- **sql_queries.py**: Contains all the SQL queries, and is imported into the two files above.
- **dwh.cfg**: Contains the Redshift cluster and IAM role configurations. This file is generated automatically by Terraform.
- **terraform/**: Directory containing Terraform configuration files to set up AWS infrastructure.

## Prerequisites

- **Python 3.x**
- **AWS Account**: You need access to AWS to create resources.
- **Terraform**: Infrastructure as Code tool to provision AWS resources.
- **AWS CLI**: For configuring AWS credentials on your local machine.

## Setup Instructions

### 1. Clone the Repository

Clone the project repository to your local machine.

    git clone https://github.com/your-username/sparkify-data-warehouse.git
    cd sparkify-data-warehouse


### 2. Create an Environment

To set up the project, create a Python virtual environment and install the required dependencies.

#### Steps:

Create a Python virtual environment and install the required dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate        # On Linux or macOS
.venv\Scripts\activate           # On Windows
pip install -r requirements.txt
```

### 3. Install Terraform

Download and install Terraform from the official website: https://www.terraform.io/downloads.html. Verify the installation:

    terraform -v

### 4. Configure Terraform Variables

Navigate to the `terraform` directory.

    cd terraform

#### 4.1. Create `terraform.tfvars`

Create a file named `terraform.tfvars` to provide sensitive variables. **Do not commit this file to version control.**

    # terraform.tfvars

    aws_access_key  = "YOUR_AWS_ACCESS_KEY_ID"
    aws_secret_key  = "YOUR_AWS_SECRET_ACCESS_KEY"
    db_password     = "DB_PASSWORD"

- Replace `"YOUR_AWS_ACCESS_KEY_ID"` and `"YOUR_AWS_SECRET_ACCESS_KEY"` with your AWS credentials.
- Replace `"DB_PASSWORD"` with a strong database password.

### 5. Initialize and Apply Terraform Configuration

#### a. Initialize Terraform

From the `terraform` directory, run:

    terraform init

#### b. Apply Terraform Configuration

    terraform apply

- Type `yes` when prompted to confirm the creation of resources.
- Terraform will provision the following AWS resources:
  - VPC and subnet
  - IAM role with S3 read access
  - Redshift cluster
  - Security group allowing access on port 5439
- Terraform will generate the `dwh.cfg` file in the project root directory.

### 6. Verify the Generated `dwh.cfg`

Ensure that the `dwh.cfg` file has been created in the project root directory with the correct configurations.

### 7. Run the ETL Pipeline

#### a. Create Tables

Navigate back to the project root directory and run:

    python create_tables.py

#### b. Execute the ETL Process

    python etl.py

### 8. Verify the Data Loaded

Connect to your Redshift cluster to verify that the data has been loaded correctly.

#### a. Using AWS Redshift Query Editor

1. Log in to the AWS Management Console.
2. Navigate to Amazon Redshift service.
3. Open the Query Editor.
4. Connect to your cluster using the credentials from `dwh.cfg`.
5. Run SQL queries to verify data.

#### b. Example Queries

    -- Count the number of records in the fact_songplays table
    SELECT COUNT(*) FROM fact_songplays;

    -- View some records from the dim_users table
    SELECT * FROM dim_users LIMIT 5;

    -- Count the number of records in the dim_songs table
    SELECT COUNT(*) FROM dim_songs;

    -- View some records from the dim_artists table
    SELECT * FROM dim_artists LIMIT 5;

    -- View some records from the dim_time table
    SELECT * FROM dim_time LIMIT 5;

### 9. Destroy the Infrastructure

After completing the project, destroy the AWS resources to avoid incurring costs.

    terraform destroy

- Confirm the destruction by typing `yes` when prompted.

## ETL Pipeline

The ETL pipeline processes the data in three steps:

1. **Extract**: Loads JSON log and song files from S3 into staging tables on Redshift.
2. **Transform**: Processes the data in the staging tables and prepares it for insertion into the fact and dimension tables.
3. **Load**: Inserts data into the fact and dimension tables defined by the star schema.

## Handling Sensitive Data

- **Sensitive variables** like AWS credentials and database passwords are stored in `terraform.tfvars`, which is excluded from version control.
- **Generated files** like `dwh.cfg` that contain sensitive information are also excluded from version control.

## Conclusion

This project demonstrates how to build a data warehouse on AWS Redshift and develop an ETL pipeline for a music streaming company. The data warehouse allows the analytics team to query and analyze data efficiently, providing insights into user behaviors and song preferences.

## References

- [Amazon Redshift Documentation](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)
- [Terraform Documentation](https://www.terraform.io/docs/index.html)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

---

