import mediares


def test_version():
    assert isinstance(mediares.__version__, str)
    assert mediares.__version__
    for x in mediares.__version__.split('.'):
        assert int(x) >= 0
