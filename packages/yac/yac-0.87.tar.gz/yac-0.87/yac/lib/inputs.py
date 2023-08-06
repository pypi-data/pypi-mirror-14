import boto3, jmespath, sys, json, requests
from sets import Set
from yac.lib.variables import get_variable, set_variable
from yac.lib.naming import get_stack_name
from yac.lib.stack import stack_exists, get_asg_subnet_ids, get_stack_service_inputs_value
from yac.lib.stack import get_stack_vpc, get_stack_ssh_keys
                   
def get_inputs(params):

    user_inputs = {}

    # get service input params
    if 'service-inputs' in params and 'inputs' in params['service-inputs']:

        service_param = params['service-inputs']['inputs']

        for param_key in service_param:

            # handle the service input
            value = handle_service_input(params, service_param[param_key], param_key)

            # accumulate the resulting inputs
            user_inputs[param_key] = value

    # get conditional input params
    if 'service-inputs' in params and 'conditional-inputs' in params['service-inputs']:
        conditional_params = params['service-inputs']['conditional-inputs']
        
        for param_key in conditional_params:

            # get the conditional check
            conditional_input = conditional_params[param_key]['condition']['input']

            conditional_value = ""
            if 'value' in conditional_params[param_key]['condition']:
                conditional_value = conditional_params[param_key]['condition']['value']

            # get state of the input
            input_setting = get_variable(params,conditional_input,"")

            # if not conditional value specified, or a value was specified and the 
            # input setting value matches the condition value, then
            # perform the conditional check
            if (not conditional_value or 
                  (conditional_value and conditional_value == input_setting)
                ):

                # handle the conditional input
                value = handle_service_input(params, conditional_params[param_key], param_key)

                # accumulate the resulting inputs
                user_inputs[param_key] = value

    # convert inputs into a string and save to a variable that can be connected to the stack
    # for reference by 'yac stack' during stack updates
    user_inputs_str = json.dumps(user_inputs)
    set_variable(params,'user-inputs',user_inputs_str)

def handle_service_input(params, dynamic_param, param_key):

    wizard_arg = ""                
    if 'arg' in dynamic_param['wizard_fxn']:
        wizard_arg = dynamic_param['wizard_fxn']['arg']

    options = []
    if 'options' in dynamic_param['constraints']:
        options = dynamic_param['constraints']['options']

    elif 'options_fxn' in dynamic_param['constraints']:
        # call the spec'd options fxn to generate the list of options

        options_fxn = dynamic_param['constraints']['options_fxn']['name']

        if 'namespace' in dynamic_param['constraints']['options_fxn']:
            name_space = dynamic_param['constraints']['options_fxn']['name_space']
            # do an import in the options fxn
            import_statement = "from %s import %s"%(name_space,options_fxn)
            exec(import_statement)
               
        # next evaluate the options fxn
        if 'arg' in dynamic_param['constraints']['options_fxn']:
            options_arg = dynamic_param['constraints']['options_fxn']['arg']
            options = eval(options_fxn)(params,options_arg)
        else:
            options = eval(options_fxn)(params)

    required = True
    if 'required' in dynamic_param['constraints']:
        required = dynamic_param['constraints']['required']

    value = set_service_input(params, 
                     param_key, 
                     dynamic_param['description'], 
                     dynamic_param['help'],
                     dynamic_param['wizard_fxn']['name'],
                     required,
                     options,
                     wizard_arg)

    return value

# set a scalar input in params
def set_service_input(params, 
                     param_key, 
                     param_desc,
                     param_help, 
                     wizard_fxn,
                     required,
                     options, 
                     wizard_arg=""):

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
            value = get_stack_service_inputs_value(params, ['UserData', param_key])
 
            # give the user the choice of changing existing value
            if change_wizard(value, param_desc, wizard_fxn ):
                value = eval(wizard_fxn)(param_desc,param_help,options,required,wizard_arg)

        if value:

            set_variable(params, param_key,value, param_desc)

    return value 

def string_wizard(param_desc, help_msg, options, required, str_len=""):

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

def array_wizard(param_desc, help_msg, options, required, layer=""):
      
    value = validated_array_input(param_desc,
                                       help_msg,
                                       options,
                                       array_validation,
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

def validated_array_input(param_desc, help_msg, options, function, required=True, optional_arg=""):

    validation_failed = True
    array_building = True

    if required:
        param_msg = "\nThis service requires the following input: %s"%param_desc
    else:
        param_msg = "\nThis service accepts the following optional input: %s"%param_desc

    print param_msg
    print pp_help(help_msg)

    if options:

        input = raw_input("Press <enter> to see a list of availble options >> ")
        print "Choices include: \n%s"%pp_list(options)

    print "Paste in values one at a time and press Enter ( press Enter when done ) ..."

    inputs = []

    while validation_failed:

        input = raw_input("... input an item for '%s' >> "%param_desc)

        if input:
            inputs.append(input)
        else:
            validation_failed,inputs = function(inputs, options, optional_arg)

    return inputs

def validated_array_input_old(param_desc, retry_msg, options, function):

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
        
        if type(options[0])==dict:
            # pull out just the options values
            options = jmespath.search("[*].Option",options)

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

def array_validation(inputs,options,arg=""):

    validation_failed = len(Set(inputs) & Set(options)) != len(inputs)

    if validation_failed:
        retry_msg = "Input invalid - please select from the available options"
        print retry_msg
        inputs=[]

    return validation_failed, inputs    

# get the ids of the vpcs available to this user
def get_vpc_ids(params):

    ec2 = boto3.client('ec2')

    # Environment tag contains VPC_MAPPING values
    vpcs = ec2.describe_vpcs()

    # get id's only
    vpc_ids = jmespath.search("Vpcs[*].VpcId", vpcs)

    return vpc_ids

# get names of available sns topics buckets
def get_s3_buckets(params):

    s3 = boto3.client('s3')

    buckets = s3.list_buckets()

    # get names only
    bucket_names = jmespath.search("Buckets[*].Name", buckets)

    return bucket_names

# get names of available sns topic arns
def get_sns_topic_arns(params):

    s3 = boto3.client('sns')

    topics = s3.list_topics()

    topics_arns = jmespath.search("Topics[*].TopicArn", topics)

    return topics_arns

# get names of available key pairs
def get_key_pairs(params):

    s3 = boto3.client('iam')

    public_keys = s3.list_ssh_public_keys()

    # get names only
    key_names = jmespath.search("SSHPublicKeys[*].SSHPublicKeyId", public_keys)

    return key_names

# get names of available key pairs
def get_ssl_certs(params):

    iam = boto3.client('iam')

    certs = iam.list_server_certificates()

    # get names only
    cert_name = jmespath.search("ServerCertificateMetadataList[*].ServerCertificateName", certs)

    return cert_name

# get names of available iam roles
def get_iam_roles(params):

    iam = boto3.client('iam')

    profiles = iam.list_instance_profiles()

    # get id only
    profile_ids = jmespath.search("InstanceProfiles[*].InstanceProfileId", profiles)

    return profile_ids  

# get names of available db snapshots
def get_snapshot_ids(params,name_search_string):

    iam = boto3.client('rds')

    filters = [{'Name':"tag:Name", 'Values' : [name_search_string]}]

    snapshots = iam.describe_db_snapshots(Filters=filters)

    # get id only
    snapshots_ids = jmespath.search("DBSnapshots[*].DBSnapshotIdentifier", snapshots)

    return snapshots_ids        

# get the zones available to this user
def get_azs(params):

    ec2 = boto3.client('ec2')

    # Environment tag contains VPC_MAPPING values
    azs = ec2.describe_availability_zones(Filters=[{'Name': 'state','Values': ['available']}])

    # get id's only
    az_names = jmespath.search("AvailabilityZones[*].ZoneName", azs)

    return az_names  

# get CoreOS AMI suitable for use with Jira
def get_coreos_ami(params):

    ec2 = boto3.client('ec2')

    # only return CoreOS hvm releases on the stable channel
    images = ec2.describe_images(Filters=[{"Name": "name", "Values": ["CoreOS-stable*hvm"]},
                                          {"Name": "owner-id", "Values": ["595879546273"]}])

    # get image id and image name
    image_ids = jmespath.search("Images[*].{Option: ImageId, Description: Name}", images)

    return image_ids

# get the subnets available in a given vpc and a given set of 
# availability zones
def get_subnet_ids(params):

    vpc_id = get_variable(params,"vpc-id") 
    availabilty_zones = get_variable(params,"availability-zones") 

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

# find the versions (tags) available for a container image
def get_image_versions(params, image_name, registry_url='https://registry.hub.docker.com'):

    # endpoint use to determine the latest version in the registry input for this app
    endpoint_uri = "/v2/repositories/%s/tags"%(image_name)

    # hit the endpoint
    endpoint_response = requests.get(registry_url + endpoint_uri) 

    # use jmespath to extract just the version value for each
    versions = jmespath.search("results[*].name",endpoint_response.json())

    return versions

def pp_list(list):
    str = ""
    for item in list:
        str = str + '* %s\n'%item

    return str

def pp_help(help):

    if type(help)==list:
        ret = pp_list(help)
    else:
        ret = str(help)

    return ret
