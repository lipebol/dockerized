from common.initialize import add
from airflow.providers.postgres.hooks.postgres import PostgresHook
import adbc_driver_postgresql.dbapi
from os import getenv
import psycopg2


class db:

    def __init__(self, settings: object) -> None:
        """
        Conexão com o banco de dados [_**PostgreSQL**_](https://www.postgresql.org/).

        Conecta-se usando:
        
        - [__`adbc`__](https://github.com/apache/arrow-adbc)
        - [__`psycopg2`__](https://github.com/psycopg/psycopg2)
        
        Parâmetros
        ----------
        **`settings`** (_`object`_): _**`variáveis`**_ e _**`métodos`**_ que estão no arquivo de configuração do projeto.

        Atributos
        ---------
        **`__schema`** (_`object`_): nome do _**`schema`**_ no banco de dados onde estão as tabelas do projeto.
        """
        self.__engine = PostgresHook.get_hook('postgresql_default').get_uri()
        self.__schema = settings.mainSchema

    @add.exception
    def adbc(self, pyarrowTable: object, table: str, schema=None) -> str:
        """
        Conexão via [_**Arrow Database Connectivity**_](https://github.com/apache/arrow-adbc).

        Parâmetros
        ----------
        **`pyarrowTable`** (_`object`_): carregue uma [_**`pyarrow.Table`**_](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html).
        
        **`table`** (_`str`_): o nome da tabela no banco de dados.
        
        **`schema`** (_`str`_): por padrão será o _**`schema`**_ que está no arquivo de configuração, mas pode receber uma `string`.

        Retorno
        -------
        **`return`** (_`str`_): mensagem de conclusão do processo. 
        """
        self.__conn = adbc_driver_postgresql.dbapi.connect(self.__engine)
        with self.__conn.cursor() as cursor:
            cursor.adbc_ingest(
                db_schema_name=(schema if schema else self.__schema),
                table_name=table, data=pyarrowTable, mode='append'
            )
        self.__conn.commit()
        self.__conn.close()
        return getenv('SUCCESS')
        

    @add.exception
    def execute(self, command: str, idx=None) -> object:
        """
        Conexão via [_**Database API Specification v2.0**_](https://github.com/psycopg/psycopg2).

        Parâmetros
        ----------
        **`command`** (_`str`_): query _SQL_.
        
        **`idx`** (_`str`_): você pode definir um `list` no arquivo de configuração ou em `.env` e informar a posição.

        Retorno
        -------
        **`return`** (_`object`_): 
        """
        self.__conn = psycopg2.connect(self.__engine)
        self.__conn.set_session(autocommit=True)
        with self.__conn.cursor() as cursor:
            cursor.execute(command[(idx if idx else 0)])
            self.__content = cursor.fetchall()
        self.__conn.close()
        return self.__content