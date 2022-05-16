import yaml


def get_config() -> dict:
    with open("config.yml", "r") as file:
        config = yaml.load(file, Loader=yaml.CLoader)
        return config


def get_env() -> dict:
    with open(".env", "r") as file:
        lines = file.readlines()

        env_dict = {}
        for line in lines:
            if line != "":
                env_dict[line.split("=")[0].strip()] = line.split("=")[1].strip()

        return env_dict


if __name__ == "__main__":
    print(get_env())
