import configparser
import redshift_connector
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)


def create_tables(cur, conn):
    for query in create_table_queries:
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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()