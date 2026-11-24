import os
from pathlib import Path
import subprocess

wasi_sdk = "/opt/wasi-sdk"
c_compiler = f"{wasi_sdk}/bin/clang"
cxx_compiler = f"{wasi_sdk}/bin/clang++"
common_flags = ["--target=wasm32-unknown-wasip1", "--sysroot", wasi_sdk]
compile_flags = ["-Werror", "-O2", "-fno-exceptions"]
link_flags = ["-nostartfiles", "-Wl,--export-table", "-Wl,--no-entry"]
dist_path = Path("dist")
chip_linker = c_compiler

def compile_base(compiler, input_file):
    input_path = Path(input_file);
    output_path = Path(dist_path, input_path.with_suffix(".o"))
    args = [compiler] + common_flags + compile_flags
    args.append("-o")
    args.append(str(output_path))
    args.append(str(input_path))
    subprocess.run(args, check=True)
    return str(output_path)

def compile_file(input_file):
    global chip_linker
    if input_file.endswith(".c"):
        return compile_base(c_compiler, input_file)
    chip_linker = cxx_compiler
    return compile_base(cxx_compiler, input_file)

def link_chip(object_files):
    args = [chip_linker] + common_flags + link_flags
    args.append("-o")
    args.append("chip.wasm")
    args += object_files
    subprocess.run(args, check=True)

def main():
    input_files = os.environ["SOURCES"].split()
    object_files = []
    for input_file in input_files:
        object_files.append(compile_file(input_file))
    link_chip(object_files)

if __name__ == "__main__":
    main()
