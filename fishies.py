#!/usr/bin/env python3

import argparse


def chunk(text, chunk_size=2):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def compile(text, run=False):
    byte = ""
    output = ""
    for i in chunk(text, 4):
        char = i[0]
        if char in ("<", ">"):
            byte += "0" if char == ">" else "1"
            if len(byte) == 8:
                output += chr(int(byte, 2))
                byte = ""
    if run:
        exec(output)
    return output


def add_zero(binary):
    return "0" * (8 - len(binary)) + binary


def bin_to_fishies(binary):
    return "".join(["><> " if i == "0" else "<>< " for i in binary])


def main():
    lang = "fishies"
    desc = {
        "help": "show this help message and exit",
        "compile": f"compile a .{lang} file to a .py file",
        "interpret": f"compile and run a .{lang} file",
        "run": f"interpret a .{lang} string and print the output",
        "write": f"convert a .py file to a .{lang} file",
    }

    parser = argparse.ArgumentParser(description=f"{lang.capitalize()} executable", add_help=False)
    parser.add_argument("--help", "-h", action="help", help=desc["help"])
    parser.add_argument("--compile", "-c", help=desc["compile"])
    parser.add_argument("--run", "-r", help=desc["run"])
    parser.add_argument("--interpret", "-i", help=desc["interpret"])
    parser.add_argument("--write", "-w", help=desc["write"])
    args = parser.parse_args()

    if args.compile:
        if not args.compile.endswith(f".{lang}"):
            return f"File must be a .{lang} file"
        with open(args.compile, "r") as f:
            with open(f"{args.compile[:-(len(lang) + 1)]}.py", "w") as g:
                g.write(compile(f.read()))
        print(f"Created: {args.compile[:-(len(lang) + 1)]}.py")
    elif args.run:
        if not args.run.endswith(f".{lang}"):
            return f"File must be a .{lang} file"
        with open(args.run) as f:
            compile(f.read(), True)
    elif args.interpret:
        for i in args.interpret:
            if i not in "<>":
                print(f"This isn't {lang}!")
                exit()
        compile(args.interpret, True)
    elif args.write:
        if not args.write.endswith(".py"):
            return "File must be a .py file"
        with open(args.write, "r") as f:
            with open(f"{args.write[:-3]}.{lang}", "w") as g:
                g.write("".join(bin_to_fishies(add_zero(bin(ord(i))[2:])) for i in f.read()))
        print(f"Created: {args.write[:-3]}.{lang}")
    else:
        parser.print_help()


if __name__ == "__main__":
    print(main() or "")
