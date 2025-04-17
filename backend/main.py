import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from backend import ioc
from backend.config import Config
from backend.presentation.bot.handlers.user import router

config = Config()


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting bot')


def create_bot(token: str) -> Bot:
    return Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )


def create_dispatcher(router: Router) -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    return dp


async def main(bot: Bot, dp: Dispatcher) -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    setup_logging()

    container = make_async_container(
        ioc.ApplicationProvider(),
        ioc.InfrastructureProvider(),
        AiogramProvider(),
        context={Config: config},
    )

    bot = create_bot(token=config.bot.token)
    dp = create_dispatcher(router=router)
    setup_dishka(container=container, router=dp, auto_inject=True)

    asyncio.run(main(bot, dp))
