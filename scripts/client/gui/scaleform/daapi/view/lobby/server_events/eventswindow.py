# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/server_events/EventsWindow.py
from account_helpers.settings_core.SettingsCore import g_settingsCore
from account_helpers.settings_core.settings_constants import TUTORIAL
import constants
from debug_utils import LOG_WARNING
from gui.Scaleform.daapi.view.lobby.server_events import events_helpers
from gui.server_events import g_eventsCache, settings as quest_settings, caches, isPotapovQuestEnabled
from gui.Scaleform.daapi.view.meta.QuestsWindowMeta import QuestsWindowMeta
from gui.Scaleform.genConsts.QUESTS_ALIASES import QUESTS_ALIASES as _QA
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.shared.ItemsCache import g_itemsCache

class EventsWindow(QuestsWindowMeta):

    def __init__(self, ctx = None):
        super(EventsWindow, self).__init__()
        self._navInfo = caches.getNavInfo()
        self._updateNavInfo(ctx.get('eventType'), ctx.get('eventID'))

    def onWindowClose(self):
        caches.clearVehiclesData()
        self.destroy()

    def navigate(self, eventType = None, eventID = None):
        if self._updateNavInfo(eventType, eventID):
            tabID = self._selectLastTab()
            self.onTabSelected(tabID)

    def onTabSelected(self, tabID):
        if tabID == _QA.TAB_PERSONAL_QUESTS:
            if quest_settings.isNeedToShowPQIntro(g_eventsCache.potapov):
                return self._showWelcomeView()
            if self._navInfo.potapov.tileID is not None:
                self._showTileChainsView(self._navInfo.potapov.tileID, self._navInfo.potapov.questID)
            else:
                self._showSeasonsView()
        elif tabID == _QA.TAB_COMMON_QUESTS:
            self._showCommonQuestsView(self._navInfo.common.questID)
        elif tabID == _QA.TAB_LADDER_QUESTS:
            self._showLadderQuestsView(self._navInfo.common.questID)
        elif tabID == _QA.TAB_BEGINNER_QUESTS:
            self._showBeginnerQuestsView(self._navInfo.tutorial.questID)
        else:
            LOG_WARNING('Unknown personal quests tab id', tabID)
        return

    def _populate(self):
        super(EventsWindow, self)._populate()
        self.__initWindow()
        self._selectLastTab()

    def __initWindow(self):
        tabs = []
        if isPotapovQuestEnabled():
            tabs.append(self.__packTabDataItem(QUESTS.QUESTS_TABS_PERSONAL, _QA.TAB_PERSONAL_QUESTS))
        tabs.append(self.__packTabDataItem(QUESTS.QUESTS_TABS_CURRENT, _QA.TAB_COMMON_QUESTS))
        if g_eventsCache.getQuests(lambda x: x.getType() == constants.EVENT_TYPE.CLUBS_QUEST):
            tabs.append(self.__packTabDataItem(QUESTS.QUESTS_TABS_LADDER, _QA.TAB_LADDER_QUESTS))
        if g_settingsCore.serverSettings.getTutorialSetting(TUTORIAL.WAS_QUESTS_TUTORIAL_STARTED):
            tabs.append(self.__packTabDataItem(QUESTS.QUESTS_TABS_BEGINNER, _QA.TAB_BEGINNER_QUESTS))
        self.as_initS({'tabs': tabs})

    def __packTabDataItem(self, label, id):
        return {'label': label,
         'id': id}

    def _selectLastTab(self):
        tabID = self._navInfo.tabID
        if not tabID:
            tabID = _QA.TAB_PERSONAL_QUESTS if isPotapovQuestEnabled() else _QA.TAB_COMMON_QUESTS
        self.as_selectTabS(tabID)
        return tabID

    def _updateNavInfo(self, eventType = None, eventID = None):
        if eventType is not None and eventID is not None:
            if eventType == constants.EVENT_TYPE.POTAPOV_QUEST:
                pQuest = g_eventsCache.potapov.getQuests()[int(eventID)]
                self._navInfo.selectPotapovQuest(pQuest.getTileID(), pQuest.getID())
            elif eventType == constants.EVENT_TYPE.TUTORIAL:
                self._navInfo.selectTutorialQuest(eventID)
            else:
                self._navInfo.selectCommonQuest(eventID)
            return True
        else:
            if g_settingsCore.serverSettings.getTutorialSetting(TUTORIAL.WAS_QUESTS_TUTORIAL_STARTED):
                tutorialQuestsDescriptor = events_helpers.getTutorialEventsDescriptor()
                if tutorialQuestsDescriptor is not None:
                    completed = g_itemsCache.items.stats.tutorialsCompleted
                    if not tutorialQuestsDescriptor.areAllBonusesReceived(completed):
                        self._navInfo.selectTutorialQuest('')
                        return True
            return False

    def _onRegisterFlashComponent(self, viewPy, alias):
        if alias in (_QA.PERSONAL_WELCOME_VIEW_ALIAS, _QA.TILE_CHAINS_VIEW_ALIAS, _QA.SEASONS_VIEW_ALIAS):
            viewPy._setMainView(self)
        self.as_hideWaitingS()

    def _showWelcomeView(self):
        self._navInfo.selectTab(_QA.TAB_PERSONAL_QUESTS)
        return self._loadView(_QA.PERSONAL_WELCOME_VIEW_LINKAGE, _QA.PERSONAL_WELCOME_VIEW_ALIAS)

    def _showSeasonsView(self, doResetNavInfo = False):
        self._navInfo.selectTab(_QA.TAB_PERSONAL_QUESTS, doResetNavInfo)
        return self._loadView(_QA.SEASONS_VIEW_LINKAGE, _QA.SEASONS_VIEW_ALIAS)

    def _showTileChainsView(self, tileID, questID = None):
        self._navInfo.selectPotapovQuest(tileID, questID)
        quest_settings.markPQTileAsVisited(tileID)
        return self._loadView(_QA.TILE_CHAINS_VIEW_LINKAGE, _QA.TILE_CHAINS_VIEW_ALIAS)

    def _showCommonQuestsView(self, questID = None):
        self._navInfo.selectCommonQuest(questID)
        return self._loadView(_QA.COMMON_QUESTS_VIEW_LINKAGE, _QA.COMMON_QUESTS_VIEW_ALIAS)

    def _showLadderQuestsView(self, questID = None):
        self._navInfo.selectCommonQuest(questID)
        return self._loadView(_QA.COMMON_QUESTS_VIEW_LINKAGE, _QA.LADDER_QUESTS_VIEW_ALIAS)

    def _showBeginnerQuestsView(self, questID = None):
        self._navInfo.selectTutorialQuest(questID)
        return self._loadView(_QA.BEGINNER_QUESTS_VIEW_LINKAGE, _QA.BEGINNER_QUESTS_VIEW_ALIAS)

    def _loadView(self, linkage, alias):
        self.as_showWaitingS('', {})
        self.as_loadViewS(linkage, alias)
