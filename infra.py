from stackformation import (Infra, BotoSession)
from stackformation.aws import (Ami)
from stackformation.aws.stacks import (ec2, vpc, iam,
                                        asg, )








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

Ami.ANSIBLE_DIR='./ansible'

session = BotoSession(region_name='us-west-1')

infra = Infra('StackDemo', session)

infra.add_image(ubuntu_ami())
