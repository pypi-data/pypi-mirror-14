import sys

from app.Utils import Utils


class KaptlAdd:
    def __init__(self, arguments):
        self.app_id = Utils.get_manifest_data()["appName"]
        self.rules = arguments["<rule>"]

    def add_rule_to_rules_file(self):
        try:
            with open(self.app_id + ".kaptl", "a") as rules_file:
                rules_file.write('\n' + self.rules)
                print "Rule is added to a rules file"
        except IOError:
            print "Couldn't find the rules file. Check if the rules file is present in the directory."
            sys.exit()
