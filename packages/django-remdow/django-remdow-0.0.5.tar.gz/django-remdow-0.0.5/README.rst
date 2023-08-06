django-remdow
=============

Simple Django app for static files (img files):

- Download external images
- To center images
- Lazy load images

Install
=======

```python
pip install django_remdow
```

Add `'django_remdow',` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_remdow',
    ...
]
```


Usage
=====

remdow app contains different filters and tags. You can activate them with line in your template:


```python
# example.html

{% load remdow %}
```


Download external images
------------------------

If you have model with HTML content which contains external images, you can download external images to local folder and receive static with help `nginx`:

Use filter `img_local`:

```python
{{ '<img src="http://placehold.it/350x150"><img src="http://placehold.it/350x150">'|img_local }}
```

This filter parse HTML code, finds `img` tag, parses urls and then downloads image to local folder, and finally, replaces img url to local url.

Lazy images
-----------

You can use `layzr.js` for lazy loading images.

Load lazy script:

```python
{% lazy_script_include %}
```

And use filter `img_lazy`:

```python
{{ '<img src="http://placehold.it/350x150">'|img_lazy }}
```


Center images with `Bootstrap`
------------------------------

Filter `img_center` centers all images

```python
{{ '<img src="http://placehold.it/350x150">'|img_center }}
```

Filter adds class `center-block` to all img tags


Image responsive with `Bootstrap`
---------------------------------

Filter `img-responsive` responsives all images

```python
{{ '<img src="http://placehold.it/350x150">'|img_responsive }}
```

Filter adds class `img-responsive` to all img tags
