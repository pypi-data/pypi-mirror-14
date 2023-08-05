### updated by the toplevel Makefile
version_tag="6.0.7"
scm_url="git://git.onelab.eu/nepi.git"
import socket
 
def version_core (more=None):
    if more is None: more={}
    core = { 'code_tag' : version_tag,
             'code_url' : scm_url,
             'hostname' : socket.gethostname(),
             }
    core.update(more)
    return core
