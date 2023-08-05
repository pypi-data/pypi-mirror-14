#!/usr/bin/python

import os
import sys
import yaml

ROOT_SRC = os.path.normpath(
    os.path.dirname(os.path.abspath(__file__)) + "../../../")
CONF_SRC = os.path.abspath(ROOT_SRC + "/../conf/generated")

sdconf = None


def getConfEntry(entryName):
    global sdconf
    if sdconf is None:
        sdconf = {}
        conf_file_path = "/".join([CONF_SRC, "rubrik_conf.yml"])
        conf_file = yaml.load(open(conf_file_path), Loader=yaml.CLoader)
        for inc in conf_file.get("includes", []):
            conf_inc_file = yaml.load(open("/".join([CONF_SRC, inc])),
                                      Loader=yaml.CLoader)
            for entry in conf_inc_file:
                sdconf[entry['name']] = entry['value']

    if entryName in sdconf:
        return sdconf[entryName]

    raise Exception('Invalid entry name: %s' % entryName)


if __name__ == '__main__':
    try:
        print getConfEntry(sys.argv[1])
        sys.exit(0)
    except Exception as e:
        print e
        sys.exit(1)
