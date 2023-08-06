import os
import shutil
import sys
import paramiko
import traceback

import click
from click.exceptions import ClickException
import requests

from constants import *
from interactive import interactive_shell
from pyhero import Client
from prompter import *
from utils import (write_to_file, set_keys_to_empty_values,
                   get_docker_ip_for_environment)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def persist_token(user_token):
    """
    Set token environment variable.
    """
    os.environ['CLOUD_HERO_TOKEN'] = user_token
    write_token(user_token)


def forget_token():
    """
    Unset token environment variable.
    """
    env_token = os.environ.get(CLOUD_HERO_TOKEN_ENV_VARIABLE, None)
    del env_token


def write_token(content):
    """
    Write token to config file.
    """
    config_file_path = os.path.expanduser(CLOUD_HERO_TOKEN)
    write_to_file(content, config_file_path)


def read_token():
    """
    Read CloudHero config file.
    """
    config_file_path = os.path.expanduser(CLOUD_HERO_TOKEN)
    if not os.path.isfile(config_file_path):
        return None

    with open(config_file_path, "r") as file_handler:
        token_from_file = file_handler.read()
        return token_from_file.strip().replace('\n', '').replace('\t', '')


def exception_handler(api_exception):
    if isinstance(api_exception, requests.HTTPError):
        response = api_exception.response

        status_code = response.status_code
        content = response.json()
        if status_code == 500:
            message = 'CloudHero server error'
        elif status_code == 409:
            message = '{message} - ID {id}'.format(**content)
        elif status_code == 404:
            message = 'Resource not found'
        elif status_code == 401:
            message = 'Create an account and login, to have access to this!'
        elif status_code == 400:
            message = content.get('error')
        else:
            message = content

        show_user = ('({}) {}'.format(status_code, message))
        raise ClickException(show_user)


token = os.environ.get(CLOUD_HERO_TOKEN_ENV_VARIABLE)
if not token:
    token = read_token()
cloud_hero = Client(base_url=CLOUD_HERO_URI, token=token,
                    exception_callback=exception_handler,
                    clean_up_arguments=True,
                    user_agent=CLOUD_HERO_USER_AGENT)


def verify_one_of(kwargs, *args):
    args_for_printing = '/'.join(['--{}'.format(arg) for arg in args])
    arguments_value_list = [kwargs[arg] for arg in args]
    if not any(arguments_value_list):
        sys.exit('At least one of {} is required'.format(args_for_printing))

    arguments_provided = [arg for arg in arguments_value_list if arg]
    if len(arguments_provided) > 1:
        sys.exit('Provide just one of {}'.format(args_for_printing))


def tags_for_pprint(tags):
    if not tags:
        return NOTHING_TO_SHOW
    return ', '.join(['{}:{}'.format(key, value)
                      for key, value in tags.items()])


def tags_to_dict(kwargs):
    """
    Updates kwargs with correct `tags` value.
    """
    tags = kwargs.pop('tags', None)
    if not tags:
        return
    dict_tags = {}
    for tag in tags.split(','):
        tag = tag.strip()
        key, value = tag.split(':')
        dict_tags[key] = value
    kwargs['tags'] = dict_tags


def log_response(response):
    if not response:
        return
    elif response.get('message'):
        print('{message}'.format(**response))
    elif response.get('id'):
        print('Created "{name}" (ID {id})'.format(**response))


# ------------------------------------------------------------------------
# ROOT-LEVEL
# ------------------------------------------------------------------------
class OrderedHeroCommands(click.Group):

    COMMANDS_ORDER = ['login', 'register', 'provider', 'integration',
                      'environment', 'node', 'docker', 'ssh']

    COMMANDS_ALIASES = {
        'env': 'environment'
    }

    def list_commands(self, ctx):
        return self.COMMANDS_ORDER

    def get_command(self, ctx, cmd_name):
        """
        For matching multiple commands.
        """
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [
            x for x in self.list_commands(ctx)
            if cmd_name and
            (x == cmd_name or self.COMMANDS_ALIASES.get(cmd_name) == x)
        ]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.command(cls=OrderedHeroCommands, context_settings=CONTEXT_SETTINGS)
@click.version_option(version=CLI_VERSION, help='Show the version')
@click.help_option('-h', '--help', help='Show usage')
@click.help_option('-v', '--verbose', help='Enable verbose mode')
def hero_cli(**kwargs):
    if kwargs.get('verbose'):
        global VERBOSE
        VERBOSE = True


@hero_cli.command('token', help='See your token')
def show_token():
    print token


# ------------------------------------------------------------------------
# NODE COMMANDS
# ------------------------------------------------------------------------
@hero_cli.group(name='node', help='Node operations')
def node():
    pass


@node.command('add', short_help='Add node', help='Add node')
@click.option('-e', '--environment_id', required=True, prompt=True, help='Environment ID')
@click.option('-k', '--pkg', prompt=True, help='Packages to be installed on the node')
@click.option('-s', '--size', help='Node size')
@click.option('-t', '--tags', help='Tags to be applied on the node')
@click.option('-n', '--name', prompt=True, help='Node name')
def add_node(**node_kwargs):
    environment_id = node_kwargs.pop('environment_id')
    if node_kwargs.get('pkg'):
        node_kwargs['packages'] = node_kwargs['pkg'].split(',')
    tags_to_dict(node_kwargs)
    log_response(cloud_hero.create_node(environment_id, [node_kwargs]))


@node.command('scale', help='Scale based node')
@click.option('-e', '--environment_id', required=True, prompt=True, help='Environment ID')
@click.option('-n', '--name', help='Scale based on an existing node name')
@click.option('-t', '--tags', help='Scale based on an existing node tags')
@click.option('--up', help='Scale UP')
@click.option('--down', help='Scale DOWN')
def scale_node(**kwargs):
    verify_one_of(kwargs, 'name', 'tags')
    verify_one_of(kwargs, 'up', 'down')
    if kwargs.get('name') and kwargs.get('down'):
        print('Note that scaling down by name will only remove the selected '
              'node!')
    tags_to_dict(kwargs)

    environment_id = kwargs.pop('environment_id')
    if kwargs.get('up'):
        kwargs['count'] = int(kwargs.pop('up'))
        log_response(cloud_hero.scale_up_node(environment_id, kwargs))
    else:
        kwargs['count'] = int(kwargs.pop('down'))
        log_response(cloud_hero.scale_down_node(environment_id, kwargs))


@node.command('ls', short_help='List all your nodes',
               help='List all your nodes')
def list_nodes():
    node_format = ('{node[name]:<20}{environment[name]:<20}'
                   '{node[public_ip]:<15}{node[private_ip]:<15}'
                   '{node[status]:<10}{node[provider]:<15}{node[id]:<25}'
                   '{environment[id]:<25}{node[tags]:<15}{node[packages]:<15}')
    print node_format.format(**PROMPTER_KWARGS)

    environments = cloud_hero.list_environments()
    for environment in environments:
        for node in environment['nodes']:
            node_data = {
                'node': {
                    'id': node['id'],
                    'name': node['name'],
                    'status': node.get('status', NOT_AVAILABLE),
                    'provider': environment['provider']['name'],
                    'public_ip': node.get('public_ip', NOT_AVAILABLE),
                    'private_ip': node.get('private_ip', NOT_AVAILABLE),
                    'packages': ','.join(node['packages']),
                    'tags': tags_for_pprint(node['tags'])
                },
                'environment': {
                    'id': environment['id'],
                    'name': environment['name'],
                },
            }
            print(node_format.format(**node_data))


@node.command('rm', short_help='Remove an existing node',
              help='Remove an existing node')
@click.argument('node_id', required=False)
def remove_node(**kwargs):
    node_id = kwargs.get('node_id')
    if not node_id:
        node_id = click.prompt('Node id')
    log_response(cloud_hero.delete_node(node_id))


# ------------------------------------------------------------------------
# ENVIRONMENT COMMANDS
# ------------------------------------------------------------------------
@hero_cli.group(name='environment', help='Environment set-up')
def environment():
    pass


@environment.command('add', short_help='Add environment', help='Add environment')
@click.option('-p', '--provider_id', prompt=True, help='Select the provider ID')
@click.option('-l', '--location', prompt=True,
              help='Cloud provider location/region for environment')
@click.option('-n', '--name', prompt=True, help='Environment name')
def add_environment(**kwargs):
    data = {
        'region': kwargs['location'],
        'environment': kwargs['name'],
        'provider_id': kwargs['provider_id']
    }
    log_response(cloud_hero.add_environment(data))


@environment.command('rm', short_help='Remove an existing environment',
                     help='Remove an existing environment')
@click.argument('environment_id', required=False)
@click.option('-id', '--environment_id', help='Environment ID to be removed')
def remove_environment(**kwargs):
    environment_id = kwargs.get('environment_id')
    if not environment_id:
        environment_id = click.prompt('Environment id')
    log_response(cloud_hero.delete_environment(environment_id))


@environment.command('ls', short_help='List all your environments',
                      help='List all your environments')
def list_environments():
    format_string = ('{node[name]:<25}{environment[location]:<15}'
                     '{nodes_count:<15}{environment[name]:<20}'
                     '{environment[id]:<30}'
                     '{provider[name]:<30}{provider[id]:<30}')
    print format_string.format(**PROMPTER_KWARGS)

    environments_list = cloud_hero.list_environments()
    for environment in environments_list:
        environment_data = {
            'environment': {
                'id': environment['id'],
                'name': environment['name'],
                'location': environment['os_region'],
            },
            'nodes_count': len(environment['nodes']),
            'provider': {
                'id': environment['provider']['id'],
                'name': environment['provider']['name']
            }
        }
        nodes_list = environment['nodes'] or [{'name': NOTHING_TO_SHOW}]
        for index, node in enumerate(nodes_list):
            if index == 0:
                print format_string.format(node=node, **environment_data)
                continue

            environment_data = set_keys_to_empty_values(environment_data)
            print(format_string.format(node=node, **environment_data))


# ------------------------------------------------------------------------
# PROVIDER COMMANDS
# ------------------------------------------------------------------------
@hero_cli.group(help='Cloud providers')
def provider():
    pass


class OptionsBasedCLI(click.MultiCommand):

    COMMAND_TYPE_TO_ENDPOINT = {
        'integration': 'integrations',
        'provider': 'providers'
    }

    def __init__(self, *args, **kwargs):
        self.command_type = kwargs.pop('command_type')
        self.endpoint = self.COMMAND_TYPE_TO_ENDPOINT[self.command_type]
        self.field_type = kwargs.pop('field_type')
        super(OptionsBasedCLI, self).__init__(*args, **kwargs)

    def list_commands(self, ctx):
        rv = cloud_hero.show_options(self.endpoint).keys()
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        if name not in self.list_commands(ctx):
            ctx.fail('No such command "%s".' % name)

        api_description = cloud_hero.show_options(self.endpoint)
        params = [click.Option((('-n'), ('--name'), ),
                               help='{} name'.format(self.command_type.capitalize()))]
        for mandatory_field in api_description[name]['mandatory_fields']:
            option_args = ('-{}'.format(mandatory_field['short']),
                           '--{}'.format(mandatory_field['long']), )
            click_option = click.Option(option_args,
                                        help=mandatory_field['description'])
            params.append(click_option)

        @click.pass_context
        def callback(ctx, **kwargs):
            if list(set(kwargs.values())) == [None]:
                sys.exit(ctx.get_help())

            kwargs[self.field_type] = ctx.info_name
            # Hacks
            if self.command_type == 'provider':
                if 'accesskey' in kwargs:
                    kwargs['accessKey'] = kwargs['accesskey']
                    kwargs['secretKey'] = kwargs['secretkey']

            response = cloud_hero.create_from_options(self.endpoint, kwargs)
            log_response(response)

        cmd_return = click.Command(name, params=params, callback=callback,
                                   help=api_description[name]['description'])
        return cmd_return


@provider.command('add', cls=OptionsBasedCLI, command_type='provider',
                   field_type='cloud_provider',
                   short_help='Add a new cloud provider',
                   help='Add a new cloud provider')
@click.pass_context
def add_cloud_provider(ctx, *args, **kwargs):
    pass


@provider.command('ls', short_help='List all configured providers',
                   help='List all configured providers')
@click.option('-k', '--show-keys', is_flag=True, help='Show provider keys')
def list_providers(**kwargs):
    format_string = '{name:<15}{provider_type:<15}{id:<30}'
    if kwargs.get('show_keys'):
        format_string = '{name:<15}{provider_type:<15}{id:<30}{keys:<30}'

    print (format_string.format(provider_type='PROVIDER-TYPE', id='PROVIDER-ID',
                                name='NAME', keys='PROVIDER-KEYS'))

    cloud_providers = cloud_hero.list_providers()
    for provider_type, providers_list in cloud_providers.items():
        for provider in providers_list:
            if provider['provider_type'] == 'ec2':
                provider['keys'] = 'key: {accessKey}, secret: {secretKey}'.format(
                    **provider['provider_meta'])
            else:
                provider['keys'] = provider['provider_meta'].values()[0]
            print(format_string.format(**provider))


@provider.command('rm', short_help='Remove a provider',
                  help='Remove a provider')
@click.argument('provider_id', required=False)
def remove_provider(**kwargs):
    provider_id = kwargs.get('provider_id')
    if not provider_id:
        provider_id = click.prompt('Provider id')
    log_response(cloud_hero.delete_provider(provider_id))


# ------------------------------------------------------------------------
# DOCKER
# ------------------------------------------------------------------------
@hero_cli.command('docker', help='Handle your docker cluster')
@click.argument('environment', required=True)
def export_docker_environment(**kwargs):
    environment = kwargs['environment']
    node_details = cloud_hero.get_all_details()
    try:
        docker_ip = get_docker_ip_for_environment(node_details, environment)
    except NotFound as exception:
        sys.exit(exception.message)
    if docker_ip is None:
        sys.exit('Node is still being created, could not find the IP to '
                 'connect to')

    print('export DOCKER_HOST=tcp://{}:4000'.format(docker_ip))
    print('# Run this command to configure your shell:\n'
          '# eval "$(hero docker {})"'.format(environment))


# ------------------------------------------------------------------------
# INTEGRATIONS
# ------------------------------------------------------------------------
@hero_cli.group(help='Add custom integrations')
def integration():
    pass


@integration.command('add', cls=OptionsBasedCLI, command_type='integration',
                      field_type='type',
                      short_help='Configure a new integration',
                      help='Configure a new integration')
@click.pass_context
def add_integration(ctx, *args, **kwargs):
    pass

@integration.command('ls', short_help='List all configured integrations',
                      help='List all configured integrations')
def list_integrations():
    string_format = '{name:<15}{type:<20}{meta:<30}{id:<30}'
    print string_format.format(type='INTEGRATION-TYPE', id='INTEGRATION-ID',
                               name='NAME', meta='INTEGRATION-METADATA')
    integrations_list = cloud_hero.list_integrations()
    for integration in integrations_list:
        integration['meta'] = tags_for_pprint(integration['integration_meta'])
        print string_format.format(**integration)


@integration.command('rm', short_help='Remove an integration',
                     help='Remove an integration')
@click.argument('integration_id', required=False)
def remove_integration(**kwargs):
    integration_id = kwargs.get('integration_id')
    if not integration_id:
        integration_id = click.prompt('Integration id')
    cloud_hero.delete_integration(integration_id)


# ------------------------------------------------------------------------
# SSH
# ------------------------------------------------------------------------
@hero_cli.command('ssh', help='SSH to virtual machine')
@click.argument('host', required=True)
def ssh_to_vm(**kwargs):
    host_name = kwargs['host']
    node_details = cloud_hero.get_all_details()
    if not node_details.get(host_name):
        sys.exit('No node with name {} found!'.format(host_name))

    node_index = 0
    nodes_data = node_details[host_name]
    if len(nodes_data) > 1:
        nodes_format = ('{index:<10}{node[name]:<25}{node[public_ip]:<20}'
                        '{node[private_ip]:<20}{node[packages]:<20}'
                        '{environment[name]:<20}{environment[id]:<20}')
        print('Node exists in two environments:')
        print(nodes_format.format(**PROMPTER_KWARGS))
        for index, node_data in enumerate(nodes_data):
            node_data['node']['packages'] = ','.join(node_data['node']['packages'])
            print nodes_format.format(index=index, **node_data)
        user_prompt = 'Pick the node you want to ssh to'.format(nodes_format)
        node_index = click.prompt(user_prompt, default=0)
    node = nodes_data[node_index]

    remote_ip = node['node']['public_ip']
    remote_user = node['provider']['username']

    # Get key and write it to the local path
    expanded_file_path = os.path.expanduser(CLOUD_HERO_SSH_KEY)
    if not os.path.exists(expanded_file_path):
        ssh_key_content = cloud_hero.list_key()['content']
        write_to_file(ssh_key_content, expanded_file_path)
        os.chmod(expanded_file_path, 0600)

    # Connect to remote host.
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting to {} ...'.format(remote_ip))
        rsa_key = paramiko.RSAKey.from_private_key_file(expanded_file_path)
        client.connect(remote_ip, username=remote_user, pkey=rsa_key)

        chan = client.invoke_shell()
        print('*** Here we go!\n')
        interactive_shell(chan)
        chan.close()
        client.close()

    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)


# ------------------------------------------------------------------------
# AUTH-RELATED
# ------------------------------------------------------------------------
@hero_cli.command(short_help='Logout user', help='Logout user')
def logout():
    forget_token()

    # Remove everything from the CLOUD_HERO_PATH.
    cloud_hero_path = os.path.expanduser(CLOUD_HERO_DIR)
    try:
        shutil.rmtree(cloud_hero_path)
    except OSError as os_exception:
        print(os_exception.strerror)

    print('Logout successful!')


@hero_cli.command(short_help='Login user', help='Login user')
@click.option('-e', '--email', prompt=True, help='Email')
@click.option('-p', '--password', prompt=True, hide_input=True, help='Password')
def login(**kwargs):
    persist_token(cloud_hero.login(**kwargs))
    print('Let\'s launch some servers!')


@hero_cli.command(short_help='Create account', help='Create account')
@click.option('-e', '--email', prompt=True, help='Email')
@click.option('-p', '--password', prompt=True, confirmation_prompt=True,
              hide_input=True, help='Password')
@click.option('-o', '--organisation', prompt=True, help='Organisation')
def register(**kwargs):
    data = cloud_hero.register(kwargs['email'], kwargs['password'],
                               kwargs['organisation'])

    # Handle registration errors.
    errors = data.get('errors')
    if errors:
        for error_field, error_data in errors.items():
            print('Invalid {:<15} {}'.format(error_field,
                                             error_data[0]))
        sys.exit(1)

    # Persist token.
    user_token = str(data['persistent_token'])
    persist_token(user_token)

    # And welcome user :)
    print('Welcome to CloudHero!'.format(**kwargs))


if __name__ == '__main__':
    hero_cli()
