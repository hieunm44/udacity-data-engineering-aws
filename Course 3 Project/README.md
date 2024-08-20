# Project: Data Warehouse

## Introduction

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, I am tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to.

## Project Datasets

- Song data: s3://udacity-dend/song_data
- Log data: s3://udacity-dend/log_data
- This third file s3://udacity-dend/log_json_path.jsoncontains the meta information that is required by AWS to correctly load s3://udacity-dend/log_data

#### Fact Table

1. songplays - records in event data associated with song plays i.e. records with page NextSong
- songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

#### Dimension Tables

2. users - users in the app
- user_id, first_name, last_name, gender, level

3. songs - songs in music database
- song_id, title, artist_id, year, duration

4. artists - artists in music database
- artist_id, name, location, lattitude, longitude

5. time - timestamps of records in songplays broken down into specific units
- start_time, hour, day, week, month, year, weekday

## Project Steps

#### Create Table Schemas

1. Design schemas for your fact and dimension tables
2. Write a SQL `CREATE` statement for each of these tables in `sql_queries.py`
3. Complete the logic in `create_tables.py` to connect to the database and create these tables
4. Write SQL `DROP` statements to drop tables in the beginning of `create_tables.py` if the tables already exist. This way, you can run `create_tables.py` whenever you want to reset your database and test your ETL pipeline.
5. Launch a redshift cluster and create an IAM role that has read access to S3.
6. Add redshift database and IAM role info to `dwh.cfg`.
7. Test by running `create_tables.py` and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.

#### Build ETL Pipeline

1. Implement the logic in `etl.py` to load data from S3 to staging tables on Redshift.
2. Implement the logic in `etl.py` to load data from staging tables to analytics tables on Redshift.
3. Test by running `etl.py` after running `create_tables.py` and running the analytic queries on your Redshift database to compare your results with the expected results.
4. Delete your redshift cluster when finished.

## Run Scripts

Set environment variables KEY and SECRET.

Choose DB/DB_PASSWORD in dhw.cfg.

Create IAM role, Redshift cluster, and configure TCP connectivity

Drop and recreate tables

```python
python create_tables.py
```

Run ETL pipeline

```python
python etl.py
```