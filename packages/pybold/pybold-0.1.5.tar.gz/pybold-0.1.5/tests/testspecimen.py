'''
:author: Iyad Kandalaft <iyad.kandalaft@canada.ca>
:organization: Agriculture and Agri-Foods Canada
:group: Microbial Biodiversity Bioinformatics
:contact: mbb@agr.gc.ca 
:license: LGPL v3
'''

from lxml import objectify
import os.path
import unittest

import pybold.sequence
import pybold.specimen
import pybold.tracefile
from tests import TESTDATA


class SpecimenTest(unittest.TestCase):
    def setUp(self):
        with open(TESTDATA['specimen'], 'r') as f:
            specimen_data = f.read()
            
        bold_specimens = objectify.fromstring(specimen_data)
        
        if not hasattr(bold_specimens, "record"):
            raise AttributeError("BOLD specimen test data ({}) should have one or more records.".format(TESTDATA['specimen']))
        
        self.specimen = pybold.specimen.Specimen(bold_specimens.record[0])

    def tearDown(self):
        del self.specimen
        
    def _has_attribute(self, attr_name):
        self.assertTrue(hasattr(self.specimen, attr_name), "Specimen should have the {} attribute.".format(attr_name))
        
    def test_has_record(self):
        self._has_attribute("record")
    
    def test_is_instance(self):
        self.assertIsInstance(self.specimen, pybold.specimen.Specimen, "self.specimen failed to instantiate as a Specimen.")
        
    def test_taxonomy(self):
        self._has_attribute("taxonomy")

        taxa = self.specimen.taxonomy
        self.assertIsInstance(taxa, dict, 'Specimen.taxonomy should return a dictionary.')
        for rank in ('phylum', 'class', 'order', 'family', 'subfamily', 'genus', 'species'):
            self.assertIn(rank, taxa.keys(), "Rank {} is not present in the Specimen.taxonomy dictionary.".format(rank))
             
        msg = "Loaded taxonomy doesn't match content of test data {}".format(TESTDATA['specimen'])
        self.assertEqual(taxa['phylum'], "Arthropoda", msg)
        self.assertEqual(taxa['class'], "Insecta", msg)
        self.assertEqual(taxa['order'], "Lepidoptera", msg)
        self.assertEqual(taxa['family'], '', msg)
        self.assertEqual(taxa['subfamily'], '', msg)
        self.assertEqual(taxa['genus'], '', msg)
        self.assertEqual(taxa['species'], '', msg)
    
    def test_record_id(self):
        self._has_attribute("record_id")
        self.assertEqual(self.specimen.record_id, 2376157, "Specimen.record_id {} should be 2376157".format(self.specimen.record_id))
    
    def test_process_id(self):
        self._has_attribute("process_id")
        self.assertIsInstance(self.specimen.process_id, basestring, "Specimen.process_id")
        exp_process_id = "ACRJP618-11"
        self.assertEqual(self.specimen.process_id, exp_process_id, "Specimen.process_id {} does not match content of test data {}".format(self.specimen.process_id, exp_process_id))
        
    def test_geography(self):
        self._has_attribute("geography")
        msg = "Specimen.geography should return an object with Country, Province, Region, Coordinates attributes."
        geo = self.specimen.geography
        for attribute in ("country", "province", "region", "coordinates"):
            self.assertTrue(hasattr(geo, attribute), msg)
                    
    def test_sequence(self):
        self._has_attribute("sequence")
        self.assertIsInstance(self.specimen.sequence, pybold.sequence.Sequence, "Specimen.sequence should return a Sequence object.")
        self.assertEqual(self.specimen.process_id, self.specimen.sequence.process_id, "Specimen.process_id should match its Sequence.process_id.")
    
    def test_tracefiles(self):
        self._has_attribute("tracefiles")
        self.assertIsInstance(self.specimen.tracefiles, list, "Specimen.tracefiles should return a list of Tracefile objects.")
        for tracefile in self.specimen.tracefiles:
            self.assertIsInstance(tracefile, pybold.tracefile.Tracefile, "Specimen.tracefiles should return a list of Tracefile objects.")
        
class SpecimensClientTest(unittest.TestCase):
    def setUp(self):
        # Search criteria to be used and validated against
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

        # Instantiate the SpecimensClient class to be used throughout all tests
        self.specimen_client = pybold.specimen.SpecimensClient()

    def tearDown(self):
        self.process_ids = None
        self.record_ids = None
        self.taxons = None
        self.bins = None
        self.institutions = None
        self.researchers = None
        self.specimen_client = None


    def test_isinstance(self):
        self.assertIsInstance(self.specimen_client, pybold.specimen.SpecimensClient, 'specimen_client failed to instantiate as a SpecimensClient object.')
        
    def test_specimen_list_attribute(self):
        self.assertTrue(hasattr(self.specimen_client, 'specimen_list'), 'SpecimensClient does not have a specimen_list attribute')
        self.assertIsInstance(self.specimen_client.specimen_list, list, 'SpecimensClient.specimen_list must be of a list')
       
    def _test_get(self,taxon=None, ids=None, bins=None, containers=None, institutions=None, researchers=None, geo=None, timeout=5):
        specimen_list = self.specimen_client.get(taxon=taxon, 
                                                 ids=ids, 
                                                 bins=bins, 
                                                 containers=containers, 
                                                 institutions=institutions, 
                                                 researchers=researchers, 
                                                 geo=geo,
                                                 timeout=timeout)
        msg = 'SpecimensClient.get() should return a list of Specimen objects'
        self.assertIsNotNone(specimen_list, msg)
        self.assertIsInstance(specimen_list, list, msg )
        self.assertIsInstance(specimen_list[0], pybold.specimen.Specimen, msg)
        self.assertListEqual(specimen_list, self.specimen_client.specimen_list, 'SpecimensClient.get() and SpecimensClient.specimen_list should be equal')
        return specimen_list

    def test_get_by_processids(self):
        specimen_list = self._test_get(ids='|'.join(self.process_ids))
        for specimen in specimen_list:
            self.assertIn(specimen.process_id, self.process_ids, 'Returned Specimen was not part of original search criteria')
    
    def test_get_by_taxon_and_geo(self):
        specimen_list = self._test_get(taxon='|'.join(self.taxons), geo='|'.join(self.geographies))
        for specimen in specimen_list:
            found = False
            specimen_taxonomy = ' '.join(specimen.taxonomy.values())
            for taxon in self.taxons:
                if taxon in specimen_taxonomy:
                    found = True
                    break
            
            self.assertTrue(found, 'Specimen {} does not match the taxon search critera.'.format(specimen.process_id))
            
            found = False
            specimen_geography = [ specimen.geography.country, specimen.geography.province, specimen.geography.region ]
            for geo in self.geographies:
                if geo in specimen_geography:
                    found = True
                    break
            
            self.assertTrue(found, 'Specimen {} does not match the geography search criteria.'.format(specimen.process_id))
    
    def test_get_by_institution_and_researcher(self):
        specimen_list = self._test_get(institutions='|'.join(self.institutions), researchers='|'.join(self.researchers), timeout=10)
        for specimen in specimen_list:
            found = False
            
            specimen_researchers = []
            if hasattr(specimen.record.taxonomy, "identification_provided_by"): 
                specimen_researchers.append(str(specimen.record.taxonomy.identification_provided_by))
            if hasattr(specimen.record.collection_event, "collectors"):
                specimen_researchers.append(str(specimen.record.collection_event.collectors))
            
            specimen_researchers = ' '.join(specimen_researchers).upper()
            for researcher in self.researchers:
                if researcher.upper() in specimen_researchers:
                    found = True
                    break
            
            self.assertTrue(found, 'Specimen {} does not match the researcher search critera.'.format(specimen.process_id))
            
            found = False
            specimen_institution = str(specimen.record.specimen_identifiers.institution_storing).upper()
            for institution in self.institutions:
                if institution.upper() in specimen_institution:
                    found = True
                    break
            
            self.assertTrue(found, 'Specimen {} does not match the institution search criteria.'.format(specimen.process_id))
    
    def test_get_taxonomies(self):
        self.specimen_client.get(ids='|'.join(self.process_ids))
        specimen_taxonomies = self.specimen_client.get_taxonomies()

        self.assertIsInstance(specimen_taxonomies, dict, "SpecimensClient.get_taxonomies() should return a dictionary with process ID keys and taxonomy dictionary values.")
        for process_id, taxonomy in specimen_taxonomies.iteritems(): 
            self.assertIn(process_id, self.process_ids, "Process ID {} was not in the dictionary returned by SpecimensClient.get_taxonomies().".format(process_id))
            self.assertIsInstance(taxonomy, dict, "The dictionary's values returned by SpecimensClient.get_taxonomies() are not dictionaries.")        
                 
    def test_get_record_ids(self):
        self.specimen_client.get(ids='|'.join(self.process_ids))
        record_ids = self.specimen_client.get_record_ids()
        self.assertIsInstance(record_ids, list, "SpecimensClient.get_record_ids() should return a list of record ids.")
    
    def test_get_process_ids(self):
        self.specimen_client.get(ids='|'.join(self.process_ids))
        process_ids = self.specimen_client.get_process_ids()
        self.assertIsInstance(process_ids, list, "SpecimensClient.get_process_ids() should return a list of process ids.")
        for process_id in process_ids:
            self.assertIn(process_id, self.process_ids, "Returned specimen process_id ({}) was not part of original search criteria".format(process_id))
    
    def test_sequences(self):
        self.specimen_client.get(ids='|'.join(self.process_ids))
        sequences = self.specimen_client.get_sequences()
        self.assertIsInstance(sequences, list, "SpecimensClient.get_sequences() should return a list of Sequence.")
        for sequence in sequences:
            self.assertIsInstance(sequence, pybold.sequence.Sequence, "SpecimensClient.get_sequences() should return a list of Sequence.")
        
    def test_get_tracefiles(self):
        self.specimen_client.get(ids='|'.join(self.process_ids))
        tracefiles = self.specimen_client.get_tracefiles()
        self.assertIsInstance(tracefiles, list, "SpecimensClient.get_tracefiles() should return a list of Tracefile.")
        for tracefile in tracefiles:
            self.assertIsInstance(tracefile, pybold.tracefile.Tracefile, "SpecimensClient.get_tracefiles() should return a list of Tracefile.")

suite = unittest.TestLoader().loadTestsFromTestCase(SpecimensClientTest)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()