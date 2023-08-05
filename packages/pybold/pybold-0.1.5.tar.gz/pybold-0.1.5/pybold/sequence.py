'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import StringIO
from exceptions import TypeError

from pybold import Endpoint, PUBLIC_API_URL
import pybold.specimen
import pybold.tracefile


class Sequence(object):
    '''Class to hold Sequence information.'''
    def __init__(self, sequence_record):
        '''Initializes Sequence object
        :param sequence_record: SeqRecord object from BioPython
        :raise TypeError: when sequence_record is not an instance of SeqRecord 
        '''
        if not isinstance(sequence_record, SeqRecord):
            raise TypeError()
        
        self.sequence_record = sequence_record
        self.specimen = None
        self.tracefiles = None
        super(Sequence, self).__init__()
    
    @property
    def _description(self):
        return self.sequence_record.description
    
    @property
    def seq(self):
        '''Returns the ASCII sequence.
        e.g. CTAG'''
        return self.sequence_record.seq
    
    @property
    def process_id(self):
        return self._description.split('|')[0]
    
    @property
    def identification(self):
        return self._description.split('|')[1]
    
    @property
    def marker(self):
        return self._description.split('|')[2]
    
    @property
    def accession(self):
        return self._description.split('|')[3]
    
    @property
    def specimen(self):
        '''Lookup and return the Specimen object associated with this sequence based on the process ID.'''
        if self.__specimen is None:
            self.specimen = pybold.specimen.SpecimensClient().get(ids=self.process_id).pop()
             
        return self.__specimen
    
    @specimen.setter
    def specimen(self, specimen_obj):
        self.__specimen = specimen_obj
    
    @property
    def tracefiles(self):
        '''Lookup and return the Tracefile object associated with this sequence based on the process ID.'''
        if self._tracefiles is None:
            self.tracefiles = pybold.tracefile.TracefilesClient().get(ids=self.process_id)
            
        return self._tracefiles
    
    @tracefiles.setter
    def tracefiles(self, traces_list):
        self._tracefiles = traces_list
        
class SequencesClient(Endpoint):
    '''WebServices consumer for the Sequences end-point that fetches Sequences based on the provided criteria and returns a list of Sequence objects.'''
    ENDPOINT_NAME = 'sequence'
    
    def __init__(self, base_url=PUBLIC_API_URL):
        '''Initialize the object
        :param base_url: Override the end-point URL
        '''
        self.base_url = base_url
        super(SequencesClient, self).__init__()
        
        self.sequence_list = []

    
    def get(self, taxon=None, ids=None, bins=None, containers=None, institutions=None, researchers=None, geo=None, marker=None, timeout=5):
        '''Fetch sequences that match the provided criteria and assign it to self.sequence_list and return the list'''
        result = super(SequencesClient, self).get({'taxon': taxon, 
                                    'ids': ids, 
                                    'bin': bins, 
                                    'container': containers, 
                                    'institutions': institutions, 
                                    'researchers': researchers, 
                                    'geo': geo,
                                    'marker': marker })
    
        sequences_handle = StringIO.StringIO(result)
        
        for record in SeqIO.parse(sequences_handle, "fasta"):
            self.sequence_list.append(Sequence(record))
    
        return self.sequence_list
    
    def get_process_ids(self):
        '''Return a list of process IDs for the fetched sequences'''
        ids = []
        for sequence in self.sequence_list:
            ids.append(sequence.process_id)
        
        return ids
    
    def get_specimens(self):
        '''Lookup and return Specimen objects for fetched sequences based on the process IDs'''
        ids_query = '|'.join(self.get_process_ids())
        return pybold.specimen.SpecimensClient(self.base_url).get(ids=ids_query)
    
    def get_tracefiles(self):
        '''Lookup and return Tracefile objects for fetched sequences based on the process IDs'''
        ids_query = '|'.join(self.get_process_ids())
        return pybold.tracefile.TracefilesClient(self.base_url).get(ids=ids_query)
    
if __name__ == "__main__":
    pass

    