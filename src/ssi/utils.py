from django.utils.hashcompat import md5_constructor
from django.conf import settings

def generate_ssi_cache_key(template_string):
    return md5_constructor(':'.join(["ssi", 
                getattr(settings, 'CACHE_SSI_KEY_PREFIX', ''), 
                template_string])).hexdigest()