from tinycm import Dependency
from tinycm.basedefinition import BaseDefinition
from tinycm.reporting import VerifyResult

import pwd
import os


class VimDefinition(BaseDefinition):
    def __init__(self, identifier, parameters, source, after, context):
        # Run the BaseDefinition init so the graph library works
        super().__init__(identifier)

        # The usual fields
        self.identifier = identifier
        self.source = source
        self.after = after
        self.context = context
        self.name = parameters['name']

        # Optional fields
        self.is_global = parameters['is-global'] if 'is-global' in parameters else False
        self.ensure = parameters['ensure'] if 'ensure' in parameters else 'exists'
        self.config = parameters['config'] if 'config' in parameters else self._get_default_config()
        self.type = parameters['type'] if 'type' in parameters else 'constant'
        self.interpolate = parameters['interpolate'] if 'interpolate' in parameters else False

        # Add dependencies
        self.after.append('file::{}'.format(self._get_config_path()))
        if not self.is_global:
            self.after.append('user::{}'.format(self.name))

    def dependencies(self):
        user = self.name
        after = ['user::{}'.format(self.name)]
        if self.is_global:
            user = 'root'
            after = []

        after.append('package::vim')

        dependencies = [
            Dependency('package', 'vim', {'ensure': 'installed'}),
            Dependency('file', self._get_config_path(), {
                'ensure': 'exists',
                'type': self.type,
                'contents': self.config,
                'interpolate': self.interpolate,
                'permission-mask': '644',
                'owner': user,
                'after': after
            })
        ]
        if not self.is_global:
            Dependency('user', self.name, {'ensure': 'exists'})
        return dependencies

    def try_merge(self):
        pass

    def lint(self):
        pass

    def verify(self):
        return VerifyResult(self.identifier, success=True)

    def exec(self):
        pass

    def _get_config_path(self):
        if self.is_global:
            return '/etc/vim/vimrc.local'

        homedir = pwd.getpwnam(self.name).pw_dir
        return os.path.join(homedir, '.vimrc')

    def _get_default_config(self):
        return "set nocompatible\n" \
               "filetype ident plugin on\n" \
               "syntax on\n" \
               "set hlsearch\n" \
               "set ignorecase\n" \
               "set smartcase\n" \
               "set autoindent\n" \
               "set shiftwidth=4\n" \
               "set softtabstop=4\n" \
               "set expandtab\n"
