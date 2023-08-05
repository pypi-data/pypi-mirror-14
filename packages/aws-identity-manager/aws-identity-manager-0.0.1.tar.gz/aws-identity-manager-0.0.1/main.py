import cmd2

from awsident.storage import identity_store, IdentityExists
from awsident.handlers import ConfigHandler

class Main(cmd2.Cmd):
    multilineCommands = ['add']
    add_command_steps = ['name', 'access_key_id', 'secret_access_key']
    add_command_step = None
    debug = True
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
        return True
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
    def do_edit(self, arg):
        identity_id = self.select(self.identities, 'Select Identity: ')
        identity = identity_store.get(identity_id)
        attr = self.select(self.add_command_steps, 'Select Attribute: ')
        prompt = 'Enter {0} [{1}]: '.format(attr, getattr(identity, attr))
        response = raw_input(prompt)
        if not response:
            print('No change detected')
        else:
            setattr(identity, attr, response)
            print('{0}.{1} set to {2}'.format(identity, attr, response))

def main():
    Main().cmdloop()

if __name__ == '__main__':
    main()
