# Visual.py

Python interface for the Visual.js library, wrapper for Three.js as substitution for matplotlib and open3d.

## Installation

Execute 
```bash
pip install .
```

or

```bash
python setup.py install
```

If you are in developer mode run

```bash
pip install -e .
```

## Test

Take a look to `test.py` to see how the library works.


## Distribtion

Using build (`pip install build --upgrade`)

```bash
python -m build
```

Then upload to pypi

```bash
python3 -m twine upload --repository visual_py dist/*
```

LEGACY:
```bash
python setup.py sdist bdist_wheel
```
