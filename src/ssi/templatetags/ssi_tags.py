from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.template import resolve_variable
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor
from django.db.models import Model
from django.conf import settings

register = Library()

class SSINode(Node):
    def __init__(self, nodelist, ssi_key):
        self.nodelist = nodelist
        self.ssi_key_var = Variable(ssi_key)
    
    def render(self, context):
        return """<!--# include virtual="/ssi/%s/" -->""" % \
            self.ssi_key_var.resolve(context)
    


@register.tag
def ssi(parser, token):
    nodelist = parser.parse(('endssi',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 2:
        raise TemplateSyntaxError(u"'%s' tag requires at least 1 arguments" % tokens[0])
    return SSINode(nodelist, tokens[1])
    

