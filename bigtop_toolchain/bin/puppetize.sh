#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use /etc/os-release to determine Linux Distro

if [ -f /etc/os-release ]; then
    . /etc/os-release
else
    if [ -f /etc/redhat-release ]; then
	if grep "CentOS release 6" /etc/redhat-release >/dev/null ; then
	    ID=centos
	    VERSION_ID=6
	fi
    else
	echo "Unknown Linux Distribution."
	exit 1
    fi
fi

case ${ID}-${VERSION_ID} in
    centos-6*)
        rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-6.noarch.rpm
	yum -y install curl sudo unzip wget puppet tar
	;;
    centos-7*)
        rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm
	yum -y install hostname curl sudo unzip wget puppet
	;;
    *)
	echo "Unsupported OS ${ID}-${VERSION_ID}."
	exit 1
esac

puppet module install puppetlabs-stdlib

case ${ID} in
   debian|ubuntu)
      puppet module install puppetlabs-apt;;
esac
