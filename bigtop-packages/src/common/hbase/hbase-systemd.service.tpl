[Unit]
Description=The HBase __SERVICE__ daemon
After=network.target
After=NetworkManager.target

[Service]
Type=simple
ExecStart=/usr/lib/hbase/libexec/hbase-__SERVICE__ start
ExecStop=/usr/lib/hbase/libexec/hbase-__SERVICE__ stop
PIDFile=/var/run/hbase/hbase-hbase-__SERVICE__.pid

#######################################
# Note: Below are cgroup options
#######################################
#Delegate=true
#CPUAccounting=true
#CPUShares=1024

[Install]
WantedBy=multi-user.target
