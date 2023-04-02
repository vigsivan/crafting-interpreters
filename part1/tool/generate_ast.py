import sys
from pathlib import Path
from typing import List

preamble = """
from abc import ABC
from typing import Any, Callable, Optional
from util import Token

class Expr(ABC):
\tdef accept(self, visitor):
\t\treturn visitor(self)
"""

def generate_ast(output_dir: Path):
    define_ast(
        output_dir,
        "Expr",
        [
            "Binary, left: Expr, operator: Token, right: Expr",
            "Grouping, expression: Expr",
            "Literal, value",
            "Unary, operator: Token, right: Expr"
        ]
    )

def define_ast(output_dir: Path, base_name: str, types: List[str]):
    path = output_dir / f"{base_name}.py"

    def _write_class(file_obj, class_str):
        comps = class_str.split(",")
        class_name, args = comps[0], comps[1:]
        arg_assignments = "\n\t\t" + "\n\t\t".join(["self."+arg+"= "+ arg.split(":")[0] for arg in args])
        init_line = "\n\t" + f"def __init__(self, {','.join(args)}): {arg_assignments}"
        file_obj.write("\n\n" + f"class {class_name}(Expr):{init_line}")

    def _define_visitor(file_obj, class_str):
        accept_line = "\n\tdef accept(self, visitor):" 
        visit_line = f"\n\t\treturn visitor.visit_{class_str.split(',')[0].lower()}(self)" 
        file_obj.write(accept_line + visit_line)

    with open(path, 'w') as f:
        f.write(preamble)
        for typ in types:
            _write_class(f, typ)
            _define_visitor(f, typ)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Expected output directory"
    output_dir = Path(sys.argv[1])
    if not output_dir.exists():
        raise ValueError(f"Output directory {output_dir} does not exist")
    generate_ast(output_dir)
