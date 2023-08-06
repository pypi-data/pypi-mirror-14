import os
import shutil
import unittest
from os import listdir
from wshubsapi.ClientFileGenerator.JAVAFileGenerator import JAVAFileGenerator
from wshubsapi.ClientFileGenerator.JSClientFileGenerator import JSClientFileGenerator
from wshubsapi.ClientFileGenerator.PythonClientFileGenerator import PythonClientFileGenerator
from wshubsapi.Hub import Hub
from wshubsapi.Hub import HubException
from wshubsapi.HubsInspector import HubsInspector
from wshubsapi.HubsInspector import HubsInspectorException
from wshubsapi.Test.utils.HubsUtils import removeHubsSubclasses


class TestHubDetection(unittest.TestCase):
    def setUp(self):
        # Building hubs for testing
        class TestHub(Hub):
            def getData(self):
                pass

        class TestHub2(Hub):
            pass

        self.testHubClass = TestHub
        self.testHub2Class = TestHub2
        HubsInspector.inspectImplementedHubs(forceReconstruction=True)

    def tearDown(self):
        del self.testHubClass
        del self.testHub2Class
        removeHubsSubclasses()

    def test_hubsInspection(self):
        self.assertEqual(len(HubsInspector.HUBs_DICT), 3, 'Detects all Hubs')
        self.assertTrue(issubclass(HubsInspector.HUBs_DICT['TestHub'].__class__, Hub), 'Hubs subclass is class')
        self.assertTrue(issubclass(HubsInspector.HUBs_DICT['TestHub2'].__class__, Hub), 'Hubs subclass is class')
        self.assertTrue(getattr(HubsInspector.HUBs_DICT['TestHub'], "getData"), 'Detects function')

    def test_hubsLimitations(self):
        class TestHubLimitation(Hub):
            pass

        class TestHubLimitation2(Hub):
            __HubName__ = "TestHubLimitation"

        self.assertRaises(HubException, HubsInspector.inspectImplementedHubs, forceReconstruction=True)
        TestHubLimitation2.__HubName__ = "TestHubLimitation2"

        class TestHubLimitation3(Hub):
            def __init__(self, aux):
                super(TestHubLimitation3, self).__init__()

        self.assertRaises(HubsInspectorException, HubsInspector.inspectImplementedHubs, forceReconstruction=True)
        TestHubLimitation3.__init__ = lambda: 1 + 1

    def test_hubsLimitations_startWithUnderscores(self):
        class __TestHubLimitation(Hub):
            pass

        self.assertRaises(HubException, HubsInspector.inspectImplementedHubs, forceReconstruction=True)

    def test_hubsLimitations_wsClient(self):
        class wsClient(Hub):
            pass

        self.assertRaises(HubException, HubsInspector.inspectImplementedHubs, forceReconstruction=True)

    def test_getHubInstance_returnsAnInstanceOfHubIfExists(self):
        self.assertIsInstance(HubsInspector.getHubInstance(self.testHubClass), Hub)

    def test_getHubInstance_RaisesErrorIfNotAHub(self):
        self.assertRaises(AttributeError, HubsInspector.getHubInstance, (str,))

    def test_getHubsInformation_ReturnsDictionaryWithNoClientFunctions(self):
        infoReport = HubsInspector.getHubsInformation()

        self.assertIn("TestHub2", infoReport)
        self.assertIn("getData", infoReport["TestHub"]["serverMethods"])

    def test_getHubsInformation_ReturnsDictionaryWithClientFunctions(self):
        class TestHubWithClient(Hub):
            def getData(self):
                pass

            def _defineClientFunctions(self):
                self.clientFunctions = dict(client1=lambda x, y: None,
                                            client2=lambda x, y=1: None,
                                            client3=lambda x=0, y=1: None)

        HubsInspector.inspectImplementedHubs(forceReconstruction=True)

        infoReport = HubsInspector.getHubsInformation()

        self.assertIn("TestHubWithClient", infoReport)
        client1Method = infoReport["TestHubWithClient"]["clientMethods"]["client1"]
        client2Method = infoReport["TestHubWithClient"]["clientMethods"]["client2"]
        client3Method = infoReport["TestHubWithClient"]["clientMethods"]["client3"]
        self.assertEqual(client1Method["args"], ["x", "y"])
        self.assertEqual(client2Method["defaults"], [1])
        self.assertEqual(client3Method["defaults"], [0, 1])


class TestClientFileConstructor(unittest.TestCase):
    def setUp(self):
        class TestHub(Hub):
            def getData(self):
                pass

        class TestHub2(Hub):
            def getData(self):
                pass

        HubsInspector.inspectImplementedHubs(forceReconstruction=True)

    def tearDown(self):
        removeHubsSubclasses()

        try:
            otherPath = "onTest"
            os.removedirs(otherPath)
        except:
            pass
        try:
            fullPath = os.path.join(otherPath, JSClientFileGenerator.FILE_NAME)
            os.remove(fullPath)
        except:
            pass
        try:
            fullPath = os.path.join(otherPath, PythonClientFileGenerator.FILE_NAME)
            packageFilePath = os.path.join(otherPath, "__init__.py")
            os.remove(fullPath)
            os.remove(packageFilePath)
            os.removedirs("onTest")
        except:
            pass

    def test_JSCreation(self):
        HubsInspector.constructJSFile()

        self.assertTrue(os.path.exists(JSClientFileGenerator.FILE_NAME))
        os.remove(JSClientFileGenerator.FILE_NAME)

        otherPath = "onTest"
        fullPath = os.path.join(otherPath, JSClientFileGenerator.FILE_NAME)
        HubsInspector.constructJSFile(otherPath)

        self.assertTrue(os.path.exists(fullPath))

    def test_JAVACreation(self):
        path = "onTest"
        try:
            HubsInspector.constructJAVAFile("test", path)
            self.assertTrue(os.path.exists(os.path.join(path, JAVAFileGenerator.SERVER_FILE_NAME)))
            self.assertTrue(os.path.exists(os.path.join(path, JAVAFileGenerator.CLIENT_PACKAGE_NAME)))
        finally:
            for f in listdir(path):
                fullPath = os.path.join(path, f)
                os.remove(fullPath) if os.path.isfile(fullPath) else shutil.rmtree(fullPath)

    def test_PythonCreation(self):
        HubsInspector.constructPythonFile()
        self.assertTrue(os.path.exists(PythonClientFileGenerator.FILE_NAME))
        self.assertTrue(os.path.exists("__init__.py"), "Check if python package is created")
        os.remove(PythonClientFileGenerator.FILE_NAME)

        otherPath = "onTest"
        fullPath = os.path.join(otherPath, PythonClientFileGenerator.FILE_NAME)
        packageFilePath = os.path.join(otherPath, "__init__.py")
        HubsInspector.constructPythonFile(otherPath)
        self.assertTrue(os.path.exists(fullPath))
        self.assertTrue(os.path.exists(packageFilePath), "Check if python package is created")
