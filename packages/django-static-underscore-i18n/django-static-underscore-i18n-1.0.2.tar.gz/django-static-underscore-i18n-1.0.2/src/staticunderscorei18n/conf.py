from django.conf import settings  # noqa

from appconf import AppConf


class StaticFilesConf(AppConf):

    # A list of packages to check for translations.
    PACKAGES = ('django.conf')
    # Controls the file path that generated catalog will be written into.
    ROOT = settings.STATIC_ROOT
    # Controls the directory inside STATICI18N_ROOT
    # that generated files will be written to.
    OUTPUT_DIR = 'jsunderscorei18n'
    # The dotted path to the function that creates the filename
    FILENAME_FUNCTION = 'staticunderscorei18n.utils.default_filename'
