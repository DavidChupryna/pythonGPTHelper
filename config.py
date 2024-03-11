import configparser

config = configparser.ConfigParser()
config['LOGGING'] = {
    'level': 'INFO',
    'format': '%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s',
    'filename': 'log_file.txt',
    'filemod': 'w'
}

config['GPT'] = {
    'URL': 'http://localhost:1234/v1/chat/completions',
    'TEMPERATURE': '1',
    'MAX_TOKENS': '64',
    'MAX_MESSAGE_TOKENS': '35',

}

config['TEMPLATE_GPT'] = {
    'PYTHON_BEGINNER': 'Объясняй как новичку по языку программирования Python',
    'PYTHON_ADVANCED': 'Объясняй как профессионалу по языку программирования Python',
    'JAVA_SCRIPT_BEGINNER': 'Объясняй как новичку по языку программирования JavaScript',
    'JAVA_SCRIPT_ADVANCED': 'Объясняй как профессионалу по языку программирования JavaScript'
}

token = '6678952150:AAHi8AuOnyhKOJ-5jzQHqj808b5u2m8HNyM'

