from stackformation import (Infra, BotoSession)
from stackformation.aws import (Ami)
from stackformation.aws.stacks import (ec2, vpc, iam,
                                        asg, )


def common_stacks(infra):

    # create VPC
    vpc_stack = infra.add_stack(vpc.VPCStack())


def prod_infra(infra):
    pass

def dev_infra(infra):
    pass

def staging_stacks(infra):
    pass





def ubuntu_ami():
    ami = Ami("WebUbuntu", "ubuntu")
    ami.add_role('sudo-nopw', {}, 100)
    ami.add_role('users', {'githubusers':[ 'ibejohn818', 'slikk66'] }, 200)
    return ami

def aws_linux_ami():
    ami = Ami("WebUbuntu", "awslinux")
    ami.add_role('sudo-nopw', {}, 100)
    ami.add_role('users', {'githubusers':[ 'ibejohn818', 'slikk66'] }, 200)
    return ami

# set path to ansible directory
Ami.ANSIBLE_DIR='./ansible'
# set list to individual ansible roles
# Ami.ANSIBLE_ROLES = [
    # '/path/to/role',
    # '/path/to/another/role'
# ]


session = BotoSession(region_name='us-west-1')

infra = Infra('StackDemo', session)

infra.add_image(ubuntu_ami())
