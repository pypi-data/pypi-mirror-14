from django import template
from django.utils.safestring import mark_safe
from django.template.base import Node

register = template.Library()

from tag_parser import template_tag
from tag_parser.basetags import BaseNode

@template_tag(register, 'asset')
class JsCssAssetNode(BaseNode):
    """
    Implement asset filter
    Usage: 
    {% asset js jquery 3.0.0-beta1 %}
    {% asset css bootstrap 3.3.6 %}
    """
    max_args = 10
    compile_args = False
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

    def render_tag(self, context, *tag_args, **tag_kwargs):
        asset_type = tag_args[-1]
        host = self.HOST_MAPPINGS.get(self.host)
        url = '//%s/%s.%s' % (host, '/'.join(tag_args[:-1]), asset_type)
        if asset_type == 'css':
            output = '<link href="%s" rel="stylesheet">' % url
        elif asset_type == 'js':
            output = '<script src="%s"></script>' % url
        else:
            output = ''
        return mark_safe(output)



class CDNNode(Node):
    """Implements the actions of the asserts tag."""
    def __init__(self, host, nodelist):
        self.host = host
        self.nodelist = nodelist
        for node in self.nodelist:
            node.host = host

    def __repr__(self):
        return "<CDNNode>"

    def render(self, context):
        output = self.nodelist.render(context)
        return mark_safe(output)


@register.tag('cdn')
def do_cdn(parser, token):
    """
    Implement cdn filter
    Usage: 
    {% cdn bootcss %}
        {% asset jquery 3.0.0-beta1 jquery.min js %}
        {% asset bootstrap 3.3.6 css bootstrap.min css %}
        {% asset bootstrap 3.3.6 js bootstrap.min js %}
    {% endcdn %}
    this will output:
        <script src="//cdn.bootcss.com/jquery/3.0.0-beta1/jquery.min.js"></script>
        <link href="//cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    """
    bits = token.split_contents()[1]
    nodelist = parser.parse(('endcdn',))
    token = parser.next_token()
    return CDNNode(bits, nodelist)



class JsCssFontNode(Node):
    """Implements the actions of the js tag."""
    def __init__(self, asset_type, bits):
        self.type = asset_type #JS or CSS or font
        self.bits = bits # name,version such as jquery 1.11

    def __repr__(self):
        return "<JsCssNode>"

    def render(self, context):
        output = ''
        return mark_safe(output)

@register.tag
def js(parser, token):
    bits = token.split_contents()
    nodelist = parser.parse(('endjs',))
    token = parser.next_token()
    return JsCssFontNode('js', bits)

@register.tag
def css(parser, token):
    bits = token.split_contents()
    nodelist = parser.parse(('endcss',))
    token = parser.next_token()
    return JsCssFontNode('css', bits)

@register.tag
def font(parser, token):
    bits = token.split_contents()
    nodelist = parser.parse(('endfont',))
    token = parser.next_token()
    return JsCssFontNode('font', bits)

@register.simple_tag
def local(file):
    return mark_safe('<link href="" rel="stylesheet">')

