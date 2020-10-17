import configparser


def get_crawl_mode():
    config = configparser.ConfigParser()
    config.sections()
    config.read("config.ini")
    return config['CRAWL_MODE']['crawl_mode']
