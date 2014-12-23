from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on


@plugin
class TestPlugin (SectionPlugin):
    def init(self):
        self.title = 'Test'  # those are not class attributes and can be only set in or after init()
        self.icon = 'question'
        self.category = 'MyDemo'

        """
        UI Inflater searches for the named XML layout and inflates it into
        an UIElement object tree
        """
        self.append(self.ui.inflate('mytest:main'))

        self.counter = 0
        self.refresh()

    def refresh(self):
        """
        Changing element properties automatically results
        in an UI updated being issued to client
        """
        self.find('counter-label').text = 'Counter: %i' % self.counter

    @on('increment-button', 'click')
    def on_button(self):
        """
        This method is called every time a child element
        with ID 'increment-button' fires a 'click' event
        """
        self.counter += 1
        self.refresh()