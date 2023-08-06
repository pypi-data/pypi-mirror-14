# BOFH Excuse Generator

Generate random BOFH themed technical excuses!

## Installation

`pip install bofhexcuse`

or

`easy_install bofhexcuse`

or

Clone the repository and `python setup.py install`

## Usage

### Python

Import `bofhexcuse` and call `bofh_excuse()`:

```python
from bofhexcuse import bofh_excuse
print bofh_excuse()[0]
```

### Command Line

Run the `bofhexcuse` command provided by `setuptools` `entry_points`.

```
C:\>bofhexcuse
Synchronous Decryption Overflow Warning
```