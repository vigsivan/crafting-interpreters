import sys
from scanner import Scanner
from util import Token, TokenType
from parser import Parser, ParserException
from interpreter import Interpreter
from runtime_error import RuntimeError
from tool.ast_printer import AstPrinter


class Lox:
    had_error: bool = False
    had_runtime_error: bool = False

    @classmethod
    def main(cls, *args):
        if len(args) > 1:
            print(f"Usage: {sys.argv[0]} [script]")
            sys.exit(64)
        elif len(args) == 1:
            cls.run_file(args[0])
        else:
            print("Running REPL")
            cls.run_prompt()

    @classmethod
    def run_file(cls, arg: str):
        with open(arg, "rb") as f:
            bytes = f.read()

        cls.run(bytes.decode("utf-8"))
        if cls.had_error:
            sys.exit(65)
        if cls.had_runtime_error:
            sys.exit(70)

    @classmethod
    def run_prompt(cls):
        while True:
            line = input("> ")
            if len(line.strip()) == 0:
                break
            cls.run(line)

    @classmethod
    def run(cls, source: str):
        try:
            scanner = Scanner(source, cls.error)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            statements = parser.parse()

            # for debugging (now OUTDATED)
            # for statement in statements:
            #     print(AstPrinter().print(statement))

            interpreter = Interpreter()
            interpreter.interpret(statements)

        except ParserException as parse_exception:
            cls.error(parse_exception.token, parse_exception.message)
        except RuntimeError as runtime_error:
            cls.runtime_error(runtime_error)

        if cls.had_error:
            return

    @classmethod
    def error(cls, line: int | Token, message: str):
        if isinstance(line, int):
            cls.report(line, "", message)
        else:
            if line.type == TokenType.EOF:
                cls.report(line.line, " at end", message)
            else:
                cls.report(line.line, f" at '{line.lexeme}'", message)

    @classmethod
    def runtime_error(cls, error: RuntimeError):
        print(error.message + f"\n[line {error.token.line}] ")
        cls.had_runtime_error = True

    @classmethod
    def report(cls, line: int, where: str, message: str):
        s = f"[line {line}] Error {where}: {message}"
        print(s)
        cls.had_error = True
        return s
