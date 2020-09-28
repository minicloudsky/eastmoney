import configparser
import platform

linux_database_config_path = '/config/database.ini'
windows_database_config_path = 'D:\\database.ini'


def get_db_config():
    config = configparser.ConfigParser()
    config.sections()
    if 'linux' in platform.system().lower():
        config.read(linux_database_config_path)
    else:
        config.read(windows_database_config_path)
    return {
        'host': config['DATABASE']['host'],
        'port': int(config['DATABASE']['port']),
        'user': config['DATABASE']['user'],
        'password': config['DATABASE']['password']
    }


if __name__ == '__main__':
    print(get_db_config())
