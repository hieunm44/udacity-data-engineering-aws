import pendulum
from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator
from sql_statements import SqlQueries

start_date = datetime(2018, 11, 1)
end_date = datetime(2018, 11, 30)

s3_bucket = "nd027-hieu"
events_s3_key = "log-data"
songs_s3_key = "song-data/A/A/"
log_json_file = 'log_json_path.json'

default_args = {
    'owner': 'Hieu',
    'start_date': pendulum.now(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def final_project():

    start_operator = EmptyOperator(task_id='Begin_execution')

    drop_staging_events = PostgresOperator(
        task_id='Drop_staging_events',
        postgres_conn_id="redshift",
        sql=SqlQueries.drop_staging_events
    )

    drop_staging_songs = PostgresOperator(
        task_id='Drop_staging_songs',
        postgres_conn_id="redshift",
        sql=SqlQueries.drop_staging_songs
    )

    drop_songplays = PostgresOperator(
        task_id='Drop_songplays',
        postgres_conn_id="redshift",
        sql=SqlQueries.drop_songplays
    )

    drop_users = PostgresOperator(
        task_id='Drop_users',
        postgres_conn_id="redshift",
        sql=SqlQueries.drop_users
    )

    drop_songs = PostgresOperator(
        task_id='Drop_songs',
        postgres_conn_id="redshift",
        sql=SqlQueries.drop_songs
    )

    drop_artist = PostgresOperator(
        task_id='Drop_artist',
        postgres_conn_id="redshift",
        sql=SqlQueries.drop_artist
    )

    drop_time = PostgresOperator(
        task_id='Drop_time',
        postgres_conn_id="redshift",
        sql=SqlQueries.drop_time
    )

    create_stating_events = PostgresOperator(
        task_id='Create_staging_events',
        postgres_conn_id="redshift",
        sql=SqlQueries.create_staging_events
    )

    create_staging_songs = PostgresOperator(
        task_id='Create_staging_songs',
        postgres_conn_id="redshift",
        sql=SqlQueries.create_staging_songs
    )

    create_songplays = PostgresOperator(
        task_id='Create_songplays',
        postgres_conn_id="redshift",
        sql=SqlQueries.create_songplays
    )

    create_users = PostgresOperator(
        task_id='Create_users',
        postgres_conn_id="redshift",
        sql=SqlQueries.create_users
    )

    create_songs = PostgresOperator(
        task_id='Create_songs',
        postgres_conn_id="redshift",
        sql=SqlQueries.create_songs
    )

    create_artists = PostgresOperator(
        task_id='Create_artists',
        postgres_conn_id="redshift",
        sql=SqlQueries.create_artists
    )

    create_time = PostgresOperator(
        task_id='Create_time',
        postgres_conn_id="redshift",
        sql=SqlQueries.create_time
    )
    
    songplay_table_insert = PostgresOperator(
        task_id='Songplay_table_insert',
        postgres_conn_id="redshift",
        sql=SqlQueries.songplay_table_insert
    )

    user_table_insert = PostgresOperator(
        task_id='User_table_insert',
        postgres_conn_id="redshift",
        sql=SqlQueries.user_table_insert
    )

    song_table_insert = PostgresOperator(
        task_id='Song_table_insert',
        postgres_conn_id="redshift",
        sql=SqlQueries.song_table_insert
    )

    artist_table_insert = PostgresOperator(
        task_id='Artist_table_insert',
        postgres_conn_id="redshift",
        sql=SqlQueries.artist_table_insert
    )

    time_table_insert = PostgresOperator(
        task_id='Time_table_insert',
        postgres_conn_id="redshift",
        sql=SqlQueries.time_table_insert
    )

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        table="staging_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=s3_bucket,
        s3_key=events_s3_key,
        log_json_file=log_json_file
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table="staging_songs",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=s3_bucket,
        s3_key=songs_s3_key
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id="redshift",
        sql_query=SqlQueries.songplay_table_insert
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id="redshift",
        sql_query=SqlQueries.user_table_insert
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id="redshift",
        sql_query=SqlQueries.song_table_insert
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id="redshift",
        sql_query=SqlQueries.artist_table_insert
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id="redshift",
        sql_query=SqlQueries.time_table_insert
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id = "redshift",
        tables = ["songplays", "users", "songs", "artists", "time"]
    )

    end_operator = EmptyOperator(task_id='End_execution')

    start_operator >> [drop_staging_events, drop_staging_songs, drop_songplays, drop_users, drop_songs, drop_artist, drop_time] \
    >> create_stating_events >> [create_staging_songs, create_songplays, create_users, create_songs, create_artists, create_time] \
    >> songplay_table_insert >> [user_table_insert, song_table_insert, artist_table_insert, time_table_insert] \
    >> stage_events_to_redshift >> stage_songs_to_redshift >> load_songplays_table \
    >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] \
    >> run_quality_checks >> end_operator

final_project_dag = final_project()