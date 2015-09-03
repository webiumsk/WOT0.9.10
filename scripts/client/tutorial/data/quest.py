# Embedded file name: scripts/client/tutorial/data/quest.py
from tutorial.data.has_id import HasID
from tutorial.data.chapter import Chapter

class QuestChapter(Chapter):

    def __init__(self, questConditions, image, unlockChapter, progressCondition, sharedTriggers, sharedEntities, sharedVars, isHidden, entityID, title, descriptions, bonus, forcedLoading, filePaths, sharedScene, predefinedVars):
        super(QuestChapter, self).__init__(entityID, title, descriptions, bonus, forcedLoading, filePaths, sharedScene, predefinedVars)
        self.__image = image
        self.__progressCondition = progressCondition
        self.__unlockChapter = unlockChapter
        self.__questConditions = questConditions
        self.__sharedTriggersPath = sharedTriggers
        self.__sharedEntitiesPath = sharedEntities
        self.__sharedVarsPath = sharedVars
        self.__isHidden = isHidden

    def getQuestConditions(self):
        return self.__questConditions

    def getSharedTriggersPath(self):
        return self.__sharedTriggersPath

    def getSharedEntitiesPath(self):
        return self.__sharedEntitiesPath

    def getSharedVarsPath(self):
        return self.__sharedVarsPath

    def getImage(self):
        return self.__image

    def getUnlockChapter(self):
        return self.__unlockChapter

    def getProgressCondition(self):
        return self.__progressCondition

    def isHidden(self):
        return self.__isHidden


class ProgressCondition(HasID):

    def __init__(self, entityID, values):
        super(ProgressCondition, self).__init__(entityID=entityID)
        self.__values = values

    def getValues(self):
        return self.__values
