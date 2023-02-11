import logging
import pytest
from util import Token, TokenType
from scanner import Scanner

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

def test_scan_program_with_multiple_newlines(error_handler):
    program = '''


    print "Hello World!"



    var x = 
    3
    var y = 4
    print x + y
    '''

    scanner = Scanner(program, error_handler) 
    tokens = scanner.scan_tokens()
    # NOTE: we expect 15, because we have to account for EOF token
    assert len(tokens) == 15

    EXPECTED_TOKENS = [
    TokenType.PRINT, TokenType.STRING, 
    TokenType.VAR, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER,
    TokenType.VAR, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER,
    TokenType.PRINT, TokenType.IDENTIFIER, TokenType.PLUS, TokenType.IDENTIFIER
    ]

    for token in tokens:
        print(token)

    for token, exp_token_type in zip(tokens, EXPECTED_TOKENS):
        assert token.type == exp_token_type



def test_scan_simple_program(error_handler):
    program = '''
    print "Hello World!"
    var x = 3
    var y = 4
    print x + y
    '''

    scanner = Scanner(program, error_handler) 
    tokens = scanner.scan_tokens()
    # NOTE: we expect 15, because we have to account for EOF token
    assert len(tokens) == 15

    EXPECTED_TOKENS = [
    TokenType.PRINT, TokenType.STRING, 
    TokenType.VAR, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER,
    TokenType.VAR, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER,
    TokenType.PRINT, TokenType.IDENTIFIER, TokenType.PLUS, TokenType.IDENTIFIER
    ]

    for token in tokens:
        print(token)

    for token, exp_token_type in zip(tokens, EXPECTED_TOKENS):
        assert token.type == exp_token_type

if __name__ == "__main__":
    test_scan_simple_program(lambda x: logging.info(x[1]))
