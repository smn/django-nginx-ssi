from django.test import TestCase
from django.template import Template, Context

class SSITestCase(TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_ssi_template_rendering(self):
        template = Template("""
        {% load ssi_tags %}
        {% ssi "test-ssi-template" %}
            <b> okidoki </b> {% now "jS F Y H:i" %} Hello {{ foo }}
        {% endssi %}
        """)
        context = Context({'foo': 'bar'})
        response = template.render(context)
        self.assertTrue('<!--# include virtual="/ssi/test-ssi-template/" -->' \
                            in response)