#!/usr/bin/env python

import argparse
from yac.lib.naming import get_stack_name
from yac.lib.container.api import get_connection_str
from yac.lib.container.build import build_image, get_image_name
from yac.lib.container.config import load_container_configs, get_aliases

def main():
	
	parser = argparse.ArgumentParser(description='Build image for an arbitrary container.')     

	# required args   
	parser.add_argument('path',      help='the path to the dockerfile for this image')        
	parser.add_argument('label',     help='version label of to tag image with' )
	parser.add_argument('ip',        help='the ip address of the ec2 instance to build to')

	# pull out args
	args = parser.parse_args()
	build_path = args.path
	target_host_ip = args.ip

	# get the image tag
	image_tag = args.label

	# get connection string for the docker remote api on the target host
	docker_api_conn_str = get_connection_str( target_host_ip )

	# get connection string for the docker remote api on the target host
	docker_api_conn_str = get_connection_str( target_host_ip )

	# start building ...
	# sanity check
	raw_input('About to build image for %s on %s using dockerfile at %s. Hit <enter> to continue...'%(image_tag, target_host_ip, build_path))

	# build the image
	build_image( image_tag, build_path, docker_api_conn_str )
