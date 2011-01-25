from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django import template
from django.template import resolve_variable
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
from django.db.models import Model
from django.conf import settings
from ssi.utils import generate_ssi_cache_key

register = Library()

class NginxSSINode(Node):
    def __init__(self, cache_key):
        self.cache_key = cache_key
    
    def render(self, context):
        cache.set("%s:context" % self.cache_key, context)
        return """<!--# include virtual="/nginxssi/%s/" -->""" % self.cache_key
    

@register.tag
def nginxssi(parser, token):
    tokens = token.split_contents()
    # automatically generate key based on template code
    template_string = render_raw_template(parser, token, 'endnginxssi')
    cache_key = generate_ssi_cache_key(template_string)
    if cache_key not in cache:
        cache.set(cache_key, template_string)
    return NginxSSINode(cache_key)

def render_raw_template(parser, token, parse_until):
    # from http://www.holovaty.com/writing/django-two-phased-rendering/
    # Whatever is between {% raw %} and {% endraw %} will be preserved as
    # raw, unrendered template code.
    text = []
    tag_mapping = {
        template.TOKEN_TEXT: ('', ''),
        template.TOKEN_VAR: ('{{', '}}'),
        template.TOKEN_BLOCK: ('{%', '%}'),
        template.TOKEN_COMMENT: ('{#', '#}'),
    }
    # By the time this template tag is called, the template system has already
    # lexed the template into tokens. Here, we loop over the tokens until
    # {% endraw %} and parse them to TextNodes. We have to add the start and
    # end bits (e.g. "{{" for variables) because those have already been
    # stripped off in a previous part of the template-parsing process.
    while parser.tokens:
        token = parser.next_token()
        if token.token_type == template.TOKEN_BLOCK and token.contents == parse_until:
            return u''.join(text)
        start, end = tag_mapping[token.token_type]
        text.append(u'%s%s%s' % (start, token.contents, end))
    
    parser.unclosed_block_tag(parse_until)
