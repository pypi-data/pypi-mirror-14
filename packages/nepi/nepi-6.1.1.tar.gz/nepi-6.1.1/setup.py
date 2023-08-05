#!/usr/bin/env python

from distutils.core import setup

# python2 or python3 ?
import sys
PY2 = sys.version_info[0] == 2

# read version
# while cleaning up version.py might just not be there
try:
    from nepi.util.version import version_tag
except:
    version_tag = 'cleaningup'

### NOTE: these 2 files are made available at install-time in MANIFEST.in
# read licence info
with open("COPYING") as f:
    license = f.read()
with open("README.md") as f:
    long_description = f.read()

### requirements - used by pip install
required_modules = [ ]
   # we are now using six for a portable code
required_modules.append('six')
   # ipaddr in py2 used to be a separate lib
   # within recent py3, it is now in standard library but named ipaddress
if PY2:
    required_modules.append('ipaddr')
   # this is required regardless of the python version
required_modules.append('networkx')
   # refrain from mentioning these ones that are not exactly crucial
   # and that have additional, non-python, dependencies
   # that can easily break the whole install
#required_modules.append('matplotlib')
#required_modules.append('pygraphviz')

setup(
    name             = "nepi",
    version          = version_tag,
    description      = "Network Experiment Management Framework",
    long_description = long_description,
    license          = license,
    author           = "Alina Quereilhac",
    author_email     = "alina.quereilhac@inria.fr",
    download_url     = "http://build.onelab.eu/nepi/nepi-{v}.tar.gz".format(v=version_tag),
    url              = "http://nepi.inria.fr/",
    platforms        = "Linux, OSX",
    packages         = [
        "nepi",
        "nepi.execution",
        "nepi.resources",
        "nepi.resources.all",
        "nepi.resources.linux",
        "nepi.resources.linux.ccn",
        "nepi.resources.linux.ns3",
        "nepi.resources.linux.ns3.ccn",
        "nepi.resources.linux.netns",
        "nepi.resources.netns",
        "nepi.resources.ns3",
        "nepi.resources.ns3.classes",
        "nepi.resources.omf",
        "nepi.resources.planetlab",
        "nepi.resources.planetlab.ns3",
        "nepi.resources.planetlab.openvswitch",
        "nepi.util",
        "nepi.util.parsers",
        "nepi.data",
        "nepi.data.processing",
        "nepi.data.processing.ccn",
        "nepi.data.processing.ping"],
    package_data     = {
        "nepi.resources.planetlab" : [ "scripts/*.py" ],
        "nepi.resources.linux" : [ "scripts/*.py" ],
        "nepi.resources.linux.ns3" : [ "dependencies/*.tar.gz" ]
    },
    install_requires = required_modules,
)
