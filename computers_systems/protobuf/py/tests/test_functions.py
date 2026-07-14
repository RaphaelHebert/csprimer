from my_project.functions import encode, decode


def test_encode():
    assert encode(255) == 11111111
    assert encode(1) == 1


def test_decode():
    assert decode(11111111) == 255