import pytest

from importscanner.scan import extract_package_name


@pytest.mark.parametrize('line', [
    'import pandas',
    'import pandas as pd',
    'import pandas.DataFrame',
    'import pandas.DataFrame as df'
])
def test_direct_imports(line):
    assert extract_package_name(line) == 'pandas'


@pytest.mark.parametrize('line', [
    'from pandas import DataFrame',
    'from pandas import DataFrame as df',
    'from pandas import DataFrame, Series',
    'from pandas.testing import assert_frame_equal'
])
def test_from_imports(line):
    assert extract_package_name(line) == 'pandas'


@pytest.mark.parametrize('line', [
    '  import      pandas  ',
    ' import  pandas as    pd',
    'import      pandas.   DataFrame     ',
    ' import   pandas .     DataFrame as  df '
])
def test_direct_imports_with_excessive_spacing(line):
    assert extract_package_name(line) == 'pandas'


@pytest.mark.parametrize('line', [
    '     from   pandas    import DataFrame ',
    ' from pandas     import  DataFrame  as    df',
    '   from    pandas  import    DataFrame,    Series',
    'from   pandas    .    testing import assert_frame_equal'
])
def test_from_imports_with_excessive_spacing(line):
    assert extract_package_name(line) == 'pandas'


@pytest.mark.parametrize('line', [
    'frompandas import DataFrame',
    'importpandas as pd',
    'df = pandas.DataFrame()',
    'for i in range(10)',
    'with open(path_to_file) as f:',
    'print(import_packag)'
])
def test_no_imports(line):
    assert extract_package_name(line) is None
