'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''
from __builtin__ import super, str
import __builtin__
from lxml import objectify
import pickle
import threading 

from pybold import PUBLIC_API_URL, Endpoint
import pybold.sequence
import pybold.tracefile


class Specimen(object):
    '''Class to hold specimen information'''

    def __init__(self, objectified_element=None, specimen_record_xml=None):
        '''Initialize Specimen object
        Either the specimen_record_xml or the objectified_element parameter must be provided.
        :param objectified_element: (optional) Objectified XML returned from BOLD specimen end-point
        :param specimen_record_xml: (optional) XML returned from BOLD specimen end-point'''
        if isinstance(specimen_record_xml, __builtin__.str):
            obj = objectify.fromstring(specimen_record_xml)
        elif isinstance(objectified_element, objectify.ObjectifiedElement):
            obj = objectified_element
        elif objectified_element is None and specimen_record_xml is None:
            raise ValueError()
        
        
        self.record = obj
        self.sequence = None
        self.tracefiles = None
        
        super(Specimen, self).__init__()
    
    @property
    def taxonomy(self):
        '''Return a dictionary containing the taxonomy for this specimen
        The taxonomy dictionary will contain phylum, class, order, family, subfamily, genus, and species.
        If the taxonomy rank is not provided, it will be set to an empty string.'''
        if not hasattr(self.record, 'taxonomy'):
            return None
        
        ranks = ('phylum', 'class', 'order', 'family', 'subfamily', 'genus', 'species')
        taxonomy = {}
        for rank in ranks:
            name = None
            if hasattr(self.record.taxonomy, rank):
                name = str(getattr(self.record.taxonomy, rank).taxon.name)
            
            taxonomy[rank] = name or ''

        return taxonomy
    
    @property
    def record_id(self):
        return int(self.record.record_id)
    
    @property
    def process_id(self):
        return str(self.record.processid)
    
    @property
    def geography(self):
        '''Return an object containing the geography associated with the specimen.
        The Geography object will contain the attributes (country, province, region, coordinates:tupple), which will either be None or contain a value.
        '''
        class Geography():
            def __init__(self):
                self.country = None
                self.province = None
                self.region = None
                self.coordinates = (None, None)
        
        geo = Geography()
        try:
            geo.country = self.record.collection_event.country
            geo.province = self.record.collection_event.province
            geo.region = self.record.collection_event.region
            geo.coordinates = (self.record.collection_event.coordinates.lat, self.record.collection_event.coordinates.long)
        except (KeyError, AttributeError):
            pass
        
        return geo
    
    @property
    def sequence(self):
        '''Lookup and return the Sequence object associated with this specimen based on the process ID.''' 
        # If property is not set, then call the setter
        if self.__sequence is None:
            # Provide the setter with a Sequence object using an API query that fetches the sequence
            self.sequence = pybold.sequence.SequencesClient().get(ids=self.process_id).pop()
        
        return self.__sequence
    
    @sequence.setter
    def sequence(self, sequence_obj):        
        self.__sequence =  sequence_obj
    
    @property
    def tracefiles(self):
        '''Lookup and return the Tracefile object associated with this specimen based on the process ID.'''
        if self._tracefiles is None:
            self.tracefiles = pybold.tracefile.TracefilesClient().get(ids=self.process_id)
            
        return self._tracefiles
    
    @tracefiles.setter
    def tracefiles(self, traces_list):
        self._tracefiles = traces_list
    
class SpecimensClient(Endpoint):
    '''WebServices consumer for the Specimens end-point that fetches specimens based on provided criteria and returns Specimen objects.'''
    ENDPOINT_NAME = 'specimen'
    
    def __init__(self, base_url=PUBLIC_API_URL):
        '''Initialize the object
        :param base_url: Override the end-point URL
        '''
        self.base_url = base_url
        super(SpecimensClient, self).__init__()
        
        self.specimen_list = []


    def get(self, taxon=None, ids=None, bins=None, containers=None, institutions=None, researchers=None, geo=None, timeout=5):
        '''Fetch specimen that match the provided criteria and assign it to self.specimen_list and return the list'''
        result = super(SpecimensClient, self).get({'taxon': taxon, 
                                    'ids': ids, 
                                    'bin': bins, 
                                    'container': containers, 
                                    'institutions': institutions, 
                                    'researchers': researchers, 
                                    'geo': geo, 
                                    'format': 'xml'}, timeout=timeout)
    
        bold_specimens = objectify.fromstring(result)
        
        for record in bold_specimens.record:
            self.specimen_list.append(Specimen(record))
    
        return self.specimen_list
    
    def get_taxonomies(self):
        '''Return list of taxonomies of fetched specimen'''
        taxonomies = {}
        for specimen in self.specimen_list:
            taxonomies[specimen.process_id] = specimen.taxonomy
        return taxonomies 
    
    def get_record_ids(self):
        '''Return list of record IDs of fetched specimen'''
        ids = []
        for specimen in self.specimen_list:
            ids.append(specimen.record_id)    
        return ids
    
    def get_process_ids(self):
        '''Return list of process IDs of fetched specimen'''
        ids = []
        for specimen in self.specimen_list:
            ids.append(specimen.process_id)
        
        return ids
    
    def get_sequences(self):
        '''Return Sequence objects for fetched specimen based on the process IDs'''
        ids_query = '|'.join(self.get_process_ids())
        return pybold.sequence.SequencesClient(self.base_url).get(ids=ids_query)
    
    def get_tracefiles(self):
        '''Return Tracefile objects for fetched specimen based on the process IDs'''
        ids_query = '|'.join(self.get_process_ids())
        return pybold.tracefile.TracefilesClient(self.base_url).get(ids=ids_query)
    
if __name__ == "__main__":
    pass