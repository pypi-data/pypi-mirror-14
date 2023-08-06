import os

import subprocess

from app.exceptions import MSBuildNotFoundException, MSBuildFailedException


class Builder:
    def __init__(self, msbuild=None):
        if msbuild is None:
            self.msbuild = r'C:\Program Files (x86)\MSBuild\14.0\bin\MSBuild.exe'
        else:
            self.msbuild = msbuild

    def build(self, project_path):
        # make sure msbuild is available
        if not os.path.isfile(self.msbuild):
            raise MSBuildNotFoundException("MSBuild not found. path is " + self.msbuild)

        arg1 = "/t:Build"
        arg2 = "/p:Configuration=Debug"
        arg3 = "/verbosity:minimal"
        p = subprocess.call([self.msbuild, project_path, arg1, arg2, arg3])
        if p != 0:
            raise MSBuildFailedException("MSBuild failed to build the project")

        return True
