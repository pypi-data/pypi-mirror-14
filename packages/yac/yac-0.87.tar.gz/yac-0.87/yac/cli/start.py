#!/usr/bin/env python

import argparse, os, inspect, jmespath, json
from yac.lib.service import get_service, get_service_parmeters
from yac.lib.stack import get_stack_templates
from yac.lib.container.start import start
from yac.lib.container.config import get_aliases, env_ec2_to_api, get_volumes_map
from yac.lib.container.config import get_port_bindings
from yac.lib.container.api import get_connection_str
from yac.lib.vpc import get_vpc_prefs

def get_conf_dir():

    # return the abs path to the config directory
    return os.path.join(os.path.dirname(inspect.getfile(slib)),'../config')

def get_env_param(env,suffix):

    if suffix:
        env_param = '%s/%s'%(suffix,env)
    else:
        env_param = env

    return env_param

def load_user_variables(taskdef_template_vars, variables_str):

    if variables_str:

        user_variables = json.loads(variables_str)

        taskdef_template_vars.update(user_variables.copy())

    return taskdef_template_vars    

def main():

    parser = argparse.ArgumentParser(description='Starts a containers per the container defintion in a Servicefile')

    # required args
    parser.add_argument('service_alias', help='alias of the stack where this container should be run'),
    parser.add_argument('name',  help='name of container to start')                                          
    parser.add_argument('servicefile',    help='path to Servicefile')

    parser.add_argument('ip',  help='ip of ec2 host to start container on') 
    parser.add_argument('-s', '--source', 
                        help='image source for this container (hub=dockerhub, local=image on host filesystem)', 
                        choices=['hub','local'], 
                        default='local')
    parser.add_argument('-e',
                        '--env',  help='the environment to build stack cluster for', 
                                  choices=  ['dev','stage','prod'],
                                  default= "dev")    
    parser.add_argument('-c', '--cmd', 
                        help='run this cmd instead of the stock container CMD (see associated Dockerfile)')
    parser.add_argument('-d','--dryrun',  help='dry run the container start by printing rendered template to stdout', 
                                          action='store_true')
    parser.add_argument('-p',
                        '--params',  help='path to a file containing additional, static, service parameters (e.g. vpc params, of service constants)',
                                     default='') 

    args = parser.parse_args()

     # determine service defintion, complete service name, and service alias based on the args
    service_descriptor, service_name, servicefile_path = get_service(args.servicefile) 

    # get vpc preferences in place
    vpc_prefs = get_vpc_prefs()

    # get the service parameters for use with yac-ref's in service templates
    service_parmeters = get_service_parmeters(args.service_alias, args.env, args.params, 
                                              service_name, service_descriptor,
                                              servicefile_path, vpc_prefs)

    # get cloud formation template for the service requested and apply yac intrinsic 
    # functions (yac-ref, etc.) using  the service_parmeters
    stack_template = get_stack_templates(service_descriptor,
                                         vpc_prefs,  
                                         service_parmeters)

    app_taskdefs = stack_template['Resources']['TaskDefs']['Properties']

    image_tag = jmespath.search("ContainerDefinitions[?Name=='%s'].Image"%args.name,app_taskdefs)[0]

    # get the ip address of the target host
    target_host_ip = args.ip

    # get connection string for the docker remote api on the target host
    docker_api_conn_str = get_connection_str( target_host_ip )

    if jmespath.search("ContainerDefinitions[?Name=='%s'].Environment"%args.name,app_taskdefs):
        ecs_env = jmespath.search("ContainerDefinitions[?Name=='%s'].Environment"%args.name,app_taskdefs)[0]
        env_variables = env_ec2_to_api(ecs_env)
    else:
        env_variables = {}

    # get the volumes map
    all_volumes = jmespath.search("Volumes",app_taskdefs)
    mount_points = jmespath.search("ContainerDefinitions[?Name=='%s'].MountPoints"%args.name,app_taskdefs)[0]
    volumes_map, volumes_bindings = get_volumes_map(all_volumes,mount_points)

    # get the volumes
    # volumes_bindings = jmespath.search("volumes[*].host.sourcePath",app_taskdefs)

    # get the port bindings for this container
    port_mappings = jmespath.search("ContainerDefinitions[?Name=='%s'].PortMappings"%args.name,app_taskdefs)[0]
    port_bindings = get_port_bindings(port_mappings)

    source = 'local' if args.source=='local' else 'remote (hub)'

    user_msg = "%sStarting the %s container on %s using the %s image %s%s"%('\033[92m',
                                                            args.name,
                                                            target_host_ip,
                                                            source, 
                                                            image_tag,                                                         
                                                            '\033[0m')
    if args.dryrun:

        # do a dry-run by printing the stack template and stack parameters to stdout
        print "environment variables ... \n%s"%json.dumps(env_variables,indent=2)
        print "volumes map ... \n%s"%json.dumps(volumes_map,indent=2)
        print "volumes bindings ... \n%s"%json.dumps(volumes_bindings,indent=2)
        print "port bindings ... \n%s"%json.dumps(port_bindings,indent=2)
        print "special command ... \n%s"%args.cmd
        print user_msg

    else:

        raw_input(user_msg + "\nHit <enter> to continue..." )

        # start the container
        start(
            image_tag=image_tag,
                envs=env_variables,
                alias=args.name,
                volume_mapping=volumes_map,
                volumes_bindings=volumes_bindings,
                port_bindings=port_bindings,
                connection_str=docker_api_conn_str,
                start_cmd=args.cmd,
                image_source=args.source,
                template_vars={},
                files_to_load=[],
                volumes_from=[],
                create_only=False) 
