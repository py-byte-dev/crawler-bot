from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend.application import interfaces
from backend.application.interfaces import Keyboard


class UserKeyboardBuilder(interfaces.UserKeyboardBuilder):
    def __init__(self):
        self._kb_builder: InlineKeyboardBuilder | None = None

    def get_main_menu_kb(self) -> Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='📥 Upload file', callback_data='upload_file')

        return self._kb_builder

    def get_main_menu_return_kb(self) -> Keyboard:
        if self._kb_builder is not None:
            return self._kb_builder
        self._kb_builder = InlineKeyboardBuilder()

        self._kb_builder.button(text='❌ Cancel upload', callback_data='main_menu')

        return self._kb_builder
