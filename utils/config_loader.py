import yaml


def load_config(config_path="config/config.yaml"):
    """
    Load configuration from YAML file.
    """

    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        return config

    except Exception as e:
        raise Exception(f"Unable to load configuration: {e}")


config = load_config()