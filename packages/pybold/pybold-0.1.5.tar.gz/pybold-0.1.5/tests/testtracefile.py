'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''

import os.path
import tarfile
import unittest

import pybold.sequence
import pybold.specimen
import pybold.tracefile
from tests import TESTDATA


class TracefilesTest(unittest.TestCase):
    def setUp(self):
        self.process_ids = ['ACRJP618-11', 'ACRJP619-11']
        self.markers = ['COI-5P']
        self.formats = ['ab1']
        self.taxons = ['Lepidoptera']
        self.filenames = ['ACRJP619-11[LepF1,LepR1]_R.ab1','ACRJP619-11[LepF1,LepR1]_F.ab1', 'ACRJP618-11[LepF1,LepR1]_F.ab1']
        self.tracefile_list = pybold.tracefile.Tracefile.parse_from_tar(file_name=TESTDATA['tracefiles_tar'])
    
    def tearDown(self):
        del self.process_ids
        del self.markers
    
    def _parse_from_tar(self, tracefile_list):
        self.assertIsNotNone(tracefile_list, "Failed to parse a tar with tracefiles: returned null.")
        self.assertIsInstance(tracefile_list, list, "Tracefile.parse_from_tar should return a list of Tracefile objects.")
        for item in tracefile_list:
            self.assertIsInstance(item, pybold.tracefile.Tracefile, "Tracefile.parse_from_tar should return a list of Tracefile objects")
    
    def test_parse_from_tar_by_string(self):
        with open(TESTDATA['tracefiles_tar'], 'r') as f:
            tracefile_list = pybold.tracefile.Tracefile.parse_from_tar(tar_string=f.read())            
            self._parse_from_tar(tracefile_list)
    
    def test_parse_from_tar_by_path(self):
        tracefile_list = pybold.tracefile.Tracefile.parse_from_tar(file_name=TESTDATA['tracefiles_tar'])
        self._parse_from_tar(tracefile_list)
        
    def test_parse_from_tar_without_params(self):
        with self.assertRaises(ValueError):
            pybold.tracefile.Tracefile.parse_from_tar()
    
    def _has_attribute(self, attr_name):
        for item in self.tracefile_list:
            self.assertTrue(hasattr(item, attr_name), "Tracefile should have the {} attribute.".format(attr_name))
    
    def test_specimen(self):
        self._has_attribute("specimen")
        for tracefile in self.tracefile_list:
            self.assertIsInstance(tracefile.specimen, pybold.specimen.Specimen, "Tracefile objects should have a specimen attribute.")
            self.assertEqual(tracefile.process_id, tracefile.specimen.process_id, "Tracefile.process_id should equal Tracefile.specimen.process_id.")
            
    def test_sequence(self):
        self._has_attribute("sequence")
        for tracefile in self.tracefile_list:
            self.assertIsInstance(tracefile.sequence, pybold.sequence.Sequence, "Tracefile objects should have a sequence attribute.")
    
    def test_process_id(self):
        self._has_attribute("process_id")
        for tracefile in self.tracefile_list:
            self.assertIn(tracefile.process_id, self.process_ids, "Tracefile %s's process id (%s) is not in the anticipated list for the test-data.".format(tracefile.filename, tracefile.process_id))
            
    def test_format(self):
        self._has_attribute("format")
        for tracefile in self.tracefile_list:
            self.assertEqual(tracefile.format, "ab1", "Tracefile %s's format (%s) is not in the anticipated list for the test-data.".format(tracefile.filename, tracefile.format))
        
    def test_marker(self):
        self._has_attribute("marker")
        for tracefile in self.tracefile_list:
            self.assertIn(tracefile.marker, self.markers, "Tracefile %s's marker (%s) is not in the anticipated list of the test-data.".format(tracefile.filename, tracefile.marker))
    
    def test_taxon(self):
        self._has_attribute("taxon")
        for tracefile in self.tracefile_list:
            self.assertIn(tracefile.taxon, self.taxons, "Tracefile %s's taxon (%s) is not in the anticipated list for the test-data.".format(tracefile.filename, tracefile.taxon))
    
    def test_genbank_accession(self):
        self._has_attribute("genbank_accession")
        # TODO: test for genbank accession
    
    def test_filename(self):
        self._has_attribute("filename")
        for tracefile in self.tracefile_list:
            self.assertIn(tracefile.filename, self.filenames, "Tracefile's filename (%s) is not in the anticipated list for the test-data.".format(tracefile.filename))
    
    def test_to_file(self):
        for tracefile in self.tracefile_list:
            tracefile_path = tracefile.to_file()
            self.assertTrue(os.path.exists(tracefile_path), "Attempted to write %s, but it does not exist.".format(tracefile_path))
            self.assertEqual(os.path.basename(tracefile_path), tracefile.filename, "The tracefile was written to disk with an unexpected file name.")
    
    def test_to_file_with_dir_path(self):
        chromat_dir = "/tmp"
        for tracefile in self.tracefile_list:
            tracefile_path = tracefile.to_file('/tmp')
            self.assertTrue(os.path.exists(tracefile_path), "Attempted to write %s, but it does not exist.".format(tracefile_path))
            self.assertEqual(os.path.basename(tracefile_path), tracefile.filename, "The tracefile was written to disk with an unexpected file name.")
            self.assertEqual(os.path.dirname(tracefile_path), chromat_dir, "The tracefile was written to disk to an unexpected path.")

    
    def test_to_file_with_dir_path_and_filename(self):
        chromat_dir = "/tmp"
        chromat_name = "tmp_chromat.ab1"
        for tracefile in self.tracefile_list:
            tracefile_path = tracefile.to_file(chromat_dir, chromat_name)
            self.assertTrue(os.path.exists(tracefile_path), "Attempted to write %s, but it does not exist.".format(tracefile_path))
            self.assertEqual(os.path.basename(tracefile_path), chromat_name, "The tracefile was written to disk with an unexpected file name.")
            self.assertEqual(os.path.dirname(tracefile_path), chromat_dir, "The tracefile was written to disk to an unexpected path.")
    
    def test_to_file_with_filename(self):
        chromat_name = "tmp_chromat.ab1"
        for tracefile in self.tracefile_list:
            tracefile_path = tracefile.to_file(filename=chromat_name)
            self.assertTrue(os.path.exists(tracefile_path), "Attempted to write %s, but it does not exist.".format(tracefile_path))
            self.assertEqual(os.path.basename(tracefile_path), chromat_name, "The tracefile was written to disk with an unexpected file name.")
    
class TracefilesClientTest(unittest.TestCase):


    def setUp(self):
        self.process_ids = ["BOM1525-10", "BOM1528-10", "GBIR5337-13", "KKBNA817-05", "KKBNA820-05", "KKBNA821-05", 
                            "KKBNA824-05", "KKBNA827-05", "KKBNA830-05", "KKBNA831-05", "KKBNA834-05", "KKBNA840-05", 
                            "KKBNA851-05", "KKBNA852-05", "KKBNA854-05", "KKBNA855-05", "KKBNA856-05", "KKBNA857-05"]
        self.record_ids = ["6283631", "6283648", "6283659", "6283679", "5064977", "5064989", "5065007", "5065009", 
                           "5065014", "6039995", "6039996", "6040002", "6040009", "6040013", "6040016", "6040035", 
                           "6040047", "6040055", "6040056", "6040057", "6040061", "6040062", "6040077", "6040078"]
        self.taxons = ["Archaeorhizomycetes", "Arthoniomycetes"]
        self.geographies = ["Canada", "United States"]
        self.bins = ["BOLD:AAA5125", "BOLD:AAA5126"]
        #self.containers = ["ACRJP", "ACRJI"]
        self.institutions = ["Biodiversity Institute of Ontario", "Agriculture and Agri-Food Canada"]
        self.researchers = ["Rodolphe Rougerie","Hai D. T. Nguyen"]
        self.markers = ["ITS", "COI"]
        # Instantiate the SequencesClient class to be used throughout all tests
        self.tracefiles_client = pybold.tracefile.TracefilesClient()

    def tearDown(self):
        self.process_ids = None
        self.record_ids = None
        self.taxons = None
        self.bins = None
        self.institutions = None
        self.researchers = None
        self.sequences_client = None
    
    def test_isinstance(self):
        self.assertIsInstance(self.tracefiles_client, pybold.tracefile.TracefilesClient, "tracefiles_client failed to instantiate as a TracefilesClient")
    
    def test_tracefile_list_attribute(self):
        self.assertTrue(hasattr(self.tracefiles_client, 'tracefile_list'), 'TracefilesClient does not have a tracefile_list attribute')
        self.assertIsInstance(self.tracefiles_client.tracefile_list, list, 'TracefilesClient.tracefile_list must be of type list')
    
    def test_get_process_ids(self):
        self.tracefiles_client.get(ids='|'.join(self.process_ids))
        process_ids = self.tracefiles_client.get_process_ids()
        for process_id in process_ids:
            self.assertIn(process_id, self.process_ids, 'Returned tracefile process_id ({}) was not part of original search criteria'.format(process_id))
    
    def test_get_sequences(self):
        self.tracefiles_client.get(ids='|'.join(self.process_ids))
        sequences = self.tracefiles_client.get_sequences()
        self.assertIsInstance(sequences, list, "TracefilesClient.get_sequences() should return a list of Sequence.")
        for sequence in sequences:
            self.assertIsInstance(sequence, pybold.sequence.Sequence, "TracefilesClient.get_sequences() should return a list of Sequence.")
    
    def test_get_specimens(self):
        self.tracefiles_client.get(ids='|'.join(self.process_ids))
        specimen_list = self.tracefiles_client.get_specimens()
        self.assertIsInstance(specimen_list, list, "TracefilesClient.get_specimens() should return a list of Specimen.")
        for specimen in specimen_list:
            self.assertIsInstance(specimen, pybold.specimen.Specimen, "TracefilesClient.get_specimens() should return a list of Specimen.")

    def _test_get(self,taxon=None, ids=None, bins=None, containers=None, institutions=None, researchers=None, geo=None, marker=None, timeout=5):
        tracefile_list = self.tracefiles_client.get(taxon=taxon, 
                                                 ids=ids, 
                                                 bins=bins, 
                                                 containers=containers, 
                                                 institutions=institutions, 
                                                 researchers=researchers, 
                                                 geo=geo,
                                                 marker=marker,
                                                 timeout=timeout)
        msg = 'SequencesClient.get() should return a list of Tracefile objects'
        self.assertIsNotNone(tracefile_list, msg)
        self.assertIsInstance(tracefile_list, list, msg )
        self.assertIsInstance(tracefile_list[0], pybold.tracefile.Tracefile, msg)
        self.assertListEqual(tracefile_list, self.tracefiles_client.tracefile_list, 'TracefilesClient.get() and TracefilesClient.sequence_list should be equal')
        return tracefile_list
    
    def test_get_by_processids(self):
        tracefile_list = self._test_get(ids='|'.join(self.process_ids))
        for tracefile in tracefile_list:
            self.assertIn(tracefile.process_id, self.process_ids, 'Returned Tracefile process_id ({}) does not match original search criteria'.format(tracefile.process_id))

    def test_get_by_taxon_and_marker(self):
        tracefile_list = self._test_get(taxon='|'.join(self.taxons), marker='|'.join(self.markers))
        for tracefile in tracefile_list:
            found = False
            for marker in self.markers:
                if marker in tracefile.marker:
                    found = True
            self.assertTrue(found, "Returned Sequence was not part of original search criteria for markers {}.".format(', '.join(self.markers)))
             
        #TODO validate taxons

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()