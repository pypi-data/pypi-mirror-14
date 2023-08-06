#!/usr/bin/env python

import argparse, getpass
from yac.lib.container.api import get_connection_str
from yac.lib.container.push import push_image

def main():
	
	parser = argparse.ArgumentParser(description='Push images from a remote host to docker hub.')     

	# required args           
	parser.add_argument('label',  help='the image label to push to hub (e.g. nordstromsets/confluence:5.8.8)' )
	parser.add_argument('ip',     help='the ip address of the ec2 instance that contains the image')

	# pull out args
	args = parser.parse_args()
	image_label = args.label
	target_host_ip = args.ip

	# get connection string for the docker remote api on the target host
	docker_api_conn_str = get_connection_str( target_host_ip )

	# get username/pwd/email for docker hub account
	hub_uname=raw_input('Hub username: ')
	hub_pwd=getpass.getpass('Hub password: ')
	hub_email=raw_input('Hub email: ')

	# sanity check
	raw_input('About to push image %s on %s to docker hub. Hit <enter> to continue...'%(image_label, target_host_ip))

	# push the image
	push_image( image_label,
	            hub_uname,
	            hub_pwd,
	            hub_email,
	            docker_api_conn_str )
