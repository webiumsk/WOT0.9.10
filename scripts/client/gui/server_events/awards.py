# Embedded file name: scripts/client/gui/server_events/awards.py
import random
from collections import namedtuple
import BigWorld
import constants
import potapov_quests
from helpers import i18n
from shared_utils import findFirst
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION
from gui.server_events import g_eventsCache
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.daapi.view.lobby.AwardWindow import AwardAbstract, packRibbonInfo
from gui.shared.formatters import text_styles
_BG_IMG_BY_VEH_TYPE = {'lightTank': RES_ICONS.MAPS_ICONS_QUESTS_LTAWARDBACK,
 'mediumTank': RES_ICONS.MAPS_ICONS_QUESTS_MTAWARDBACK,
 'heavyTank': RES_ICONS.MAPS_ICONS_QUESTS_HTAWARDBACK,
 'AT-SPG': RES_ICONS.MAPS_ICONS_QUESTS_AT_SPGAWARDBACK,
 'SPG': RES_ICONS.MAPS_ICONS_QUESTS_SPGAWARDBACK}

def _getNextQuestInTileByID(questID):
    quests = g_eventsCache.potapov.getQuests()
    questsInTile = sorted(potapov_quests.g_cache.questListByTileIDChainID(quests[questID].getTileID(), quests[questID].getChainID()))
    try:
        questInd = questsInTile.index(questID)
        for nextID in questsInTile[questInd + 1:]:
            if quests[nextID].isAvailableToPerform():
                return nextID

        for nextID in questsInTile[:questInd + 1]:
            if quests[nextID].isAvailableToPerform():
                return nextID

    except ValueError:
        LOG_ERROR('Cannot find quest ID {questID} in quests from tile {quests}'.format(questID=questID, quests=questsInTile))
        LOG_CURRENT_EXCEPTION()

    return None


class AchievementsAward(AwardAbstract):

    def __init__(self, achieves):
        raise hasattr(achieves, '__iter__') or AssertionError
        self.__achieves = achieves

    def getWindowTitle(self):
        return i18n.makeString(MENU.AWARDWINDOW_TITLE_NEWMEDALS)

    def getBackgroundImage(self):
        return RES_ICONS.MAPS_ICONS_REFERRAL_AWARDBACK

    def getAwardImage(self):
        return RES_ICONS.MAPS_ICONS_REFERRAL_AWARD_CREDITS_GLOW

    def getHeader(self):
        return text_styles.highTitle(i18n.makeString(MENU.AWARDWINDOW_QUESTS_MEDALS_HEADER))

    def getDescription(self):
        descr = []
        for achieve in self.__achieves:
            noteInfo = achieve.getNotificationInfo()
            if len(noteInfo):
                descr.append(noteInfo)

        return text_styles.main('\n\n'.join(descr))

    def getExtraFields(self):
        result = []
        for a in self.__achieves:
            result.append({'type': a.getRecordName()[1],
             'block': a.getBlock(),
             'icon': {'big': a.getBigIcon(),
                      'small': a.getSmallIcon()}})

        return {'achievements': result}


class TokenAward(AwardAbstract):

    def __init__(self, potapovQuest, tokenID, count):
        self.__potapovQuest = potapovQuest
        self.__tokenID = tokenID
        self.__tokenCount = count

    def getWindowTitle(self):
        return i18n.makeString(MENU.AWARDWINDOW_TITLE_TOKENS)

    def getBackgroundImage(self):
        return RES_ICONS.MAPS_ICONS_REFERRAL_AWARDBACK

    def getAwardImage(self):
        return RES_ICONS.MAPS_ICONS_QUESTS_TOKEN256

    def getHeader(self):
        return text_styles.highTitle(i18n.makeString(MENU.AWARDWINDOW_QUESTS_TOKENS_HEADER, count=self.__tokenCount))

    def getDescription(self):
        return text_styles.main(i18n.makeString(MENU.AWARDWINDOW_QUESTS_TOKENS_DESCRIPTION))

    def handleBodyButton(self):
        from gui.server_events import events_dispatcher as quests_events
        nextQuestID = _getNextQuestInTileByID(int(self.__potapovQuest.getID()))
        if nextQuestID is not None:
            quests_events.showEventsWindow(nextQuestID, constants.EVENT_TYPE.POTAPOV_QUEST)
        return

    def getBodyButtonText(self):
        return i18n.makeString(MENU.AWARDWINDOW_TAKENEXTBUTTON)

    def getButtonStates(self):
        if not self.__potapovQuest.isFinal():
            return super(TokenAward, self).getButtonStates()
        else:
            nextQuestID = _getNextQuestInTileByID(int(self.__potapovQuest.getID()))
            return (False, True, nextQuestID is not None)
            return None


class VehicleAward(AwardAbstract):

    def __init__(self, vehicle):
        self.__vehicle = vehicle

    def getWindowTitle(self):
        return i18n.makeString(MENU.AWARDWINDOW_TITLE_NEWVEHICLE)

    def getBackgroundImage(self):
        return RES_ICONS.MAPS_ICONS_REFERRAL_AWARDBACK

    def getAwardImage(self):
        return self.__vehicle.iconUniqueLight

    def getHeader(self):
        return text_styles.highTitle(i18n.makeString(MENU.AWARDWINDOW_QUESTS_VEHICLE_HEADER, vehicleName=self.__vehicle.userName))

    def getDescription(self):
        return text_styles.main(i18n.makeString(MENU.AWARDWINDOW_QUESTS_VEHICLE_DESCRIPTION))


class TankwomanAward(AwardAbstract):

    def __init__(self, questID, tankmanData):
        self.__questID = questID
        self.__tankmanData = tankmanData

    def getWindowTitle(self):
        return i18n.makeString(MENU.AWARDWINDOW_TITLE_NEWTANKMAN)

    def getBackgroundImage(self):
        return RES_ICONS.MAPS_ICONS_REFERRAL_AWARDBACK

    def getAwardImage(self):
        return RES_ICONS.MAPS_ICONS_QUESTS_TANKMANFEMALEORANGE

    def getHeader(self):
        return text_styles.highTitle(i18n.makeString(MENU.AWARDWINDOW_QUESTS_TANKMANFEMALE_HEADER))

    def getDescription(self):
        return text_styles.main(i18n.makeString(MENU.AWARDWINDOW_QUESTS_TANKMANFEMALE_DESCRIPTION))

    def getOkButtonText(self):
        return i18n.makeString(MENU.AWARDWINDOW_RECRUITBUTTON)

    def handleOkButton(self):
        from gui.server_events import events_dispatcher as quests_events
        quests_events.showTankwomanRecruitWindow(self.__questID, self.__tankmanData.isPremium, self.__tankmanData.fnGroupID, self.__tankmanData.lnGroupID, self.__tankmanData.iGroupID)


class FormattedAward(AwardAbstract):

    class _BonusFormatter(object):
        _BonusFmt = namedtuple('_BonusFmt', 'icon value')

        def __call__(self, bonus):
            return []

    class _SimpleFormatter(_BonusFormatter):

        def __init__(self, icon):
            self._icon = icon

        def __call__(self, bonus):
            return [self._BonusFmt(self._icon, BigWorld.wg_getIntegralFormat(bonus.getValue()))]

    class _SimpleNoValueFormatter(_SimpleFormatter):

        def __call__(self, bonus):
            return [self._BonusFmt(self._icon, '')]

    class _ItemsFormatter(_BonusFormatter):

        def __call__(self, bonus):
            result = []
            for item, count in bonus.getItems().iteritems():
                if item is not None and count:
                    result.append(self._BonusFmt(item.icon, BigWorld.wg_getIntegralFormat(count)))

            return result

    def __init__(self):
        self._formatters = {'gold': self._SimpleFormatter(RES_ICONS.MAPS_ICONS_LIBRARY_GOLDICONBIG),
         'credits': self._SimpleFormatter(RES_ICONS.MAPS_ICONS_LIBRARY_CREDITSICONBIG_1),
         'freeXP': self._SimpleFormatter(RES_ICONS.MAPS_ICONS_LIBRARY_FREEXPICONBIG),
         'premium': self._SimpleNoValueFormatter(RES_ICONS.MAPS_ICONS_LIBRARY_PREMDAYICONBIG),
         'items': self._ItemsFormatter()}

    def clear(self):
        if self._formatters is not None:
            self._formatters.clear()
            self._formatters = None
        return


class RegularAward(FormattedAward):

    def __init__(self, potapovQuest, isMainReward = False, isAddReward = False):
        super(RegularAward, self).__init__()
        raise True in (isMainReward, isAddReward) or AssertionError
        self.__potapovQuest = potapovQuest
        self.__isMainReward = isMainReward
        self.__isAddReward = isAddReward

    def getWindowTitle(self):
        return i18n.makeString(MENU.AWARDWINDOW_TITLE_TASKCOMPLETE)

    def getBackgroundImage(self):
        vehType = findFirst(None, self.__potapovQuest.getVehicleClasses())
        if vehType in _BG_IMG_BY_VEH_TYPE:
            return _BG_IMG_BY_VEH_TYPE[vehType]
        else:
            return random.choice(_BG_IMG_BY_VEH_TYPE.values())

    def getAwardImage(self):
        return ''

    def getHeader(self):
        return i18n.makeString(MENU.AWARDWINDOW_QUESTS_TASKCOMPLETE_HEADER, taskName=self.__potapovQuest.getUserName())

    def getDescription(self):
        return i18n.makeString(MENU.AWARDWINDOW_QUESTS_TASKCOMPLETE_DESCRIPTION)

    def getAdditionalText(self):
        nextQuestID = _getNextQuestInTileByID(self.__potapovQuest.getID())
        if nextQuestID:
            nextQuestInfo = i18n.makeString(MENU.AWARDWINDOW_QUESTS_TASKCOMPLETE_NEXTTASKAUTOCHOICE, taskName=g_eventsCache.potapov.getQuests()[nextQuestID].getUserName())
        else:
            nextQuestInfo = ''
        if self.__isAddReward:
            result = []
            for b in self.__potapovQuest.getBonuses(isMain=False):
                if b.isShowInGUI():
                    result.append(b.format())

            taskComplete = i18n.makeString(MENU.AWARDWINDOW_QUESTS_TASKCOMPLETE_ADDITIONAL, award=', '.join(result))
            return text_styles.main('{0}\n{1}'.format(taskComplete, nextQuestInfo))
        else:
            return '{0}\n{1}'.format(i18n.makeString(MENU.AWARDWINDOW_QUESTS_TASKCOMPLETE_ADDITIONALNOTCOMPLETE), nextQuestInfo)

    def getButtonStates(self):
        nextQuestID = _getNextQuestInTileByID(int(self.__potapovQuest.getID()))
        return (False, True, nextQuestID is not None)

    def getBodyButtonText(self):
        return i18n.makeString(MENU.AWARDWINDOW_TAKENEXTBUTTON)

    def getRibbonInfo(self):
        if self.__isMainReward:
            return packRibbonInfo(awardForCompleteText=i18n.makeString(MENU.AWARDWINDOW_QUESTS_TASKCOMPLETE_AWARDFORCOMLETE), awards=self.__getMainRewards())
        else:
            return packRibbonInfo(awardReceivedText=i18n.makeString(MENU.AWARDWINDOW_QUESTS_TASKCOMPLETE_AWARDRECIEVED))

    def handleBodyButton(self):
        from gui.server_events import events_dispatcher as quests_events
        nextQuestID = _getNextQuestInTileByID(int(self.__potapovQuest.getID()))
        if nextQuestID is not None:
            quests_events.showEventsWindow(nextQuestID, constants.EVENT_TYPE.POTAPOV_QUEST)
        return

    def __getMainRewards(self):
        result = []
        for b in self.__potapovQuest.getBonuses(isMain=True):
            formatter = self._formatters.get(b.getName(), lambda *args: [])
            for bonus in formatter(b):
                result.append({'itemSource': bonus.icon,
                 'value': bonus.value})

        return result
