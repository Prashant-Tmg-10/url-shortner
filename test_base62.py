from src.utils.helpers import encode_base62

def test_encode_base62_returns_correct_value():
    result = encode_base62(125)
    assert result == "21"



def test_encode_base62_returns_1_for_id():
    result=encode_base62(1)
    assert result == "1"

def test_encode_base62_returns_0_for_id_0():
    result = encode_base62(0)
    assert result== "0"