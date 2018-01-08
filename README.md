Stackformation Demo
-------------------
This repo contains demonstrations of stackformation infrastructures.
You can quickly launch and destroy these infrastructures to get an understanding of how to use the framework or even use these as a starting base.

Perferred method of execution is docker as all the dependencies are installed. ( Python 3.5.x / Ansible / Packer / AWSCLI )
The bash scripts run.sh. (*nix) & run-osx.sh (MacOS) wrap the docker container and link your AWSCLI credentials to the container. ( Windows coming soon )

Example MacOS:   
_Build AMI's and mark active_  
`./run-osx.sh -z stacks-nat-gw-asg.py images build web -a`   

![ami-build](https://s3.us-east-2.amazonaws.com/stf-assets/build-ami.gif)

_Build Cloudformation Stacks_   
`./run-osx.sh -z stacks-nat-gw-asg.py stacks build`

