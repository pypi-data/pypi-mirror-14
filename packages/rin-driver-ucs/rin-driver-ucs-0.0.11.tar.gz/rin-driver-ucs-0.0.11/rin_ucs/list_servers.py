from UcsSdk import *
from UcsSdk.MoMeta.LsServer import LsServer
from rin.config import Config

import json
import os,sys

DEFAULT_PATH = '/usr/local/etc/rin-ucs.yml'

def get_blade_info(opts):
    handle = UcsHandle()

    def _filter(data):
        return not data.Name == 'ESXi'

    try:
        handle.Login(opts['server'], opts['userid'], opts['passwd'])
        ret = [{
            'name': blade.Name,
            'location': ' / '.join(blade.PnDn.split('/')[1:]),
            'status': blade.OperState,
            'manager': "UCS:%s" % (opts['server']),
            'type': 'PhysicalMachine'
            } for blade in handle.GetManagedObject(None, LsServer.ClassId()) if _filter(blade)]

        handle.Logout()
    except Exception, err:
        print "Runtime error: %s" % str(err)
        handle.Logout()

    return ret

def main():
    blades = []
    conf = Config.load(DEFAULT_PATH if 'RIN_CONFIG' in os.environ else os.environ['RIN_CONFIG'])
    if conf == None:
        sys.exit(1)

    for manager_info in conf['ucs']:
        blades += get_blade_info(manager_info)

    print json.dumps(blades)
