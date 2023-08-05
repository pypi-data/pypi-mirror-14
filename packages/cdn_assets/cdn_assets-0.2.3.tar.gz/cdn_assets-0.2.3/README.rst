==========
CDN Assets
==========

This package help you to use CDN Assets instead of downloading js and css by your self.

Quick start
-----------

0. Install this package:

    pip install cdn_assets

1. Add "cdn-assets" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cdn_assets',
    ]

2. Using filter we provide like this::

    {% load cdn_assets %}

    {% cdn bootcss %}
        {% asset bootstrap 3.3.5 css bootstrap.min css %}
        {% asset jquery 2.2.1 jquery.min js %}
    {% endcdn %}


    This will output ::
    <script src="//cdn.bootcss.com/jquery/2.2.1/jquery.min.js"></script>
    <link href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">

    Explaination ::
    {% cdn bootcss %}
        {% asset jquery 2.2.1 jquery.min js %}
    {% endcdn %}
    The last parameter for asset filter is js, It would generate <script>
    If the last parameter is css, then it would be <link rel='stylesheet'>
    '/'.join() jquery 2.2.1 jquery.min -> jquery/2.2.1/jquery.min 
    adding the js it becomes jquery/2.2.1/jquery.min.js
    The host is bootcss, so the url would be //cdn.bootcss.com/jquery/2.2.1/jquery.min.js

3. CDN Host list::

    HOST_MAPPINGS = {
        'bootcss':      'cdn.bootcss.com',
        'baidu':        'libs.baidu.com',
        'sinaapp':      'lib.sinaapp.com',
        'aspnetcdn':    'jax.aspnetcdn.com',
        'google':       'ajax.googleapis.com',
        'upai':         'upcdn.b0.upaiyun.com',
        'cdnjs':        'cdnjs.cloudflare.com',
        'staticfile':   'cdn.staticfile.org',
        '360':          'libs.useso.com'
    }



