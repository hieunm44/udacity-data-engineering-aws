import configparser
import redshift_connector
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = redshift_connector.connect(
        host=config['CLUSTER']['HOST'],
        database=config['CLUSTER']['DB_NAME'],
        port=config['CLUSTER']['DB_PORT'],
        user=config['CLUSTER']['DB_USER'],
        password=config['CLUSTER']['DB_PASSWORD']
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()