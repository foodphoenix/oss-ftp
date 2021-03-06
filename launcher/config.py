
import os
import launcher_log


import json
from distutils.version import LooseVersion


current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath( os.path.join(current_path, os.pardir))
data_path = os.path.join(root_path, 'data')
config_path = os.path.join(root_path, 'config.json')

config = {}
def load():
    global config, config_path
    try:
        config = json.load(file(config_path, 'r'))
        #print json.dumps(config, sort_keys=True, separators=(',',':'), indent=4)
    except Exception as  exc:
        print "Error in configuration file:", exc


def save():
    global config, config_path
    try:
        json.dump(config, file(config_path, "w"), sort_keys=True, separators=(',',':'), indent=2)
    except Exception as e:
        launcher_log.warn("save config %s fail %s", config_path, e)

def get(path, default_val=""):
    global config
    try:
        value = default_val
        cmd = "config"
        for p in path:
            cmd += '["%s"]' % p
        value = eval(cmd)
        return value
    except:
        return default_val

def _set(m, k_list, v):
    k0 = k_list[0]
    if len(k_list) == 1:
        m[k0] = v
        return
    if k0 not in m:
        m[k0] = {}
    _set(m[k0], k_list[1:], v)

def set(path, val):
    global config
    _set(config, path, val)

def recheck_module_path():
    global config
    need_save_config = False

    modules = ["ossftp", "launcher"]

    if get(["modules", "ossftp", "address"], -1) == -1:
        need_save_config = True
        set(["modules", "ossftp", "address"], "127.0.0.1")

    if get(["modules", "ossftp", "port"], -1) == -1:
        need_save_config = True
        set(["modules", "ossftp", "port"], 2048)

    if get(["modules", "launcher", "control_port"], 0) == 0:
        need_save_config = True
        set(["modules", "launcher", "control_port"], 8192)

    return need_save_config

def create_data_path():
    if not os.path.isdir(data_path):
        os.mkdir(data_path)

    data_launcher_path = os.path.join(data_path, 'launcher')
    if not os.path.isdir(data_launcher_path):
        os.mkdir(data_launcher_path)

    data_ossftp_path = os.path.join(data_path, 'ossftp')
    if not os.path.isdir(data_ossftp_path):
        os.mkdir(data_ossftp_path)

def main():
    create_data_path()
    if os.path.isfile(config_path):
        load()

    if recheck_module_path():
        save()

main()

def test():
    load()
    val = get(["web_ui", "popup_webui"], 0)
    print val

def test2():
    set(["web_ui", "popup_webui"], 0)
    set(["web_ui", "popup"], 0)
    print config

if __name__ == "__main__":
    test2()
    #main()
    #a = eval('2*3')
    #eval("conf = {}")
