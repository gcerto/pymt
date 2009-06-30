'''
Modules: UI module you can plug on any running PyMT apps.
'''

__all__ = ['pymt_modules']

import pymt
import os
import sys

class ModuleContext:
    pass

class Modules:
    def __init__(self, **kwargs):
        self.mods = {}
        self.wins = []

    def add_path(self, path):
        '''Add a path to search modules in'''
        if not os.path.exists(path):
            return
        if path not in sys.path:
            sys.path.append(path)
        dirs = os.listdir(path)
        for module in dirs:
            if module[-3:] != '.py' or module == '__init__.py':
                continue
            module = module[:-3]
            self.mods[module] = {'id': module, 'activated': False, 'context': ModuleContext()}

    def list(self):
        '''Return the list of available modules'''
        return self.mods

    def activate_module(self, id, win):
        '''Activate a module on a window'''
        if not id in self.mods:
            pymt.pymt_logger.warning('Module <%s> not found' % id)
            return

        if not 'module' in self.mods[id]:
            module = __import__(name=id, fromlist='mods')
            # basic check on module
            if not hasattr(module, 'start'):
                pymt.pymt_logger.warning('Module <%s> missing start() function' % id)
                return
            if not hasattr(module, 'stop'):
                pymt.pymt_logger.warning('Module <%s> missing stop() function' % id)
                return
            self.mods[id]['module'] = module

        module = self.mods[id]['module']
        if not self.mods[id]['activated']:
            module.start(win, self.mods[id]['context'])

    def deactivate_module(self, id, win):
        '''Deactivate a module from a window'''
        if not id in self.mods:
            pymt.pymt_logger.warning('Module <%s> not found' % id)
            return
        if not hasattr(self.mods[id], 'module'):
            return
        module = self.mods[id]['module']
        if self.mods[id]['activated']:
            module.stop(win, self.mods[id]['context'])

    def register_window(self, win):
        '''Add window in window list'''
        self.wins.append(win)
        self.update()

    def update(self):
        '''Update status of module for each windows'''
        modules_to_activate = map(lambda x: x[0], pymt.pymt_config.items('modules'))
        for win in self.wins:
            for id in self.mods:
                if not id in modules_to_activate:
                    self.deactivate_module(id, win)
            for id in modules_to_activate:
                self.activate_module(id, win)


pymt_modules = Modules()
pymt_modules.add_path(pymt.pymt_modules_dir)
if not os.path.basename(sys.argv[0]).startswith('sphinx'):
    pymt_modules.add_path(pymt.pymt_usermodules_dir)

if __name__ == '__main__':
    print pymt_modules.list()
