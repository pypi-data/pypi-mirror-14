import os
import sys
import zipfile

import pyprind
import requests

from Utils import Utils

KAPTL_HOST = "https://www.kaptl.com"
KAPTL_PARSE_URL = KAPTL_HOST + "/api/apps/parse"
KAPTL_DOWNLOAD_URL = KAPTL_HOST + "/api/apps/download"


class Common:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def parse_rules(session, rules, stack, recipe=None, kaptl_cookie=None):
        print "Parsing the rules..."
        request_data = dict(rulesText=rules.replace('\\', '').replace('\'', '"'), stack=stack)
        if recipe is not None:
            request_data["recipe"] = recipe
        try:
            if kaptl_cookie is not None:
                response = session.post(KAPTL_PARSE_URL, json=request_data, cookies=kaptl_cookie)
            else:
                response = session.post(KAPTL_PARSE_URL, json=request_data)
            response_content = response.json()
            if response.status_code and response_content["success"]:
                print "Rules were parsed successfully"
                return response_content["appName"]
            else:
                print "ERROR: There was a problem with parsing the rules"
                if response_content["compilerOutput"]:
                    print response_content["compilerOutput"]
                return None
        except requests.exceptions.RequestException:
            print("ERROR: API is unavailable at the moment, please try again later")
            sys.exit()

    @staticmethod
    def get_file_info(session, app_name, rules, stack, angular_only=False, is_update=False):
        print "Downloading the generated app..."
        request_data = dict(app={
            'id': 0,
            'name': app_name,
            'rules': rules,
            'stack': stack
        }, angularOnly=angular_only, isUpdate=is_update)

        try:
            response = session.post(KAPTL_DOWNLOAD_URL, json=request_data)
            response_content = response.json()
            if response.status_code and response_content["success"]:
                return response_content["fileUrl"], response_content["fileName"]
            else:
                return None
        except requests.exceptions.RequestException:
            print("ERROR: API is unavailable at the moment, please try again later.")
            sys.exit()

    @staticmethod
    def download_file(session, file_info):
        try:
            with open(file_info[1], 'wb') as f:
                r = session.get(file_info[0], stream=True)
                total_length = int(r.headers.get('content-length'))
                bar = pyprind.ProgBar(total_length / 1024)
                if total_length is None:  # no content length header
                    f.write(r.content)
                else:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                        bar.update()
        except IOError:
            print "ERROR: Couldn't download a file"
            sys.exit()

    @staticmethod
    def unzip_archive(filename, existing):
        try:
            with open(filename, "rb") as f:
                z = zipfile.ZipFile(f)
                if existing:
                    result = Utils.query_yes_no("This action may override changes you already made to your project "
                                                "in the current directory. Do you want to proceed?")
                    if result == "yes" or result == "y":
                        for name in z.namelist():
                            z.extract(name, os.getcwd())
                    elif result == "no" or result == "n":
                        print "Exiting the program..."
                else:
                    for name in z.namelist():
                        z.extract(name, os.getcwd())
            try:
                print "Cleaning up..."
                os.remove(filename)
            except IOError:
                print "ERROR: Couldn't delete a zip file"
        except IOError:
            print "ERROR: Couldn't unzip the file"
