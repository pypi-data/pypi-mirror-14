import sys
import os
import glob
import argparse

import cmd2

from awsident.storage import identity_store, IdentityExists, IAMCSVParser
from awsident.handlers import ConfigHandler

PY2 = sys.version_info.major == 2

class Main(cmd2.Cmd):
    prompt = '> '
    doc_cmds = ['save', 'change', 'add', 'edit', 'import', 'reload']
    undoc_cmds = ['exit', 'help', 'quit']
    multilineCommands = ['add']
    add_command_steps = ['name', 'access_key_id', 'secret_access_key']
    add_command_step = None
    pytest_mode = False
    @property
    def identities(self):
        return [(key, str(identity)) for key, identity in identity_store.items()]
    def do_save(self, *args):
        try:
            identity = ConfigHandler.save_identity()
            print('Current credentials saved as "{0}"'.format(identity))
        except IdentityExists as e:
            print('Credentials already saved as "{0}"'.format(e.existing))
    def help_save(self):
        print('Saves credentials (if any) found in existing config files')
    def do_change(self, arg):
        identity_id = self.select(self.identities, 'Select Identity: ')
        identity = ConfigHandler.change_identity(identity_id)
        print('Switched identity to {0}'.format(identity))
        if not self.pytest_mode:
            return True
    def help_change(self):
        print('Select a saved identity and set credentials in your config files')
    def parsed(self, raw, **kwargs):
        if raw.startswith('add'):
            if self.add_command_step is None:
                self.add_command_step = 0
            elif self.add_command_step < len(self.add_command_steps):
                self.add_command_step += 1
            try:
                attr = self.add_command_steps[self.add_command_step]
                self.continuation_prompt = '{0}: '.format(attr)
            except IndexError:
                raw = '{0};'.format(raw)
                self.add_command_step = None
        return cmd2.Cmd.parsed(self, raw, **kwargs)
    def do_add(self, arg):
        vals = arg.split('\n')
        d = {k:v for k, v in zip(self.add_command_steps, vals)}
        try:
            identity = identity_store.add_identity(d)
            print('Identity {0} added'.format(identity))
        except IdentityExists as e:
            print('Identity already exists: {0}'.format(e.existing))
    def help_add(self):
        print('Add a new identity interactively')
    def do_edit(self, arg):
        identity_id = self.select(self.identities, 'Select Identity: ')
        identity = identity_store.get(identity_id)
        attr = self.select(self.add_command_steps, 'Select Attribute: ')
        prompt = 'Enter {0} [{1}]: '.format(attr, getattr(identity, attr))
        if PY2:
            response = raw_input(prompt)
        else:
            response = input(prompt)
        if not response:
            print('No change detected')
        else:
            setattr(identity, attr, response)
            print('{0}.{1} set to {2}'.format(identity, attr, response))
    def help_edit(self):
        print('Select a saved identity and edit its settings')
    def do_import(self, arg):
        parser = IAMCSVParser(os.path.expanduser(arg))
        identities = parser()
        names = []
        for identity in identities:
            try:
                identity_store.add_identity(identity)
                names.append(identity.name)
            except IdentityExists:
                print('Identity "{0}" already exists'.format(identity))
        print('Imported identities: {0}'.format(', '.join(names)))
    def help_import(self):
        print('Import identities from a csv file downloaded from the IAM Console')
    def complete_import(self, text, line, begIdx, endIdx):
        return self._path_completions(text, line, begIdx, endIdx)
    def _path_completions(self, text, line, begIdx, endIdx):
        def _append_slash_if_dir(p):
            if p and os.path.isdir(p) and not p.endswith(os.sep):
                return ''.join([p, os.sep])
            return p
        before_arg = line.rfind(" ", 0, begIdx)
        if before_arg == -1:
            return # arg not found

        fixed = line[before_arg+1:begIdx]  # fixed portion of the arg
        arg = line[before_arg+1:endIdx]
        pattern = line[before_arg+1:endIdx] + '*'
        user_dir = os.path.expanduser('~' + os.sep)

        completions = []
        for path in glob.glob(os.path.expanduser(pattern)):
            path = _append_slash_if_dir(path)
            if path.startswith(user_dir) and pattern.startswith('~'):
                path = path.replace(user_dir, '~' + os.sep)
            completions.append(path.replace(fixed, "", 1))
        return completions
    def do_reload(self, arg):
        identity_store.reload()
        print('Reload complete')
    def help_reload(self):
        print('Reloads identities from config file')
    def print_topics(self, header, cmds, cmdlen, maxcol):
        if 'Documented commands' in header:
            cmds = self.doc_cmds
        elif 'Undocumented commands' in header:
            cmds = self.undoc_cmds
        cmd2.Cmd.print_topics(self, header, cmds, cmdlen, maxcol)
    def preloop(self):
        self.do_help('')

def main():
    default_conf = '~/.aws-identity-manager'
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--config', dest='config_path', default=default_conf,
        help='Configuration path (default is {0})'.format(default_conf))
    p.add_argument('--pytest-mode', dest='pytest_mode', action='store_true')
    args, remaining = p.parse_known_args()
    o = vars(args)
    sys.argv = remaining
    config_path = os.path.expanduser(o.get('config_path'))
    identity_store.config_path = config_path
    ConfigHandler.handler_config_path = config_path
    Main.pytest_mode = o.get('pytest_mode')
    app = Main()
    return app

def run():
    app = main()
    app.cmdloop()

if __name__ == '__main__':
    run()
