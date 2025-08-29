from common.initialize import load
from airflow.providers.postgres.hooks.postgres import PostgresHook
import adbc_driver_postgresql.dbapi

class db:

    @property
    def __postgres(self):
        return PostgresHook(load.variable('POSTGRES_CONN'))
    
    @staticmethod
    def conn():
        return db().__postgres.get_conn()
    
    @staticmethod
    def columns(schema: str, table: str):
        with db().conn().cursor() as __cursor:
            __cursor.execute(
                load.variable('SELECT_COMMAND') % (schema, table)
            )
            return [column[0] for column in __cursor.description]

    @staticmethod
    def select(schema: str, table: str, params=None):
        sql_command = load.variable('SELECT_COMMAND') % (schema, table)
        if params:
            pass
        return db().__postgres.get_records(sql_command)

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