import string
import random
import datetime
from app import functions

ALLOWED_EXTENSIONS = ['png', 'pdf', 'jpg', 'jpeg']
NOTALLOWED_EXTENSIONS = ['war', 'jar', 'py', 'exe', 'bmp', 'tif', 'ppt']

def date_gen():
    year = random.choice(range(1950,2019))
    month = random.choice(range(1,13))
    if month == 2:
        day = random.choice(range(1,29))
    elif month in [4, 6, 9, 11]:
        day = random.choice(range(1,31))
    else:
        day = random.choice(range(1,32))
    return (year, month, day)

def test_date():
    """
    """
    rand_date_args = date_gen()
    string_date = '/'.join([str(rand_date_args[a]) for a in range(2, -1, -1)])
    assert datetime.date(rand_date_args[0], rand_date_args[1], rand_date_args[2]) == functions.str_to_date(string_date)

def test_intstr_to_float():
    """
    """
    int_str = str(random.choice(range(0, 100001)))
    assert float(int_str) == functions.str_to_float(int_str)

def test_floatstr_to_float():
    """
    """
    int_part = str(random.choice(range(0, 100001)))
    float_part = str(random.random()).split('.')[-1]
    assert float('.'.join([int_part,float_part])) == functions.str_to_float(','.join([int_part,float_part]))

def test_file_isallowed():
    """
    """
    rand_string = ''.join([random.choice(string.ascii_letters) for i in range (random.randint(5,16))])
    rand_filename = '.'.join([rand_string, random.choice(ALLOWED_EXTENSIONS)])
    assert  functions.allowed_file(rand_filename)

def test_file_notallowed():
    """
    """
    rand_string = ''.join([random.choice(string.ascii_letters) for i in range (random.randint(5,16))])
    rand_filename = '.'.join([rand_string, random.choice(NOTALLOWED_EXTENSIONS)])
    assert  functions.allowed_file(rand_filename) == False
