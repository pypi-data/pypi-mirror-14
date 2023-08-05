import unittest
from solr_instance import SolrInstance
import time
import os
from solrcloudpy import SolrConnection, SolrCollection

solrprocess = None


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.conn = SolrConnection()

    def test_list(self):
        colls = self.conn.list()
        self.assertTrue(len(colls) >= 1)

    def test_live_nodes(self):
        nodes = self.conn.live_nodes
        # to support easy use of solrcloud gettingstarted
        self.assertTrue(len(nodes) >= 1)

    def test_cluster_leader(self):
        leader = self.conn.cluster_leader
        self.assertTrue(leader is not None)

    def test_create_collection(self):
        coll = self.conn.create_collection('test2')
        self.assertTrue(isinstance(coll, SolrCollection))
        self.conn.test2.drop()


def setUpModule():
    if os.getenv('SKIP_STARTUP', False):
        return
    # start solr
    solrprocess = SolrInstance("solr2")
    solrprocess.start()
    solrprocess.wait_ready()
    time.sleep(1)


def tearDownModule():
    if os.getenv('SKIP_STARTUP', False):
        return
    if solrprocess:
        solrprocess.terminate()


if __name__ == '__main__':
    unittest.main()
