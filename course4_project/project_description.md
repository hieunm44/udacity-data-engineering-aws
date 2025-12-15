# Project Overview
## Spark and Human Balance
As you have learned in this course Spark and AWS Glue allow you to process data from multiple sources, categorize the data, and curate it to be queried in the future for multiple purposes. In this project you will directly use the skills you have used, including some of the code you have already written.

You will go beyond that to write additional AWS Glue jobs to create curated step trainer data that can be used for machine learning.

## Project Introduction: STEDI Human Balance Analytics
In this project, you'll act as a data engineer for the STEDI team to build a data lakehouse solution for sensor data that trains a machine learning model.

## Project Details
The STEDI Team has been hard at work developing a hardware __STEDI Step Trainer__ that:

trains the user to do a STEDI balance exercise;
and has sensors on the device that collect data to train a machine-learning algorithm to detect steps;
has a companion mobile app that collects customer data and interacts with the device sensors.
STEDI has heard from millions of early adopters who are willing to purchase the STEDI Step Trainers and use them.

Several customers have already received their Step Trainers, installed the mobile application, and begun using them together to test their balance. The Step Trainer is just a motion sensor that records the distance of the object detected. The app uses a mobile phone accelerometer to detect motion in the X, Y, and Z directions.

The STEDI team wants to use the motion sensor data to train a machine learning model to detect steps accurately in real-time. Privacy will be a primary consideration in deciding what data can be used.

Some of the early adopters have agreed to share their data for research purposes. __Only these customers’ Step Trainer and accelerometer data should be used in the training data for the machine learning model__.

## Project Summary
As a data engineer on the STEDI Step Trainer team, you'll need to extract the data produced by the STEDI Step Trainer sensors and the mobile app, and curate them into a data lakehouse solution on AWS so that Data Scientists can train the learning model.


# Project Environment
## AWS Environment
You'll use the data from the STEDI Step Trainer and mobile app to develop a lakehouse solution in the cloud that curates the data for the machine learning model using:
* Python and Spark
* AWS Glue
* AWS Athena
* AWS S3
On the next page, you'll find instructions for accessing a temporary AWS account you can use to complete the project. This account has a budget of $25 you should be aware of when creating resources on the AWS platform. Pay special attention to what you are creating and running and the cost of these services.

## Github Environment
You'll also need a github repository to store your SQL scripts and Python code in. You'll submit the code in this github repo for the project submission.

## Workflow Environment Configuration
You'll be creating Python scripts using AWS Glue and Glue Studio. These web-based tools and services contain multiple options for editors to write or generate Python code that uses PySpark. Remember to save any code you develop or run in these editors on AWS to a local Github Repository.

You can use any Python editor locally to work with and save code as well, but be aware that to actually test or run Glue Jobs, you'll need to submit them to your AWS Glue environment.


# Project Data
STEDI has three [JSON data sources](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter) to use from the Step Trainer. Check out the JSON data in the following folders in the Github repo:
* customer
* step_trainer
* accelerometer
Here are the steps to download the data:
1. Go to [nd027-Data-Engineering-Data-Lakes-AWS-Exercises]((https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main)) repository and click on Download Zip.
2. Extract the zip file.
3. Navigate to the project/starter folder in the extracted output to find the JSON data files within three sub-folders. You should have
* 956 rows in the customer_landing table,
* 81273 rows in the accelerometer_landing table, and
* 28680 rows in the step_trainer_landing table.

## 1. Customer Records
This is the data from fulfillment and the STEDI website.
[Data Download URL](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter/customer/landing) \
`AWS S3 Bucket URI - s3://cd0030bucket/customers/` contains the following fields:
* serialnumber
* sharewithpublicasofdate
* birthday
* registrationdate
* sharewithresearchasofdate
* customername
* email
* lastupdatedate
* phone
* sharewithfriendsasofdate

## 2. Step Trainer Records
This is the data from the motion sensor. [Data Download URL](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter/step_trainer/landing) \
`AWS S3 Bucket URI - s3://cd0030bucket/step_trainer/` contains the following fields:
* sensorReadingTime
* serialNumber
* distanceFromObject

## 3. Accelerometer Records
This is the data from the mobile app. [Data Download URL](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter/accelerometer/landing) \
`AWS S3 Bucket URI - s3://cd0030bucket/accelerometer/` contains the following fields:
* timeStamp
* user
* x
* y
*z


# Project Instructions
Using AWS Glue, AWS S3, Python, and Spark, create or generate Python scripts to build a lakehouse solution in AWS that satisfies these requirements from the STEDI data scientists.

Refer to the flowchart below to better understand the workflow.
![](https://video.udacity-data.com/topher/2023/October/6527a6fc_flowchart/flowchart.jpeg)

## Requirements
To simulate the data coming from the various sources, you will need to create your own S3 directories for customer_landing, step_trainer_landing, and accelerometer_landing zones, and copy the data there as a starting point.
* You have decided you want to get a feel for the data you are dealing with in a semi-structured format, so you decide to create three Glue tables for the three landing zones. Share your customer_landing.sql, accelerometer_landing.sql, and step_trainer_landing.sql scripts in git.
* Query those tables using Athena, and take a screenshot of each one showing the resulting data. Name the screenshots customer_landing(.png,.jpeg, etc.), accelerometer_landing(.png,.jpeg, etc.), step_trainer_landing (.png, .jpeg, etc.).

The Data Science team has done some preliminary data analysis and determined that the Accelerometer Records each match one of the Customer Records. They would like you to create 2 AWS Glue Jobs that do the following:
1. Sanitize the Customer data from the Website (Landing Zone) and only store the Customer Records who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called customer_trusted.
2. Sanitize the Accelerometer data from the Mobile App (Landing Zone) - and only store Accelerometer Readings from customers who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called accelerometer_trusted.
3. You need to verify your Glue job is successful and only contains Customer Records from people who agreed to share their data. Query your Glue customer_trusted table with Athena and take a screenshot of the data. Name the screenshot customer_trusted(.png,.jpeg, etc.).

Data Scientists have discovered a data quality issue with the Customer Data. The serial number should be a unique identifier for the STEDI Step Trainer they purchased. However, there was a defect in the fulfillment website, and it used the same 30 serial numbers over and over again for millions of customers! Most customers have not received their Step Trainers yet, but those who have, are submitting Step Trainer data over the IoT network (Landing Zone). The data from the Step Trainer Records has the correct serial numbers.

The problem is that because of this serial number bug in the fulfillment data (Landing Zone), we don’t know which customer the Step Trainer Records data belongs to.

The Data Science team would like you to write a Glue job that does the following:
1. Sanitize the Customer data (Trusted Zone) and create a Glue Table (Curated Zone) that only includes customers who have accelerometer data and have agreed to share their data for research called customers_curated.

Finally, you need to create two Glue Studio jobs that do the following tasks:
1. Read the Step Trainer IoT data stream (S3) and populate a Trusted Zone Glue Table called step_trainer_trusted that contains the Step Trainer Records data for customers who have accelerometer data and have agreed to share their data for research (customers_curated).
2. Create an aggregated table that has each of the Step Trainer Readings, and the associated accelerometer reading data for the same timestamp, but only for customers who have agreed to share their data, and make a glue table called machine_learning_curated.

Refer to the relationship diagram below to understand the desired state.
![](https://video.udacity-data.com/topher/2023/October/6527a70f_dataset/dataset.jpeg)

## Check your work!
After each stage of your project, check if the row count in the produced table is correct. You should have the following number of rows in each table:
__Landing__
* Customer: 956
* Accelerometer: 81273
* Step Trainer: 28680

__Trusted__
* Customer: 482
* Accelerometer: 40981
* Step Trainer: 14460

__Curated__
* Customer: 482
* Machine Learning: 43681

_Hint__: Use Transform - SQL Query nodes whenever you can. Other node types may give you unexpected results. For example, rather than a Join node, you may use a SQL node that has two parents, then join them through a SQL query.