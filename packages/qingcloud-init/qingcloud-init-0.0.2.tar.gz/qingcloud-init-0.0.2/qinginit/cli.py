"""Qingcloud init cli

Usage:
    qinginit init
    qinginit config id <access_key_id>
    qinginit config key <secret_access_key>
    qinginit config zone <zone_id>
    qinginit create default
    qinginit create -f <file>

Options:
    -v, --version  show verison
    -h, --help show help document

"""

from docopt import docopt
import os
import qingcloud.iaas
import time
import yaml


def init():
    if not os.path.isfile('config.yml'):
        print('第一次运行qinginit,请参考当前目录下的config.yml文件配置修改参数')
        from pkg_resources import resource_string
        data = resource_string(__name__, 'example.yml')
        with open('config.yml', 'w') as f:
            f.write(str(data, encoding='utf-8'))
            f.close()
    return load_config()


def load_config(file='config.yml'):
    with open(file, 'r') as f:
        tmpconfig = yaml.load(f)
        f.close()
    return tmpconfig


def save_config(tmpconfig):
    with open('config.yml', 'w') as f:
        f.write(yaml.dump(tmpconfig, default_flow_style=False))
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


def print_example():
    from pkg_resources import resource_string
    data = resource_string(__name__, 'example.yml')
    print(str(data, encoding='utf-8'))


def check_job(response):
    if 'job_id' not in response:
        print('your job %s is finished' % (response['action']))
        return True
    else:
        for i in range(100):
            time.sleep(5)
            r = conn.describe_jobs(
                jobs=[response['job_id']]
            )
            print('your job %s is %s' % (r['job_set'][0]['job_action'], r['job_set'][0]['status']))
            if r['job_set'][0]['status'] == 'successful':
                return True
        return False


def get_eip(bandwidth):
    r = conn.allocate_eips(
        bandwidth=bandwidth
    )
    # print(r)
    check_job(r)
    return r['eips']


def get_route():
    r = conn.create_routers()
    # print(r)
    check_job(r)
    return r['routers']


def get_vxnet(vxnet_name, vxnet_type=1):
    r = conn.create_vxnets(
        vxnet_name=vxnet_name,
        vxnet_type=vxnet_type
    )
    # print(r)
    check_job(r)
    return r['vxnets']


def get_instance(image_id, instance_type, login_passwd, vxnets=['vxnet-0'], ):
    r = conn.run_instances(
        image_id=image_id,
        instance_type=instance_type,
        vxnets=vxnets,
        login_mode='passwd',
        login_passwd=login_passwd
    )
    # print(r)
    check_job(r)
    return r['instances']


def get_rdb(vxnet, rdb_username, rdb_password, rdb_type, rdb_engine, engine_version,
            storage_size):
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
        eip=eip
    )
    # print(r)
    check_job(r)
    return r


def add_rules_to_security(protocol, action, val1):
    r = conn.describe_security_groups()
    check_job(r)
    security_id = r['security_group_set'][0]['security_group_id']
    rule = {
        'protocol': protocol,
        'priority': 10,
        'action': action,
        'val1': val1
    }
    r = conn.add_security_group_rules(
        security_group=security_id,
        rules=[rule]
    )
    check_job(r)
    r = conn.apply_security_group(security_id)
    check_job(r)
    return r


def create_by_file(file='config.yml'):
    # set config file
    config = load_config(file)
    bandwidth = config['bandwidth']
    ip_network = config['ip_network']
    vxnet_name = config['vxnet_name']

    image_id = config['image_id']
    instance_type = config['instance_type']
    login_passwd = config['login_passwd']

    is_rdb = bool(config['is_rdb'])
    rdb_username = config['rdb_username']
    rdb_password = config['rdb_password']
    rdb_type = config['rdb_type']
    storage_size = config['storage_size']
    rdb_engine = config['rdb_engine']
    engine_version = config['engine_version']
    is_cache = bool(config['is_cache'])
    cache_size = config['cache_size']
    cache_type = config['cache_type']

    # begin create
    route = get_route()  # create route
    vxnet = get_vxnet(vxnet_name)  # create vxnet
    join = conn.join_router(  # add vxnet to route
        vxnet=vxnet[0],
        router=route[0],
        ip_network=ip_network
    )
    eip = get_eip(bandwidth)  # create eip
    bind_ip_to_route(route[0], eip[0])  # bind ip to route
    if is_rdb:
        get_rdb(  # create rdb
            vxnet=vxnet[0],
            rdb_username=rdb_username,
            rdb_password=rdb_password,
            rdb_type=rdb_type,
            storage_size=storage_size,
            rdb_engine=rdb_engine,
            engine_version=engine_version
        )
    if is_cache:
        get_cache(  # create cache
            vxnet=vxnet[0],
            cache_size=cache_size,
            cache_type=cache_type
        )
    instance = get_instance(  # create instance
        image_id=image_id,
        instance_type=instance_type,
        vxnets=vxnet,
        login_passwd=login_passwd
    )

    # add security rules
    add_rules_to_security('tcp', 'accept', 80)
    print('创建完毕！')


def main():
    arguments = docopt(__doc__, version="0.0.1")
    global conn
    config = init()
    conn = qingcloud.iaas.connect_to_zone(
        config['zone'],
        config['access_key_id'],
        config['secret_access_key']
    )

    # begin main process
    if arguments['config']:
        if arguments['id']:
            config_access_key_id(arguments['<access_key_id>'])
        elif arguments['key']:
            config_secret_access_key(arguments['<secret_access_key>'])
        elif arguments['zone']:
            config_zone(arguments['zone'])
    elif arguments['init']:
        from pkg_resources import resource_string
        data = resource_string(__name__, 'example.yml')
        with open('config.yml', 'w') as f:
            f.write(str(data, encoding='utf-8'))
            f.close()
    elif arguments['create']:
        if arguments['-f']:
            create_by_file(arguments['<file>'])
        elif arguments['default']:
            create_by_file()


if __name__ == '__main__':
    main()
