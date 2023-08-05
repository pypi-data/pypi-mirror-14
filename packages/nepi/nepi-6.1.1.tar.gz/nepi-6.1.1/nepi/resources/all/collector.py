#
#    NEPI, a framework to manage network experiments
#    Copyright (C) 2013 INRIA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as
#    published by the Free Software Foundation;
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Alina Quereilhac <alina.quereilhac@inria.fr>

from nepi.execution.attribute import Attribute, Flags, Types
from nepi.execution.trace import Trace, TraceAttr
from nepi.execution.resource import ResourceManager, clsinit_copy, \
        ResourceState, ResourceAction

import os
import tempfile

@clsinit_copy
class Collector(ResourceManager):
    """ The collector entity is reponsible of collecting traces
    of a same type associated to RMs into a local directory.

    .. class:: Class Args :

        :param ec: The Experiment controller
        :type ec: ExperimentController
        :param guid: guid of the RM
        :type guid: int

    """
    _rtype = "Collector"
    _help = "A Collector can be attached to a trace name on another " \
        "ResourceManager and will retrieve and store the trace content " \
        "in a local file at the end of the experiment"
    _platform = "all"

    @classmethod
    def _register_attributes(cls):
        cls._register_attribute(
            Attribute("traceName", 
                      "Name of the trace to be collected", 
                      flags = Flags.Design))
        cls._register_attribute(
            Attribute("subDir", 
                      "Sub directory to collect traces into", 
                      flags = Flags.Design))
        cls._register_attribute(
            Attribute("rename", 
                      "Name to give to the collected trace file", 
                      flags = Flags.Design))

    def __init__(self, ec, guid):
        super(Collector, self).__init__(ec, guid)
        self._store_path =  None

    @property
    def store_path(self):
        return self._store_path
   
    def do_provision(self):
        trace_name = self.get("traceName")
        if not trace_name:
            self.fail()
            
            msg = "No traceName was specified"
            self.error(msg)
            raise RuntimeError(msg)

        self._store_path = self.ec.run_dir

        subdir = self.get("subDir")
        if subdir:
            self._store_path = os.path.join(self.store_path, subdir)
        
        msg = "Creating local directory at {} to store {} traces "\
              .format(self.store_path, trace_name)
        self.info(msg)

        try:
            os.makedirs(self.store_path)
        except OSError:
            pass

        super(Collector, self).do_provision()

    def do_deploy(self):
        self.do_discover()
        self.do_provision()

        super(Collector, self).do_deploy()

    def do_release(self):
        trace_name = self.get("traceName")
        rename = self.get("rename") or trace_name

        msg = "Collecting '{}' traces to local directory {}"\
              .format(trace_name, self.store_path)
        self.info(msg)

        rms = self.get_connected()
        for rm in rms:
            fpath = os.path.join(self.store_path, "{}.{}"\
                                 .format(rm.guid, rename))

            try:
                result = self.ec.trace(rm.guid, trace_name)
                print("collector.do_release ..")
                with open(fpath, "w") as f:
                    f.write(result)
            except:
                import traceback
                err = traceback.format_exc()
                msg = "Couldn't retrieve trace {} for {} at {} "\
                    .format(trace_name, rm.guid, fpath)
                self.error(msg, out = "", err = err)
                continue

        super(Collector, self).do_release()

    def valid_connection(self, guid):
        # TODO: Validate!
        return True

