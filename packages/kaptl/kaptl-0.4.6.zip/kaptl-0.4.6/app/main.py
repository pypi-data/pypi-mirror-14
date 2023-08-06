#!/usr/bin/env python

"""Usage: kaptl init [--backend=mvc] [--frontend=angular] [<rules> | --rules-file=RULESFILE ] [--build] [--recipe=cms]
       kaptl update [--build] [--recipe=cms]
       kaptl add <rule> [--build]
       kaptl show
       kaptl status
       kaptl -h | --help

Commands:
    init                    Initialize a new application in a current directory
    update                  Regenerate an existing application.
                            Requires .kaptl directory to be present in the directory.
    show                    Get information about current project
    status                  See if the rules have been changed but update wasn't performed
    add                     Add rule string to a rules file for current project

Arguments:
    <rules>                 Inline string with KAPTL rules.
                            See --rules-file  to use a text file instead

Options:
    -b STACKNAME --backend=STACKNAME           Backend framework. Possible values are: "mvc", "sails".
                                               If not specified, backend won't be generated
    -f STACKNAME --frontend=STACKAME           Frontend framework. Possible values are: "angular".
                                               If not specified, frontend won't be generated
    -r RULESFILE --rules-file=RULESFILE        Path to a file with KAPTL Rules
    -i --build                                 Build the project after it is unpacked
    --recipe=RECIPENAME                        Recipe to use when generating the application.
                                               Possible values are "cms", "stripe", "master".
                                               If not specified, "master" will be used as a default value.
    -h --help                                  Open this window

"""
import requests

from KaptlInit import *
from app.KaptlShow import KaptlShow
from app.KaptlUpdate import KaptlUpdate
from docopt import docopt
from KaptlStatus import *
from KaptlAdd import KaptlAdd


def main():
    args = docopt(__doc__)
    session = requests.Session()
    print "KAPTL CLI (c) 8th Sphere, Inc."
    print
    """
    Parse parameters and launch the proper operation
    :type arguments: object
    """
    if args["init"]:
        if os.path.exists(os.getcwd() + "/.kaptl"):
            print "There is an existing project in a current directory. Aborting..."
            sys.exit()
        else:
            init = KaptlInit(session, args)
            init.initialize_project()

    if args["status"]:
        status = KaptlStatus()
        status.display()

    if args["update"]:
        update = KaptlUpdate(session, args)
        update.update_project()

    if args["show"]:
        show = KaptlShow()
        show.output_project_info()

    if args["add"]:
        add = KaptlAdd(args)
        add.add_rule_to_rules_file()
        update = KaptlUpdate(session, args)
        update.update_project()

    if args["--build"]:
        Utils.build_project()


if __name__ == '__main__':
    "Main entry point for KAPTL CLI"
    main()
