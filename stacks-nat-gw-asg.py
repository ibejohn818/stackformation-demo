import os
from stackformation import (BotoSession, Infra)
from stackformation.aws import (Ami)
from stackformation.aws.stacks import (vpc, asg, elb, iam, s3,
                                        ec2, sns, alarms )


def common_stacks(infra):

    # add VPC Stack
    vpc_stack = infra.add_stack(vpc.VPCStack())

    # security groups
    sf_sg = vpc_stack.add_security_group(vpc.SelfReferenceSecurityGroup())
    ssh_sg = vpc_stack.add_security_group(vpc.SSHSecurityGroup("SSHAll"))
    web_sg = vpc_stack.add_security_group(vpc.WebSecurityGroup("WebAll"))

    # s3 stack
    s3_stack = infra.add_stack(s3.S3Stack("MediaBuckets"))

    pub_media_bucket = s3_stack.add_bucket(s3.S3Bucket("Media"))
    pub_media_bucket.public = True

    # iam stack
    iam_stack = infra.add_stack(iam.IAMStack("BaseRoles"))

    # ec2 profile
    ec2_profile = iam_stack.add_role(iam.EC2Profile("WebServer"))
    # give role write access to the s3 bucket
    ec2_profile.add_policy(iam.S3FullBucketAccess(pub_media_bucket))

    # create a user for codedeploy
    codedeploy_user = iam_stack.add_user(iam.IAMUser('CodeDeoloyUser'))

    # alarms
    alarm_stack = infra.add_stack(alarms.AlarmStack("Alarms"))
    alarm_stack.add_topic(sns_stack)

    # create rds stack
    # rds_stack = infra.add_stack(rds.RDSStack("WebApp", vpc))
    # rds_stack.db_type = "MySQL"
    # rds_stack.db_version = "5.6"


def prod_stacks(infra):

    # create production sub-infra
    prod = infra.create_sub_infra("Prod")

    # init common stacks
    common_stacks(prod)

    # configure production VPC with 3 AZ's
    vpc_stack = prod.find_stack(vpc.VPCStack)
    vpc_stack.num_azs = 3
    # add nat-gateway
    vpc_stack.nat_gateway = True

    sf_sg = vpc_stack.find_security_group(vpc.SelfReferenceSecurityGroup)
    ssh_sg = vpc_stack.find_security_group(vpc.SSHSecurityGroup)
    web_sg = vpc_stack.find_security_group(vpc.WebSecurityGroup)


    elb_stack = prod.add_stack(elb.ELBStack('Web', vpc))
    elb_stack.add_security_group(sf_sg)
    elb_stack.add_security_group(web_sg)

    


    return prod


def dev_stacks(infra):
    pass


def web_ubuntu_ami():

    ami = Ami("WebUbuntuNatGateway", 'ubuntu')
    ami.add_role('common-pkgs', {}, 1)
    ami.add_role('sudo-nopw', {}, 100)
    ami.add_role('users', {'githubusers':[ 'ibejohn818' ] }, 200)
    ami.add_role("nginx", {}, 300)
    return ami

def aws_bastion_ami():

    ami = Ami("BastionAwsNatGateway", 'awslinux')
    ami.add_role('common-pkgs', {}, 1)
    ami.add_role('sudo-nopw', {}, 100)
    ami.add_role('users', {'githubusers':[ 'ibejohn818' ] }, 200)
    return ami

# ANSIBLE PATH
Ami.ANSIBLE_DIR="{}/ansible".format(os.path.dirname(os.path.realpath(__file__)))


session = BotoSession(region_name='us-east-2')

infra = Infra('NatDemo', session)

# create sns topic for alarms
# top level sns topic
sns_stack = infra.add_stack(sns.SNSTopicStack("AlarmNotifications"))
# topic subscriptions
## slack subscription
slack_sub = sns_stack.add_subscription(sns.SlackSubscription("AwsAlarms"))
## email subscription
email_sub = sns_stack.add_subscription(sns.EmailSubscription('EmailNotify'))
infra.add_vars({
    'InputEmailNotifySNSEmailAddress': 'john@johnchardy.com'
})


# add ami's to infra
web_ubuntu = web_ubuntu_ami()
aws_bastion = aws_bastion_ami()

infra.add_image(web_ubuntu)
infra.add_image(aws_bastion)

prod = prod_stacks(infra)
dev = dev_stacks(infra)
