import os, imp

from yac.lib.paths import get_config_path, get_lib_path
from yac.lib.registry import set_remote_string_w_challenge, get_remote_value, get_registry_keys
from yac.lib.registry import set_local_value, get_local_value, delete_local_value
from yac.lib.variables import get_variable
from yac.lib.file import get_file_contents

# the three functions that all services leverage.
# services can either use the defaults, or provide their
# own versions

def get_stack_name( params ):

    return get_namer_module().get_stack_name( params )

def get_resource_name( params , resource):

    return get_namer_module().get_resource_name( params , resource)

def get_namer_module():

    return imp.load_source('yac.lib.naming',get_namer())

def get_namer():

    yac_namer = get_local_value('yac_namer')

    if not yac_namer:

        # load default namer
        yac_namer = os.path.join( get_lib_path(),'naming_default.py')

    return yac_namer

def set_namer(service_descriptor, vpc_prefs):

    # if a namer is specified as part of the servicefile
    if get_variable(service_descriptor, "resource-namer",""):

        service_namer_path = get_variable(service_descriptor, "resource-namer","")

        create_namer_customization(service_namer_path)

    # if a namer is specified as part of the vpc preferences
    elif get_variable(vpc_prefs, "resource-namer",""):

        vpc_prefs_namer_path = get_variable(vpc_prefs, "resource-namer","")

        create_namer_customization(vpc_prefs_namer_path) 

    else:

        # use the default namer
        yac_default_namer = os.path.join( get_lib_path(),'naming_default.py')

        set_local_value('yac_namer',yac_default_namer)

def create_namer_customization(service_namer_path):

    namer_code = get_file_contents(service_namer_path)

    if namer_code:

        # write namer code to file under lib
        namer_file_name = 'service_namer.py'
        yac_namer_path = os.path.join( get_lib_path(),'customizations', namer_file_name)

        with open(yac_namer_path,'w') as yac_namer_path_fp:
           yac_namer_path_fp.write(namer_code)

        # save namer to local db
        set_local_value('yac_namer',yac_namer_path)

