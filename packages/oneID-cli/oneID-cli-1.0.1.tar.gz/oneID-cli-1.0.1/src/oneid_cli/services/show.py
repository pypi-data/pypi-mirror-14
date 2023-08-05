import logging

import oneid.utils

from .. import config_file
from .base import Service, add_project_id_param

logger = logging.getLogger(__name__)


class Show(Service):
    """
    Show project specific information through the command line
    """
    def setup_argparser(self, parser, required=False):
        if not required:
            add_project_id_param(parser, False)
            parser.add_argument('--key', '-k', action='store_true', required=True)

    def run(self, *args):
        """
        Show the information given the parameters passed in

        :param args: Command Line arguments
        :return: None
        """
        service_args = self._parse_args(*args)
        with config_file.load(service_args.project_id) as config:
            key = config and 'AES' in config and oneid.utils.base64url_decode(config['AES'])
            if service_args.key and key:
                print(key)
