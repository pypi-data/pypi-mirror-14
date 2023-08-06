# Dynamic form set for Django app

Allows to add and delete forms with a click of a button. Can make forms sortable.

## Requirements

Django framework, jQuery and jQuery UI.

## Installation

```
pip install dynamicformset
```

## Usage
Add "dynamicformset" to installed apps in django settings file:

```python
INSTALLED_APPS = (
    ...
    'dynamicformset',
    ...
)
```

Then it can be used in model:

```python
from django.forms import formset_factory
from dynamicformset import DynamicFormSet

myformset = formset_factory(MyForm, formset=DynamicFormSet, can_order=True, can_delete=True, extra=0)
```

Make sure required css and js files are included in a template:

```
{{ myformset.media.css }}
{{ myformset.media.js }}
```

