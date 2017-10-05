"""This module contains the Settings class."""

import ConfigParser
import sys


class Settings(object):
    """Settings class."""

    settings = None

    @staticmethod
    def get_section(primarySection, secondarySection=None):
        """Return the appropriate section in the settings."""
        if Settings.settings is None:
            sys.stderr.write("Warning: Settings.get_section() called before Settings.init()\n")
            return None
        settingsSection = primarySection + '_' + secondarySection
        if secondarySection is None or settingsSection not in Settings.settings.sections():
            settingsSection = primarySection
            if settingsSection not in Settings.settings.sections():
                return None
        if Settings.settings.has_option(settingsSection, 'ignore') and Settings.settings.get(settingsSection, 'ignore') == 'TRUE':
            return None
        return settingsSection

    @staticmethod
    def init(file):
        """Initialize the settings."""
        Settings.settings = ConfigParser.ConfigParser()
        Settings.settings.read(file)

    @staticmethod
    def has_option(section, option):
        """Determine if a section has this option."""
        if Settings.settings is None:
            sys.stderr.write("Warning: Settings.has_option() called before Settings.init()\n")
            return False
        elif not Settings.settings.has_section(section):
            return False
        else:
            return Settings.settings.has_option(section, option)

    @staticmethod
    def getfloat(section, option):
        """Return a float corresponding to the option value."""
        if Settings.settings is None:
            sys.stderr.write("Warning: Settings.getfloat() called before Settings.init()\n")
            return None
        else:
            return Settings.settings.getfloat(section, option)

    @staticmethod
    def get(section, option):
        """Return the value corresponding to the option."""
        if Settings.settings is None:
            sys.stderr.write("Warning: Settings.get() called before Settings.init()\n")
            return None
        else:
            return Settings.settings.get(section, option)

    @staticmethod
    def getint(section, option):
        """Return an int corresponding to the option value."""
        if Settings.settings is None:
            sys.stderr.write("Warning: Settings.getint() called before Settings.init()\n")
            return None
        else:
            return Settings.settings.getint(section, option)

    @staticmethod
    def sections():
        """Return the list of sections in the settings."""
        if Settings.settings is None:
            sys.stderr.write("Warning: Settings.sections() called before Settings.init()\n")
            return None
        else:
            return Settings.settings.sections()
