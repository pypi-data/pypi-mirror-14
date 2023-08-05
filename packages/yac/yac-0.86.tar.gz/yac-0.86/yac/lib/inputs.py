import boto3, jmespath, sys, json
from sets import Set
from yac.lib.variables import get_variable, set_variable
from yac.lib.naming import get_stack_name
from yac.lib.stack import stack_exists, get_asg_subnet_ids, get_stack_service_inputs_value
from yac.lib.stack import get_stack_vpc
                   
def get_inputs(params):

    user_inputs = {}

    # get dynamic input params
    if 'service-inputs' in params and 'inputs' in params['service-inputs']:

        dynamic_params = params['service-inputs']['inputs']

        for param_key in dynamic_params:

            if ('type' in dynamic_params[param_key] and dynamic_params[param_key]['type'] == 'scalar'):

                value = set_scalar_dynamic_input(params, dynamic_params, param_key)

                # accumulate the resulting inputs
                user_inputs[param_key] = value

    # convert inputs into a string and save to a variable that can be connected to the stack
    # for reference by 'yac stack' during stack updates
    user_inputs_str = json.dumps(user_inputs)
    set_variable(params,'user-inputs',user_inputs_str)


def set_scalar_dynamic_input(params, dynamic_params, param_key):

    statusquo_arg = ""                
    if 'arg' in dynamic_params[param_key]['statusquo_fxn']:
        statusquo_arg = dynamic_params[param_key]['statusquo_fxn']['arg']

    wizard_arg = ""                
    if 'arg' in dynamic_params[param_key]['wizard_fxn']:
        wizard_arg = dynamic_params[param_key]['wizard_fxn']['arg']

    options = []
    if 'options' in dynamic_params[param_key]['constraints']:
        options = dynamic_params[param_key]['constraints']['options']
    elif 'options_fxn' in dynamic_params[param_key]['constraints']:
        # call the spec'd options fxn to generate the list of options
        options_arg = ""                
        if 'arg' in dynamic_params[param_key]['constraints']['options_fxn']:
            options_arg = dynamic_params[param_key]['constraints']['options_fxn']['arg']
            options = eval(dynamic_params[param_key]['constraints']['options_fxn']['name'])(options_arg)
        else:
            options = eval(dynamic_params[param_key]['constraints']['options_fxn']['name'])()

    required = True
    if 'required' in dynamic_params[param_key]['constraints']:
        required = dynamic_params[param_key]['constraints']['required']

    value = set_scalar_input(params, 
                     param_key, 
                     dynamic_params[param_key]['description'], 
                     dynamic_params[param_key]['help'],
                     dynamic_params[param_key]['wizard_fxn']['name'],
                     required,
                     options,
                     dynamic_params[param_key]['statusquo_fxn']['name'],
                     wizard_arg,
                     statusquo_arg)

    return value

# set a scalar input in params
def set_scalar_input(params, 
                     param_key, 
                     param_desc,
                     param_help, 
                     wizard_fxn,
                     required,
                     options, 
                     statusquo_fxn, 
                     wizard_arg="",
                     statusquo_arg=""):

    value = ""

    # see if the param is already defined
    value = get_variable(params, param_key)

    if not value:

        # get the name of the stack
        stack_name = get_stack_name(params)

        if not stack_exists(stack_name):

            # this is a new stack...
            # prompt user to provide a value for this param
            value = eval(wizard_fxn)(param_desc,param_help,options,required,wizard_arg)

        else:
            # a stack for this service already exists ...
            # determine the param value currently in use
            if statusquo_arg:
                current_value = eval(statusquo_fxn)(params, statusquo_arg)
            else:
                current_value = eval(statusquo_fxn)(params)

            # give the user the choice of changing existing value
            if change_wizard(current_value, param_desc, wizard_fxn ):
                value = eval(wizard_fxn)(param_desc,param_help,options,required,wizard_arg)
            else:
                value = current_value

        if value:

            set_variable(params, param_key ,value, param_desc)

    return value 

def string_wizard(param_desc, help_msg, options, required,str_len=""):

    value = validated_input(param_desc,
                             help_msg,
                             options,
                             string_validation,
                             required,
                             str_len)

    return value

def int_wizard(param_desc, help_msg, options, required, arg=""):

    value = validated_input(param_desc,
                            help_msg, 
                            options,
                            int_validation,
                            required)

    return value    

def change_wizard(current_value, field_name, wizard_fxn):

    msg = "Current '%s' value is %s. Do you want to change it? (y/n) >> "%(field_name,current_value)

    validation_failed = True
    change = False
    options = ['y','n']

    while validation_failed:

        input = raw_input(msg)

        # validate the input
        validation_failed = string_validation(input, options)

    if input == 'y':
        change = True

    return change

def validated_input(param_desc, help_msg, options, function, required=True, optional_arg=""):

    validation_failed = True

    if required:
        param_msg = "\nThis service requires the following input: %s"%param_desc
    else:
        param_msg = "\nThis service accepts the following optional input: %s"%param_desc

    print param_msg
    print help_msg

    if options:

        input = raw_input("Press <enter> to see a list of availble options >> ")
        print "Choices include: \n%s"%pp_list(options)

    while validation_failed:

        input = raw_input("Please paste in one of the available options for %s >> "%param_desc)

        input = input.strip("'")

        # validate the input
        validation_failed = function(input, options, optional_arg)

    return input

def validated_array_input(param_desc, retry_msg, options, function):

    validation_failed = True
    array_building = True

    print "enter values one at a time, cr when done ..."

    inputs = []

    while validation_failed:

        input = raw_input(param_desc).strip("'")

        if input:
            inputs.append(input)
        else:
            validation_failed,inputs = function(inputs, options,retry_msg)

def string_validation(input,options,max_strlen=4000):

    validation_failed = False
    if options:
        if input not in options:
            validation_failed = True
            retry_msg = "Input invalid - please select from the available options"

    if max_strlen:
        if len(input)>max_strlen:
            validation_failed = True
            retry_msg = "Input invalid (too long) - please input a string with <= %s chars"%max_strlen

    if validation_failed:
        print retry_msg

    return validation_failed

def int_validation(input,options,max_value=sys.maxint):

    validation_failed = False
    if options:
        if input not in options:
            validation_failed = True
            retry_msg = "Input invalid - please select from the available options"

    if max_value:
        if input>max_value:
            validation_failed = True
            retry_msg = "Input invalid - please input an int <= %s"%max_value

    if not input.isdigit():
        validation_failed = True
        retry_msg = "Input invalid - integers only"
        
    if validation_failed:
        print retry_msg

    return validation_failed    

def input_validation(input,options,retry_msg):

    # attempt to find the vpc input
    validation_failed = input not in options

    if validation_failed:
        print retry_msg

    return validation_failed

def array_validation(inputs,options,retry_msg):

    # attempt to find the vpc input
    validation_failed = len(Set(inputs) & Set(options)) != len(inputs)

    if validation_failed:
        print retry_msg
        inputs=[]

    return validation_failed, inputs    


# set the ids of subnets to use
def set_subnets( params ):

    subnet_param_ids = {"dmz":     "dmz-subnet-ids", 
                        "public":  "public-subnet-ids", 
                        "private": "private-subnet-ids"}

    # set subnet ids of private subnets, since all stacks need this layer
    set_subnet_layer( params,
                      subnet_param_ids['private'], 
                      'private' )

    # if vpc has a DirectConnect route to corporate domain
    set_direct_connect(params)

    direct_connect = get_variable(params, 'direct-connect')

    if direct_connect:

        # if public internet access is needed
        set_external_access(params)

        if get_variable(params, 'external-access', False):
    
            # set the dmz subnet ids, since ASG should be placed in dmz
            set_subnet_layer( params,
                              subnet_param_ids['public'], 
                              'dmz' )

            # set public subnet ids
            set_subnet_layer( params,
                              subnet_param_ids['public'], 
                              'public' )
    else:

        # set public subnet ids
        set_subnet_layer( params,
                          subnet_param_ids['public'], 
                          'public' )

# get the subnet to use for a given vpc and a given layer
def set_subnet_layer( params, layer_param_id, layer_name ):

    # get the name of the stack
    stack_name = get_stack_name(params)

    # see if the subnets are already defined (usually via the vpc prefs)
    subnets_ids = get_variable(layer_param_id)

    if not subnets_ids:

        if not stack_exists(stack_name):

            vpc_id = get_variable("vpc-id")

            # use the wizard to prompt user for subnets
            subnets_ids = subnets_wizard(layer_name,vpc_id)

        else:

            # determine the existing subnets in use for this service
            if layer_name == "private":
                # get the current subnets based on the internal ELB
                ielb_name = get_resource_name(params,'ielb')
                subnets_ids = get_elb_subnet_ids(ielb_name)

            elif layer_name == "dmz":
                # get the subnets based on the auto-scaling group
                asg_name = get_resource_name(params,'asg')
                subnets_ids = get_asg_subnet_ids(asg_name)

        if subnets_ids:
            set_variable(params,
                         layer_param_id, 
                         subnets_ids, 
                         "%s subnet ids"%layer_name) 

def subnets_wizard(layer_name, vpc_id):

   subnet_ids = validated_array_input("Enter the id of a subnet in your %s subnet layer >> "%layer_name, 
                                      "One of more subnets not valid, please try again",
                                      get_subnets(vpc_id,get_azs()),
                                      array_validation)

   return subnet_ids

# get the ids of the vpcs available to this user
def get_vpc_ids():

    ec2 = boto3.client('ec2')

    # Environment tag contains VPC_MAPPING values
    vpcs = ec2.describe_vpcs()

    # get id's only
    vpc_ids = jmespath.search("Vpcs[*].VpcId", vpcs)

    return vpc_ids

# get names of available sns topics buckets
def get_s3_buckets():

    s3 = boto3.client('s3')

    buckets = s3.list_buckets()

    # get names only
    bucket_names = jmespath.search("Buckets[*].Name", buckets)

    return bucket_names

# get names of available sns topic arns
def get_sns_topic_arns():

    s3 = boto3.client('sns')

    topics = s3.list_topics()

    topics_arns = jmespath.search("Topics[*].TopicArn", topics)

    return topics_arns

# get names of available key pairs
def get_key_pairs():

    s3 = boto3.client('iam')

    public_keys = s3.list_ssh_public_keys()

    # get names only
    key_names = jmespath.search("SSHPublicKeys[*].SSHPublicKeyId", public_keys)

    return key_names

# get names of available key pairs
def get_ssl_certs():

    iam = boto3.client('iam')

    certs = iam.list_server_certificates()

    # get names only
    cert_name = jmespath.search("ServerCertificateMetadataList[*].ServerCertificateName", certs)

    return cert_name

# get names of available iam roles
def get_iam_roles():

    iam = boto3.client('iam')

    profiles = iam.list_instance_profiles()

    # get id only
    profile_ids = jmespath.search("InstanceProfiles[*].InstanceProfileId", profiles)

    return profile_ids  

# get names of available db snapshots
def get_snapshot_ids(name_search_string):

    iam = boto3.client('rds')

    filters = [{'Name':"tag:Name", 'Values' : [name_search_string]}]

    snapshots = iam.describe_db_snapshots(Filters=filters)

    # get id only
    snapshots_ids = jmespath.search("DBSnapshots[*].DBSnapshotIdentifier", snapshots)

    return snapshots_ids        

# get the zones available to this user
def get_azs():

    ec2 = boto3.client('ec2')

    # Environment tag contains VPC_MAPPING values
    azs = ec2.describe_availability_zones()

    # get id's only
    az_names = jmespath.search("AvailabilityZones[*].ZoneName", azs)

    return az_names  


# get the subnets available in a given vpc and a given set of 
# availability zones
def get_subnets(vpc_id, availabilty_zones):

    ec2 = boto3.client('ec2')
    
    subnets = ec2.describe_subnets(Filters=[
        {
            'Name': 'vpc-id',
            'Values': [
                vpc_id,
            ]
        },
        {
            'Name': 'availability-zone',
            'Values': availabilty_zones
        }])

    subnet_ids = jmespath.search('Subnets[*].SubnetId',subnets)

    return subnet_ids

def pp_list(list):
    str = ""
    for item in list:
        str = str + '* %s\n'%item

    return str


