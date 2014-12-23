from ajenti.api import *
from ajenti.plugins import *

info = PluginInfo(
	title = 'myTest',
	icon = None,
	dependencies = [
		PluginDependency('main'),
	],
)

def init():
	#import main
	import notifications.main