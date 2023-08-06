# django-reactjs #
A simple templatetag to load reactjs libraries.

## install ##
Just include `reactjs` into your `INSTALLED_APPS`
```
#!python

INSTALLED_APPS += [ "reactjs" ]
```


## templatetag ##

Load the templatetag
```
#!html
{% load reactjs %}
```

### reactjs ###
Include the reactjs file(s) as `<scrip...></script>` tag(s).
```
#!html
{% reactjs %}
```

### reactjs-with-addons ###
Include the reactjs-with-addons file(s) as `<scrip...></script>` tag(s).
```
#!html
{% reactjs-with-addons %}
```


