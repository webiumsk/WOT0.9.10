# Embedded file name: scripts/client/gui/shared/gui_items/dossier/achievements/PromisingFighterAchievement.py
from dossiers2.ui.achievements import ACHIEVEMENT_BLOCK as _AB
from abstract import SimpleProgressAchievement

class PromisingFighterAchievement(SimpleProgressAchievement):

    def __init__(self, dossier, value = None):
        super(PromisingFighterAchievement, self).__init__('promisingFighterMedal', _AB.TEAM_7X7, dossier, value)

    def _readProgressValue(self, dossier):
        return dossier.getRecordValue(_AB.TEAM_7X7, 'promisingFighter')
