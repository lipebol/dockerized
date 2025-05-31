from common.initialize import add
from ast import literal_eval
from dotenv import load_dotenv
from glob import glob
from os import getenv


class settings:

    load_dotenv()
    def __init__(self) -> None:
        """
        Arquivo de configurações do projeto onde pode ser adicionado:
         
          - __`caminho (path)`__
          - __`colunas (csv e/ou database)`__
          - __`arquivos em '/datasets' (csv e/ou parquet)`__
          - __`'schema' (database)`__
          - __`estratégia para nomear dinamicamente (csv)`__
          - __`'endpoints' e 'querys'`__
          - __`outras particularidades necessárias.`__
        
        Defina _**`csv_files`**_, _**`fetch`**_, _**`file_fields`**_, _**`mainSchema`**_, 
        _**`path`**_ e _**`resolveName`**_ mesmo que com o valor _**`None`**_.
        
        Atributos
        ---------
        **`path`** (_`str`_): variável de ambiente no arquivo _**`_common/.env`**_ com a 
        localização do diretório no _**`airflow`**_.

        **`file_fields`** (_`list`_): variável de ambiente no arquivo _**`.env`**_ com os nomes 
        dos campos (_**`colunas`**_) do arquivo _**`csv`**_, os mesmos da tabela no banco de dados.

        **`mainSchema`** (_`str`_): variável de ambiente no arquivo _**`.env`**_ com o nome do 
        _**`schema`**_ no banco de dados.

        """
        self.path = getenv('CONVERT_DATE_USING_PYARROW_PATH')
        self.file_fields = literal_eval(getenv('CONVERT_DATE_USING_PYARROW_FILE_FIELDS'))
        self.mainSchema = getenv('POSTS_SCHEMA')
        self.fetch = self.resolveName = None

    @add.exception
    def csv_files(self):
        """
        Retorna uma lista com o caminho de cada arquivo 
        [_**`csv`**_](https://pt.wikipedia.org/wiki/Comma-separated_values) 
        existente no diretório _**`/datasets`**_, utilizado para armazenamento temporário.

        Retorno
        -------
        **`return`** (_`list`_): caminhos dos arquivos.
        """
        return glob(getenv('CSV_FILES') % self.path)
    