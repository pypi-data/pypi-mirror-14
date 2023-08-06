#!/usr/bin/env python

import cirrus.chef_tools as ct
import arrow, copy
from cirrus.fabric_helpers import FabricHelper
from fabric.operations import run, settings, env
from fabric.decorators import hosts


for x in ['sapi1.sapitest001.cloudant.com', 'lb1.sapitest001.cloudant.com']:

    with FabricHelper(x, 'evansde77', '/Users/evansde77/.ssh/id_rsa'):
        run('/bin/date')




# REPO = "/Users/evansde77/Documents/chef-repo"


# r = ct.ChefRepo(REPO)

# attrs = {
#     "override_attributes.cloudant_sapi.applications.wilson.installs.wilson": "X.Y.Z",
#     "override_attributes.cloudant_sapi.applications.emissions_test.installs.emissions_test": "A.B.C"

# }

# cert = "/Users/evansde77/.chef/evansde77.pem"
# query = "environment:sapi_testing AND (roles:load_balancer OR roles:sapi)"

# print ct.list_nodes('https://chef.cloudant.com', cert, 'evansde77', query, attribute='automatic.ip.public')


# print ct.list_nodes('https://chef.cloudant.com', cert, 'evansde77', query, attribute='name', format_str='{}.cloudant.com')



