from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from database.requests import get_notes, add_note, delete_note
from aiogram.utils.keyboard import InlineKeyboardBuilder

notes_router = Router()

class Form(StatesGroup):
    waiting_note_text = State()
    waiting_delete_note = State()





@notes_router.message(Command('add'))
async def state_def(message: Message, state: FSMContext):
    await message.answer("Введите текст заметки")
    await state.set_state(Form.waiting_note_text)

@notes_router.message(Form.waiting_note_text)
async def process_waiting_note_text(message: Message, state: FSMContext):
    await state.update_data(note_text=message.text)
    data = await state.get_data()
    await add_note(message.from_user.id, data.get('note_text'))
    await message.answer(f"Заметка сохранена: {data.get('note_text')}")
    await state.clear()





@notes_router.message(Command('list'))
async def list_notes(message: Message):
    notes = await get_notes(message.from_user.id)
    if notes:
        for i, note in enumerate(notes, start=1):
            await message.answer(f'{i}. {note[2]}')
    else:
        await message.answer('Ваши заметки пусты')





@notes_router.message(Command('delete'))
async def cmd_delete_note(message: Message):
    notes = await get_notes(message.from_user.id)
    if not notes:
        await message.answer("Ваши заметки пусты")
        return

    builder = InlineKeyboardBuilder()
    for note in notes:
        builder.button(
            text=note[2],
            callback_data=f'delete_{note[0]}'
        )
    builder.adjust(1)

    await message.answer("Выбери заметку для удаления:", reply_markup=builder.as_markup())


@notes_router.callback_query(F.data.startswith('delete_'))
async def process_delete_callback(callback: CallbackQuery):
    note_id = int(callback.data.split("_")[-1])
    await delete_note(note_id, callback.from_user.id)
    await callback.message.edit_text('Заметка удалена')
    await callback.answer("Заметка удалена")















