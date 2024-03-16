# Seattle 911 Crime Incident Analysis Project

## Description

This repository contains the architecture diagram and documentation for a real-time data processing pipeline aimed at analyzing crime incidents in Seattle. The pipeline utilizes various AWS services to ingest, process, and analyze data from both historical sources and real-time API feeds. The data used in this project is sourced from the Seattle government's data portal, available at [data.seattle.gov](https://data.seattle.gov/).

## Technologies Used

- AWS
- Python
- AWS SDK
- AWS S3
- AWS EC2
- Apache Kafka
- AWS Glue
- AWS Lambda
- AWS Athena
- Tableau

## Usage

This repository serves as a reference and starting point for understanding and implementing a real-time data processing pipeline for analyzing crime incidents in Seattle. The architecture diagram provided in the repository illustrates the flow of data through various AWS services, from ingestion to analysis.

## Data Architecture
![Alt Text](https://github.com/samvit98/Seattle-Crime-Analysis/blob/main/seattle_911_final.drawio.png)

## Data Flow

**1. Historical Data:** Data is exported from the Seattle data repository in CSV format, cleaned, and processed using Python. It is then ingested into an AWS S3 bucket.

**2. Real-time Data:** An Apache Kafka cluster hosted on an AWS EC2 instance pulls real-time data from the Seattle data repository API. A Python script acts as a Kafka Producer to push this data to the cluster.

**3. Lambda Functions:** Messages from the Kafka cluster trigger Lambda functions, which store the data as files in the same S3 bucket, organized within an "incremental_data" folder.

**4. Data Analysis:** The data stored in S3 is queried and analyzed using AWS Glue and Athena.

**5. Visualization:** The database is connected to Tableau for visualization and interactive analysis.

This pipeline enables continuous ingestion, processing, and analysis of both historical and real-time crime incident data from Seattle, facilitating informed decision-making and insights for various stakeholders.

## Tableau Visualization Link
https://public.tableau.com/app/profile/samvit.patankar/viz/SeattleCrimeDashboard_17105458776540/Dashboard1
