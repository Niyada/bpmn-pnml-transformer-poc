"""e2e test cases for testing the transform endpoint of the application."""

import requests
import unittest
from xml.dom import minidom
import os

class TestE2EPostTransform(unittest.TestCase):
    """A e2e test class for testing the transform endpoint of the application."""

    REQUEST_TIMEOUT = 50

    def __normalize_xml(self, xml_string: str) -> str:
        def sort_children(node):
            child_nodes = [child for child in node.childNodes
                            if child.nodeType == node.ELEMENT_NODE]
            for child in child_nodes:
                sort_children(child)
            sorted_children = sorted(child_nodes, 
                                     key=lambda x: (x.tagName, x.getAttribute('id')))
            for child in sorted_children:
                node.appendChild(node.removeChild(child))

        dom = minidom.parseString(xml_string)
        sort_children(dom.documentElement)
        result = dom.toxml().replace("\n", "").replace("\t", "").replace("\r", "")
        return result

    def setUp(self):
        """Performs setup before each test case."""
        self.url = os.getenv("E2E_URL")
        self.maxDiff = None
        if self.url is None:
            raise ValueError("E2E_URL environment variable not set.")
        self.token = os.getenv("E2E_IDENTITY_TOKEN")
        if self.token is None:
            raise ValueError("E2E_IDENTITY_TOKEN environment variable not set.")
        self.shared_haeaders = {
            "Authorization": f"Bearer {self.token}"
        }
        #self.maxDiff = None
        #self.url = "https://europe-west3-woped-422510.cloudfunctions.net/transform"

    def test_pnml_to_bpmn(self):
        """Tests the status code of the transform endpoint."""
        PAYLOAD_PNML_FILE_PATH =\
            'src/transform/tests/assets/diagrams/pnml/e2e_payload.xml'
        with open( PAYLOAD_PNML_FILE_PATH, encoding='utf-8') as file:
            payload_content = file.read()

        EXPECTED_BPMN_FILE_PATH =\
            'src/transform/tests/assets/diagrams/bpmn/e2e_expected_response.xml'
        with open( EXPECTED_BPMN_FILE_PATH, encoding='utf-8') as file:
            expected_response = file.read()

        payload = {"pnml": payload_content}

        response = requests.post(
            f'{self.url}?direction=pnmltobpmn', 
            data = payload,
            timeout=self.REQUEST_TIMEOUT,
            headers=self.shared_haeaders,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        normalized_expected_xml = self.__normalize_xml( expected_response       )
        normalized_actual_xml   = self.__normalize_xml( response.json()["bpmn"] )

        self.assertEqual( normalized_expected_xml, normalized_actual_xml )

    def test_bpmn_to_pnml(self):
        """Tests the status code of the transform endpoint."""
        PAYLOAD_BPMN_FILE_PATH =\
            'src/transform/tests/assets/diagrams/bpmn/e2e_payload.xml'
        with open( PAYLOAD_BPMN_FILE_PATH, encoding='utf-8') as file:
            payload_content = file.read()
        
        EXPECTED_PNML_FILE_PATH =\
            'src/transform/tests/assets/diagrams/pnml/e2e_expected_response.xml'
        with open( EXPECTED_PNML_FILE_PATH, encoding='utf-8') as file:
            expected_response = file.read()

        payload = {"bpmn": payload_content}

        response = requests.post(
            f'{self.url}?direction=bpmntopnml', 
            data = payload,
            timeout=self.REQUEST_TIMEOUT,
            headers=self.shared_haeaders,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        normalized_expected_xml = self.__normalize_xml( expected_response       )
        normalized_actual_xml   = self.__normalize_xml( response.json()["pnml"] )

        self.assertEqual( normalized_expected_xml, normalized_actual_xml )