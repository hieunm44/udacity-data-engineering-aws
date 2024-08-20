import pendulum
import logging

from airflow.decorators import dag, task
from airflow.secrets.metastore import MetastoreBackend
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

import sql_statements

@dag(
    start_date=pendulum.now()
)
def load_data_to_redshift():


    @task
    def load_task():    
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        redshift_hook = PostgresHook("redshift")
        redshift_hook.run(sql_statements.COPY_ALL_TRIPS_SQL.format(aws_connection.login, aws_connection.password))


    create_table_trips=PostgresOperator(
       task_id="create_table",
        postgres_conn_id="redshift",
        sql=sql_statements.CREATE_TRIPS_TABLE_SQL
    )

    drop_table_station_traffic = PostgresOperator(
        task_id="drop_table_station_traffic",
        postgres_conn_id="redshift",
        sql=sql_statements.DROP_TABLE_STATION_TRAFFIC
    )

    location_traffic_task = PostgresOperator(
        task_id="calculate_location_traffic",
        postgres_conn_id="redshift",
        sql=sql_statements.LOCATION_TRAFFIC_SQL
    )

    load_data = load_task()
    create_table_trips >> load_data
    load_data >> drop_table_station_traffic
    drop_table_station_traffic >> location_traffic_task

s3_to_redshift_dag = load_data_to_redshift()