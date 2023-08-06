"""Qingcloud init cli

Usage:
    qinginit init
    qinginit config id <access_key_id>
    qinginit config key <secret_access_key>
    qinginit config zone <zone_id>
    qinginit create

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


def check_job(response):
    if 'job_id' not in response:
        if 'action' in response:
            print('your job %s is finished' % (response['action']))
            return True
        else:
            print('your job is failed for %s' % (response['message']))
            return False
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
    check_job(r)
    return r['eips']


def get_route():
    r = conn.create_routers()
    check_job(r)
    return r['routers']


def get_vxnet(vxnet_type=1):
    r = conn.create_vxnets(
        vxnet_type=vxnet_type
    )
    check_job(r)
    return r['vxnets']


def get_instances(image_id, instance_type, login_passwd, router, vxnets):
    r = conn.run_instances(
        image_id=image_id,
        instance_type=instance_type,
        vxnets=vxnets,
        login_mode='passwd',
        login_passwd=login_passwd
    )
    check_job(r)
    check_job(conn.update_routers(router))
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
    check_job(r)
    return r['rdb']


def get_cache(vxnet, cache_size, cache_type):
    r = conn.create_cache(
        vxnet=vxnet,
        cache_size=cache_size,
        cache_type=cache_type
    )
    check_job(r)
    return r['cache_id']


def bind_ip_to_route(router, eip):
    r = conn.modify_router_attributes(
        router=router,
        eip=eip
    )
    check_job(r)
    return r


def add_vxnet_to_router(vxnet, router, ip_network):
    r = conn.join_router(
        vxnet=vxnet[0],
        router=router[0],
        ip_network=ip_network
    )
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
    check_job(conn.apply_security_group(security_id))
    return r


def add_rules_to_router(router, static_type, val1, val2, val3, val4, vxnet):
    statics = [
        {
            'static_type': static_type,
            'val1': val1,
            'val2': val2,
            'val3': val3,
            'val4': val4
        }
    ]
    # print(statics)
    r = conn.add_router_statics(
        router=router[0],
        statics=statics,
        vxnet=vxnet
    )
    # print(r)
    check_job(r)
    check_job(conn.update_routers(router))
    return r


def create_by_file(file='config.yml'):
    # set config file
    config = load_config(file)
    # create data
    data = {}

    bandwidth = config['bandwidth']
    ip_network = config['ip_network']
    image_id = config['image_id']
    instance_type = config['instance_type']
    login_passwd = config['login_passwd']
    is_rdb = bool(config['is_rdb'])
    is_cache = bool(config['is_cache'])

    # begin create
    route = get_route()  # create route
    vxnet = get_vxnet()  # create vxnet
    join = add_vxnet_to_router(vxnet, route, ip_network)  # add vxnet to router
    eip = get_eip(bandwidth)  # create eip
    bind_ip_to_route(route[0], eip[0])  # bind ip to route
    data['eip'] = eip[0]

    if is_rdb:
        # settings of rdb
        rdb_username = config['rdb_username']
        rdb_password = config['rdb_password']
        rdb_type = config['rdb_type']
        storage_size = config['storage_size']
        rdb_engine = config['rdb_engine']
        engine_version = config['engine_version']

        data['rdb'] = get_rdb(  # create rdb
            vxnet=vxnet[0],
            rdb_username=rdb_username,
            rdb_password=rdb_password,
            rdb_type=rdb_type,
            storage_size=storage_size,
            rdb_engine=rdb_engine,
            engine_version=engine_version
        )

    if is_cache:
        # settings of cache
        cache_size = config['cache_size']
        cache_type = config['cache_type']

        data['cache'] = get_cache(  # create cache
            vxnet=vxnet[0],
            cache_size=cache_size,
            cache_type=cache_type
        )

    instance = get_instances(  # create instance
        image_id=image_id,
        instance_type=instance_type,
        vxnets=vxnet,
        login_passwd=login_passwd,
        router=route
    )
    data['instance'] = instance

    # add security rules, we can add in console
    # add_rules_to_security('tcp', 'accept', 80)

    # add router forward
    r = conn.describe_instances(instance)
    check_job(r)
    instance_ip = r['instance_set'][0]['vxnets'][0]['private_ip']
    add_rules_to_router(route, 1, '22', instance_ip, '22', 'tcp', vxnet[0])
    add_rules_to_router(route, 1, '80', instance_ip, '80', 'tcp', vxnet[0])

    print('创建完毕！')

    return data


def show_data(data):
    config = load_config()
    print('您的配置参数如下：')

    # eips
    r = conn.describe_eips([data['eip']])
    print('服务器公网ip地址： %s' % (r['eip_set'][0]['eip_addr']))

    # instance
    r = conn.describe_instances(data['instance'])
    print('服务器用户名： %s' % ('ubuntu'))
    print('服务器密码： %s' % (config['login_passwd']))

    # rdb
    if 'rdb' in data:
        r = conn.describe_rdbs([data['rdb']])
        print('数据库内网地址： %s' % (r['rdb_set'][0]['master_ip']))
        print('数据库用户名： %s' % (config['rdb_username']))
        print('数据库密码： %s' % (config['rdb_password']))


def main():
    arguments = docopt(__doc__, version="0.1.2")
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
        show_data(create_by_file())


if __name__ == '__main__':
    main()
