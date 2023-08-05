# Cajax
[![Build Status](https://travis-ci.com/FelipeLimaM/django-cajax.svg?token=ssxA8iUN5Ljo85PBsCrq&branch=master)](https://travis-ci.com/FelipeLimaM/django-cajax) [![Gitter](https://badges.gitter.im/FelipeLimaM/django-cajax.svg)](https://gitter.im/FelipeLimaM/django-cajax?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

This amazing library was developed to facilitate communication between your Django Server and your Website through AJAX requests. Check below the wiki to view the operation of the library.

## Manual
Here is a manual how it works.

### Installation

Download and install package:
```sh
    $ pip install django-cajax
```

Through Github:
```sh
    $ pip install -e git://github.com/FelipeLimaM/django-cajax#egg=djangocajax
```

### Configure Cajax on your Django Project

**urls.py**
```python
urlpatterns += [
    ...
    url(r'^', include('cajax.urls')),
]

```

**settings.py**
```python
INSTALLED_APPS = (
    ...
    'cajax',
)

MIDDLEWARE_CLASSES = (
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
)
```

**base.html**
```html
{% load cajax %}
<html>
    <head>
        <title>Hello!</title>
    </head>
    <body>
        <p>My Page!</p>
        <div id="val"></div>
        <p>End of my page.</p>
        <script type="text/javascript" src="/static/js/jquery.js"></script> <!-- needs jQuery library -->
        {% cajax csrf_token %} <!-- import the library core, with csrf_token -->
    </body>
</html>
```

### Using Cajax
Create a file called "cajax.py" for each app that you want to use Cajax.
The Cajax Core will import all the methods in these files.
```
-project
--app1          <-- django app NOT using cajax
---views.py
---models.py
--app2          <-- django app using cajax
---cajax.py     <-- put your specific methods here
---views.py
---models.py
--app3          <-- django app using cajax
---cajax.py     <-- put your specific methods here
---views.py
---models.py
```

In this file, you'll create a new type of views on Django, called "Cajax Views". These views are executed by Cajax Core.
Each view will receive two arguments:
* request: Django Request Instance, like a normal django view;
* cajax: Cajax Core Instance (See attributes and methods avaliable below)

Don't worry about return anything.

**cajax.py**
```python
import json # use json.dumps() to send dictionarys

def my_cajax_view(request, cajax):
    info = "important text"
    result = cajax.data['value1'] + cajax.data['value2']
    my_dict = {
        'name': cajax.data['name'],
        'result': result
    }

    if cajax.data['name']:
        cajax.script("alert('Welcome "+ cajax.data['name'] +"!');")
        cajax.script("on_client('Result: "+ result +"');")
        cajax.script("with_dictionary("+ json.dumps(my_dict) +");")
        cajax.html("#val", '<b>info</b>')
    else:
        cajax.redirect('www.mypage.com?result=error')

    # More Methods
    # cajax.render('#id', 'template.html', {'value': 12})
    # cajax.html('.class', '<b>Hello World!</b>')
    # cajax.add_css_class('a', 'css-class')
    # cajax.redirect('www.google.com')
    # cajax.get_response()
```

Now on your template, call cajax(view) or cajax(view, data).
```javascript
function on_client(string) {
    $("#val").val(string);
}

function with_dictionary(dict) {
    alert(dict['name']);
}

// Cajax Calls
cajax("my_cajax_view");
// or
cajax("my_cajax_view", {'name': 'João', 'value1': 2, 'value2': 3});

```

## Cajax Core Attributes and Methods

The Cajax Core has the following attributes and methods avaliable to use:

Attribute | Description
--------- | -----------
data | Dicionary with data passed by cajax(url, data)

Method | Description
------ | -----------
get_response() | Return the HttpResponse that will be returned on the end. USE WITH CAUTION!
clean() | Erase all data on response
script(code) | Put a raw javascript code on response
redirect(url) | Redirect page to **url**
show(selector) | Force *display: block;* on node
hide(selector) | Force *display: none;* on node
prepend(selector, value) | Prepend value on node
append(selector, value) | Append value on node
assign(selector, attribute, value) | Put a value on attribute of each node
add_css_class(selector, class) | Add class on node
remove_css_class(selector, class) | Remove class on node
html(selector, html) | Put html value on node
render(selector, template, context={}) | Render a template using context with Django Template on node


## Contributors
* Felipe Lima Morais
* ElaboraInfo
* Elabora Consultoria Ltda
* Gabriel de Biasi
