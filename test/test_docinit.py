import pytest
from docinit.docinit import convert

def test_convert_bool():
    assert convert('tRUe') == True