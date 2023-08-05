# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import os.path as osp
import re
import getpass
from soma.crypt import generate_RSA, encrypt_RSA, decrypt_RSA

from catidb_api import catidb_url

def find_login_and_password(server):
    """
    Automatically find a login and password according to user 
    configuration and targeted server
    """
    # Find file containing passwords
    secrets = os.environ.get('CATI_SECRETS')
    if secrets is None:
        for i in ('~/.catidb/secrets', '/etc/catidb/secrets'):
            secrets = osp.expanduser(i)
            if osp.exists(secrets):
                break
        else:
            raise EnvironmentError('Cannot find any valid secrets file for automatic login to CatiDB')
    
    # Find file containing RSA key
    private_file = osp.expanduser(os.environ.get('CATI_RSA', '~/.catidb/id_rsa'))

    # Find an entry for the current user and server in the secrets file
    user = getpass.getuser()
    for line in decrypt_RSA(private_file, open(secrets).read()).split('\n'):
        user_re, server_re, login, password = line.split('\t')
        if re.match(user_re, user) and re.match(server_re, server):
            return (login, password)
    raise EnvironmentError('Cannot find login and password for CatiDB server %s' % server)

    
def store_login_and_password(login, password, server=catidb_url, secrets_file=None):
    """
    Store a login and password to use for automatic login on the given server.
    The password is passed to the function in clear text. It's the user
    responsability to enter it securely (for instance using the getpass
    standard module).
    """
        
    # Find file containing private RSA key
    private_file = osp.expanduser(os.environ.get('CATI_RSA', '~/.catidb/id_rsa'))
    public_file = private_file + '.pub'
    if not osp.exists(private_file):
        # Create the private and public key files
        directory = osp.dirname(private_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        private, public = generate_RSA()
        open(private_file,'w').write(private)
        os.chmod(private_file, 0600)
        open(public_file,'w').write(public)
    user = getpass.getuser()
    line = '\t'.join(('^%s$' % user, '^%s$' % server, login, password))
    if secrets_file is None:
        secrets_file = osp.expanduser('~/.catidb/secrets')
    if osp.exists(secrets_file):
        content = open(secrets_file).read()
        if content:
            lines = decrypt_RSA(private_file, content).split('\n')       
            for i in xrange(len(lines)):
                user_re, server_re, login, password = lines[i].split('\t')
                if re.match(user_re, user) and re.match(server_re, server):
                    lines[i] = line
            else:
                lines.append(line)
        else:
            lines = [line]
        open(secrets_file,'w').write(encrypt_RSA(public_file, '\n'.join(lines)))
    else:
        open(secrets_file,'w').write(encrypt_RSA(public_file, line))
        os.chmod(secrets_file, 0600)
