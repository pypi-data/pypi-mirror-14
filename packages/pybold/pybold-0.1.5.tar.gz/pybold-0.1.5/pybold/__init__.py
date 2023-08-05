'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''

PUBLIC_API_URL = 'http://www.boldsystems.org/index.php/API_Public/'
TAXON_API_URL = 'http://www.boldsystems.org/index.php/API_Tax/'

from exceptions import ValueError
import requests 
from urlparse import urljoin

class Endpoint(object):   
    ENDPOINT_NAME = None
    base_url = PUBLIC_API_URL
    
    def __init__(self):
        super(Endpoint,self)
        self._set_base_url()
        self.session = None;

        
    def _set_base_url(self):
        if self.base_url is None or self.base_url == '':
            raise ValueError("BOLD API's base URL cannot be empty.")
        
        if not self.base_url.endswith('/'): self.base_url += '/'
        
        self.url = urljoin(self.base_url, self.ENDPOINT_NAME)
        
    def get(self, payload, timeout=5, keep_alive=True):
        if keep_alive:
            if self.session is None:
                self.session = requests.Session()
            result = self.session.get(self.url, params=payload, timeout=timeout)
        else:
            result = requests.get(self.url, params=payload, timeout=timeout)
            
        if result.status_code != 200 and result.status_code != 304:
            result.raise_for_status()
        
        return result.content