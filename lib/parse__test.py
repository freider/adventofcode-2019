from .parse import ReParse

def test_int_tuple():
    rp = ReParse(r"<x={int}, y={int}, z={int}>")
    assert (-9, 10, -1) == rp.match("<x=-9, y=10, z=-1>")


def test_float_dict():
    rp = ReParse(r"<x={x:float}, y={y:int}, z=-{z:str}>")
    assert {"x": -9.0, "y": 10, "z": "1"} == rp.match("<x=-9, y=10, z=-1>")

def test_suffix_match():
    assert (15,) == ReParse(r"{int}").match("15trololol")

def test_parse_multi():
    assert (1,2,3) == ReParse(r"({int},?)*").match("1,2,3")
