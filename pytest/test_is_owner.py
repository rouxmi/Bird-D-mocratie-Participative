import pytest
from app import is_owner


@pytest.mark.parametrize('id,user,expect',[(35,5,True),(10,35,False),(34,3,True),(32,8,True),(37,None,False)])

#cross check en regardant dans la BD
def test_is_owner(id,user,expect):
    assert is_owner(id,user) == expect