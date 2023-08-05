'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''

from Bio import SeqIO
import Bio.Seq
import StringIO
import os.path
from twisted.python.util import println
import unittest

from pybold.sequence import Sequence
import pybold.sequence
from tests import TESTDATA


class SequenceTest(unittest.TestCase):
    def setUp(self):
        with open(TESTDATA['sequence'], 'r') as f:
            sequence_data = f.read()
            
        sequences_handle = StringIO.StringIO(sequence_data)
        
        for record in SeqIO.parse(sequences_handle, "fasta"):
            self.sequence = Sequence(record)
            break
    
    def tearDown(self):
        del self.sequence
    
    def _has_attribute(self, attr_name):
        self.assertTrue(hasattr(self.sequence, attr_name), "Sequence should have the {} attribute.".format(attr_name))
        
    def test_sequence_record(self):
        self._has_attribute("sequence_record")
    
    def test_seq(self):
        self._has_attribute("seq")
        self.assertIsInstance(self.sequence.seq, Bio.Seq.Seq, "Sequence.seq should return a Bio.Seq.Seq object.")
        self.assertEqual(str(self.sequence.seq), "NNNNNNNNNNNNNTTCGGCGCATGGGCTGGTATAGTAGGTACTGCCCTTAGCCTACTTATCCGTGCAGAACTAGGTCAACCAGGAACCCTTCTAGGAGACGACCAAATCTACAACGTAATCGTCACCGCCCATGCCTTTGTAATAATCTTCTTCATAGTAATACCTATCATAATTGGGGGCTTCGGAAACTGATTAGTCCCACTTATAATTGGTGCTCCCGACATGGCATTCCCACGTATGAACAACATAAGCTTCTGACTACTCCCCCCATCATTCTTACTTCTCCTAGCCTCCTCTACAGTAGAAGCTGGGGCAGGCACGGGATGAACCGTGTACCCTCCCCTAGCCGGTAATCTAGCCCATGCCGGAGCTTCAGTGGATTTAGCAATCTTCTCCCTCCATCTAGCAGGTGTATCCTCTATCCTTGGTGCTATCAACTTTATCACCACAGCTATCAACATAAAACCCCCCGCCCTTTCACAATACCAAACTCCTCTATTTGTATGATCCGTACTTATCACTGCCGTTCTACTATTACTCTCACTCCCAGTACTTGCCGCCGGTATCACTATGTTGTTAACAGACCGAAACCTAAACACAACGTTCTTTGATCCTGCTGGAGG----------------------------------------------------------------------", "Sequence.seq does not match expected string.") 
        
    def test_process_id(self):
        self._has_attribute("process_id")
        self.assertIsInstance(self.sequence.process_id, basestring, "Sequence.process_id should be a string.")
        exp_process_id = "CDUSM030-05"
        self.assertEqual(self.sequence.process_id, exp_process_id, "Sequence.process_id {} does not match content of test data {}.".format(self.sequence.process_id, exp_process_id))
    
    def test_identification(self):
        self._has_attribute("identification")
        exp_identification = "Thalasseus sandvicensis"
        self.assertEqual(self.sequence.identification, exp_identification, "Sequence.identification {} does not match content of test data {}.".format(self.sequence.identification, exp_identification))
    
    def test_marker(self):
        self._has_attribute("marker")
        exp_marker = "COI-5P"
        self.assertEqual(self.sequence.marker, exp_marker, "Sequence.marker {} does not match content of test data {}.".format(self.sequence.marker, exp_marker))
        
    def test_accession(self):
        self._has_attribute("accession")
        exp_accession = "DQ433214"
        self.assertEqual(self.sequence.accession, exp_accession, "Sequence.accession {} does not match content of test data {}.".format(self.sequence.accession, exp_accession))
        
    def test_specimen(self):
        self._has_attribute("specimen")
        self.assertIsInstance(self.sequence.specimen, pybold.specimen.Specimen, "Sequence.specimen should return a Specimen object.")
        self.assertEqual(self.sequence.process_id, self.sequence.specimen.process_id, "Sequence.sequence's process_id does not match its sequence.process_id")

    def test_tracefiles(self):
        self._has_attribute("tracefiles")
        self.assertIsInstance(self.sequence.tracefiles, list, "Sequence.tracefiles should return a list of tracefile objects.")
        for tracefile in self.sequence.tracefiles:
            self.assertIsInstance(tracefile, pybold.tracefile.Tracefile, "Sequence.tracefiles should return a list of tracefile objects.")

class SequencesClientTest(unittest.TestCase):


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
        self.sequences_client = pybold.sequence.SequencesClient()

    def tearDown(self):
        self.process_ids = None
        self.record_ids = None
        self.taxons = None
        self.bins = None
        self.institutions = None
        self.researchers = None
        self.sequences_client = None


    def test_isinstance(self):
        self.assertIsInstance(self.sequences_client, pybold.sequence.SequencesClient, "sequences_client failed to instantiate as a SequencesClient")
    
    def test_sequences_list_attribute(self):
        self.assertTrue(hasattr(self.sequences_client, 'sequence_list'), 'SequencesClient does not have a sequence_list attribute')
        self.assertIsInstance(self.sequences_client.sequence_list, list, 'SequencesClient.sequence_list must be of a list')
    
    def test_get_process_ids(self):
        self.sequences_client.get(ids='|'.join(self.process_ids))
        process_ids = self.sequences_client.get_process_ids()
        self.assertIsInstance(process_ids, list, "SequencesClient.get_process_ids should return a list of process ids")
        for process_id in process_ids:
            self.assertIn(process_id, self.process_ids, 'Returned sequence process_id ({}) was not part of original search criteria'.format(process_id))

    def test_get_specimens(self):
        self.sequences_client.get(ids='|'.join(self.process_ids))
        specimen_list = self.sequences_client.get_specimens()
        self.assertIsInstance(specimen_list, list, "SequencesClient.get_specimens() should return a list of Specimen.")
        for specimen in specimen_list:
            self.assertIsInstance(specimen, pybold.specimen.Specimen, "SequencesClient.get_specimens() should return a list of Specimen.")
    
    def test_get_tracefiles(self):
        self.sequences_client.get(ids='|'.join(self.process_ids))
        tracefiles = self.sequences_client.get_tracefiles()
        self.assertIsInstance(tracefiles, list, "SequencesClient.get_tracefiles() should return a list of Tracefile.")
        for tracefile in tracefiles:
            self.assertIsInstance(tracefile, pybold.tracefile.Tracefile, "SequencesClient.get_tracefiles() should return a list of Tracefile.")
    
    
    def _test_get(self,taxon=None, ids=None, bins=None, containers=None, institutions=None, researchers=None, geo=None, marker=None, timeout=5):
        sequence_list = self.sequences_client.get(taxon=taxon, 
                                                 ids=ids, 
                                                 bins=bins, 
                                                 containers=containers, 
                                                 institutions=institutions, 
                                                 researchers=researchers, 
                                                 geo=geo,
                                                 marker=marker,
                                                 timeout=timeout)
        msg = 'SequencesClient.get() should return a list of Sequence objects'
        self.assertIsNotNone(sequence_list, msg)
        self.assertIsInstance(sequence_list, list, msg )
        self.assertIsInstance(sequence_list[0], pybold.sequence.Sequence, msg)
        self.assertListEqual(sequence_list, self.sequences_client.sequence_list, 'SequencesClient.get() and SequencesClient.sequence_list should be equal')
        return sequence_list

    def test_get_by_processids(self):
        sequence_list = self._test_get(ids='|'.join(self.process_ids))
        for sequence in sequence_list:
            self.assertIn(sequence.process_id, self.process_ids, 'Returned Sequence process_id ({}) was not part of original search criteria'.format(sequence.process_id))

    def test_get_by_taxon_and_marker(self):
        sequence_list = self._test_get(taxon='|'.join(self.taxons), marker='|'.join(self.markers))
        for sequence in sequence_list:
            found = False
            for marker in self.markers:
                if marker in sequence.marker:
                    found = True
            self.assertTrue(found, "Returned Sequence was not part of original search criteria for markers {}.".format(', '.join(self.markers)))
            
        #TODO validate taxons
    
    #TODO validate taxonomy
    
    #TODO validate institutions, geography, etc

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()