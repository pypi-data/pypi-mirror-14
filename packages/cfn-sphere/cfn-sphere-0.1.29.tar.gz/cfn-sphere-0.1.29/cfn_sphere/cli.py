import sys
import logging

import boto
import click

from boto.exception import NoAuthHandlerFound, BotoServerError

from cfn_sphere.template.transformer import CloudFormationTemplateTransformer
from cfn_sphere.aws.cfn import CloudFormation
from cfn_sphere.aws.kms import KMS
from cfn_sphere.util import convert_file, get_logger, get_latest_version
from cfn_sphere.stack_configuration import Config
from cfn_sphere import StackActionHandler
from cfn_sphere.exceptions import CfnSphereException
from cfn_sphere.file_loader import FileLoader
from cfn_sphere import __version__

LOGGER = get_logger(root=True)
logging.getLogger('boto').setLevel(logging.FATAL)


def get_current_account_alias():
    try:
        return boto.connect_iam().get_account_alias().account_aliases[0]
    except NoAuthHandlerFound as e:
        click.echo("Authentication error! Please check credentials: {0}".format(e))
        sys.exit(1)
    except BotoServerError as e:
        if e.code == "ExpiredToken":
            click.echo(e.message)
        else:
            click.echo("AWS API Error: {0}".format(e))

        sys.exit(1)
    except Exception as e:
        click.echo("Unknown error occurred loading users account alias: {0}".format(e))
        sys.exit(1)


def check_update_available():
    latest_version = get_latest_version()
    if latest_version and __version__ != latest_version:
        click.confirm(
            "There is an update available (v: {0}).\n"
            "Changelog: https://github.com/cfn-sphere/cfn-sphere/issues?q=milestone%3A{0}+\n"
            "Do you want to continue?".format(latest_version), abort=True)


@click.group(help="This tool manages AWS CloudFormation templates "
                  "and stacks by providing an application scope and useful tooling.")
@click.version_option(version=__version__)
def cli():
    pass


@cli.command(help="Sync AWS resources with definition file")
@click.argument('config', type=click.Path(exists=True))
@click.option('--parameter', '-p', default=None, envvar='CFN_SPHERE_PARAMETERS', type=click.STRING, multiple=True,
              help="Stack parameter to overwrite, eg: --parameter stack1:p1=v1")
@click.option('--debug', '-d', is_flag=True, default=False, envvar='CFN_SPHERE_DEBUG', help="Debug output")
@click.option('--confirm', '-c', is_flag=True, default=False, envvar='CFN_SPHERE_CONFIRM',
              help="Override user confirm dialog with yes")
def sync(config, parameter, debug, confirm):
    if debug:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)

    if not confirm:
        check_update_available()
        click.confirm('This action will modify AWS infrastructure in account: {0}\nAre you sure?'.format(
            get_current_account_alias()), abort=True)

    try:

        config = Config(config_file=config, cli_params=parameter)
        StackActionHandler(config).create_or_update_stacks()
    except CfnSphereException as e:
        LOGGER.error(e)
        if debug:
            LOGGER.exception(e)
        sys.exit(1)
    except Exception as e:
        LOGGER.error("Failed with unexpected error")
        LOGGER.exception(e)
        LOGGER.info("Please report at https://github.com/cfn-sphere/cfn-sphere/issues!")
        sys.exit(1)


@cli.command(help="Delete all stacks in a stack configuration")
@click.argument('config', type=click.Path(exists=True))
@click.option('--debug', '-d', is_flag=True, default=False, envvar='CFN_SPHERE_DEBUG', help="Debug output")
@click.option('--confirm', '-c', is_flag=True, default=False, envvar='CFN_SPHERE_CONFIRM',
              help="Override user confirm dialog with yes")
def delete(config, debug, confirm):
    if debug:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)

    if not confirm:
        check_update_available()
        click.confirm('This action will delete all stacks in {0} from account: {1}\nAre you sure?'.format(
            config, get_current_account_alias()), abort=True)

    try:

        config = Config(config)
        StackActionHandler(config).delete_stacks()
    except CfnSphereException as e:
        LOGGER.error(e)
        if debug:
            LOGGER.exception(e)
        sys.exit(1)
    except Exception as e:
        LOGGER.error("Failed with unexpected error")
        LOGGER.exception(e)
        LOGGER.info("Please report at https://github.com/cfn-sphere/cfn-sphere/issues!")
        sys.exit(1)


@cli.command(help="Convert JSON to YAML or vice versa")
@click.argument('template_file', type=click.Path(exists=True))
@click.option('--debug', '-d', is_flag=True, default=False, envvar='CFN_SPHERE_DEBUG', help="Debug output")
@click.option('--confirm', '-c', is_flag=True, default=False, envvar='CFN_SPHERE_CONFIRM',
              help="Override user confirm dialog with yes")
def convert(template_file, debug, confirm):
    if not confirm:
        check_update_available()

    if debug:
        LOGGER.setLevel(logging.DEBUG)

    try:
        click.echo(convert_file(template_file))
    except Exception as e:
        LOGGER.error("Error converting {0}:".format(template_file))
        LOGGER.exception(e)
        sys.exit(1)


@cli.command(help="Render template as it would be used to create/update a stack")
@click.argument('template_file', type=click.Path(exists=True))
@click.option('--confirm', '-c', is_flag=True, default=False, envvar='CFN_SPHERE_CONFIRM',
              help="Override user confirm dialog with yes")
def render_template(template_file, confirm):
    if not confirm:
        check_update_available()

    loader = FileLoader()
    template = loader.get_file_from_url(template_file, None)
    template = CloudFormationTemplateTransformer.transform_template(template)
    click.echo(template.get_pretty_template_json())


@cli.command(help="Validate template with CloudFormation API")
@click.argument('template_file', type=click.Path(exists=True))
@click.option('--confirm', '-c', is_flag=True, default=False, envvar='CFN_SPHERE_CONFIRM',
              help="Override user confirm dialog with yes")
def validate_template(template_file, confirm):
    if not confirm:
        check_update_available()

    try:
        loader = FileLoader()
        template = loader.get_file_from_url(template_file, None)
        template = CloudFormationTemplateTransformer.transform_template(template)
        CloudFormation().validate_template(template)
        click.echo("Template is valid")
    except CfnSphereException as e:
        LOGGER.error(e)
        sys.exit(1)
    except Exception as e:
        LOGGER.error("Failed with unexpected error")
        LOGGER.exception(e)
        LOGGER.info("Please report at https://github.com/cfn-sphere/cfn-sphere/issues!")
        sys.exit(1)


@cli.command(help="Encrypt a given string with AWS Key Management Service")
@click.argument('region', type=str)
@click.argument('keyid', type=str)
@click.argument('cleartext', type=str)
@click.option('--confirm', '-c', is_flag=True, default=False, envvar='CFN_SPHERE_CONFIRM',
              help="Override user confirm dialog with yes")
def encrypt(region, keyid, cleartext, confirm):
    if not confirm:
        check_update_available()

    try:
        cipertext = KMS(region).encrypt(keyid, cleartext)
        click.echo("Ciphertext: {0}".format(cipertext))
    except CfnSphereException as e:
        LOGGER.error(e)
        sys.exit(1)
    except Exception as e:
        LOGGER.error("Failed with unexpected error")
        LOGGER.exception(e)
        LOGGER.info("Please report at https://github.com/cfn-sphere/cfn-sphere/issues!")
        sys.exit(1)


@cli.command(help="Decrypt a given ciphertext with AWS Key Management Service")
@click.argument('region', type=str)
@click.argument('ciphertext', type=str)
@click.option('--confirm', '-c', is_flag=True, default=False, envvar='CFN_SPHERE_CONFIRM',
              help="Override user confirm dialog with yes")
def decrypt(region, ciphertext, confirm):
    if not confirm:
        check_update_available()

    try:
        cleartext = KMS(region).decrypt(ciphertext)
        click.echo("Cleartext: {0}".format(cleartext))
    except CfnSphereException as e:
        LOGGER.error(e)
        sys.exit(1)
    except Exception as e:
        LOGGER.error("Failed with unexpected error")
        LOGGER.exception(e)
        LOGGER.info("Please report at https://github.com/cfn-sphere/cfn-sphere/issues!")
        sys.exit(1)


def main():
    cli()
