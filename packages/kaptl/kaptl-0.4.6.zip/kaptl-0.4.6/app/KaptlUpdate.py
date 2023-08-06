import os
import sys

from app.Utils import Utils

from app.Common import Common


class KaptlUpdate:
    def __init__(self, session, arguments):
        for filename in os.listdir(os.getcwd() + "/.kaptl"):
            if filename.endswith(".kaptl.old"):
                self.app_name = Utils.get_manifest_data()["appName"]

        if self.app_name is "":
            print "ERROR: Directory does not contain a KAPTL project"
            sys.exit()

        self.kaptl_cookie = {"kaptl-session-id": self.app_name}
        self.arguments = arguments
        self.session = session
        self.common_methods = Common(self.session)
        self.rules = Utils.read_rules_from_file(os.getcwd() + "/app.kaptl")
        self.rules_old = Utils.read_rules_from_file(os.getcwd() + "/.kaptl/app.kaptl.old")
        self.file_info = None
        self.angular_only = False
        self.stack = Utils.get_stack_info_from_manifest()
        self.angular_only = Utils.check_if_angular_only(self.stack)

    def update_project(self):
        if Utils.diff_two_strings(self.rules_old, self.rules) == '':
            print "No changes to rules were made since the last build. Skipping..."
            if not self.arguments["--build"]:
                sys.exit()
        else:
            self.app_name = self.common_methods.parse_rules(self.session, self.rules, self.stack, kaptl_cookie=self.kaptl_cookie, recipe=self.arguments["--recipe"])
            if self.app_name is not None:
                self.file_info = self.common_methods.get_file_info(self.session, self.app_name, self.rules, self.stack,
                                                                   self.angular_only, is_update=True)
                if self.file_info is not None:
                    self.common_methods.download_file(self.session, self.file_info)
                    self.common_methods.unzip_archive(self.file_info[1], existing=False)
                else:
                    print "ERROR: Couldn't retrieve a file from the server. Try again later."
                    sys.exit()
            else:
                # just exit, parse_rules will print the info about what happened
                sys.exit()
