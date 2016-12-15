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

class bigtop_toolchain::env {
  case "$::operatingsystem $::operatingsystemrelease" {
    default: { $java_version = '1.8.0' }
    }
  $java = "java-${java_version}"

  case $architecture {
    'amd64' : { $arch= "amd64" }
  }
  case $operatingsystem {
    'Fedora','Centos', 'Amazon': {
      $javahome = "/usr/lib/jvm/${java}"
    }
  }
  file { '/etc/profile.d/bigtop.sh':
    content => template('bigtop_toolchain/jenkins.sh'),
    ensure => present,
    owner  => root,
    group  => root,
    mode   => 644,
  }
}

