import os

from src.internal.algorithm_builder import AlgorithmBuilder
from src.internal.algorithm_executor import AlgorithmExecutor
from src.internal.constants import (
    DEFAULT_DEFINITION_FILE_NAME,
    DEFAULT_FUNCTION_FILE_NAME,
    DEFAULT_TEST_FILE_NAME,
    DEFAULT_TIMEOUT,
)
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors.exceptions import AlgorithmNotFoundError
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.data_element_schema import DataElementSchema
from src.internal.schemas.definition_schema import DefinitionSchema


class AlgorithmCollection:
    """Класс представляет собой набор объектов класса AlgorithmExecutor,
    созданных объектом класса AlgorithmBuilder.

    """

    def __init__(
        self,
        algorithms_catalog_path: str,
        definition_file_name: str = DEFAULT_DEFINITION_FILE_NAME,
        function_file_name: str = DEFAULT_FUNCTION_FILE_NAME,
        test_file_name: str = DEFAULT_TEST_FILE_NAME,
        execute_timeout: int = DEFAULT_TIMEOUT,
    ):
        """Конструктор класса

        :param algorithms_catalog_path: название каталога для сборки алгоритмов;
        :type algorithms_catalog_path: str
        :param definition_file_name: название файла с описанием алгоритма;
        :type definition_file_name: str
        :param function_file_name: название файла с методом для алгоритма;
        :type function_file_name: str
        :param test_file_name: название файла с авто тестами для метода
            алгоритма;
        :type test_file_name: str
        :param execute_timeout: таймаут выполнения алгоритма;
        :type execute_timeout: int
        """
        self.__algorithms: dict[str, AlgorithmExecutor] = {}
        builder = AlgorithmBuilder(
            definition_file_name,
            function_file_name,
            test_file_name,
            execute_timeout,
        )
        catalog_path = algorithms_catalog_path
        for dir in [dir for dir in os.listdir(catalog_path) if dir != "__pycache__"]:
            alg_path = catalog_path + "/" + dir
            if os.path.isdir(alg_path):
                alg = builder.build_algorithm(alg_path)
                self.__algorithms[alg.definition.name] = alg
        if len(self.__algorithms) == 0:
            raise RuntimeError(ErrMsg.NO_ALGORITHMS)

    def has_algorithm(self, algorithm_name: str) -> bool:
        """Проверяет наличие алгоритма с указанным именем.

        :param algorithm_name: имя алгоритма;
        :type algorithm_name: str
        :return: True при наличии алгоритма, иначе False.
        :rtype: bool
        """
        return algorithm_name in self.__algorithms

    def get_algorithm_list(self) -> list[DefinitionSchema]:
        """Возвращает список алгоритмов.

        :return: список алгоритмов.
        :rtype: list[BaseEntityModel]
        """
        return [alg.definition for alg in self.__algorithms.values()]

    def get_algorithm_definition(
        self, algorithm_name: str
    ) -> AlgorithmDefinitionSchema:
        """Возвращает объект класса AlgorithmDefinitionSchema с указанным именем.

        :param algorithm_name: имя алгоритма;
        :type algorithm_name: str
        :return: объект класса AlgorithmDefinitionSchema
        :rtype: AlgorithmDefinitionSchema
        :raises ValueError: если алгоритм с указанным именем отсутствует;
        """
        if algorithm_name not in self.__algorithms:
            raise AlgorithmNotFoundError(algorithm_name)
        return self.__algorithms[algorithm_name].definition

    def get_algorithm_result(
        self, algorithm_name: str, params: list[DataElementSchema]
    ) -> list[DataElementSchema]:
        """Возвращает результат выполнения алгоритма с указанным именем.

        :param algorithm_name: имя алгоритма;
        :type algorithm_name: str
        :param params: значения входных данных для выполнения алгоритма.
        :type params: list[DataElementSchema]
        :return: результат выполнения алгоритма.
        :rtype: list[DataElementSchema]
        """
        if algorithm_name not in self.__algorithms:
            raise AlgorithmNotFoundError(algorithm_name)
        return self.__algorithms[algorithm_name].execute(params)


if __name__ == "__main__":
    algo_collection = AlgorithmCollection(
        "src/algorithms",
    )
    print(algo_collection.get_algorithm_list())
