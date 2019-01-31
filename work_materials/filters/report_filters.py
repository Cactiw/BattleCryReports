from telegram.ext import BaseFilter
from work_materials.globals import CHAT_WARS_ID

class FilterCorrectReport(BaseFilter):
    def filter(self, message):
        if message.text:
            if message.forward_from is None:
                return False
            return message.forward_from.id == CHAT_WARS_ID and "Твои результаты в бою:" in message.text and \
                   'Battle Cry. You were inspired by' in message.text


filter_correct_report = FilterCorrectReport()

class FilterIncorrectReport(BaseFilter):
    def filter(self, message):
        if message.text:
            if message.forward_from is None:
                return False
            return message.forward_from.id == CHAT_WARS_ID and "Твои результаты в бою:" in message.text


filter_incorrect_report = FilterIncorrectReport()

class FilterNotForwardReport(BaseFilter):
    def filter(self, message):
        if message.text:
            return "Твои результаты в бою:" in message.text and (message.forward_from is None or message.forward_from != CHAT_WARS_ID)


filter_not_forward_report = FilterNotForwardReport()

class FilterNotReport(BaseFilter):
    def filter(self, message):
        if message.text:
            return "Твои результаты в бою:" not in message.text

filter_not_report = FilterNotReport()

class FilterOldBattleCry(BaseFilter):
    def filter(self, message):
        if message.forward_from is None:
            return False
        return message.forward_from.id == CHAT_WARS_ID and "Твои результаты в бою:" in message.text and \
               'Battle Cry.' in message.text and 'You were inspired by' not in message.text

filter_old_battle_cry = FilterOldBattleCry()