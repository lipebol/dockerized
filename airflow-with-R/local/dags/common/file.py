from common.initialize import add
from os import getenv
from pyarrow import csv
import pyarrow.parquet as pq


class file:

    def __init__(self, settings: object) -> None:
        """
        Localiza, carrega e converte arquivos [_**`csv`**_](https://pt.wikipedia.org/wiki/Comma-separated_values) 
        e [_**`parquet`**_](https://parquet.apache.org/) no diretório _**`/datasets`**_ usando [_**PyArrow**_](https://arrow.apache.org/docs/python/).

        Parâmetros
        ----------
        **`dag`** (_`object`_): _**`variáveis`**_ e _**`métodos`**_ que estão no arquivo de configuração do projeto.

        Atributos
        ---------
        **`__dag`** (_`object`_): conteúdo do parâmetro _**`dag`**_.
        """
        self.__settings = settings

    @add.exception
    def csv_To_parquet(self, fields: list, types: dict, filename=None) -> str:
        """
        Converte um arquivo [_**`csv`**_](https://pt.wikipedia.org/wiki/Comma-separated_values) em [_**`parquet`**_](https://parquet.apache.org/).

        Parâmetros
        ----------
        **`fields`** (_`list`_): todas as colunas que serão utilizadas.
        
        **`types`** (_`dict`_): um mapeamento [_**`coluna:tipo`**_](https://arrow.apache.org/docs/python/csv.html#customized-conversion).
        
        **`filename`** (_`str`_): se em _**`/datasets`**_ tiver dois ou mais arquivos, é necessário o nome do arquivo para localizá-lo.

        Retorno
        -------
        **`return`** (_`str`_): mensagem de conclusão do processo. 
        """
        pq.write_table(
            self.load_csv(fields, types, filename), 
            self.set_parquet(self.find(filename) if not filename else filename)
        )
        return getenv('SUCCESS')

    @add.exception
    def find(self, filename=None) -> str:
        """
        Localiza um arquivo em _**`/datasets`**_.

        Parâmetros
        ----------
        **`filename`** (_`str`_): se em _**`/datasets`**_ tiver dois ou mais arquivos, é necessário o nome do arquivo para localizá-lo.

        Retorno
        -------
        **`return`** (_`str`_): o _**`path`**_ do arquivo localizado. 
        """
        self.__file = "".join(self.__settings.csv_files()) if type(
                self.__settings.csv_files()) == list and len(
                    self.__settings.csv_files()) == 1 else None 
        if not self.__file:
            if filename:
                return self.find_by_name(filename)
            raise Exception(f"""'{getenv('NOT_FOUND')}' in: @find""")
        return self.__file
    
    @add.exception
    def find_by_name(self, filename: str) -> str:
        """
        Usado em _**`file.find`**_ para localizar um arquivo pelo nome.

        Parâmetros
        ----------
        **`filename`** (_`str`_): nome do arquivo a ser localizado.

        Retorno
        -------
        **`return`** (_`str`_): o _**`path`**_ do arquivo localizado. 
        """
        return "".join([item for item in self.__settings.csv_files() if filename in item])

    @add.exception
    def load_csv(self, fields: list, types: dict, filename=None) -> object:
        """
        Carregamento de arquivo [_**`csv`**_](https://pt.wikipedia.org/wiki/Comma-separated_values) 
        em [_**`pyarrow.Table`**_](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html).

        Parâmetros
        ----------
        **`fields`** (_`list`_): todas as colunas que serão utilizadas.
        
        **`types`** (_`dict`_): um mapeamento [_**`coluna:tipo`**_](https://arrow.apache.org/docs/python/csv.html#customized-conversion).
        
        **`filename`** (_`str`_): se em _**`/datasets`**_ tiver dois ou mais arquivos, é necessário o nome do arquivo para localizá-lo.

        Retorno
        -------
        **`return`** (_`object`_): uma [_**`pyarrow.Table`**_](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html). 
        """
        return csv.read_csv(
            self.find(filename),
            parse_options=csv.ParseOptions(delimiter=getenv('SEPARATOR')),
            read_options=csv.ReadOptions(
                encoding=getenv('ENCODE_LATIN'), 
                column_names=fields, skip_rows=1
            ), convert_options=csv.ConvertOptions(column_types=types)
        )

    @add.exception
    def pyarrowTable_To_csv(self, table: object, filename: str) -> str:
        """
        Converte uma [_**`pyarrow.Table`**_](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) 
        em [_**`parquet`**_](https://parquet.apache.org/).

        Parâmetros
        ----------
        
        **`table`** (_`object`_): a [_**`pyarrow.Table`**_](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html).
        
        **`filename`** (_`str`_): o nome do arquivo a ser gerado.

        Retorno
        -------
        **`return`** (_`str`_): mensagem de conclusão do processo. 
        """
        csv.write_csv(table, self.set_csv(filename))
        return getenv('SUCCESS')

    @add.exception
    def pyarrowTable_To_parquet(self, table: object, filename: str) -> str:
        """
        Converte uma [_**`pyarrow.Table`**_](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) 
        em [_**`parquet`**_](https://parquet.apache.org/).

        Parâmetros
        ----------

        **`table`** (_`object`_): a [_**`pyarrow.Table`**_](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html).
        
        **`filename`** (_`str`_): o nome do arquivo a ser gerado.

        Retorno
        -------
        **`return`** (_`str`_): mensagem de conclusão do processo. 
        """
        pq.write_table(table, self.set_parquet(filename))
        return getenv('SUCCESS')

    @add.exception
    def set_csv(self, filename: str) -> str:
        """
        Usado em _**`file.pyarrowTable_To_csv`**_.

        Parâmetros
        ----------
        **`filename`** (_`str`_): nome do arquivo a ser convertido.

        Retorno
        -------
        **`return`** (_`str`_): o _**`path`**_ do arquivo a ser convertido. 
        """
        if getenv('SLASH') not in filename:
            return getenv('SET_CSV_1') % (self.__settings.path, filename)
        return getenv('SET_CSV_2') % (filename.split(getenv('DOT'))[0])

    @add.exception
    def set_parquet(self, filename: str) -> str:
        """
        Usado em _**`file.csv_To_parquet`**_ e _**`file.pyarrowTable_To_parquet`**_.

        Parâmetros
        ----------
        **`filename`** (_`str`_): nome do arquivo a ser convertido.

        Retorno
        -------
        **`return`** (_`str`_): o _**`path`**_ do arquivo a ser convertido. 
        """
        if getenv('SLASH') not in filename:
            return getenv('SET_PARQUET_1') % (self.__settings.path, filename)
        return getenv('SET_PARQUET_2') % (filename.split(getenv('DOT'))[0])