from stackformation import (Infra, BotoSession)
from stackformation.aws import (Ami)
from stackformation.aws.stacks import (ec2, vpc, iam,
                                        asg, )


def common_stacks(infra):

    # create VPC
    vpc_stack = infra.add_stack(vpc.VPCStack())


def prod_stacks(infra):

    prod = infra.create_sub_infra("Prod")

    common_stacks(prod)

    vpc_stack = prod.find_stack(vpc.VPCStack)

    vpc_stack.base_cidr = "10.10"

    return prod


def dev_stacks(infra):

    dev = infra.create_sub_infra("Dev")

    common_stacks(dev)

    vpc_stack = dev.find_stack(vpc.VPCStack)

    vpc_stack.base_cidr = "10.20"

    return dev

def staging_stacks(infra):

    staging = infra.create_sub_infra("Staging")

    common_stacks(staging)

    vpc_stack = staging.find_stack(vpc.VPCStack)

    vpc_stack.base_cidr = "10.30"

    return staging





def ubuntu_ami():
    ami = Ami("WebUbuntu", "ubuntu")
    ami.add_role('sudo-nopw', {}, 100)
    ami.add_role('users', {'githubusers':[ 'ibejohn818'] }, 200)
    return ami

def aws_linux_ami():
    ami = Ami("WebUbuntu", "awslinux")
    ami.add_role('sudo-nopw', {}, 100)
    ami.add_role('users', {'githubusers':[ 'ibejohn818'] }, 200)
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

prod_infra = prod_stacks(infra)
dev_infra = dev_stacks(infra)
staging_infra = staging_stacks(infra)
