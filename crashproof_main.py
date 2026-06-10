"""
Supervisor (sketch).

Tiny parent process that restarts the worker on any non-zero exit.
Backs off exponentially so we don't melt the CPU on a permanent crash.
"""
import subprocess
import sys
import time

MAX_BACKOFF = 30.0


def main():
    backoff = 0.5
    while True:
        proc = subprocess.Popen([sys.executable, "main.py"])
        rc = proc.wait()
        if rc == 0:
            return
        print(f"[supervisor] worker exited rc={rc} — restarting in {backoff:.1f}s",
              file=sys.stderr)
        time.sleep(backoff)
        backoff = min(MAX_BACKOFF, backoff * 2.0)


if __name__ == "__main__":
    main()
