import datetime
from random import randrange


def send_message(user_id, vk, message, keyboard, attach=None):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'attachment': attach if attach else '',
        'random_id': randrange(10 ** 10),
        'keyboard': keyboard.get_keyboard()})


def get_user(user_id, vk):
    user = {}
    users = vk.method('users.get', {'user_id': user_id, 'v': 5.131,
                                    'fields': 'first_name, last_name, bdate, sex, city, country'})
    for key, value in users[0].items():
        if key == 'city':
            user[key] = value['id']
        elif key == 'bdate' and len(value.split('.')) == 3:
            user['age'] = datetime.datetime.now().year - int(value[-4:])
        else:
            user[key] = value
    return user


def get_couples(user_info, vk, offset):
    response = vk.method('users.search', {
        'sort': 0,
        'count': 50,
        'offset': offset,
        'city': user_info['city'],
        'sex': 3 - user_info['sex'],
        'status': 6,
        'has_photo': 1
    })
    try:
        return [item['id'] for item in response['items'] if not item['is_closed']]
    except KeyError():
        return None


def get_photos(user, vk):
    photos_info = {}
    response = vk.method('photos.get', {
        'owner_id': user,
        'album_id': 'profile',
        'extended': 1
    })
    photo_likes_counts = [photo['likes']['count'] + photo['comments']['count'] for photo in response['items']]
    top_likes = sorted(photo_likes_counts, reverse=True)[:3]

    top_photos_list = [photo for photo in response['items'] if (photo['likes']['count'] + photo['comments']['count'])
                       in top_likes]
    photo_ids = [photo['id'] for photo in top_photos_list]
    photos_info[top_photos_list[0]['owner_id']] = photo_ids
    user_id = user
    photo_attachments = [f'photo{user_id}_{photo_id}' for photo_id in photos_info[user_id]]
    attachments_list = [','.join(photo_attachments), user_id]
    return attachments_list
