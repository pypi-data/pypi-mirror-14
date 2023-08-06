import codecs
import json
import requests
import six

from kinto_client import cli_utils
from six.moves.urllib.parse import urljoin

from . import constants
from .amo import prepare_amo_records
from .kinto import get_kinto_records
from .logger import logger
from .synchronize import get_diff, push_changes


FIELDS = {
    'add-ons': ['blockID', 'os', 'guid', 'prefs', 'versionRange', 'details'],
    'certificates': ['serialNumber', 'issuerName', 'details'],
    'gfx': ['blockID', 'os', 'vendor', 'feature', 'featureStatus',
            'driverVersion', 'driverVersionmax', 'driverVersionComparator',
            'devices', 'details'],
    'plugins': ['blockID', 'os', 'xpcomabi', 'infoURL', 'versionRange',
                'matchName', 'matchFilename', 'matchDescription', 'details']
}


def sync_records(amo_records, fields,
                 kinto_client, bucket, collection, schema, permissions):

    amo_records = prepare_amo_records(amo_records, fields)
    kinto_records = get_kinto_records(
        kinto_client=kinto_client,
        bucket=bucket,
        collection=collection,
        schema=schema,
        permissions=permissions)

    to_create, to_delete = get_diff(amo_records, kinto_records)

    push_changes((to_create, to_delete), kinto_client,
                 bucket=bucket, collection=collection)


def main(args=None):
    parser = cli_utils.add_parser_options(
        description='Import the blocklists for AMO into Kinto.',
        default_collection=None,
        default_bucket=None,
        default_server=constants.KINTO_SERVER,
        default_auth=constants.AUTH,
        include_bucket=False,
        include_collection=False)

    parser.add_argument('-S', '--schema-file', help='JSON Schemas file',
                        type=str, default=constants.SCHEMA_FILE)

    parser.add_argument('--no-schema', help='Should we handle schemas',
                        action="store_true")

    parser.add_argument('--certificates-bucket',
                        help='Bucket name for certificates',
                        type=str, default=constants.CERT_BUCKET)

    parser.add_argument('--certificates-collection',
                        help='Collection name for certificates',
                        type=str, default=constants.CERT_COLLECTION)

    parser.add_argument('--gfx-bucket', help='Bucket name for gfx',
                        type=str, default=constants.GFX_BUCKET)

    parser.add_argument('--gfx-collection',
                        help='Collection name for gfx',
                        type=str, default=constants.GFX_COLLECTION)

    parser.add_argument('--addons-bucket', help='Bucket name for addons',
                        type=str, default=constants.ADDONS_BUCKET)

    parser.add_argument('--addons-collection',
                        help='Collection name for addon',
                        type=str, default=constants.ADDONS_COLLECTION)

    parser.add_argument('--plugins-bucket', help='Bucket name for plugins',
                        type=str, default=constants.PLUGINS_BUCKET)

    parser.add_argument('--plugins-collection',
                        help='Collection name for plugin',
                        type=str, default=constants.PLUGINS_COLLECTION)

    parser.add_argument('-C', '--certificates',
                        help='Only import certificates',
                        action='store_true')

    parser.add_argument('-G', '--gfx', help='Only import GFX drivers',
                        action='store_true')

    parser.add_argument('-A', '--addons', help='Only import addons',
                        action='store_true')

    parser.add_argument('-P', '--plugins', help='Only import plugins',
                        action='store_true')

    # AMO Server selection
    parser.add_argument('--amo-server', help='The AMO server to import from',
                        type=str, default=constants.AMO_SERVER)

    args = parser.parse_args(args=args)
    cli_utils.setup_logger(logger, args)

    # If none of the different "collections" were passed as parameter, then we
    # want to import them all.
    import_all = not any([
        args.certificates,
        args.gfx,
        args.addons,
        args.plugins])

    kinto_client = cli_utils.create_client_from_args(args)

    # Load the schemas
    schemas = {}
    if not args.no_schema:
        with codecs.open(args.schema_file, 'r', encoding='utf-8') as f:
            schemas = json.load(f)

    amo_blocklists_url = urljoin(args.amo_server, '/blocked/blocklists.json')
    resp = requests.get(amo_blocklists_url)
    resp.raise_for_status()
    blocklists = resp.json()

    for collection_type, records in six.iteritems(blocklists):
        args_type = collection_type.replace('-', '')
        if hasattr(args, args_type) and (getattr(args, args_type) or
                                         import_all):
            bucket = getattr(args, '%s_bucket' % args_type)
            collection = getattr(args, '%s_collection' % args_type)
            jsonschema = None
            if collection_type in schemas:
                jsonschema = schemas[collection_type]['config']['schema']
            sync_records(amo_records=records,
                         fields=FIELDS[collection_type],
                         kinto_client=kinto_client,
                         bucket=bucket,
                         collection=collection,
                         schema=jsonschema,
                         permissions=constants.COLLECTION_PERMISSIONS)
