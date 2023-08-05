# Installation
```
pip install pathvalidate
```


# Usage
## Filename validation
```python
import pathvalidate

filename = "a*b:c<d>e%f(g)h.txt"
try:
    pathvalidate.validate_filename(filename)
except ValueError:
    print("invalid filename!")
```

```console
invalid filename!
```

## Replace invalid chars
```pythn
import pathvalidate

filename = "a*b:c<d>e%f(g)h.txt"
print(pathvalidate.sanitize_filename(filename))
```

```console
abcde%f(g)h+i.txt
```

## Replace symbols
```pythn
import pathvalidate

filename = "a*b:c<d>e%f(g)h.txt"
print(pathvalidate.replace_symbol(filename))
```

```console
abcdefgh+itxt
```


# Dependencies
Python 2.6+ or 3.3+

- [DataPropery](https://github.com/thombashi/DataProperty)

## Test dependencies

-   [pytest](https://pypi.python.org/pypi/pytest)
-   [pytest-runner](https://pypi.python.org/pypi/pytest-runner)
-   [tox](https://pypi.python.org/pypi/tox)
