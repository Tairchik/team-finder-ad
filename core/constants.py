from enum import StrEnum

# Длины полей
USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256
PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 6

# Пагинация
PROJECTS_PER_PAGE = 12
USERS_PER_PAGE = 12

# Константы для генерации аватаров
AVATAR_SIZE = 100
AVATAR_TEXT_COLOR = 'white'
AVATAR_FONT_SIZE = 48
AVATAR_DEFAULT_FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


class AvatarColor(StrEnum):
    BLUE = '#5B8DEF'
    PURPLE = '#9B59B6'
    ORANGE = '#E67E22'
    GREEN = '#27AE60'
    RED = '#E74C3C'
    TEAL = '#16A085'
    LIGHT_BLUE = '#2980B9'
    DARK_PURPLE = '#8E44AD'
    DARK_ORANGE = '#D35400'
    WHITE = "#FFFFFF"


# Статусы проекта
PROJECT_STATUS_OPEN = 'open'
PROJECT_STATUS_CLOSED = 'closed'
PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_OPEN, 'Open'),
    (PROJECT_STATUS_CLOSED, 'Closed'),
]
