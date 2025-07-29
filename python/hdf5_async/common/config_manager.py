
import configparser
import os

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self.config = configparser.ConfigParser()
        # Assuming config.ini is in the parent directory of common/
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        self.config.read(config_path)

    def get(self, section, option, fallback=None):
        return self.config.get(section, option, fallback=fallback)

    def getint(self, section, option, fallback=None):
        return self.config.getint(section, option, fallback=fallback)

    def getboolean(self, section, option, fallback=None):
        return self.config.getboolean(section, option, fallback=fallback)

# Global instance to be used across the application
config_manager = ConfigManager()
