import os
import sys
import commands
from nose2.events import Plugin


class EasyGAE(Plugin):
    configSection = 'easygae'
    commandLineSwitch = (
        None, 'with-gae', 'Run tests inside the Google Appengine sandbox')

    def __init__(self, *args, **kwargs):
        super(EasyGAE, self).__init__(*args, **kwargs)
        self.register()

    def _prepare_environment(self):
        """We check for App Engine lib root in a few ways:

            - An environment variable called APPENGINE_ROOT
            - A Nose config variable called appengine-root.
            - Relative path from binary dev_appserver.py.
        """
        app_engine_path = os.environ.get(
            'APPENGINE_ROOT',
            self.config.as_str('appengine-root', self._find_path_by_bin()))

        if not app_engine_path:
            raise SystemError('Cannot find App Engine framework at all.')

        sys.path.insert(
            1, app_engine_path)

        import dev_appserver
        dev_appserver.fix_sys_path()

    def _find_path_by_bin(self):
        """If it all fails we check if the machine has the dev_appserver.py
        application and try to get the App Engine platform libs path from
        there.

        :returns: A path or None if it cannot find dev_appser.py.
        """
        bin_path = commands.getoutput('which dev_appserver.py')
        if not bin_path:
            return

        return bin_path.replace(
            'bin/dev_appserver.py', 'platform/google_appengine')

    def handleArgs(self, event):
        self._prepare_environment()

    def startTest(self, event):
        from google.appengine.ext import testbed
        self._testbed = testbed.Testbed()
        self._testbed.activate()
        self._testbed.init_urlfetch_stub()

    def stopTest(self, event):
        self._testbed.deactivate()

    # def createTests(self, event):
    #     self._start_testbed()

    # def startSubprocess(self, event):
    #     # self._loadConfig()
    #     self._start_testbed()
