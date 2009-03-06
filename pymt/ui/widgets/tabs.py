__all__ = ['MTTabs']

from ..factory import MTWidgetFactory
from widget import MTWidget
from button import MTButton
from layout.boxlayout import MTBoxLayout

class MTTabs(MTWidget):
    '''Class that implement a tabbed notebook.
    When you add a widget into tabs, make sure
    they are at least one tab information ::

    tabs = MTTabs()
    w = MTWidget()
    w.tab = 'Title of tab'
    tabs.add_widget(w)

    or ::

    tabs = MTTabs()
    w = MTWidget()
    tabs.add_widget(w, tab='Title of tab')


    If you want to select a tab, use select() ::

    tabs = MTTabs()
    tabs.add_widget(MTButton(label="Hello"), tab='Tab1')
    tabs.add_widget(MTButton(label="World"), tab='Tab2')
    tabs.select('Tab2')

    '''
    def __init__(self, **kwargs):
        super(MTTabs, self).__init__(**kwargs)
        self.topbar = MTBoxLayout(orientation='horizontal')
        self.layout = MTBoxLayout(orientation='vertical', invert_y=True)
        self.layout.add_widget(self.topbar)
        super(MTTabs, self).add_widget(self.layout)
        self.current = None
        self.tabs = dict()
        self.layout.push_handlers(on_resize=self.on_layout_resize)

    def reposition(self):
        self.layout.pos = (self.x, self.y - self.layout.height)

    def on_layout_resize(self, w, h):
        self.reposition()

    def on_move(self, x, y):
        self.reposition()

    def add_widget(self, widget, tab=None):
        if tab is None:
            if not hasattr(widget, 'tab'):
                raise Exception('Widget added without tab information')
            else:
                tab = widget.tab
        button = MTButton(label=tab, size=(120, 40))
        button.tab_container = self
        @button.event
        def on_release(touchID, x, y):
            self.select(tab)
        self.topbar.add_widget(button)
        self.tabs[tab] = (button, widget)

    def select(self, tab):
        if tab not in self.tabs:
            return
        button, widget = self.tabs[tab]
        if self.current:
            self.layout.remove_widget(self.current, do_layout=False)
        self.layout.add_widget(widget, do_layout=False)
        self.current = widget
        self.layout.do_layout()

    def draw(self):
        super(MTTabs, self).draw()


MTWidgetFactory.register('MTTabs', MTTabs)