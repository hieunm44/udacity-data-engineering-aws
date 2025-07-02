#Instructions
# 1 - Revisit our bikeshare traffic
# 2 - Update our DAG with
#   2.1 - @monthly schedule_interval
#   2.2 - max_active_runs of 1
#   2.3 - start_date of 2018/01/01
#   2.4 - end_date of 2018/02/01
# Use Airflow’s backfill capabilities to analyze our trip data on a monthly basis over 2 historical runs


import pendulum

from airflow.decorators import dag, task
from airflow.secrets.metastore import MetastoreBackend
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator

import sql_statements

@dag(
    # TODO: Set the end date to February first, schedule to be monthly, number of max active runs to 1
    start_date=pendulum.datetime(2018, 1, 1, 0, 0, 0, 0),
    end_date=pendulum.datetime(2018, 2, 1, 0, 0, 0, 0),
    schedule_interval='@monthly',
    max_active_runs=1    
)
def schedule_backfills():


    @task()
    def load_trip_data_to_redshift():
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        redshift_hook = PostgresHook("redshift")
        sql_stmt = sql_statements.COPY_ALL_TRIPS_SQL.format(
            aws_connection.login,
            aws_connection.password,
        )
        redshift_hook.run(sql_stmt)

    load_trip_data_to_redshift_task= load_trip_data_to_redshift()

    @task()
    def load_station_data_to_redshift():
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        redshift_hook = PostgresHook("redshift")
        sql_stmt = sql_statements.COPY_STATIONS_SQL.format(
            aws_connection.login,
            aws_connection.password,
        )
        redshift_hook.run(sql_stmt)

    load_station_data_to_redshift_task = load_station_data_to_redshift()

    create_trips_table = PostgresOperator(
        task_id="create_trips_table",
        postgres_conn_id="redshift",
        sql=sql_statements.CREATE_TRIPS_TABLE_SQL
    )


    create_stations_table = PostgresOperator(
        task_id="create_stations_table",
        postgres_conn_id="redshift",
        sql=sql_statements.CREATE_STATIONS_TABLE_SQL,
    )

    create_trips_table >> load_trip_data_to_redshift_task
    create_stations_table >> load_station_data_to_redshift_task

schedule_backfills_dag = schedule_backfills()


# Chú ý phần start_date ở quá khứ, DAG sẽ tự động chạy để bù vào các intervals trong quá khứ. Đây đgl catch up (back fill) tới TG hiện tại. 