from abc import abstractmethod
from typing import Any, Protocol


class Keyboard(Protocol):
    def as_markup(self) -> Any: ...


class UserKeyboardBuilder(Protocol):
    @abstractmethod
    def get_main_menu_kb(self) -> Keyboard: ...

    @abstractmethod
    def get_main_menu_return_kb(self) -> Keyboard: ...
