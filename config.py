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
    'MAX_TOKENS': '128',
    'MAX_MESSAGE_TOKENS': '35',

}

token = '6513626106:AAFmRyV9finpTWOjgbNBRcnIwVHY6b7bpR0'
