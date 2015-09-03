# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/fortifications/components/FortWelcomeInfoView.py
from adisp import process
from gui import makeHtmlString
from gui import SystemMessages
from gui.Scaleform.daapi.view.meta.FortWelcomeInfoViewMeta import FortWelcomeInfoViewMeta
from gui.Scaleform.daapi.view.lobby.fortifications.fort_utils.FortSoundController import g_fortSoundController
from gui.Scaleform.locale.FORTIFICATIONS import FORTIFICATIONS
from gui.Scaleform.locale.SYSTEM_MESSAGES import SYSTEM_MESSAGES
from gui.Scaleform.daapi.view.lobby.fortifications.fort_utils.FortViewHelper import FortViewHelper
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.shared import g_eventBus
from gui.shared.ClanCache import g_clanCache
from gui.shared.events import OpenLinkEvent
from gui.shared.formatters import text_styles
from gui.shared.fortifications.context import CreateFortCtx
from gui.shared.fortifications.settings import CLIENT_FORT_STATE, FORT_RESTRICTION
from helpers import i18n
from debug_utils import LOG_DEBUG
__author__ = 'p_kosushko'

class FortWelcomeInfoView(FortWelcomeInfoViewMeta, FortViewHelper):

    def __init__(self):
        super(FortWelcomeInfoView, self).__init__()

    def onNavigate(self, code):
        LOG_DEBUG('navigate: %s' % code)
        g_eventBus.handleEvent(OpenLinkEvent(code))

    def onClientStateChanged(self, state):
        if not self.isDisposed():
            self.__updateData()

    def onClanMembersListChanged(self):
        if not self.isDisposed():
            self.__updateData()

    def _populate(self):
        super(FortWelcomeInfoView, self)._populate()
        self.startFortListening()
        self.__updateData()
        clanSearch = self.__makeHyperLink('clanSearch', FORTIFICATIONS.FORTWELCOMEVIEW_CLANSEARCH)
        clanCreate = self.__makeHyperLink('clanCreate', FORTIFICATIONS.FORTWELCOMEVIEW_CLANCREATE)
        detail = self.__makeHyperLink('fortDescription', FORTIFICATIONS.FORTWELCOMEVIEW_HYPERLINK_MORE)
        self.as_setHyperLinksS(clanSearch, clanCreate, detail)

    @staticmethod
    def __makeHyperLink(linkType, textId):
        text = i18n.makeString(textId)
        attrs = {'linkType': linkType,
         'text': text}
        linkHtml = makeHtmlString('html_templates:lobby/fortifications', 'link', attrs)
        return linkHtml

    def _dispose(self):
        self.stopFortListening()
        super(FortWelcomeInfoView, self)._dispose()

    def _getCustomData(self):
        return {'isOnClan': g_clanCache.isInClan,
         'canRoleCreateFortRest': self.fortCtrl.getPermissions().canCreate(),
         'canCreateFortLim': self.fortCtrl.getLimits().isCreationValid()[0]}

    def __updateData(self):
        data = self.getData()
        self.as_setCommonDataS(data)
        self.__updateViewState(data)

    def __updateViewState(self, data):
        state = self.fortState
        if state.getStateID() == CLIENT_FORT_STATE.NO_CLAN:
            self.as_setRequirementTextS(self.__getNoClanText())
        elif self.fortCtrl.getPermissions().canCreate():
            result, reason = self.fortCtrl.getLimits().isCreationValid()
            if not result:
                if reason == FORT_RESTRICTION.CREATION_MIN_COUNT:
                    self.as_setWarningTextS(*self.__getNotEnoughMembersText(data))
        else:
            self.as_setRequirementTextS(self.__getClanMemberWelcomeText(data))

    def __getNoClanText(self):
        return text_styles.standard(i18n.makeString(FORTIFICATIONS.FORTWELCOMEVIEW_REQUIREMENTCLAN))

    def __getNotEnoughMembersText(self, data):
        minClanSize = data.get('minClanSize', 0)
        text = text_styles.alert(i18n.makeString(FORTIFICATIONS.FORTWELCOMEVIEW_WARNING, minClanSize=minClanSize))
        header = i18n.makeString(TOOLTIPS.FORTIFICATION_WELCOME_CANTCREATEFORT_HEADER)
        body = i18n.makeString(TOOLTIPS.FORTIFICATION_WELCOME_CANTCREATEFORT_BODY, minClanSize=minClanSize)
        return (text, header, body)

    def __getClanMemberWelcomeText(self, data):
        return ''.join((text_styles.standard(i18n.makeString(FORTIFICATIONS.FORTWELCOMEVIEW_REQUIREMENTCOMMANDER)), text_styles.neutral(data.get('clanCommanderName', ''))))

    def onCreateBtnClick(self):
        g_fortSoundController.playCreateFort()
        self.requestFortCreation()

    @process
    def requestFortCreation(self):
        result = yield self.fortProvider.sendRequest(CreateFortCtx('fort/create'))
        if result:
            SystemMessages.g_instance.pushI18nMessage(SYSTEM_MESSAGES.FORTIFICATION_CREATED, type=SystemMessages.SM_TYPE.Warning)
