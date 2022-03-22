from telethon import TelegramClient, events, utils
from telethon import functions, types
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import PeerChannel
from threading import Thread
import asyncio
import os.path
from random import randint
import random
import socket
import socks
import re

list_state = []
bots_chats_list = []
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
settings_file_name = input('Укажите название файла с настройками: ')
settings = open(str(settings_file_name) + '_settings.txt', 'r', encoding='utf-8')
for line in settings:
    data = (line.split(','))

session_name = data[0]  # Имя сессии
api_id = data[1]  # API id
hash = data[2]  # Hash
use_hash = input('Подключать proxy?\nДа/Нет:')

if use_hash.lower() == 'да':
    proxy_ip = data[3]
    proxy_port = data[4]
    proxy_name = data[5]
    proxy_password = data[6]
    client = TelegramClient("sessions\\" + str(session_name), int(api_id), str(hash),
                            proxy=(socks.SOCKS5, proxy_ip, proxy_port, proxy_name, proxy_password)).start()

    bot_chat_area = input('Укажите кол-во чатов обрабатываемых ботом: ')
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
else:
    bot_chat_area = input('Укажите кол-во чатов обрабатываемых ботом: ')
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    client = TelegramClient('sessions\\' + str(session_name), int(api_id), str(hash)).start()

print('Для начала работы бот должен отправить любой запрос.')

is_auth = []


async def start_client():
    await client.connect()
    await client.send_message('me', message='Started')


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
        isExist = await authorization()
        me = await client.get_me()
        if new_event.startswith('UpdateShortMessage'):
            user_chat = event.message.from_id.user_id
            await personal_answers(user_chat, client, me)
        else:
            # elif new_event.startswith('UpdateNewChannelMessage'):
            # Вытаскиваем значения задержки действий ботов
            join_chat_time = open('join_chat_time.txt', 'r')
            for line in join_chat_time:
                data = (line.split(','))
                # функция вступления в чат
            chat = await join_chat(client=client, interval1=data[0], interval2=data[1])
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
            except Exception as E:
                print(f'Ошибка при попытке отправить сообщение: {E}')
            event_chat_id = event.chat_id
            await do_staff_in_chat(client, chat, event_chat_id, isExist, me)
            list_state.remove(1)


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
        print(user.username + ' Blocked')
        add_user_to_black_list = open('blacklist.txt', 'a')
        add_user_to_black_list.write(user.username)
        add_user_to_black_list.close()
    return


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def grab_chats_for_bot(bot_chat_area):
    changes = []
    chats_list = open('chats.txt', 'r')
    i = 1
    for chat in chats_list:
        if int(bot_chat_area) >= i:
            bots_chats_list.append(chat)
            i += 1
    all_chats = open('chats.txt', 'r')
    for chat in all_chats:
        if chat not in bots_chats_list:
            changes.append(chat)
    update_chats_list = open('chats.txt', 'w')
    changes = listToString(changes)
    update_chats_list.write(changes)
    update_chats_list.close()
    return bots_chats_list


grab_chats_for_bot(bot_chat_area)


async def bot_on_pause(list_state):
    if list_state:
        bot_on_pause = 1
    else:
        bot_on_pause = 0
    return bot_on_pause


async def authorization():
    me = await client.get_me()
    is_auth.append(1)
    user_name = me.first_name
    path = str(user_name) + '.txt'
    isExist = os.path.exists(path)
    return isExist


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
            try:
                channel = await client.get_entity(chat)
                messages = await client.get_messages(channel, limit=int(f))  # pass your own args\

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
                            break
            except:
                print('Список чатов пуст')

        join_chat_time = open('join_chat_time.txt', 'r')
        for line in join_chat_time:
            data = (line.split(','))
        chat = await join_chat(client=client, interval1=data[0], interval2=data[1])
        await inactiv_in_chat(isExist, me)
        await send_message(chat, client)


async def remove_chat_join_new(oldchat, client):
    me = await client.get_me()
    user_name = me.first_name

    blocking_old_chat = open('blacklist_chats.txt', 'a+')
    blocking_old_chat.write(oldchat)
    blocking_old_chat.close()

    black_list_chats = open('blacklist_chats.txt', 'r')

    blacklist = []
    for black_chat in black_list_chats:
        blacklist.append(black_chat)

    insert_chats_for_bot = open(user_name + '_chats.txt', 'a+')
    for chat in bots_chats_list:
        if chat not in blacklist:
            insert_chats_for_bot.write(chat)
        else:
            bots_chats_list.remove(chat)
    insert_chats_for_bot.close()

    all_chats_list = []
    all_chats = open(user_name + '_chats.txt', 'r')

    for chat in all_chats:
        if chat != oldchat:
            all_chats_list.append(chat)
    all_chats_list = listToString(all_chats_list)
    commit_changes = open(user_name + '_chats.txt', 'w')
    commit_changes.write(all_chats_list)
    commit_changes.close()


# Function to convert


async def join_chat(client, interval1, interval2):
    # Создаем файл с чатами для конкретного бота

    me = await client.get_me()
    user_name = me.first_name
    if not bots_chats_list:
        all_lines = len(re.findall(r"[\n']+", open('chats.txt').read()))
        if int(all_lines) < int(bot_chat_area):
            try:
                grab_chats_for_bot(bot_chat_area)
            except:
                print(f'Не удалось получить {bot_chat_area} чата.\nВозможная причина: в файле chats.txt закончились '
                      f'свободные чаты')
    my_file = open(str(user_name) + "_chats.txt", "a+")
    for chat in bots_chats_list:
        my_file.write(chat)
    my_file.close()

    me = await client.get_me()
    user_name = me.first_name
    chats_list = open(user_name + '_chats.txt', 'r')
    for chat in chats_list:
        await asyncio.sleep(random.randint(int(interval1), int(interval2)))
        try:
            await client(JoinChannelRequest(chat))
        except Exception as E:
            print(f'Не удалось подключиться к чату: {E}')
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
    try:
        await client.send_message(chat, result)
    except:
        print(f'Не удалось отправить сообщение:\nЧат: {chat}\nСообщение: {result}')
    chat_text.close()
    return result
loop = asyncio.get_event_loop()
client.start()
client.run_until_disconnected(loop.create_task(client.send_message('me', 'Using asyncio!'))) # - хуйня xd
