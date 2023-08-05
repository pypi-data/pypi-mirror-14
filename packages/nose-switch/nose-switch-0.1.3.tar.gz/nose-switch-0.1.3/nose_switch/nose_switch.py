import os
import logging
from nose.plugins import Plugin
from nose.util import tolist

log = logging.getLogger('nose.plugins.nose_switch')


def switch_on(switch_string):
    if switch_string in NoseSwitch.switches:
        return True
    return False


class NoseSwitch(Plugin):

    switches = []

    def __init__(self):
        Plugin.__init__(self)

    def options(self, parser, env=os.environ):
        """Define the command line options for the plugin."""
        parser.add_option("-S", "--switch", type="string",
                          action="append", dest="switch",
                          metavar="SWITCH",
                          help="Add special switches in code, \
                                based on options set when running tests.")

    def configure(self, options, config):
        sw_lst = []
        if options.switch:
            sw_lst = tolist(options.switch)

        if sw_lst:
            self.enabled = True
            NoseSwitch.switches += sw_lst
