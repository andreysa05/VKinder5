import vk_api
from vk_api.longpoll import VkLongPoll


USER = None
GROUP = '''vk1.a.QzBodhN0Vc-A3rfMrej9ycU8EwqU5o1tJvBQpsWSwNONNUEO_hcsgW50ZMieKtgyXl9pTWhx4BKMmXPet7sY93ku3hsWKw7rlcR2
c547YonIhV_odhmC7_P2gNt0SPE2NALNJ8giXxZ3gmOsGKxiZuTff9zDvh_eq4r0DKZFn4Hmhfh2R6fEokfJlTDPvK9ZFFgeuJzZBor80PNW4PcPhg'''


def two_factor():
    code = input('Code? ')
    return [code, True]


vk_group = vk_api.VkApi(token=GROUP)
longpoll = VkLongPoll(vk_group)
couples_dict = dict()
vk_user = vk_api.VkApi(token=USER) if USER else vk_api.VkApi('+77777777777', 'password', auth_handler=two_factor)
try:
    vk_user.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
