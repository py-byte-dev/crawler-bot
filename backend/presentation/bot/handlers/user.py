import asyncio

from aiogram import F, Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka import FromDishka

from backend.application import interfaces
from backend.application.use_cases.resource import ProcessXlsxDocumentInteractor
from backend.domain.templates.user_menu_texts import (
    error_text,
    get_file_menu_text,
    main_menu_text,
    processed_resource_text,
    start_process_text,
)
from backend.infrastructrure import exceptions as infrastructure_exc
from backend.presentation.bot.states.user import UserState

router = Router()


@router.message(CommandStart())
async def process_user_start(
    message: Message,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
):
    await message.answer(
        text=main_menu_text(user_name=message.from_user.full_name),
        reply_markup=kb_builder.get_main_menu_kb().as_markup(),
    )


@router.callback_query(F.data == 'upload_file')
async def get_user_file(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
):
    msg = await call.message.edit_text(
        text=get_file_menu_text(),
        reply_markup=kb_builder.get_main_menu_return_kb().as_markup(),
    )

    await state.update_data(msg=msg)
    await state.set_state(UserState.file)


@router.callback_query(F.data == 'main_menu')
async def display_main_menu(
    call: CallbackQuery,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
):
    await state.clear()
    await call.message.edit_text(
        text=main_menu_text(user_name=call.from_user.full_name),
        reply_markup=kb_builder.get_main_menu_kb().as_markup(),
    )


@router.message(UserState.file)
async def process_user_file(
    message: Message,
    state: FSMContext,
    kb_builder: FromDishka[interfaces.UserKeyboardBuilder],
    interactor: FromDishka[ProcessXlsxDocumentInteractor],
):
    await message.delete()
    state_data = await state.get_data()
    await state.clear()

    try:
        await state_data['msg'].edit_text(text=start_process_text())
        processed_resources = await interactor(message=message)
        for processed_resource in processed_resources:
            await message.answer(
                text=processed_resource_text(
                    title=processed_resource.title,
                    url=processed_resource.url,
                    xpath=processed_resource.xpath,
                    average_price=processed_resource.average_price,
                ),
            )
            await asyncio.sleep(0.3)
    except infrastructure_exc.IncorrectContentTypeError as e:
        await state_data['msg'].edit_text(text=error_text(details=str(e)))
    except infrastructure_exc.IncorrectDocumentExtensionError as e:
        await state_data['msg'].edit_text(text=error_text(details=str(e)))

    await message.answer(
        text=main_menu_text(user_name=message.from_user.full_name),
        reply_markup=kb_builder.get_main_menu_kb().as_markup(),
    )
