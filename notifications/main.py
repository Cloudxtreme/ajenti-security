from ajenti.api import plugin
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.api.helpers import subprocess_call_background, subprocess_check_output_background
from ajenti.ui.binder import Binder
import subprocess
import logging

class Module_Info(object):
    def __init__(self,name,version):
        self.module = name
        self.version = version

    def __repr__(self):
        return '{%s: %s}' % (self.module, self.version)


@plugin
class Test (SectionPlugin):
    def init(self):
        self.title = 'Security'
        self.icon = 'smile'
        self.category = 'MyDemo'

        self.append(self.ui.inflate('mytest:nof-main'))
        self.find('style').labels = self.find('style').values = ['disabled', 'permissive', 'enforcing']
        self.find('status').value = subprocess.check_output(["getenforce"])
        
        self.data = self.get_all_modules()
        logging.info(repr(self.data))

        self.binder = Binder(self, self.find('bindroot'))

        def post_item_bind(object, collection, item, ui):
            ui.find('stop').on('click', self.on_remove, item)
            ui.find('start').on('click', self.on_start, item)
            ui.find('stop').visible = item.status
            ui.find('start').visible = item.status

        self.find("modules").post_item_bind = post_item_bind
        self.binder.populate()

    @on('show', 'click')
    def on_show(self):
        if self.find('style').value != self.find('status').value:
            logging.info("[selinux] "+self.find('style').value)
            self.modify_sestate(self.find('style').value)
            subprocess.call(["reboot"])
            self.find('status').value = self.find('style').value
        

    def modify_sestate(self,status):
        self.selinux_config_file = "/etc/selinux/config"
        subprocess.call(["sed","-i","s/^SELINUX=.*$/SELINUX="+status+"/g",self.selinux_config_file])

    def get_modules(self):
        data = {}
        for line in subprocess_check_output_background(['semodule','-l']).splitlines():
            name = line.split()[0]
            version = line.split()[1]
            data[name]=version
        return data

    def get_all_modules(self):
        data = subprocess_check_output_background(["ls","/usr/share/selinux/default"])
        data = data.split('\n')
        data = [ line[:line.find('.')] for line in data if len(line)>0 ]
        modules = []
        load_modules = self.get_modules()
        for m in data:
            if m in load_modules.keys():
                module = Module_Info(m,load_modules[m])
            else:
                module = Module_Info(m,"")
            modules.append(module)
        return modules

    def on_start(self, item):
        pass

    def on_remove(self, item):
        pass
