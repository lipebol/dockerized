from common.initialize import add, load
from airflow.providers.postgres.hooks.postgres import PostgresHook
import adbc_driver_postgresql.dbapi

class db:

    @property
    def __postgres(self):
        return PostgresHook(load.variable('POSTGRES_CONN'))
    
    @add.exception
    @staticmethod
    def conn():
        return db().__postgres.get_conn()
    
    @add.exception
    @staticmethod
    def select(schema: str, table: str, params=None):
        sql_command = load.variable('SELECT_COMMAND') % (schema, table)
        if params:
            pass
        return db().__postgres.get_records(sql_command)

    @add.exception
    @staticmethod
    def adbc(pyarrowTable: object, schema: str, table: str) -> str:
        __conn = adbc_driver_postgresql.dbapi.connect(db().__postgres.get_uri())
        with __conn.cursor() as cursor:
            cursor.adbc_ingest(
                db_schema_name=schema, table_name=table, 
                data=pyarrowTable, mode='append'
            )
        __conn.commit()
        __conn.close()
        return load.variable('MESSAGE_SUCCESS')