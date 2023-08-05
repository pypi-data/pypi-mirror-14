# coding: utf-8
import requests
import sys
import datetime
import urllib
import base64
import hmac
from hashlib import sha256
from argparse import ArgumentParser
from utils import explode_array, send_request
from config import Config

config = Config()


class BaseAction(object):

      action = ''
      command = ''
      usage = ''
      description = ''

      @classmethod
      def get_argument_parser(cls):
          parser = ArgumentParser(
                  prog='qingcloud iaas %s' % cls.command,
                  usage=cls.usage,
                  description=cls.description
                  )

          cls.add_common_arguments(parser)
          cls.add_ext_arguments(parser)
          return parser

      @classmethod
      def add_common_arguments(cls, parser):
          parser.add_argument('-z', '--zone', dest='zone',
                  action='store', type=str, default=None,
                  help='the ID of zone you want to access, this will override zone ID in config file.')

          actions_with_tags = ['describe-instances']

          if cls.command.startswith('describe-'):
              parser.add_argument('-O', '--offset', dest='offset',
                      action='store', type=int, default=0,
                      help='the starting offset of the returning results.')
              parser.add_argument('-L', '--limit', dest='limit',
                      action='store', type=int, default=20,
                      help='specify the number of the returning results.')
          if cls.command in actions_with_tags:
              parser.add_argument('-T', '--tags', dest='tags',
                  action='store', type=str, default='',
                  help='the comma separated IDs of tags.')



      @classmethod
      def main(cls, args):
          parser = cls.get_argument_parser()
          options = parser.parse_args(args)
          directive = cls.build_directive(options)
          if directive is None:
              parser.print_help()
              sys.exit(-1)
          if options.zone:
            config.zone = options.zone
          return send_request(cls.action, directive)


class DescribeInstancesAction(BaseAction):
      action = 'DescribeInstances'
      command = 'describe-instances'
      usage = '%(prog)s [-i "instance_id, ..."] [options]'

      @classmethod
      def add_ext_arguments(cls, parser):

          parser.add_argument('-i', '--instances', dest='instances',
                  action='store', type=str, default='',
                  help='the comma separated IDs of instances you want to describe.')

          parser.add_argument('-s', '--status', dest='status',
                  action='store', type=str, default='',
                  help='instance status: pending, running, stopped, terminated, ceased')

          parser.add_argument('-m', '--image_id', dest='image_id',
                  action='store', type=str, default='',
                  help='the image id of instances.')

          parser.add_argument('-t', '--instance_type',
                  action='store', type=str,
                  dest='instance_type', default='',
                  help='instance type: small_b, small_c, medium_a, medium_b, medium_c, \
                  large_a, large_b, large_c')

          parser.add_argument('-W', '--search_word', dest='search_word',
                  action='store', type=str, default='',
                  help='the combined search column')

          parser.add_argument('-V', '--verbose', dest='verbose',
                  action='store', type=int, default=0,
                  help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')

          return parser

      @classmethod
      def build_directive(cls, options):
          return {
                  'instances': explode_array(options.instances),
                  'status': explode_array(options.status),
                  'image_id': explode_array(options.image_id),
                  'instance_type': explode_array(options.instance_type),
                  'search_word': options.search_word,
                  'verbose': options.verbose,
                  'offset':options.offset,
                  'limit': options.limit,
                  'tags': explode_array(options.tags),
                  }


class TerminateInstancesAction(BaseAction):

    action = 'TerminateInstances'
    command = 'terminate-instances'
    usage = '%(prog)s -i "instance_id,..." '

    @classmethod
    def add_ext_arguments(cls, parser):

        parser.add_argument('-i', '--instances', dest='instances',
                action='store', type=str, default='',
                help='the comma separated IDs of instances you want to terminate.')

        return parser

    @classmethod
    def build_directive(cls, options):
        instances = explode_array(options.instances)
        if not instances:
            print('error: [instances] should be specified')
            return None

        return {'instances': instances}


class RunInstancesAction(BaseAction):

    action = 'RunInstances'
    command = 'run-instances'
    usage = '%(prog)s --image_id <image_id> --instance_type <instance_type>'

    @classmethod
    def add_ext_arguments(cls, parser):

        parser.add_argument('-m', '--image_id', dest='image_id',
                action='store', type=str, default='',
                help='image ID')

        parser.add_argument('-t', '--instance_type', dest='instance_type',
                action='store', type=str, default=None,
                help='instance type: small_b, small_c, medium_a, medium_b, medium_c, \
                large_a, large_b, large_c')

        parser.add_argument('-c', '--count', dest = 'count',
                action='store', type=int, default=1,
                help='the number of instances to launch, default 1.')

        parser.add_argument('-C', '--cpu', dest='cpu',
                action='store', type=int, default=None,
                help='cpu core: 1, 2, 4, 8, 16')

        parser.add_argument('-M', '--memory', dest='memory',
                action='store', type=int, default=None,
                help='memory size in MB: 512, 1024, 2048, 4096, 8192, 16384')

        parser.add_argument('-N', '--instance_name', dest='instance_name',
                action='store', type=str, default='',
                help='instance name')

        parser.add_argument('-n', '--vxnets', dest='vxnets',
                action='store', type=str, default=None,
                help='specifies the IDs of vxnets the instance will join.')

        parser.add_argument('-s', '--security_group', dest='security_group',
                action='store', type=str, default=None,
                help='the ID of security group that will be applied to instance')

        parser.add_argument('-l', '--login_mode', dest='login_mode',
                action='store', type=str, default=None,
                help='SSH login mode: keypair or passwd')

        parser.add_argument('-p', '--login_passwd', dest='login_passwd',
                action='store', type=str, default='',
                help='login_passwd, should specified when SSH login mode is "passwd".')

        parser.add_argument('-k', '--login_keypair', dest='login_keypair',
                action='store', type=str, default='',
                help='login_keypair, should specified when SSH login mode is "keypair".')

        return parser

    @classmethod
    def build_directive(cls, options):

        required_params = {
                'image_id': options.image_id,
                }
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print('error: [%s] should be specified' % param)
                return None
        if not options.instance_type:
            if not options.cpu or not options.memory:
                print('error: [instance_type] should be specified or specify both [cpu] and [memory]')
                return None

        return {
                'image_id': options.image_id,
                'instance_type' : options.instance_type,
                'cpu': options.cpu,
                'memory': options.memory,
                'instance_name' : options.instance_name,
                'count' : options.count,
                'vxnets': explode_array(options.vxnets),
                'security_group': options.security_group,
                'login_mode': options.login_mode,
                'login_passwd': options.login_passwd,
                'login_keypair': options.login_keypair,
                }
