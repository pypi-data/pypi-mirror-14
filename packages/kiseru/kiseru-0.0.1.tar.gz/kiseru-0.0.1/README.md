Kiseru is Japanese pipe. That's all.


# Install

`pip install kiseru` or `git clone git@github.com:mtwtkman/kiseru`


# Usage

You can choice `class-based` or `decorator` style.

# class-based-style

```python
from kiseru import Kiseru


doggy = Kiseru(lambda: 'inu is dog')
split = Kiseru(lambda x: x.split())
capitalize = Kiseru(lambda x: [i[0].upper() + i[1:] for i in x])
join = Kiseru(lambda x: ' '.join(x))

doggy() | split | capitalize | join
# => 'Inu Is Dog'
```

# decorator-style

This is just a syntax sugar.

```python
from kiseru import kiseru


@kiseru
def kitten():
    return 'neko is cat'

@kiseru
def kebab(x):
    return '-'.join(x.split())

@kiseru
def does_cat_hide(x):
    return 'cat' in x

kitten() | kebab | does_cat_hide
# => True
```
