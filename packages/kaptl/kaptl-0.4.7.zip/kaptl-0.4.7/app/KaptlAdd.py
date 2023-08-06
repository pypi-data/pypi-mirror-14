import sys

from app.Utils import Utils


class KaptlAdd:
    def __init__(self, arguments):
        self.app_id = Utils.get_manifest_data()["appName"]
        self.rules = arguments["<rule>"]

    def add_rule_to_rules_file(self):
        try:
            with open("app.kaptl", "a+") as rules_file:
                rules_file.write(self.rules + "\n")
                print "Rule is added to a rules file"
            with open("app.kaptl", "r") as rules_file:
                print "Current rules list:"
                for line in rules_file.readlines():
                    print line
            print ""
        except IOError:
            print "Couldn't find the rules file. Check if the rules file is present in the directory."
            sys.exit()
