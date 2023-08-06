# django-beauty-view

Django collection mixin view

## Requirements

* Python (2.7.x )
* Django (1.5+ )

## Installation

Install using `pip`

```shell
pip install django-beauty-view
```


## Usage & Example


```python
# -*- coding: utf-8 -*-
from django.views import generic
...

from beauty_view.auth import PermissionRequiredMixin


class Create(PermissionRequiredMixin, generic.CreateView):
...
    permission_required = 'group.can_change'
...
```