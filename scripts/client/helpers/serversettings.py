# Embedded file name: scripts/client/helpers/ServerSettings.py
import types
from collections import namedtuple
from shared_utils import makeTupleByDict
from gui.shared.utils.decorators import ReprInjector
from gui import GUI_SETTINGS

@ReprInjector.simple(('centerID', 'centerID'), ('dbidMin', 'dbidMin'), ('dbidMin', 'dbidMin'), ('regionCode', 'regionCode'))

class _ServerInfo(object):
    __slots__ = ('centerID', 'dbidMin', 'dbidMax', 'regionCode')

    def __init__(self, centerID, dbidMin, dbidMax, regionCode):
        self.centerID = centerID
        self.dbidMin = dbidMin
        self.dbidMax = dbidMax
        self.regionCode = regionCode

    def isPlayerHome(self, playerDBID):
        return self.dbidMin <= playerDBID <= self.dbidMax


class RoamingSettings(namedtuple('RoamingSettings', 'homeCenterID curCenterID servers')):

    def getHomeCenterID(self):
        return self.homeCenterID

    def getCurrentCenterID(self):
        return self.curCenterID

    def getRoamingServers(self):
        return self.servers

    def getPlayerHome(self, playerDBID):
        for s in self.getRoamingServers():
            if s.isPlayerHome(playerDBID):
                return (s.centerID, s.regionCode)

        return (None, None)

    def isEnabled(self):
        return GUI_SETTINGS.roaming

    def isSameRealm(self, playerDBID):
        centerID, _ = self.getPlayerHome(playerDBID)
        return centerID == self.getHomeCenterID()

    def isInRoaming(self):
        return self.getCurrentCenterID() != self.getHomeCenterID()

    def isPlayerInRoaming(self, playerDBID):
        centerID, _ = self.getPlayerHome(playerDBID)
        return centerID != self.getCurrentCenterID()

    @classmethod
    def defaults(cls):
        return cls(0, 0, [])


class _FileServerSettings(object):

    def __init__(self, fsSettings):
        self.__urls = dict(((n, d.get('url_template', '')) for n, d in fsSettings.iteritems()))

    def getUrls(self):
        return self.__urls

    def getClanEmblem64x64Url(self, clanDBID):
        return self.__getUrl('clan_emblems_big', clanDBID)

    def getClanEmblem32x32Url(self, clanDBID):
        return self.__getUrl('clan_emblems_small', clanDBID)

    def getClanEmblem64x64VehicleUrl(self, clanDBID):
        return self.__getUrl('clan_emblems', clanDBID)

    def getRareAchievement67x71Url(self, rareAchieveID):
        return self.__getUrl('rare_achievements_images', rareAchieveID)

    def getRareAchievement128x128Url(self, rareAchieveID):
        return self.__getUrl('rare_achievements_images_big', rareAchieveID)

    def getRareAchievementTextsUrl(self, langID):
        raise isinstance(langID, types.StringType) or AssertionError('given langID type must be string')
        return self.__getUrl('rare_achievements_texts', langID)

    def __getUrl(self, urlKey, *args):
        if urlKey in self.__urls:
            return self.__urls[urlKey] % args
        else:
            return None

    @classmethod
    def defaults(cls):
        return cls({})


class _RegionalSettings(namedtuple('_RegionalSettings', ['starting_day_of_a_new_week', 'starting_time_of_a_new_day', 'starting_time_of_a_new_game_day'])):

    def getWeekStartingDay(self):
        return self.starting_day_of_a_new_week

    def getDayStartingTime(self):
        return self.starting_time_of_a_new_day

    def getGameDayStartingTime(self):
        return self.starting_time_of_a_new_game_day

    @classmethod
    def defaults(cls):
        return cls(0, 0, 3)


class _ESportCurrentSeason(namedtuple('_ESportSeason', ['eSportSeasonID', 'eSportSeasonStart', 'eSportSeasonFinish'])):

    def getID(self):
        return self.eSportSeasonID

    def getStartTime(self):
        return self.eSportSeasonStart

    def getFinishTime(self):
        return self.eSportSeasonFinish

    @classmethod
    def defaults(cls):
        return cls(0, 0, 0)


class ServerSettings(object):

    def __init__(self, serverSettings):
        self.__serverSettings = serverSettings if serverSettings else {}
        if 'roaming' in self.__serverSettings:
            roamingSettings = self.__serverSettings['roaming']
            self.__roamingSettings = RoamingSettings(roamingSettings[0], roamingSettings[1], [ _ServerInfo(*s) for s in roamingSettings[2] ])
        else:
            self.__roamingSettings = RoamingSettings.defaults()
        if 'file_server' in self.__serverSettings:
            self.__fileServerSettings = _FileServerSettings(self.__serverSettings['file_server'])
        else:
            self.__fileServerSettings = _FileServerSettings.defaults()
        if 'regional_settings' in self.__serverSettings:
            self.__regionalSettings = makeTupleByDict(_RegionalSettings, self.__serverSettings['regional_settings'])
        else:
            self.__regionalSettings = _RegionalSettings.defaults()
        try:
            self.__eSportCurrentSeason = makeTupleByDict(_ESportCurrentSeason, self.__serverSettings)
        except TypeError:
            self.__eSportCurrentSeason = _ESportCurrentSeason.defaults()

    def getSettings(self):
        return self.__serverSettings

    @property
    def roaming(self):
        return self.__roamingSettings

    @property
    def fileServer(self):
        return self.__fileServerSettings

    @property
    def regionals(self):
        return self.__regionalSettings

    @property
    def eSportCurrentSeason(self):
        return self.__eSportCurrentSeason

    def isPotapovQuestEnabled(self):
        return self.__getGlobalSetting('isPotapovQuestEnabled', False)

    def isFortBattlesEnabled(self):
        return not self.__getGlobalSetting('isFortBattlesDisabled', True)

    def isClubsEnabled(self):
        return self.__getGlobalSetting('isClubsEnabled', False)

    def isGoldFishEnabled(self):
        return self.__getGlobalSetting('isGoldFishEnabled', False)

    def isPromoAutoViewsEnabled(self):
        return True

    def getForbiddenFortDefenseHours(self):
        return self.__getGlobalSetting('forbiddenFortDefenseHours', tuple())

    def getForbiddenSortieHours(self):
        return self.__getGlobalSetting('forbiddenSortieHours', tuple())

    def getForbiddenSortiePeripheryIDs(self):
        return self.__getGlobalSetting('forbiddenSortiePeripheryIDs', tuple())

    def getForbiddenRatedBattles(self):
        return self.__getGlobalSetting('forbiddenRatedBattles', {})

    def isPremiumInPostBattleEnabled(self):
        return self.__getGlobalSetting('isPremiumInPostBattleEnabled', True)

    def __getGlobalSetting(self, settingsName, default = None):
        return self.__serverSettings.get(settingsName, default)
