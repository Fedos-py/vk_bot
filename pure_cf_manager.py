import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
import sqlite3
import datetime

myid = -201978017

# Функция посылающая сообщение
def write_msg(peer_id, message, attachment=''):
    random_id = vk_api.utils.get_random_id()
    print(peer_id, message, random_id)
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'random_id': random_id, 'attachment': attachment})

def exit(code):
    raise SystemExit(code)



# Авторизуемся как сообщество
vk = vk_api.VkApi(token="15a4c8cc3ceaa121d1afc5032f40846ef7f01b1655f97560950e5535986e165cb49d472b72c9ede63a1be")
#longpoll = VkLongPoll(vk)
bot_api = vk.get_api()
otvet = ''
EXIT_TIME = datetime.time(3, 59, 0)



# Основной цикл
while True:
    longpoll = VkBotLongPoll(vk, 201978017)
    try:
        while True:
            for event in longpoll.listen():
                print(123)
                # Если пришло новое сообщение
                # print(event.type)
                # print([*event.object])
                print(event)
                if event.object.text == '':
                    action = event.object.action
                    print(action)
                    if action['type'] == 'chat_kick_user':
                        write_msg(event.object.peer_id, f'@id{event.object.from_id}(Пользователь) покинул чат', 'photo-201978017_457239020')
                    if action['member_id'] == myid:
                        write_msg(event.object.peer_id, f'@id{event.object.from_id}(Пользователь) присоеденился к чату')
                    else:
                        write_msg(event.object.peer_id, f'@id{event.object.from_id}(Пользователь) совершил неизвестное действие {action["type"]}')
                else:
                    if event.from_chat:
                        # Сообщение от пользователя
                        request = event.object.text.lower()
                        print(request)
                        # Логика формирования ответа бота
                        # Если есть такая команда
                        if request[0] == '/':
                            command = str(request.split(' ')[0][1:])
                            if (command == 'kick' or command == 'кик' or command == 'ban' or command == 'бан') and len(request.split(' ')) > 1:
                                kicked_id = int(str(request.split(' ')[1]).split('|')[0][3:])
                                if str(request.split(' ')[1][0]) == '[':
                                    if command == 'kick' or command == 'кик':
                                        write_msg(event.object.peer_id, f'Модератор чата @id{event.object.from_id}' \
                                                f'@id{event.object.from_id}(Админ)' \
                                                f'кикнул @id{event.object.from_id}(пользователя) ' \
                                                f'по причине {str(request.split(" ")[-1])}.')
                                    elif command == 'ban' or command == 'бан':
                                        write_msg(event.object.peer_id, f'@id{event.object.from_id}(Админ)' \
                                                                        f'забанил @id{event.object.from_id}(пользователя) ' \
                                                                        f' по причине {str(request.split(" ")[-1])}.')
                                    vk.method('messages.removeChatUser',
                                              {'chat_id': event.object.peer_id - 2000000000,
                                               'user_id': kicked_id})
                                else:
                                    write_msg(event.object.peer_id, 'Чтобы кикнуть пользователя - упомяните его через "@".\nПример: /kick @fedya_nelubin Реклама')
                            if command == 'help' or command == 'хелп':
                                write_msg(event.object.peer_id, '🧢 Команды, доступные всем пользователям: 🧢 \n' \
                                        '/help - доступные функции.\n' \
                                        '/myid - Ваш ИД ВКонтакте.\n' \
                                        '/mystats - Ваша статистика в данной беседе. \n' \
                                        '/stats @пользователь - статистика упомянутого пользователя в данной беседе.\n' \
                                        '/staff - список модераторов и администраторов.\n\n' \
                                        '🎩 Команды, доступные модератору: 🎩\n' \
                                        '/mute @пользователь [количество минут] [причина] - установить игроку заглушку.\n' \
                                        '/unmute @пользователь - снять игроку заглушку.')
                            if command == 'myid' or command == 'мойид':
                                write_msg(event.object.peer_id, f'@id{event.object.from_id}(Уважаемый пользователь), Ваш id - {event.object.from_id}')
                            else:
                                write_msg(event.object.peer_id, 'Я не знаю такой команды. Узнать все мои команды - /help, /хелп, /info, /инфо.')
                        else:
                            if request == 'ку':
                                print(True)
                                write_msg(event.object.peer_id, f'Привет, дорогой @id{event.object.from_id}(пользователь)')
                            else:
                                write_msg(event.object.peer_id, 'Я отвечаю только на свои команды. Подробнее - /help .')
                    else:
                        write_msg(event.object.peer_id, 'чтобы я работал добавьте меня в беседу')

    except requests.exceptions.ReadTimeout as timeout:
        continue
