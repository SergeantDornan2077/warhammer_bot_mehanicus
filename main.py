import re
from random import randint
from vkbottle.bot import Bot, Message ,rules , MessageEvent
from  vkbottle.api import  API
from conf import utoken
from vkbottle import VKAPIError
from custom_rules import Permission
from models import *
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots
import  g4f
import nest_asyncio
nest_asyncio.apply()
bot = Bot(token=utoken)
bot.labeler.custom_rules["permission"] = Permission
pi = API(token=utoken)
cu = [x for x in User.select()]
bl = []
b = [x for x in BlackList.select()]
for v in b:
    bl.append(v.vk_id)
mt = []
m = [x for x in Mut.select()]
for v in m:
    mt.append(v.vk_id)
usrs = []
rangs = ["Сервитор", "Технограф", "Мех-ремесленник", "Электрожрец", "Технопровидец", "Техножрец", "Техномансер", "Омнипророк", "Логис", "Ремесленник","Генетор","Магос","Магос доминус","Архимагос","Архимагос доминус","Локум фабрикатор","Генерал-фабрикатор"]
for  v in cu:
    usrs.append(v.vk_id)
print(usrs)
kick = []
mut = []
ban = []
for member in usrs:
    d = User().select().where(User.vk_id == member)
    usr = []
    for v in d:
        usr.append(v.rang)
        r = rangs.index(usr[0])
        if r >= 9:
            mut.append(member)
        if r >= 11:
            kick.append(member)
        if  r >= 13:
            ban.append(member)
print(ban)
print(mut)
print(kick)

@bot.on.chat_message(text=["/d", "/d <cube:int>"])
async def dices(message: Message, cube: int = None):
    if cube is None:
        await  message.answer("Так какой кубик кидаем?")
    else:
        await message.answer(randint(1, cube))

@bot.on.chat_message(permission=kick, text=["/кик", "/кик <member>"])
async def kick_handler(message: Message, member=None):
    if member is None:
        await message.answer("Укажите на предателя")
    else:
        try:
            member = re.findall(r"[0-9]+", member)[0]
            await message.answer("Проваливай со своим Еретехом!")
            print(member)
            await bot.api.messages.remove_chat_user(message.peer_id - 2e9, int(member))
            pass
        except VKAPIError(15):
            await message.answer("Недостаточно прав")

@bot.on.chat_message(text=["/сшк", "/сшк <ask>"])
async def ask(message: Message, ask: str = None):
    if ask is None:
        await message.answer("Какую древнюю мудрость Изуверского Интеллекта ты хочешь получить сегодня?")
    else:
        try:
            client = Client(
                provider=RetryProvider([Phind, FreeChatgpt, Liaobots], shuffle=False)
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": ask}],
            )
            await message.answer(response.choices[0].message.content)
        except VKAPIError(15):
            await message.answer("Недостаточно прав")

@bot.on.chat_message(permission=ban, text=["/бан", "/бан <member>"])
async def ban_handler(message: Message, member=None):
    if member is None:
        await message.answer("Укажите на предателя")
    else:
        try:
            chat_id = message.peer_id - 2e9
            member = re.findall(r"[0-9]+", member)[0]
            if not int(member) in bl:
                BlackList(
                    vk_id=int(member),
                    chat_id=chat_id
                ).save()
                User.delete().where(User.vk_id==int(member) and User.chat_id == chat_id).execute()
                bl.append(int(member))
            if int(member) in usrs: usrs.remove(int(member))
            await message.answer("Объявляю Экстерминатус!")
            await bot.api.messages.remove_chat_user(message.peer_id - 2e9, int(member))
            pass
        except VKAPIError(15):
            await message.answer("Недостаточно прав")


@bot.on.chat_message(permission=ban, text=["/разбан", "/разбан <member>"])
async def unban_handler(message: Message, member=None):
    if member is None:
        await message.answer("Кого помиловать?")
    else:
        try:
            chat_id = message.peer_id - 2e9
            member = re.findall(r"[0-9]+", member)[0]
            BlackList().delete().where(BlackList.vk_id == int(member) and BlackList.chat_id == chat_id).execute()
            if int(member) in bl: bl.remove(int(member))
            await message.answer("Ты помилован Омниссией!")
            pass
        except VKAPIError(15):
            await message.answer("Недостаточно прав")


@bot.on.chat_message(permission=mut, text=["/мут", "/мут <member>"])
async def mud_handler(message: Message, member=None):
    if member is None:
        await message.answer("Кому заглушить Вокс?")
    else:
        try:
            c_id = message.peer_id - 2e9
            member = re.findall(r"[0-9]+", member)[0]
            Mut(
                vk_id=int(member),
                chat_id=c_id
            ).save()
            await message.answer("Заткнись , еретик!")

            pass
        except VKAPIError(15):
            await message.answer("Недостаточно прав")


@bot.on.chat_message(permission=mut, text=["/размут", "/размут <member>"])
async def mud_handler(message: Message, member=None):
    if member is None:
        await message.answer("Кому вернуть Вокс?")
    else:
        try:
            c_id = message.peer_id - 2e9
            member = re.findall(r"[0-9]+", member)[0]
            Mut.delete().where(Mut.vk_id == int(member) and Mut.chat_id == c_id).execute()
            await message.answer("Омниссия вернула тебе право голоса!")

            pass
        except VKAPIError(15):
            await message.answer("Недостаточно прав")

@bot.on.chat_message(permission=ban, text=["/повысить", "/повысить <member> <lvl:int>"])
async def lvlup(message: Message, member=None, lvl : int = None):
    if member is None or lvl is None:
        await message.answer("Кого повысить в звании?")
    elif lvl > 16:
        await message.answer("Выше только Омниссия!")
    else:
        try:
            member = re.findall(r"[0-9]+", member)[0]
            c_id = message.peer_id - 2e9
            d = User().select().where(User.vk_id == int(member))
            usr = []
            for v in d:
                usr.append(v.rang)
            r = rangs.index(usr[0])
            print(r)
            if r == 16:
                await message.answer("[Пользователь достиг максимального звания]")
            else:
                ra = r + lvl
                if ra > len(rangs):
                    await message.answer("[Ошибка в повышении в звании , переполнение буфера]")
                else:
                    User.update(rang=rangs[r+lvl]).where(User.vk_id == int(member)).execute()
                    s = User().select().where(User.vk_id == int(member))
                    for v in s:
                        await message.answer("Поздавляю с повышением! Теперь вы - " + v.rang)
                        break
            pass
        except VKAPIError(15):
            await message.answer("Недостаточно прав")

@bot.on.message(rules.ChatActionRule(("chat_invite_user", "chat_invite_user_by_link")))
async def add_user(message: Message):
    try:
        #chat_id = await bot.api.messages.get_conversations(filter="all") - оставим для  исправления костылей
        users = await pi.messages.get_conversation_members(peer_id=2000000004, fields="member_id")
        user_list = [member.member_id for member in users.items]
        print(user_list[-1])
        if user_list[-1] in bl:
            await message.answer("Вон отсюда , Еретик!")
            await bot.api.messages.remove_chat_user(message.peer_id - 2e9, user_list[-1])

        elif not user_list[-1] in usrs:
            User(
                vk_id=user_list[-1],
                warns= 0,
                rang= "Сервитор",
                chat_id=2000000004
            ).save()
            usrs.append(user_list[-1])
            mes = "@id" + str(user_list[-1]) + " ," + "Добро пожаловать на наш мир-кузню , твоё звание - Сервитор"
            await message.answer(mes)

        pass
    except VKAPIError(15):
        await message.answer("Недостаточно прав")

@bot.on.message()
async def add_user2(message: Message):
    try:
        chat_id  = message.peer_id - 2e9
        users = await pi.messages.get_conversation_members(peer_id=message.peer_id, fields="member_id")
        admins = await pi.messages.get_conversation_members(peer_id=message.peer_id, fields="is_admin")
        admins_list = [admin.member_id for admin in admins.items if admin.is_admin]
        user_list = [member.member_id for member in users.items]
        for u in user_list:
            if u in mt:
                id = await message.get_message_id()
                await bot.api.messages.delete(message_ids=id)
            if u in bl:
                await message.answer("Вон отсюда , Еретик!")
                await bot.api.messages.remove_chat_user(message.peer_id - 2e9, user_list[-1])

            elif not u in usrs:
                if u in admins_list:
                    User(
                        vk_id=int(u),
                        warns= 0,
                        rang= "Генерал-фабрикатор",
                        chat_id=chat_id
                    ).save()
                    mes = "@id" + str(u) + " ," + "Добро пожаловать на наш мир-кузню , твоё звание - Генерал-фабрикатор"
                else:
                    User(
                        vk_id=int(u),
                        warns= 0,
                        rang= "Сервитор",
                        chat_id=chat_id
                    ).save()
                    mes = "@id" + str(u) + " ," + "Добро пожаловать на наш мир-кузню , твоё звание - Сервитор"
                usrs.append(int(u))
                await message.answer(mes)

        pass
    except VKAPIError(15):
        await message.answer("Недостаточно прав")


bot.run_forever()
