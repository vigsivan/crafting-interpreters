import sys
from scanner import Scanner

class Lox :
    had_error: bool = False

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
        with open(arg, 'rb') as f:
            bytes  = f.read()

        cls.run(bytes.decode("utf-8"))
        if cls.had_error:
            sys.exit(65)

    @classmethod
    def run_prompt(cls):
        while True:
            line = input("> ")
            if len(line.strip()) == 0:
                break
            cls.run(line)
            had_error = False;

    @classmethod
    def run(cls, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        # TODO
        for token in tokens:
            print(token)

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        cls.had_error = True
