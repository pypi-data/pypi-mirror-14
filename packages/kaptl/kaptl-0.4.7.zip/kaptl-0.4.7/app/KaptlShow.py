import os

from app.Utils import Utils


class KaptlShow:
    def __init__(self):
        self.manifest = Utils.get_manifest_data()
        self.rules = Utils.read_rules_from_file(os.getcwd() + "/app.kaptl")

    def output_project_info(self):
        print "App name: " + self.manifest["appName"]
        print "Stack: " + Utils.get_readable_stack_string(manifest=self.manifest)
        if "\n" in self.rules:
            print "Rules:"
            print self.rules
        else:
            print "Rules: " + self.rules
