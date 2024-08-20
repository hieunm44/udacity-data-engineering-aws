# Project Introduction
## Project: Data Pipelines with Airflow
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

 
# Project Overview
This project will introduce you to the core concepts of Apache Airflow. To complete the project, you will need to create your own custom operators to perform tasks such as staging the data, filling the data warehouse, and running checks on the data as the final step.

We have provided you with a project template that takes care of all the imports and provides four empty operators that need to be implemented into functional pieces of a data pipeline. The template also contains a set of tasks that need to be linked to achieve a coherent and sensible data flow within the pipeline.

You'll be provided with a helpers class that contains all the SQL transformations. Thus, you won't need to write the ETL yourselves, but you'll need to execute it with your custom operators.
![](https://video.udacity-data.com/topher/2024/September/66f695ac_final-dag/final-dag.jpeg)


# Prerequisites
__Create an IAM User in AWS__
* Follow the steps on the page Create an IAM User in AWS in the lesson Data Pipelines.

__Configure Redshift Serverless in AWS__
* Follow the steps on the page Configure Redshift Serverless in the lesson Airflow and AWS.

## Setting up Connections
__Connect Airflow and AWS__
* Follow the steps on the page Connections - AWS Credentials in the lesson Airflow and AWS.
* Use the workspace provided on the page Project Workspace in this lesson.

__Connect Airflow to AWS Redshift Serverless__
* Follow the steps on the page Add Airflow Connections to AWS Redshift in the lesson Airflow and AWS.


# Project Instructions
## Datasets
For this project, you'll be working with two datasets. Here are the s3 links for each:
* Log data: `s3://udacity-dend/log_data`
* Song data: `s3://udacity-dend/song-data`

__Tip__: You will want to copy the data to your own bucket.

## Copy S3 Data
The data for the project is stored in Udacity's S3 bucket. This bucket is in the US West AWS Region. To simplify things, we will copy the data to your bucket in the same AWS Region where you created the Redshift workgroup so that Redshift can access the bucket.

If you haven't already, create your own S3 bucket using the AWS Cloudshell (this is just an example - buckets need to be unique across all AWS accounts): `aws s3 mb s3://sean-murdock/`

Copy the data from the udacity bucket to the home cloudshell directory:
```
aws s3 cp s3://udacity-dend/log-data/ ~/log-data/ --recursive
aws s3 cp s3://udacity-dend/song-data/ ~/song-data/ --recursive
aws s3 cp s3://udacity-dend/log_json_path.json ~/
```
Copy the data from the home cloudshell directory to your own bucket -- this is only an example:
```
aws s3 cp ~/log-data/ s3://sean-murdock/log-data/ --recursive
aws s3 cp ~/song-data/ s3://sean-murdock/song-data/ --recursive
aws s3 cp ~/log_json_path.json s3://sean-murdock/
```
List the data in your own bucket to be sure it copied over -- this is only an example:
```
aws s3 ls s3://sean-murdock/log-data/
aws s3 ls s3://sean-murdock/song-data/
aws s3 ls s3://sean-murdock/log_json_path.json
```

## Project Template
To get started with the project:
1. You will find the project starter code in the Udacity workspace on the Project Workspace page. You can work on your project and submit your work through this workspace. After all the changes are made, you can create a zip of the final solution and submit it on the Project Submission page.
2. We recommend using the project workspace provided however if you decide to work on this project on your local machine, you can download the project template from this [GitHub repository](https://github.com/udacity/cd12380-data-pipelines-with-airflow) and follow the instructions outlined in the GitHub README. You will have an option to submit the final solution through your forked Github repository or create a zip of the final solution and submit it on the Project Submission page.
3. The project template package contains three major components for the project:
* The dag template has all the imports and task templates in place, but the task dependencies have not been set
* The operators folder with operator templates
* A helper class for the SQL transformations
4. With these template files, you should be able see the new DAG in the Airflow UI. The graph view should look like this:
![](https://video.udacity-data.com/topher/2024/September/66f68bb0_project-dag/project-dag.jpeg)

## DAG Graph in the Project Template
There are 9 tasks in the project template's DAG graph that exist independently: `Begin_execution`, `Load_artist_dim_table`, `Load_song_dim_table`, `Load_songplays_fact_table`, `Load_time_dim_table`, `Load_user_dim_table`, `Run_data_quality_checks`, `Stage_events`, and `Stage_songs`. Your task is to configure the dependencies between them.

You should be able to execute the DAG successfully, but if you check the logs, you will see only `operator not implemented` messages.

## Configuring the DAG
In the DAG, add `default parameters` according to these guidelines
* The DAG does not have dependencies on past runs
* On failure, the task are retried 3 times
* Retries happen every 5 minutes
* Catchup is turned off
* Do not email on retry

In addition, configure the task dependencies so that after the dependencies are set, the graph view follows the flow shown in the image below.
![](https://video.udacity-data.com/topher/2024/September/66f695a0_final-dag/final-dag.jpeg)

## Completed DAG Dependencies Image Description
The Begin_execution task should be followed by both Stage_events and Stage_songs. These staging tasks should both be followed by the task Load_songplays_fact_table. Completing the Load_songplays_fact_table should trigger four tasks at the same time: Load_artist_dim_table, Load_song_dim_table, Load_time_dim_table, and Load_user_dim_table. After completing all of these four tasks, the task Run_dadta_quality_checks_should_run. And, finally, run the Stop_execution task.

## Building the operators
To complete the project, you need to build four different operators to stage the data, transform the data, and run checks on data quality.

You can reuse the code from Project 2, but remember to utilize Airflow's built-in functionalities as connections and hooks as much as possible and let Airflow do all the heavy lifting when it is possible.

All of the operators and task instances will run SQL statements against the Redshift database. However, using parameters wisely will allow you to build flexible, reusable, and configurable operators you can later apply to many kinds of data pipelines with Redshift and with other databases.

## Stage Operator
The stage operator is expected to be able to load any JSON-formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.

The parameters should be used to distinguish between JSON files. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

## Fact and Dimension Operators
With dimension and fact operators, you can utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations, and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will contain the results of the transformation.

Dimension loads are often done with the truncate-insert pattern, where the target table is emptied before the load. Thus, you could also have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.

## Data Quality Operator
The final operator to create is the data quality operator, which runs checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each test, the test result and expected result need to be checked, and if there is no match, the operator should raise an exception, and the task should retry and fail eventually.

For example, one test could be a SQL statement that checks if a certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs, so the expected result would be 0, and the test would compare the SQL statement's outcome to the expected result.