# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/server_events/TutorialHangarQuestDetails.py
from gui.Scaleform.daapi.view.meta.TutorialHangarQuestDetailsMeta import TutorialHangarQuestDetailsMeta
from gui.server_events.bonuses import getTutorialBonusObj
from gui.server_events import formatters
from gui.shared.formatters import text_styles
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.Scaleform.daapi.view.lobby.header import battle_selector_items
from gui.shared.events import TutorialEvent, OpenLinkEvent
from gui.prb_control.settings import PREBATTLE_ACTION_NAME
from helpers import i18n

class CONDITION_TYPE(object):
    CHAIN = 'chain'
    TUTORIAL = 'tutorial'
    VIDEO = 'video'


class TutorialHangarQuestDetails(TutorialHangarQuestDetailsMeta):

    def __init__(self):
        super(TutorialHangarQuestDetailsMeta, self).__init__()
        self.__questsDescriptor = None
        return

    def _dispose(self):
        self.__questsDescriptor = None
        super(TutorialHangarQuestDetails, self)._dispose()
        return

    def setQuestsDescriptor(self, descriptor):
        self.__questsDescriptor = descriptor

    def showTip(self, id, type):
        if type == CONDITION_TYPE.CHAIN:
            self.fireEvent(TutorialEvent(TutorialEvent.START_TRAINING, settingsID='TRIGGERS_CHAINS', initialChapter=id, restoreIfRun=True))
        elif type == CONDITION_TYPE.TUTORIAL:
            battle_selector_items.getItems().select(PREBATTLE_ACTION_NAME.BATTLE_TUTORIAL)
        elif not (type == CONDITION_TYPE.VIDEO and id in (OpenLinkEvent.REPAIRKITHELP_HELP, OpenLinkEvent.MEDKIT_HELP, OpenLinkEvent.FIRE_EXTINGUISHERHELP_HELP)):
            raise AssertionError
            self.fireEvent(OpenLinkEvent(id, title=i18n.makeString('#tutorial:tutorialQuest/video/%s' % id)))

    def requestQuestInfo(self, questID):
        if self.__questsDescriptor is None:
            return
        else:
            chapter = self.__questsDescriptor.getChapter(questID)
            image = chapter.getImage()
            description = chapter.getDescription()
            self.as_updateQuestInfoS({'image': image,
             'awards': self.__getBonuses(chapter),
             'title': text_styles.highTitle(chapter.getTitle()),
             'description': self.__getDescription(description, chapter)})
            return

    def __getBonuses(self, chapter):
        result = []
        bonus = chapter.getBonus()
        if bonus is not None:
            for n, v in bonus.getValues().iteritems():
                b = getTutorialBonusObj(n, v)
                if b is not None:
                    result.append(b.format())

        if len(result):
            return formatters.todict([formatters.packTextBlock(', '.join(result))])
        else:
            return []

    def __getDescription(self, description, chapter):
        return {'descTitle': text_styles.middleTitle(QUESTS.BEGINNERQUESTS_DETAILS_DESCRIPTIONTITLE),
         'descText': text_styles.main(description),
         'conditionItems': self.__getTopConditions(chapter),
         'conditionsTitle': text_styles.middleTitle(QUESTS.BEGINNERQUESTS_DETAILS_CONDITIONSTITLE)}

    def __getTopConditions(self, chapter):
        blocks = []
        for questCondition in chapter.getQuestConditions():
            chainType = questCondition['type']
            blocks.append({'type': chainType,
             'id': questCondition['id'],
             'btnText': questCondition['btnLabel'],
             'text': text_styles.main(questCondition['text'])})

        return blocks
