import yaml


class Config:
    def __init__(self, config_path: str) -> None:
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        for k, v in self.config.items():
            setattr(self, k, v)

    def __str__(self):
        attributes = [f"{k}: {v}" for k, v in self.config.items()]
        return "\n".join(attributes)
