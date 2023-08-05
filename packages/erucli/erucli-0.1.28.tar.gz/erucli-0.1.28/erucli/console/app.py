# coding: utf-8

import time
import click
import humanize
from datetime import datetime
from eruhttp import EruException

from erucli.console.style import error, info
from erucli.console.output import as_form


@click.option('--raw', '-r', help='deploy a raw image', is_flag=True)
@click.option('--version', '-v', help='version', default=None)
@click.pass_context
def register_app_version(ctx, raw, version):
    eru = ctx.obj['eru']
    try:
        eru.register_app_version(
            version or ctx.obj['sha1'],
            ctx.obj['remote'],
            ctx.obj['appname'],
            ctx.obj['appconfig'],
            raw
        )
        click.echo(info('Register successfully'))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('env')
@click.argument('vs', nargs=-1)
@click.pass_context
def set_app_env(ctx, env, vs):
    kv = {}
    for v in vs:
        if not '=' in v:
            click.echo(error('Env must be like key=value'))
            ctx.exit(-1)
        key, value = v.split('=', 1)
        kv[key] = value
    eru = ctx.obj['eru']
    try:
        eru.set_app_env(ctx.obj['appname'], env, **kv)
        click.echo(info('env variables set successfully'))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('env')
@click.pass_context
def delete_app_env(ctx, env):
    eru = ctx.obj['eru']
    try:
        eru.delete_app_env(ctx.obj['appname'], env)
        click.echo(info('env variables remove successfully'))
    except EruException as e:
        click.echo(error(e.message))


@click.argument('env')
@click.pass_context
def list_app_env_content(ctx, env):
    eru = ctx.obj['eru']
    try:
        data = eru.list_app_env_content(ctx.obj['appname'], env)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['Key', 'Value']
        content = [(key, data.get(key, '')) for key in sorted(data.keys())]
        as_form(title, content)


@click.pass_context
def list_app_containers(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    try:
        containers = eru.list_app_containers(name)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['Name', 'Time', 'Entry', 'Version', 'Alive', 'Host', 'Backends', 'ID']
        content = [
            [
                c['name'],
                humanize.naturaltime(datetime.strptime(c['created'], '%Y-%m-%d %H:%M:%S')),
                c['entrypoint'],
                c['version'],
                'yes' if c['is_alive'] else 'no', 
                '%s / %s' % (c['host'], c['hostname']),
                ','.join(n['address'] for n in c['networks']) or '-',
                str(c['container_id'][:7])
            ] for c in containers
        ]
        as_form(title, content)


@click.pass_context
def list_app_versions(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    try:
        versions = eru.list_app_versions(name)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['Time', 'Version']
        content = [
            [
                humanize.naturaltime(datetime.strptime(c['created'], '%Y-%m-%d %H:%M:%S')),
                c['sha'][:7],
            ] for c in versions
        ]
        as_form(title, content)


@click.pass_context
def list_app_env_names(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    try:
        envs = eru.list_app_env_names(name)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['Env', ]
        content = [[e, ] for e in envs]
        as_form(title, content)


@click.argument('pod')
@click.argument('entrypoint')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncore', '-c', default=1, help='how many cores per container', type=float)
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
@click.option('--network', '-i', help='networks to bind', multiple=True)
@click.option('--host', '-h', help='specific host name', default=None, type=str)
@click.option('--ip', '-p', help='specific ip', multiple=True)
@click.option('--raw', '-r', help='deploy a raw image', is_flag=True)
@click.option('--image', '-m', help='specific image', default='', type=str)
@click.option('--args', '-a', help='extend arguments', default='', type=str)
@click.pass_context
def deploy_private_container(ctx, pod, entrypoint,
        env, ncore, ncontainer, version, network, host, ip, raw, image, args):
    args = args.split(' ')
    eru = ctx.obj['eru']

    if not version:
        version = ctx.obj['short_sha1']
    try:
        r = eru.deploy_private(
            pod,
            ctx.obj['appname'],
            ncore,
            ncontainer,
            version,
            entrypoint,
            env,
            network,
            None,
            host,
            raw,
            image,
            ip,
            args,
        )
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)

        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))


@click.argument('pod')
@click.argument('entrypoint')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
@click.option('--network', '-i', help='networks to bind', multiple=True)
@click.option('--ip', '-p', help='specific ip', multiple=True)
@click.option('--raw', '-r', help='deploy a raw image', is_flag=True)
@click.option('--image', '-m', help='specific image', default='', type=str)
@click.option('--args', '-a', help='extend arguments', default='', type=str)
@click.pass_context
def deploy_public_container(ctx, pod, entrypoint, env, ncontainer,
        version, network, ip, raw, image, args):
    args = args.split(' ')
    eru = ctx.obj['eru']

    if not version:
        version = ctx.obj['short_sha1']

    try:
        r = eru.deploy_public(
            pod,
            ctx.obj['appname'],
            ncontainer,
            version,
            entrypoint,
            env,
            network,
            None,
            raw,
            image,
            ip,
            args,
        )
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)
        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))


@click.argument('pod')
@click.argument('base')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
def build_image(ctx, pod, base, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    try:
        r = eru.build_image(pod, ctx.obj['appname'], base, version)
    except EruException as e:
        click.echo(error(e.message))
    else:
        for d in eru.build_log(r['task']):
            if 'stream' in d:
                click.echo(d['stream'], nl=False)
            elif 'status' in d:
                status = d['status']
                progress = d.get('progress', '')
                if progress:
                    click.echo('%s, %s      \r' % (status, progress), nl=False)
                else:
                    click.echo(status)


@click.argument('task')
@click.pass_context
def build_log(ctx, task):
    eru = ctx.obj['eru']
    for d in eru.build_log(task):
        if 'stream' in d:
            click.echo(d['stream'], nl=False)
        elif 'status' in d:
            status = d['status']
            progress = d.get('progress', '')
            if progress:
                click.echo('%s, %s      \r' % (status, progress), nl=False)
            else:
                click.echo(status)


@click.argument('container_id')
@click.option('--stdout', '-o', is_flag=True)
@click.option('--stderr', '-e', is_flag=True)
@click.option('--tail', '-t', default=10)
@click.pass_context
def container_log(ctx, container_id, stdout, stderr, tail):
    eru = ctx.obj['eru']
    if not stdout and not stderr:
        click.echo(error('Set at least one in --stdout/--stderr'))
        ctx.exit(-1)
    for line in eru.container_log(container_id, int(stdout), int(stderr), tail):
        click.echo(line, nl=False)


@click.argument('container_ids', nargs=-1)
@click.pass_context
def remove_containers(ctx, container_ids):
    eru = ctx.obj['eru']
    try:
        r = eru.remove_containers(container_ids)
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)
        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))


@click.argument('pod')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
def offline_version(ctx, pod, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    try:
        r = eru.offline_version(pod, ctx.obj['appname'], version)
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)
        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))


@click.argument('container_id')
@click.option('--network', '-i', help='version to deploy', multiple=True)
@click.pass_context
def bind_container_network(ctx, container_id, network):
    if not network:
        click.echo(error('at least bind 1 network'))
        return

    eru = ctx.obj['eru']
    try:
        r = eru.bind_container_network(ctx.obj['appname'], container_id, network)
    except EruException as e:
        click.echo(error(e.message))
        return

    rs = ','.join(r['cidrs'])
    click.echo(info('Done.'))
    click.echo(info('%s bound' % rs))


@click.argument('container_id')
@click.argument('eip')
@click.pass_context
def bind_container_eip(ctx, container_id, eip):
    eru = ctx.obj['eru']
    try:
        eru.bind_container_eip(container_id, eip)
    except EruException as e:
        click.echo(error(e.message))
        return

    click.echo(info('%s bound' % eip))


@click.argument('container_id')
@click.argument('eip')
@click.pass_context
def release_container_eip(ctx, container_id, eip):
    eru = ctx.obj['eru']
    try:
        eru.release_container_eip(container_id, eip)
    except EruException as e:
        click.echo(error(e.message))
        return

    click.echo(info('%s released' % eip))
