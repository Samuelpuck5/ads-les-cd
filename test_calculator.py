import pytest
from calculator import *

def test_soma():
    assert soma(2, 3) == 5

def test_subtracao():
    assert subtracao(10, 4) == 6

def test_multiplicacao():
    assert multiplicacao(3, 4) == 12

def test_divisao():
    assert divisao(8, 2) == 4

def test_divisao_por_zero():
    with pytest.raises(ValueError):
        divisao(10, 0)