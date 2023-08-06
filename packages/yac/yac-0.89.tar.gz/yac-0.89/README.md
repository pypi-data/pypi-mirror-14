# yac portable services

## Your service, running on your VPC, from nothing to ka-ching, in an hour.

* Have access to an AWS VPC? 
* Want to run a service on your VPC using Docker containers?
* Have a spare hour?
* Then let's get started! 

[Quick Start Guide](https://yac-stacks.atlassian.net/wiki/display/YAC/Quick+Start+Guide)

## What is yac?

* A workflow system that does for services what docker did for applications
  * docker helped make it easy to find, run, define, and share individual applications 
  * yac does the same for services
* A cli app that lets you easily find, run, define, and share web service templates
  * yac registry works just like the docker registry
  * services are defined as templates in json
  * services templates can be browsed, instantiated, registered, and cloned via the yac registry

## What is a service?
* An application that provides some useful function
* An application that can be implemented using one of more Docker containers

# Intruiged?

Read more at:
[Your Automated Cloud](https://yac-stacks.atlassian.net/wiki/display/YAC/Your+Automated+Cloud)


# Want to contribute?

## Repo

clone [from here](https://bitbucket.org/thomas_b_jackson/yac) 

## Testing

Get unit tests to pass

>> python -m unittest discover yac/tests
