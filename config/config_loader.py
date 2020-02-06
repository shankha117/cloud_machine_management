import configparser, os

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))


def add_app_configs(cinfigs: dict, app):
    for key, val in cinfigs.items():
        env_config = os.environ.get(key)
        if os.environ.get(key) is not None:
            app.config[key] = env_config
        else:
            app.config[key] = val


def load_config(app):
    current_configs = dict()
    for sec in config.sections():
        current_configs.update(config.items(sec))

    add_app_configs(current_configs, app)
