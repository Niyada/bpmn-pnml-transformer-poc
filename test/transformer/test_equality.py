import os
import sys
import unittest

from transformer.bpmn.bpmn import BPMN
from transformer.equality.bpmn import get_all_processes_by_id
from transformer.equality.petrinet import get_all_nets_by_id
from transformer.pnml.pnml import Pnml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestSubelements(unittest.TestCase):

    def test_pnml_eqaulity_subprocess(self):
        pnml = Pnml.from_file("tests/multiplesubprocesses.pnml")
        subnets = {}
        get_all_nets_by_id(pnml.net, subnets)
        self.assertEqual(len(subnets), 7)

    def test_bpmn_eqaulity_subprocess(self):
        bpmn = BPMN.from_file("tests/multiplesubprocesses.bpmn")
        subnets = {}
        get_all_processes_by_id(bpmn.process, subnets)
        self.assertEqual(len(subnets), 5)