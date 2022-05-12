import yaml


def get_config():
    with open("config.yml", "r") as file:
        config = yaml.load(file, Loader=yaml.CLoader)
        return config
