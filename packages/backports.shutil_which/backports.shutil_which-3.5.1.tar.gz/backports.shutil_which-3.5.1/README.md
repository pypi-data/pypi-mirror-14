# Backport of Python 3 shutil.which

Backports Python 3 [shutil.which](https://docs.python.org/3/library/shutil.html#shutil.which)

## Usage

```python
try:
    from shutil import which
except ImportError:
    from backports.shutil_which import which
```
