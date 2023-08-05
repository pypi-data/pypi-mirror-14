"""Qingcloud init cli

Usage:
    qinginit
    qinginit config id <access_key_id>
    qinginit config key <secret_access_key>
    qigninit create <instance_type>

Options:
    -f, --file <config_file>

"""

from docopt import docopt
import os
import qingcloud.iaas
import qingcloud.misc
import time
import yaml


def init():
    global home
    home = os.getenv('HOME') + '/.config/qinginit'

    if not os.path.isdir(home):
        os.mkdir(home)
    if not os.path.isfile(home + '/config.yml'):
        open(home + '/config.yml', 'w+').close()

    # tmpconfig = load_config()
    # tmpconfig['zone'] = ''
    # tmpconfig['access_key_id'] = ''
    # tmpconfig['secret_access_key'] = ''
    # save_config(tmpconfig)

    return load_config()


def load_config():
    with open(home + '/config.yml', 'r') as f:
        tmpconfig = yaml.load(f)
    return tmpconfig


def save_config(tmpconfig):
    with open(home + '/config.yml', 'w') as f:
        f = yaml.dump(tmpconfig, default_flow_style=False)
        f.close()


def config_zone(zone):
    tmpconfig = load_config()
    tmpconfig['zone'] = zone
    save_config(tmpconfig)


def config_access_key_id(access_key_id):
    tmpconfig = load_config()
    tmpconfig['access_key_id'] = access_key_id
    save_config(tmpconfig)


def config_secret_access_key(secret_access_key):
    tmpconfig = load_config()
    tmpconfig['secret_access_key'] = secret_access_key
    save_config(tmpconfig)


def check_job(response):
    if 'job_id' not in response:
        print('your job %s is finished' % (response['action']))
        return True
    else:
        for i in range(100):
            time.sleep(5)
            r = conn.describe_jobs(
                jobs=[response['job_id']],
                zone=config['zone']
            )
            print('your job %s is %s' % (r['job_set'][0]['job_action'], r['job_set'][0]['status']))
            if r['job_set'][0]['status'] == 'successful':
                return True
        return False


def get_eip(bandwidth):
    r = conn.allocate_eips(
        bandwidth=bandwidth,
        zone=config['zone']
    )
    # print(r)
    check_job(r)
    return r['eips']


def get_route():
    r = conn.create_routers(
        zone=config['zone']
    )
    # print(r)
    check_job(r)
    return r['routers']


def get_vxnet(vxnet_name='test', vxnet_type=1):
    r = conn.create_vxnets(
        vxnet_name=vxnet_name,
        vxnet_type=vxnet_type,
        zone=config['zone']
    )
    # print(r)
    check_job(r)
    return r['vxnets']


def get_instance(image_id='trustysrvx64f', instance_type='c1m1', vxnets=['vxnet-0'], login_passwd='Qingcloud123'):
    r = conn.run_instances(
        image_id=image_id,
        instance_type=instance_type,
        vxnets=vxnets,
        login_mode='passwd',
        login_passwd=login_passwd,
        zone=config['zone']
    )
    # print(r)
    check_job(r)
    return r['instances']


def get_rdb(vxnet, rdb_username, rdb_password, rdb_type, rdb_engine='mysql', engine_version='5.5', storage_size='10'):
    r = conn.create_rdb(
        vxnet=vxnet,
        rdb_username=rdb_username,
        rdb_password=rdb_password,
        rdb_type=rdb_type,
        rdb_engine=rdb_engine,
        engine_version=engine_version,
        storage_size=storage_size
    )
    # print(r)
    check_job(r)
    return r['rdb']


def get_cache(vxnet, cache_size, cache_type):
    r = conn.create_cache(
        vxnet=vxnet,
        cache_size=cache_size,
        cache_type=cache_type
    )
    # print(r)
    check_job(r)
    return r['cache_id']


def bind_ip_to_route(router, eip):
    r = conn.modify_router_attributes(
        router=router,
        eip=eip,
        zone=config['zone']
    )
    # print(r)
    check_job(r)
    return r


def create(instance_type='c1m1', is_rdb=False, is_redis=False):
    route = get_route()  # create route
    vxnet = get_vxnet()  # create vxnet
    join = conn.join_router(  # add vxnet to route
        vxnet=vxnet[0],
        router=route[0],
        ip_network='192.168.100.0/24'
    )
    print(join)
    eip = get_eip(1)  # create eip
    bind = bind_ip_to_route(route[0], eip[0])  # bind ip to route
    if is_rdb:
        get_rdb(vxnet[0], 'Qingcloud', 'Qingcloud123', 1)  # create rdb
    if is_redis:
        get_cache(vxnet[0], 1, 'redis2.8.17')  # create cache
    instance = get_instance(instance_type=instance_type, vxnets=vxnet)  # create instance
    print(instance)
    print('创建完毕！')


def main():
    arguments = docopt(__doc__, version="0.0.1")
    global config, conn
    config = init()
    conn = qingcloud.iaas.connect_to_zone(
        config['zone'],
        config['access_key_id'],
        config['secret_access_key']
    )
    # create('c1m1', True, True)


if __name__ == '__main__':
    main()
