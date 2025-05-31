from common.initialize import add
from common.file import file
from common.db import db
import pyarrow as pyarrow
import pyarrow.compute as pyarrow_compute


class Transform:
    
    def __init__(self, settings: object) -> None:
        """
        Transforma e Carrega no banco os dados que estão no arquivo 
        [_**`csv`**_](https://pt.wikipedia.org/wiki/Comma-separated_values) 
        no diretório _**`/datasets`**_, usando 
        [_**PyArrow**_](https://arrow.apache.org/docs/python/).

        Parâmetros
        ----------
        **`settings`** (_`object`_): _**`variáveis`**_ e _**`métodos`**_ 
        que estão no arquivo de configuração do projeto.

        Atributos
        ---------

        **`__file`** (_`object`_): instancia [_**file**_]().

        **`__db`** (_`object`_): instancia [_**db**_]().

        **`__fields`** (_`object`_): conteúdo de  _**`file_fields`**_ em 
        _**`settings`**_.
        """
        self.__file, self.__db = file(settings), db(settings)
        self.fields = settings.file_fields.get('data')

    @add.exception
    def convert_date_using_pyarrow(self, **kwargs): 
        """
        Converte as _**`datas`**_ do formato _**`%d/%m/%Y`**_ para _**`%Y-%m-%d`**_,
        cria duas novas colunas (__`referencia`__ e __`ano`__) 
        e carrega os dados no banco dados usando [_**db**_]().
 
        Retorno
        -------
        **`return`** (_`str`_): mensagem de conclusão do processo.
        """
        @add.exception
        def setDateFormat(chunked_array: object) -> object:
            return pyarrow_compute.strftime(
                pyarrow_compute.strptime(
                    chunked_array, '%d/%m/%Y', unit='s'
                ), '%Y-%m-%d'
            ).cast(pyarrow.date32())

        self.__table = self.__file.load_csv(
            self.fields, dict(
                (field, pyarrow.string()) for field in self.fields
            )
        )

        self.__selected = self.__table.select([2,3,5,6])

        for chunked_array, column in zip(
            self.__selected.itercolumns(), self.__selected.column_names
        ):
            self.__table = self.__table.drop_columns(column).append_column(
                column, [setDateFormat(chunked_array)]
            )

        return self.__db.adbc(self.__table, table='convert_date_using_pyarrow')
