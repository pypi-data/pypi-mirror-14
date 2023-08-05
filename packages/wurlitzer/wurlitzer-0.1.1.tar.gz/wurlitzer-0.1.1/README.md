# Wurlitzer

Capture C-level stdout/stderr pipes in Python via `os.dup2`.

## Install

    pip install wurlitzer

## Usage:

Capture stdout/stderr in pipes:

```python
from wurlitzer import pipes

with pipes() as (out, err):
    call_some_c_function()

stdout = out.read()
```

Capture stdout/stderr in StringIO:

```python
from io import StringIO
from wurlitzer import pipes, STDOUT

out = StringIO()
with pipes(stdout=out, stderr=STDOUT):
    call_some_c_function()

stdout = out.getvalue()
```

Forward C-level stdout/stderr to Python sys.stdout/stderr,
which may already be forwarded somewhere by the environment, e.g. IPython:

```python
from wurlitzer import sys_pipes

with sys_pipes():
    call_some_c_function()
```

## Wurlitzer?!

[Wurlitzer](https://en.wikipedia.org/wiki/Wurlitzer) makes pipe organs. Get it? Pipes? Naming is hard.
