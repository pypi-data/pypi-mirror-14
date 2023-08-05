import subprocess, logging, os

def ok(out):
    print("\033[32mCall: %s \033[0m"%out)

def fail(out):
    print("\033[31mFailed: %s \033[0m"%out)

def call(cmd, target=None, env=None):
    env = env or os.environ.copy()
    ok(' '.join(cmd))
    return subprocess.call(cmd, env=env, cwd=target)
