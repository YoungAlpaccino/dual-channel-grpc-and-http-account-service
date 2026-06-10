"""
Tiny wrapper around grpc_tools.protoc — regenerates the _pb2 stubs.

Sketch: in production this lives in a Makefile and is run pre-commit
so the generated artefacts never drift from the .proto.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main():
    out = HERE
    proto = HERE / "protos" / "account.proto"
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{HERE / 'protos'}",
        f"--python_out={out}",
        f"--grpc_python_out={out}",
        str(proto),
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
