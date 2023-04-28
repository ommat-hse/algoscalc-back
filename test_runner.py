import unittest
from core_tests.algorithm_collection_tests import AlgorithmCollectionTests
from core_tests.algorithm_builder_tests import AlgorithmBuilderTest
from core_tests.algorithm_tests import AlgorithmTests
from core_tests.data_element_tests import DataElementTests
from core_tests.data_type_tests import DataTypeTests
from core_tests.data_shape_tests import DataShapeTests


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(DataShapeTests))
suite.addTest(unittest.makeSuite(DataTypeTests))
suite.addTest(unittest.makeSuite(DataElementTests))
suite.addTest(unittest.makeSuite(AlgorithmTests))
suite.addTest(unittest.makeSuite(AlgorithmBuilderTest))
suite.addTest(unittest.makeSuite(AlgorithmCollectionTests))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)