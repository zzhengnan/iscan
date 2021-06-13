from iscan.std_lib import separate_third_party_from_std_lib


def test_separate_third_party_from_std_lib():
    packages = ['numpy', 'pandas', 'os', 'time']
    expected = ['numpy', 'pandas'], ['os', 'time']
    assert separate_third_party_from_std_lib(packages) == expected
