import configparser
import platform



def get_crawl_mode():
    config = configparser.ConfigParser()
    config.sections()
    config.read("config.ini")
    return config['CRAWL_MODE']['crawl_mode']


if __name__ == '__main__':
    print(get_db_config())
    # print(get_crawl_mode())
