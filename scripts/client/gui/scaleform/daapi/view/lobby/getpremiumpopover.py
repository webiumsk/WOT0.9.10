# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/GetPremiumPopover.py
import BigWorld
from gui.Scaleform.daapi.view.meta.GetPremiumPopoverMeta import GetPremiumPopoverMeta
from gui.shared import event_dispatcher
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.BATTLE_RESULTS import BATTLE_RESULTS
from gui.shared.formatters import text_styles
from helpers.i18n import makeString as _ms

class GetPremiumPopover(GetPremiumPopoverMeta):

    def __init__(self, ctx = None):
        super(GetPremiumPopover, self).__init__()
        self.__context = ctx.get('data')

    def _populate(self):
        super(GetPremiumPopover, self)._populate()
        self.as_setDataS(self.__makeVO(self.__context))

    def onActionBtnClick(self, arenaUniqueID):
        event_dispatcher.showPremiumWindow(arenaUniqueID)
        self.destroy()

    def __makeVO(self, data):
        creditsDiff = '+ %s' % BigWorld.wg_getNiceNumberFormat(data.creditsDiff)
        xpDiff = '+ %s' % BigWorld.wg_getNiceNumberFormat(data.xpDiff)
        premStr = text_styles.neutral(BATTLE_RESULTS.GETPREMIUMPOPOVER_PREM)
        awardStr = text_styles.neutral(BATTLE_RESULTS.GETPREMIUMPOPOVER_AWARD)
        descriptionText = _ms(BATTLE_RESULTS.GETPREMIUMPOPOVER_DESCRIPTIONTEXT, prem=premStr, award=awardStr)
        result = {'arenaUniqueID': data.arenaUniqueID,
         'headerTF': {'htmlText': text_styles.highTitle(BATTLE_RESULTS.GETPREMIUMPOPOVER_HEADERTEXT)},
         'creditsTF': {'htmlText': text_styles.promoTitle(creditsDiff)},
         'creditsIcon': {'source': RES_ICONS.MAPS_ICONS_LIBRARY_CREDITSICONBIG_1},
         'xpTF': {'htmlText': text_styles.promoTitle(xpDiff)},
         'xpIcon': {'source': RES_ICONS.MAPS_ICONS_LIBRARY_XPICONBIG_1},
         'descriptionTF': {'htmlText': text_styles.main(descriptionText)},
         'actionBtn': {'label': BATTLE_RESULTS.GETPREMIUMPOPOVER_ACTIONBTN_LABEL}}
        return result
