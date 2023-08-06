import sys

from app.Utils import Utils

from Common import Common
from app.exceptions import WrongStackInfoException


class KaptlInit:
    def __init__(self, session, arguments):
        self.arguments = arguments
        self.app_name = ""
        self.session = session
        self.common_methods = Common(self.session)

        if self.arguments["<rules>"]:
            self.rules = self.arguments["<rules>"]
        elif self.arguments["--rules-file"]:
            self.rules = Utils.read_rules_from_file(self.arguments["--rules-file"])
        else:
            print "ERROR: Cannot find rules to use for creating a project. Aborting..."
            sys.exit()

        self.file_info = None

        self.stack = {}
        try:
            self.stack = Utils.get_stack_info(self.arguments)
        except WrongStackInfoException, e:
            print e.message
            sys.exit()

        self.angular_only = Utils.check_if_angular_only(self.stack)

    def initialize_project(self):
        self.app_name = self.common_methods.parse_rules(self.session, self.rules, self.stack,
                                                        self.arguments["--recipe"])
        if self.app_name is not None:
            self.file_info = self.common_methods.get_file_info(self.session, self.app_name, self.rules, self.stack,
                                                               self.angular_only)
            if self.file_info is not None:
                self.common_methods.download_file(self.session, self.file_info)
                self.common_methods.unzip_archive(self.file_info[1], existing=False)
            else:
                print "ERROR: Couldn't retrieve a file from the server. Try again later."
                sys.exit()
        else:
            # just exit, parse_rules will print the info about what happened
            sys.exit()
