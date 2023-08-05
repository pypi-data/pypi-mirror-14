import yaml
import os
import logging


class Config:
    """
    Mezzanine Client configuration
    """

    def __init__(self, filename=None, logger=None):
        self.filename = filename or os.path.join(os.path.expanduser('~'), '.mezzanine.yml')
        self.yaml_key = 'refresh_token'
        logging.basicConfig(level=logging.WARNING)
        self.logger = logger or logging.getLogger(__name__)

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as handle:
                    data = yaml.safe_load(handle.read())
                    refresh_token = data[self.yaml_key]
            except IOError:
                self.logger.info('Yaml config file, {}, could not be opened.'
                                 .format(self.filename))
                return None
            except KeyError:
                self.logger.info('Yaml config file, {}, does not contain a "{}" setting.'
                                 .format(self.filename, self.yaml_key))
                return None

            return refresh_token

    def dump(self, data):
        with open(self.filename, 'w') as yaml_file:
            yaml_file.write(yaml.dump(data, default_flow_style=False))
