import pendulum

from airflow.decorators import dag,task

from custom_operators.facts_calculator import FactsCalculatorOperator
from custom_operators.has_rows import HasRowsOperator
from custom_operators.s3_to_redshift import S3ToRedshiftOperator
from airflow.operators.empty import EmptyOperator

@dag(start_date=pendulum.now())
def full_pipeline():
# TODO: Load trips data from S3 to RedShift. Use the s3_key
#       "data-pipelines/divvy/unpartitioned/divvy_trips_2018.csv"
#       and YOUR s3_bucket
    copy_trips_task = S3ToRedshiftOperator(
        task_id="load_trips_from_s3_to_redshift",
        table="trips",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="sean-murdock",
        s3_key="data-pipelines/divvy/unpartitioned/divvy_trips_2018.csv"
    )

# TODO: Perform a data quality check on the Trips table
    check_trips = HasRowsOperator(
        task_id="check_trips_data",
        redshift_conn_id="redshift",
        table="trips"
    )

# TODO: Use the FactsCalculatorOperator to create a Facts table in RedShift. The fact column should
#       be `tripduration` and the groupby_column should be `bikeid`
    calculate_facts = FactsCalculatorOperator(
        task_id="calculate_facts_trips",
        redshift_conn_id="redshift",
        origin_table="trips",
        destination_table="trips_facts",
        fact_column="tripduration",
        groupby_column="bikeid"
    )

# TODO: Define task ordering for the DAG tasks you defined
    copy_trips_task >> check_trips
    check_trips >> calculate_facts

full_pipeline_dag = full_pipeline()