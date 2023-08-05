import argparse
from fabric.api import *

parser = argparse.ArgumentParser()
parser.add_argument('--user', help='the target user', 
                    action='store', default='ubuntu', dest='user')
parser.add_argument('--hosts', help='the target address', 
                    action='store', dest='hosts')

subparsers = parser.add_subparsers(dest="subparser_name") 

install = subparsers.add_parser('install', help='install HAProxy')

config = subparsers.add_parser('config', help='configure HAProxy')
config.add_argument('--upload-conf', help='upload configuration file to the target host',
                    action='store', default=False, dest='upload_conf')
config.add_argument('--configure-keepalived', help='configure keepalived',
                    action='store_true', default=False, dest='configure_keepalived')
config.add_argument('--router_id', help='Keepalived router id e.g. lb1',
                    action='store', default=False, dest='router_id')
config.add_argument('--priority', help='Keepalived priority e.g. 150',
                    action='store', default=False, dest='priority')
config.add_argument('--state', help='Keepalived state e.g. MASTER',
                    action='store', default=False, dest='state')
config.add_argument('--interface', help='Keepalived binding interface e.g. eth0',
                    action='store', default=False, dest='interface')
config.add_argument('--vip', help='Keepalived virtual ip e.g. CONTROLLER_VIP',
                    action='store', default=False, dest='vip')
gen_conf = subparsers.add_parser('gen-conf', help='generate the example configuration to the current location')

args = parser.parse_args()

conf_haproxy_cfg = """global
  daemon

defaults
  mode http
  maxconn 10000
  timeout connect 10s
  timeout client 10s
  timeout server 10s

listen stats
  bind 0.0.0.0:9999
  mode http
  stats enable
  stats uri /stats
  stats realm HAProxy\ Statistics
  stats auth admin:admin

listen dashboard_cluster
  bind 0.0.0.0:80
  balance  source
  option  tcpka
  option  httpchk
  server controller1 controller1:80 check inter 2000 rise 2 fall 5
  server controller2 controller2:80 check inter 2000 rise 2 fall 5

listen galera_cluster
  bind 0.0.0.0:3306
  balance  source
  mode tcp
  option tcpka
  option mysql-check user haproxy
  server controller1 controller1:3306 check inter 2000 rise 2 fall 5
  server controller2 controller2:3306 backup check inter 2000 rise 2 fall 5

listen glance_api_cluster
  bind 0.0.0.0:9292
  balance  source
  option  tcpka
  option  httpchk
  server controller1 controller1:9292 check inter 2000 rise 2 fall 5
  server controller2 controller2:9292 check inter 2000 rise 2 fall 5

listen glance_registry_cluster
  bind 0.0.0.0:9191
  balance  source
  option  tcpka
  server controller1 controller1:9191 check inter 2000 rise 2 fall 5
  server controller2 controller2:9191 check inter 2000 rise 2 fall 5

listen keystone_admin_cluster
  bind 0.0.0.0:35357
  balance  source
  option  tcpka
  option  httpchk
  server controller1 controller1:35357 check inter 2000 rise 2 fall 5
  server controller2 controller2:35357 backup inter 2000 rise 2 fall 5

listen keystone_public_internal_cluster
  bind 0.0.0.0:5000
  balance  source
  option  tcpka
  option  httpchk
  server controller1 controller1:5000 check inter 2000 rise 2 fall 5
  server controller2 controller2:5000 backup inter 2000 rise 2 fall 5

listen nova_ec2_api_cluster
  bind 0.0.0.0:8773
  balance  source
  option  tcpka
  server controller1 controller1:8773 check inter 2000 rise 2 fall 5
  server controller2 controller2:8773 check inter 2000 rise 2 fall 5

listen nova_compute_api_cluster
  bind 0.0.0.0:8774
  balance  source
  option  tcpka
  option  httpchk
  server controller1 controller1:8774 check inter 2000 rise 2 fall 5
  server controller2 controller2:8774 check inter 2000 rise 2 fall 5

listen nova_metadata_api_cluster
  bind 0.0.0.0:8775
  balance  source
  option  tcpka
  server controller1 controller1:8775 check inter 2000 rise 2 fall 5
  server controller2 controller2:8775 check inter 2000 rise 2 fall 5

listen cinder_api_cluster
  bind 0.0.0.0:8776
  balance  source
  option  tcpka
  option  httpchk
  server controller1 controller1:8776 check inter 2000 rise 2 fall 5
  server controller2 controller2:8776 check inter 2000 rise 2 fall 5

listen ceilometer_api_cluster
  bind 0.0.0.0:8777
  balance  source
  option  tcpka
  server controller1 controller1:8777 check inter 2000 rise 2 fall 5
  server controller2 controller2:8777 check inter 2000 rise 2 fall 5

listen nova_vncproxy_cluster
  bind 0.0.0.0:6080
  balance  source
  option  tcpka
  server controller1 controller1:6080 check inter 2000 rise 2 fall 5
  server controller2 controller2:6080 check inter 2000 rise 2 fall 5

listen neutron_api_cluster
  bind 0.0.0.0:9696
  balance  source
  option  tcpka
  option  httpchk
  server controller1 controller1:9696 check inter 2000 rise 2 fall 5
  server controller2 controller2:9696 check inter 2000 rise 2 fall 5

listen swift_proxy_cluster
  bind 0.0.0.0:8080
  balance  source
  option  tcpka
  server controller1 controller1:8080 check inter 2000 rise 2 fall 5
  server controller2 controller2:8080 check inter 2000 rise 2 fall 5
"""

def main():
    if args.subparser_name == 'install':
        from playback import haproxy_install
        target = haproxy_install.HaproxyInstall(user=args.user, hosts=args.hosts.split(','))
        execute(target._install)
    if args.subparser_name == 'config':
        from playback import haproxy_config
        target = haproxy_config.HaproxyConfig(user=args.user, hosts=args.hosts.split(','))
        if args.upload_conf:
            execute(target._upload_conf, args.upload_conf)
        if args.configure_keepalived:
            execute(target._configure_keepalived, args.router_id, args.priority, 
                    args.state, args.interface, args.vip)
    if args.subparser_name == 'gen-conf':
        with open('haproxy.cfg', 'w') as f:
            f.write(conf_haproxy_cfg)


if __name__ == '__main__':
    main()
