# Mezzanine API Client

[![Download from PyPI](https://img.shields.io/pypi/v/mezzanine-client.svg)](https://pypi.python.org/pypi/mezzanine-client)
[![License](https://img.shields.io/pypi/l/mezzanine-client.svg)](https://pypi.python.org/pypi/mezzanine-client)
[![Join the chat](https://badges.gitter.im/gcushen/mezzanine-api.svg)](https://gitter.im/gcushen/mezzanine-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Python client SDK and remote CLI for [Mezzanine API](http://gcushen.github.io/mezzanine-api/).

# Installation

    pip install --upgrade mezzanine-client

# Documentation

[Documentation Website](http://gcushen.github.io/mezzanine-api/client/)

Example code to display recent blog posts:

```python
from mezzanine_client import Mezzanine
api = Mezzanine( 'app_id', 'app_secret' )

# Recent posts
published_posts = api.get_posts(page=1)
for post in published_posts:
    print('{} (ID: {})'.format(post['title'], post['id']))
```

# Community
[Chat Room](https://gitter.im/gcushen/mezzanine-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)


Created by [George Cushen](https://twitter.com/GeorgeCushen)
