'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''
import os

TESTDATA = {
            'specimen': os.path.join(os.path.dirname(__file__), '../test-data/specimen_data.xml'),
            'sequence': os.path.join(os.path.dirname(__file__), '../test-data/sequence_data.fa'),
            'tracefiles_tar': os.path.join(os.path.dirname(__file__), '../test-data/trace_files.tar')
            }


