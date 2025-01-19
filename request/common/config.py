import configparser

SETTINGS_FILE = '../settings.ini'

def get_port():
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    return config.get('DEFAULT', 'port', fallback=None)

def get_pwd():
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    return config.get('DEFAULT', 'passwd', fallback=None)

def get_dest_url(index):
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    return config.get('DESTINATION_URL', f'dest{index}', fallback=None)

def get_dest_mac(index):
    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)
    return config.get('DESTINATION_MAC', f'dest{index}', fallback=None)
