from ajenti.api import plugin
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
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
        self

    @on('show', 'click')
    def on_show(self):
        if self.find('style').value != self.find('status').value:
            logging.info("[selinux] "+self.find('style').value)
            self.modify_sestate(self.find('style').value)
            subprocess.call(["reboot"])
            self.find('status').value = self.find('style').value
        # if self.find('status').value == "permissive":
        #     print subprocess.call(["setenforce","0"])
        # elif self.find('status').value == "enforcing":
        #     print subprocess.call(["setenforce","1"])

    def modify_sestate(self,status):
        self.selinux_config_file = "/etc/selinux/config"
        subprocess.call(["sed","-i","s/^SELINUX=.*$/SELINUX="+status+"/g",self.selinux_config_file])