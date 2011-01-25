from django.test import TestCase, Client
from django.template import Template, Context
from django.core.urlresolvers import reverse
from ssi.utils import generate_ssi_cache_key

class SSITestCase(TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_ssi_template_rendering(self):
        ssi_fragment = '<b> okidoki </b> {%now "jS F Y H:i"%} Hello {{foo}}'
        template_string = """
            {% load nginxssi_tags %}
            {% nginxssi %}""" + ssi_fragment + """{% endnginxssi %}
        """
        template = Template(template_string)
        context = Context({'foo': 'bar'})
        template_response = template.render(context)
        cache_key = generate_ssi_cache_key(ssi_fragment)
        self.assertTrue('<!--# include virtual="/nginxssi/%s/" -->' % cache_key \
                            in template_response)
        
        client = Client()
        response = client.get(reverse('nginxssi',args=(cache_key,)))
        template = Template(ssi_fragment)
        self.assertEquals(response.content.strip(), template.render(context).strip())
    
