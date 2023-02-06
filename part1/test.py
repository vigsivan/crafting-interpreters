import logging
import pytest
from util import Token
from scanner import Scanner

@pytest.fixture
def simple_lox_program():
    return '''
    print "Hello World!"
    var x = 3
    var y = 4
    print x + y
    '''

@pytest.fixture
def error_handler():
    f = lambda _, x: logging.info(x)
    return f


@pytest.fixture
def expect_error_handler():
    def expect_error(*args):
        raise ValueError()
    return expect_error

def test_unparseable_chracter(expect_error_handler):
    program = """print ~3"""
    scanner = Scanner(program, expect_error_handler)
    try:
        scanner.scan_tokens()
        assert False
    except ValueError:
        pass 
    assert True

def test_unterminated_string_throws_error(expect_error_handler):
    program = """print "Hello World!"""
    scanner = Scanner(program, expect_error_handler)
    try:
        scanner.scan_tokens()
        assert False
    except ValueError:
        pass 
    assert True

def test_scan_simple_program_num_tokens(simple_lox_program, error_handler):
    scanner = Scanner(simple_lox_program, error_handler) 
    tokens = scanner.scan_tokens()
    # NOTE: we expect 15, because we have to account for EOF token
    assert len(tokens) == 15
