# Django-Clubhouse
An Open Source content management system build to compliment the [Mezzanine CMS](https://github.com/stephenmcd/mezzanine), by adding the concept of Modular Pages and block admin for multi-model change lists.

## Installation
+ Install django-clubhouse with `pip install django-clubhouse`
+ Add `mezzanine.conf`, `mezzanine.core`, `mezzanine.generic`, `mezzanine.pages`, `mezzanine.twitter` to `INSTALLED_APPS` in your Django settings module
+ Add `clubhouse.core`, `clubhouse.contrib`, `clubhouse.forms` to `INSTALLED_APPS` in your Django Settings module
+ Add the following snippet to the end of the Django settings module:
```python
try:
    from clubhouse.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
```



