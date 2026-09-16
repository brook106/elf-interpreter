import sys
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def run(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    evaluator = Evaluator()
    evaluator.evaluate(ast)

def run_file(path):
    with open(path, "r") as f:
        source = f.read()
    run(source)

def run_prompt():
    buffer = []
    while True:
        prompt = "...   " if buffer else "nox> "
        line = input(prompt)
        if line == "exit" and not buffer:
            break
        buffer.append(line)
        # keep collecting while a block is open
        if line.strip().endswith(":") or (buffer and line.strip() and line.startswith((" ", "\t"))):
            continue
        source = "\n".join(buffer)
        buffer = []
        try:
            run(source)
        except Exception as e:
            print(f"error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: elfin [script.nox]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()