"""Command line interface for ltd-mason that runs a doc build."""
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from builtins import *  # NOQA
from future.standard_library import install_aliases
install_aliases()

import os
import argparse
import textwrap
import sys
from io import open
import tempfile
import shutil
import logging

import requests

from .manifest import Manifest
from .product import Product
from .uploader import upload_via_keeper


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def run_ltd_mason():
    """Command line app: ``ltd-mason``.

    This app is intended to be called from ``buildlsstsw.sh`` and is
    responsible for running the full documentation build and upload
    process.
    """
    logging.basicConfig(level=logging.INFO)
    args, unknown_args = parse_args()
    if args.manifest_path is None:
        # Read manifest from stdin
        manifest_data = sys.stdin.read()
    else:
        # Read manifest from file
        with open(args.manifest_path, mode='r', encoding='utf-8') as f:
            manifest_data = f.read()
    manifest = Manifest(manifest_data)

    if args.build_dir is None:
        # Use a temporary directory by default
        build_dir = tempfile.mkdtemp()
    else:
        # Use a debug directory
        build_dir = os.path.abspath(args.build_dir)
        assert build_dir is not os.getcwd(), "--build-dir can't be CWD"
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)

    product = Product(manifest, build_dir)
    product.clone_doc_repo()
    product.link_package_repos()
    product.install_dependencies()
    product.build_sphinx()

    if not args.no_upload:
        aws_credentials = read_aws_credentials()
        keeper_credentials = read_keeper_credentials()
        keeper_token = get_keeper_token(
            keeper_credentials['keeper_url'],
            keeper_credentials['keeper_username'],
            keeper_credentials['keeper_password'])
        upload_via_keeper(manifest, product,
                          keeper_url=keeper_credentials['keeper_url'],
                          keeper_token=keeper_token,
                          aws_credentials=aws_credentials)

    if args.build_dir is None:
        shutil.rmtree(build_dir)


def parse_args():
    """Create an ``argparse.ArgumentParser`` instance that define's ltd-mason's
    command line interface.
    """
    parser = argparse.ArgumentParser(
        prog='ltd-mason',
        description=textwrap.dedent("""
            Build Sphinx product documentation for LSST the Docs.

            ltd-mason is driven by a YAML-formatted manifest file. The manifest
            can either be provided as a file using the `--manifest` argument,

            ltd-mason --manifest manifest.yaml

            or piped in,

            cat manifest.yaml | ltd-mason

            ltd-mason's use of Amazon S3 and LTD Keeper are configured with
            environment variables:

            LTD_MASON_AWS_ID
               AWS access key ID.

            LTD_MASON_AWS_SECRET
               AWS secret access key.

            LTD_MASON_AWS_PROFILE
               This variable can be set as an alternative ``LTD_MASON_AWS_ID``
               and ``LTD_MASON_AWS_SECRET``. ``LTD_MASON_AWS_PROFILE`` is the
               name of a profile in `~/.aws/credentials` that contains your
               secret key and ID. See the `boto3 configuration guide
               <http://bit.ly/1WuF7rY>`_ for more information.

            Note that the AWS credentials specified here must have permission
            to read and write into the S3 buckets managed by the LTD Keeper
            server.

            LTD_KEEPER_URL
               URL of LTD Keeper instance.

            LTD_KEEPER_USER
               Username for LTD Keeper instance.

            LTD_KEEPER_PASSWORD
               Password for LTD Keeper instance.
            """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='See https://github.com/lsst-sqre/ltd-mason for more info.')
    parser.add_argument(
        '--manifest',
        dest='manifest_path',
        default=None,
        help='Path to YAML manifest file that defines the doc build.')
    parser.add_argument(
        '--no-upload',
        dest='no_upload',
        default=False,
        action='store_true',
        help='Skip the upload to S3 and ltd-keeper; only build the docs')
    parser.add_argument(
        '--build-dir',
        default=None,
        dest='build_dir',
        help='Directory to use for building the documentation. By default a '
             'temporary directory is created an deleted. This manually-set '
             'directory is not deleted to aid debugging. Beware that any '
             'existing content in that directory will be deleted.')
    args, unknown_args = parser.parse_known_args()
    return args, unknown_args


def read_aws_credentials():
    keys = (('aws_profile', 'LTD_MASON_AWS_PROFILE'),
            ('aws_access_key_id', 'LTD_MASON_AWS_ID'),
            ('aws_secret_access_key', 'LTD_MASON_AWS_SECRET'))
    c = {k: os.getenv(envvar) for (k, envvar) in keys}
    if c['aws_access_key_id'] is not None \
            and c['aws_secret_access_key'] is not None:
        del c['aws_profile']
        log.info('Using $LTD_MASON_AWS_ID and $LTD_MASON_AWS_SECRET')
    else:
        del c['aws_access_key_id']
        del c['aws_secret_access_key']
        if c['aws_profile'] is None:
            log.info('Assuming default AWS credential setup')
            del c['aws_profile']
        else:
            log.info('Using $LTD_MASON_AWS_PROFILE')

    return c


def read_keeper_credentials():
    keys = (('keeper_url', 'LTD_KEEPER_URL'),
            ('keeper_username', 'LTD_KEEPER_USER'),
            ('keeper_password', 'LTD_KEEPER_PASSWORD'))
    c = {k: os.getenv(envvar) for (k, envvar) in keys}
    for (k, envvar) in keys:
        if c[k] is None:
            raise RuntimeError('Please set {0}'.format(envvar))
    return c


def get_keeper_token(base_url, username, password):
    """Get a temporary auth token from ltd-keeper."""
    token_endpoint = base_url + '/token'
    r = requests.get(token_endpoint, auth=(username, password))
    if r.status_code != 200:
        raise RuntimeError('Could not authenticate to {0}: error {1:d}\n{2}'.
                           format(base_url, r.status_code, r.json()))
    return r.json()['token']
