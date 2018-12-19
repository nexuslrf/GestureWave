import configparser

DEFCONFIG = '../config/default.cfg'
USERCONFIG = '../config/personal.cfg'

def getInstance(relative=""):
    global instance
    if instance is None:
        instance = ConfigProvider(relative)
    return instance
    
instance = None


class ConfigProvider:

    def __init__(self, relative=""):
        self.relative = relative
        self.defaultConfig = configparser.ConfigParser()
        self.defaultConfig.read(self.relative + DEFCONFIG)
        self.userConfig = configparser.ConfigParser()
        self.userConfig.read(self.relative + USERCONFIG)

    def getAudioConfig(self):
        return self.getConfig('audio')

    def getRecordConfig(self):
        return self.getConfig('record')

    def getPathsConfig(self):
        return self.getConfig('paths')

    def getUserConfig(self):
        return self.getConfig('user')

    def getOSConfig(self):
        return self.getConfig('os')

    def getConfig(self, section):
        try:
            return dict(self.userConfig.items(section))
        except configparser.NoSectionError:
            items = self.defaultConfig.items(section)
            self.userConfig.add_section(section)
            for item in items:
                self.userConfig.set(section, item[0], item[1])
            with open(self.relative + USERCONFIG, 'w') as configfile:
                self.userConfig.write(configfile)
            return dict(self.userConfig.items(section))

    def setConfig(self, section, option, value):
        self.userConfig.set(section, option, value)
        with open(self.relative + USERCONFIG, 'w') as configfile:
            self.userConfig.write(configfile)
