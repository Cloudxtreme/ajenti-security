from ajenti.api import plugin
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.api.helpers import subprocess_call_background, subprocess_check_output_background
from ajenti.ui.binder import Binder
import subprocess
import logging

@plugin
class Test (SectionPlugin):
    def init(self):
        self.title = 'Security'
        self.icon = 'smile'
        self.category = 'MyDemo'

        self.append(self.ui.inflate('mytest:nof-main'))
        self.find('style').labels = self.find('style').values = ['disabled', 'permissive', 'enforcing']
        self.find('status').value = subprocess.check_output(["getenforce"])
        
        self.data = self.get_modules()

        self.binder = Binder(self, self.find('bindroot'))
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
        data = []
        for line in subprocess_check_output_background(['semodule','-l']).splitlines():
            module = {line.split()[0]:line.split()[1]}
            data.append(module)
        return data

