# Embedded file name: scripts/client/notification/NotificationMVC.py
from notification.AlertController import AlertController
from notification.LayoutController import LayoutController
from notification.NotificationsModel import NotificationsModel
from notification.actions_handlers import NotificationsActionsHandlers

class _NotificationMVC:

    def __init__(self):
        self.__model = None
        self.__alertsController = None
        self.__layoutController = None
        self.__actionsHandlers = None
        return

    def initialize(self):
        self.__model = NotificationsModel()
        self.__actionsHandlers = NotificationsActionsHandlers()
        self.__alertsController = AlertController(self.__model)
        self.__layoutController = LayoutController(self.__model)

    def getModel(self):
        return self.__model

    def getAlertController(self):
        return self.__alertsController

    def handleAction(self, typeID, entityID, action):
        self.__actionsHandlers.handleAction(self.__model, int(typeID), long(entityID), action)

    def cleanUp(self):
        self.__alertsController.cleanUp()
        self.__layoutController.cleanUp()
        self.__actionsHandlers.cleanUp()
        self.__model.cleanUp()
        self.__alertsController = None
        self.__layoutController = None
        self.__actionsHandlers = None
        self.__model = None
        return


g_instance = _NotificationMVC()
