# coding=utf-8
import json
import unittest

from jsonpickle.pickler import Pickler

from wshubsapi.ClientInHub import ClientInHub
from wshubsapi.CommEnvironment import CommEnvironment
from wshubsapi.ConnectedClient import ConnectedClient
from wshubsapi.ConnectedClientsHolder import ConnectedClientsHolder
from wshubsapi.Hub import Hub
from wshubsapi.HubsInspector import HubsInspector
from wshubsapi.Test.utils.HubsUtils import removeHubsSubclasses
from wshubsapi.Test.utils.MessageCreator import MessageCreator
from flexmock import flexmock


class TestConnectedClient(unittest.TestCase):
    def setUp(self):
        class TestHub(Hub):
            def __init__(self):
                super(TestHub, self).__init__()
                self.testFunctionReplayArg = lambda x: x
                self.testFunctionReplayNone = lambda: None

            def testFunctionError(self):
                raise Exception("Error")

        class ClientMock:
            def __init__(self):
                self.writeMessage = flexmock()
                self.close = flexmock()
                pass

        HubsInspector.inspectImplementedHubs(forceReconstruction=True)
        self.testHubClass = TestHub
        self.testHubInstance = HubsInspector.getHubInstance(self.testHubClass)

        self.jsonPickler = Pickler(max_depth=3, max_iter=30, make_refs=False)
        self.commEnvironment = CommEnvironment(maxWorkers=0, unprovidedIdTemplate="unprovidedTest__{}")
        self.clientMock = ClientMock()
        self.connectedClient = ConnectedClient(self.commEnvironment, self.clientMock.writeMessage)
        self.connectedClientsHolder = ConnectedClientsHolder(self.testHubClass.__HubName__)

    def tearDown(self):
        self.connectedClientsHolder.allConnectedClientsDict.clear()
        del self.testHubClass
        del self.testHubInstance
        removeHubsSubclasses()

    def test_onOpen_appendsClientInConnectedClientsHolderWithDefinedID(self):
        ID = 3

        self.commEnvironment.onOpen(self.connectedClient, ID)

        self.assertIsInstance(self.connectedClientsHolder.getClient(ID), ClientInHub)

    def test_onOpen_appendsUndefinedIdIfNoIDIsDefine(self):
        self.commEnvironment.onOpen(self.connectedClient)

        self.assertIsInstance(self.connectedClientsHolder.getClient("unprovidedTest__0"), ClientInHub)

    def test_onOpen_appendsUndefinedIdIfOpenAlreadyExistingClientId(self):
        self.commEnvironment.onOpen(self.connectedClient, 3)
        secondId = self.commEnvironment.onOpen(self.connectedClient, 3)

        self.assertEqual(secondId, "unprovidedTest__0")
        self.assertIsInstance(self.connectedClientsHolder.getClient(3), ClientInHub)
        self.assertIsInstance(self.connectedClientsHolder.getClient(secondId), ClientInHub)

    def __setUp_onMessage(self, functionStr, args, replay, success=True):
        message = MessageCreator.createOnMessageMessage(hub=self.testHubClass.__HubName__,
                                                        function=functionStr,
                                                        args=args)
        replayMessage = MessageCreator.createReplayMessage(hub=self.testHubClass.__HubName__,
                                                           function=functionStr,
                                                           replay=replay,
                                                           success=success)
        messageStr = json.dumps(message)
        self.commEnvironment = flexmock(self.commEnvironment)

        return messageStr, replayMessage

    def test_onMessage_callsReplayIfSuccess(self):
        messageStr, replayMessage = self.__setUp_onMessage("testFunctionReplayArg", [1], 1)
        self.commEnvironment.should_receive("replay").with_args(self.connectedClient, replayMessage, messageStr).once()

        self.commEnvironment.onMessage(self.connectedClient, messageStr)

    def test_onMessage_callsOnErrorIfError(self):
        messageStr, replayMessage = self.__setUp_onMessage("testFunctionError", [], dict, success=False)
        self.commEnvironment.should_receive("replay").with_args(self.connectedClient, dict, messageStr).once()

        self.commEnvironment.onMessage(self.connectedClient, messageStr)

    def test_onMessage_notCallsReplayIfFunctionReturnNone(self):
        messageStr, replayMessage = self.__setUp_onMessage("testFunctionReplayNone", [], None)
        self.commEnvironment.should_receive("replay").never()

        self.commEnvironment.onMessage(self.connectedClient, messageStr)

    def test_onMessage_onErrorIsCalledIfMessageCanNotBeParsed(self):
        messageStr, replayMessage = self.__setUp_onMessage("testFunctionReplayNone", [], None)
        self.commEnvironment.should_receive("replay").never()
        self.commEnvironment.should_receive("onError").once()

        self.commEnvironment.onMessage(self.connectedClient, messageStr + "breaking message")

    def test_onAsyncMessage_putsTheMessageAndTheConnectionInTheQueue(self):
        message = MessageCreator.createOnMessageMessage()
        self.commEnvironment.wsMessageReceivedQueue = flexmock(self.commEnvironment.wsMessageReceivedQueue)
        self.commEnvironment.wsMessageReceivedQueue.should_receive("put").with_args((message, self.connectedClient)).once()

        self.commEnvironment.onAsyncMessage(self.connectedClient, message)

    def test_onClose_removeExistingConnectedClient(self):
        ID = 3
        self.commEnvironment.onOpen(self.connectedClient, ID)

        self.commEnvironment.onClosed(self.connectedClient)

        self.assertRaises(KeyError, self.connectedClientsHolder.getClient, ID)
        self.assertEqual(len(self.connectedClientsHolder.allConnectedClientsDict), 0)

    def test_replay_writeMessageWithAString(self):
        replayMessage = MessageCreator.createReplayMessage()
        self.connectedClient = flexmock(self.connectedClient)
        self.connectedClient.should_receive("api_writeMessage").with_args(str).once()

        self.commEnvironment.replay(self.connectedClient, replayMessage, "test")
