from telethon import TelegramClient, events, utils
from telethon import functions, types
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import PeerChannel
from threading import Thread
import asyncio
import os.path
from random import randint
import random
import re

list_state = []
client = TelegramClient('main', '15504024', '1926863fda6bca9b40d2535b12c72f5a')


@client.on(events.NewMessage)
async def my_event_handler(event):
    try:
        chat_from = event.chat if event.chat else (await event.get_chat())
        chat_from = '@' + chat_from.username
    except:
        pass
    new_event = event.original_update
    new_event = str(new_event)

    if await bot_on_pause(list_state) == 0:
        client = await work()
        client, isExist = client[0], client[1]
        me = await client.get_me()
        if new_event:
            if new_event.startswith('UpdateShortMessage'):
                user_chat = event.message.from_id.user_id
                await personal_answers(user_chat, client, me)
            elif new_event.startswith('UpdateNewChannelMessage'):

                # Вытаскиваем значения задержки действий ботов
                join_chat_time = open('inactive_in_chat.txt', 'r')

                for line in join_chat_time:
                    data = (line.split(','))
                    # функция вступления в чат
                chat = await join_chat(client=client)
                list_state.append(1)
                # проверяем заданы ли у бота персональные настройки
                # первые 2 параметра отвечают за задержку между вступлением в чат и отправкой сообщения
                if isExist:
                    user_name = me.first_name
                    path = str(user_name) + '.txt'
                    personal_join_chat_time = open(path)
                    for line in personal_join_chat_time:
                        data = (line.split(','))
                    await asyncio.sleep(random.randint(int(data[0]), int(data[1])))
                else:
                    await asyncio.sleep(random.randint(int(data[0]), int(data[1])))
                # функция отправки сообщения в чат
                try:
                    await send_message(chat, client)
                except:
                    pass
                event_chat_id = event.chat_id
                await do_staff_in_chat(client, chat, event_chat_id, isExist, me)
                list_state.remove(1)


async def work(client, phone_number, first_name):
    await client.connect()
    me = await client.get_me()
    if me is None:
        await client.send_code_request(phone_number)
        code = input(f'Еnter code for {first_name}: ')

        await client.sign_up(code, first_name=first_name)
    user_name = me.first_name
    path = str(user_name) + '.txt'
    isExist = os.path.exists(path)
    return client, isExist
    # except:
    # print(f'Phone number:{data[0]}, Password:{data[7]}')
    # await user.sign_in(password=data[7])


def main(client, phone_number, first_name):
    asyncio.run(work(client, phone_number, first_name))


threadlist = []
users = []
phone_number = []
first_name = []
i = 0
f = open('accounts.txt', 'r', encoding="utf8")
for line in f:
    data = (line.split(','))
    users.append(TelegramClient(data[0], '15504024', '1926863fda6bca9b40d2535b12c72f5a'))
    phone_number.append(data[0])
    first_name.append(data[6])
for u in users:
    threadlist.append(Thread(target=main, args=(u, phone_number[i], first_name[i])))
    print(i)
    i += 1
for t in threadlist:
    t.start()
for t in threadlist:
    t.join()


async def personal_answers(chat, client, me):
    # получаем количество строк в файле
    all_lines = len(re.findall(r"[\n']+", open('personal_messages.txt').read()))

    # получаем рандомную строчку в файле
    msg = random.randint(0, int(all_lines))

    # сохраняем выбранную строку в переменную result
    result = open('personal_messages.txt').read().split('\n')[int(msg)]

    is_user_blocked = open('blacklist.txt', 'r')
    user = await client.get_entity(chat)

    for i in is_user_blocked:
        if i == user.username:
            return

    chat_text = open('personal_messages.txt', 'r')
    for line in chat_text:
        data = (line.split(','))
    chat_text.close()

    if user.username != me.username:
        await client.send_message(user, result)
        print('Im gonna  block: ' + user.username)
        add_user_to_black_list = open('blacklist.txt', 'a')
        add_user_to_black_list.write(user.username)
        add_user_to_black_list.close()
    return


async def bot_on_pause(list_state):
    if list_state:
        bot_on_pause = 1
    else:
        bot_on_pause = 0
    return bot_on_pause


async def authorization(client):
    me = await client.get_me()
    if me is None:
        sent = await client.send_code_request(data[0])
        code = input('Еnter code: ')
        try:
            await client.sign_up(code, first_name=data[6])
        except:
            await client.sign_in(password='7368245194')
        me = await client.get_me()
        print(f'User {me.username} successfully logged in')
        user_name = me.first_name
        path = str(user_name) + '.txt'
        isExist = os.path.exists(path)
        return client, isExist
    user_name = me.first_name
    path = str(user_name) + '.txt'
    isExist = os.path.exists(path)
    return client
    f.close()


# добавить отмену тасков в нужное время

# функция отвечающая за действия бота в чате
async def do_staff_in_chat(client, chat, event_chat_id, isExist, me):
    a = True
    last_messages = []
    while a is True:
        # Инактивим в чате
        await inactiv_in_chat(isExist, me)
        # парсим последние 10 сообщений в чате, если среди них попадается наше сообщение, то ггшочка
        with open('interval_soobsheniy.txt', 'r') as f:
            f = f.read()
            channel = await client.get_entity(chat)
            messages = await client.get_messages(channel, limit=int(f))  # pass your own args
        my_msg_list = open('chat_messages.txt', 'r')
        for msg in my_msg_list:
            data = (msg.split('\n'))
            last_messages.append(data)
        for message in messages:
            for msg in last_messages:
                if message.text == msg[0]:
                    await client.delete_dialog(chat)
                    await remove_chat_join_new(oldchat=chat, client=client)
                    last_messages = []
                    a = False
                    break
        chat = await join_chat(client)
        await inactiv_in_chat(isExist, me)
        await send_message(chat, client)


async def remove_chat_join_new(oldchat, client):
    deleted_chat = ''
    all_chats_list = []
    # getting all chats...
    all_chats = open('chats.txt', 'r')
    for chat in all_chats:
        if chat != oldchat:
            all_chats_list.append(chat)
    all_chats_list = await listToString(all_chats_list)

    commit_changes = open('chats.txt', 'w')
    commit_changes.write(all_chats_list)
    commit_changes.close()


# Function to convert
async def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


async def join_chat(client):
    chats_list = open('chats.txt', 'r')

    for chat in chats_list:
        await asyncio.sleep(random.randint(5, 10))
        await client(JoinChannelRequest(chat))
        return chat


async def inactiv_in_chat(isExist, me):
    inactiv_in_chat = open('intevral_bezdeystviya.txt', 'r')
    for line in inactiv_in_chat:
        data = (line.split(','))
        if isExist:
            user_name = me.first_name
            path = str(user_name) + '.txt'
            personal_join_chat_time = open(path)
            for line in personal_join_chat_time:
                data = (line.split(','))
            await asyncio.sleep(random.randint(int(data[0]), int(data[1])))
        else:
            await asyncio.sleep(random.randint(int(data[0]), int(data[1])))
    inactiv_in_chat.close()
    return


# Отправка сообщения ботом. Отправка осуществляется только если в файле указан username бота и текст.
async def send_message(chat, client):
    # получаем количество строк в файле
    all_lines = len(re.findall(r"[\n']+", open('chat_messages.txt').read()))

    # получаем рандомную строчку в файле
    msg = random.randint(0, int(all_lines))

    # сохраняем выбранную строку в переменную result
    result = open('chat_messages.txt').read().split('\n')[int(msg)]

    chat_text = open('chat_messages.txt', 'r')
    for line in chat_text:
        data = (line.split(','))
    await client.send_message(chat, result)
    chat_text.close()
    return result


client.start()
client.run_until_disconnected()
