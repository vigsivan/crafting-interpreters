import logging
import pytest
from lox import Lox
from scanner import Scanner
from util import Token, TokenType

@pytest.fixture
def error_handler():
    f = lambda _, x: logging.info(x)
    return f


@pytest.fixture
def expect_error_handler():
    def expect_error(*args):
        raise ValueError()
    return expect_error

def test_unscanable_chracter(expect_error_handler):
    program = """print ~3"""
    scanner = Scanner(program, expect_error_handler)
    try:
        scanner.scan_tokens()
        assert False, "Lox scanner should not be able to parse '~'"
    except ValueError:
        pass 
    assert True

def test_unterminated_string_throws_error(expect_error_handler):
    program = """print "Hello World!"""
    scanner = Scanner(program, expect_error_handler)
    try:
        scanner.scan_tokens()
        assert False, "Scanner should've failed due to unterminated string"
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

def test_execute_simple_program():
    basic_program = '''
    print "one";
    print true;
    print 2 + 1;
    '''
    Lox().run(basic_program)

def test_execute_simple_program_with_vars():
    basic_program = '''
    var a = 1;
    var b = 2;
    print a + b;
    '''
    Lox().run(basic_program)

def test_execute_program_with_scopes():
    program = \
    """
    var a = "global a";
    var b = "global b";
    var c = "global c";
    {
      var a = "outer a";
      var b = "outer b";
      {
        var a = "inner a";
        print a;
        print b;
        print c;
      }
      print a;
      print b;
      print c;
    }
    print a;
    print b;
    print c;
    """
    Lox().run(program)

def test_conditionals_shortcircuiting():
    program = \
    """
    print "hi" or 2;
    print nil or "yes";
    """
    Lox().run(program)

def test_while_loop():
    program = \
    """
    var i = 100;
    while (true) {
        print "Hi";
        i = i - 1;
        if (i == 0) {
            break;
        }
    }
    """
    Lox().run(program)

def test_for_loop():
    program = \
    """
    for ( var i=0; i< 5; i = i + 1 )
    {
        print i;
        if (i > 2){
            break;
        }
    }
    """
    Lox().run(program)

def test_nested_for_loop():
    program = \
    """
    for ( var i=0; i< 15; i = i + 1 )
    {
        for ( var j = 0; j < i; j = j + 1)
        {
            if (i * j > i + j){
                print "Breaking inner";
                break;
            }
            print i;
            print j;
        }
    }
    """
    Lox().run(program)

def test_fibonacci():
    program = \
    """
    var n = 10;
    var prev = 1;
    var curr = 1;
    if (n == 0){
        curr = 0;
    }
    else if (n > 3) {
        for(var i = 3; i <= n; i = i + 1) {
            var tmp = curr;
            curr = prev + curr;
            prev = tmp;
        }
    }
    print "Fibonacci " + n + " = " + curr;
    """
    Lox().run(program)

def test_builtin_clock():
    program = \
    """
    print clock();
    """
    Lox().run(program)

def test_fibonacci_function():
    program = \
    """
    fun fib(n) {
        var prev = 1;
        var curr = 1;
        if (n == 0){
            curr = 0;
        }
        else if (n > 3) {
            for(var i = 3; i <= n; i = i + 1) {
                var tmp = curr;
                curr = prev + curr;
                prev = tmp;
            }
        }
        return curr;
    }
    print "Fibonacci " + 10 + " = " + fib(10);
    print "Fibonacci " + 13 + " = " + fib(13);
    print "Fibonacci " + 15 + " = " + fib(15);

    """
    Lox().run(program)

def test_recursive_fibonacci_function():
    program = \
    """
    fun fib(n) {
        if (n < 0) {
            return nil;
        }
        if (n == 0) {
            return 0;
        }
        if (n < 3) {
            return 1;
        }
        else return fib(n-1) + fib(n-2);
    }
    print "Fibonacci " + 15 + " = " + fib(15);

    """
    Lox().run(program)

def test_function_expression():
    program = \
    """
    var mongoose = fun () {
        print "Hello world";
    };
    mongoose();
    """
    Lox().run(program)

def test_function_closure():
    program = \
    """
    fun outer_function(){
        var i = 5;
        fun inner_function(n) {
            if (i < 0) {
                return i + n;
            }
            else {
                return i - n;
            }
        }
        return inner_function;
    }
    var foo = outer_function();
    print foo(2);
    print foo(2);
    print foo(2);
    print foo(2);
    """
    Lox().run(program)


def test_return():
    program = \
    """
    fun mongoose() {
        if (true) {
            return "foo";
        }
    }
    """
    Lox().run(program)


if __name__ == "__main__":
    # test_execute_simple_program_with_vars()
    # test_conditionals_shortcircuiting()
    # test_execute_program_with_scopes()
    # test_execute_simple_program_with_vars()
    # test_while_loop()
    # test_for_loop()
    # test_nested_for_loop()
    # test_fibonacci()
    # test_fibonacci_function()
    # test_return()
    # test_recursive_fibonacci_function()
    # test_builtin_clock()
    # test_function_expression()
    test_function_closure()
