from random import randrange

import vk_api
from vk_api.longpoll import VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from functions import get_user, get_couples, get_photos, send_message
from models import *
from config import vk_group, vk_user, longpoll, couples_dict

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            keyboard = VkKeyboard()
            keyboard.add_button('Найди мне пару', color=VkKeyboardColor.PRIMARY)
            if request.lower() == "найди мне пару":
                user = User.get_or_none(User.user_id == event.user_id)
                if not user:
                    user = User.create(user_id=event.user_id)
                couple_num = user.offset
                user_info = get_user(event.user_id, vk_group)
                if 'city' in user_info and 'sex' in user_info:
                    if event.user_id not in couples_dict or not couples_dict[event.user_id]:
                        couples_dict[event.user_id] = get_couples(user_info, vk_user, couple_num)
                    showed_couples = user.couples
                    showed_couples = showed_couples.split(', ') if type(showed_couples) == str else []
                    showed_couples = list(map(int, list(showed_couples))) if showed_couples else []
                    couple = couples_dict[event.user_id].pop(0)
                    if showed_couples:
                        while (couple in showed_couples) and couples_dict[event.user_id]:
                            couple = couples_dict[event.user_id].pop(0)
                    if couple:
                        attach = get_photos(couple, vk_user)
                        send_message(event.user_id, vk_group,
                                          f"Бот нашел Вам пару:\nhttps://vk.com/id{attach[1]}\n"
                                          f"Хотите еще, введите - Найди мне пару",
                                          keyboard,
                                          attach[0])
                        couple_num += 1
                        showed_couples.append(couple)
                        couples = ', '.join(list(map(str, showed_couples))) if len(showed_couples) > 1 else str(couple)
                        user.offset = couple_num
                        user.couples = couples
                        user.save()
                    else:
                        send_message(event.user_id, vk_group, 'Ошибка', keyboard)
                else:
                    send_message(event.user_id, vk_group, '''Чтобы найти себе пару, у Вас должен быть открытый
профиль, и заполненые все данные (пол, возраст, город, семейное положение)''', keyboard)
            else:
                send_message(event.user_id, vk_group, 'Неизвестная комманда\nДля поиска пары, введите - '
                                                      'Найди мне пару', keyboard)
