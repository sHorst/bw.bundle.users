from passlib.hash import bcrypt

directories = {}
git_deploy = {}
actions = {}

no_password = "*"
salt = repo.vault.password_for("root_user_{}_salt".format(node.name), length=16).value
default_shell = "/bin/zsh"

users = {
    "root": {
        'password': repo.vault.password_for("root_user_{}".format(node.name)),
        'salt': salt,
        'needs': ['pkg_apt:zsh'],
    },
}

for username, user_attrs in node.metadata['users'].items():
    if user_attrs.get('delete', False):
        users[username] = {
            'delete': True,
        }
    else:
        if 'home_git' in user_attrs:
            # TODO: fix this for the current user it will break the run :/
            git_deploy['/home/{}'.format(username)] = {
                'needs': ['directory:/home/{}'.format(username)],
                'repo': user_attrs['home_git'],
                'rev': node.metadata.get('git_branch', 'master'),
                'triggers': {
                    'action:change_user_{}'.format(username),
                }
            }

            actions['change_user_{}'.format(username)] = {
                    'command': 'chown -R %s:%s /home/%s' % (username, username, username),
                    'triggered': True,
                }

        add_groups = []

        if 'add_groups' in user_attrs:
            add_groups += user_attrs['add_groups']

        home = user_attrs.get('home', "/home/{}".format(username))

        # Don't reset user password. Run if reset_password = False
        if not user_attrs.get('reset_password', True) and \
                bytes.decode(
                    node.run(f"passwd --status {username} | cut -d ' ' -f2", may_fail=True).stdout
                ).strip() == 'P':
            password_hash = bytes.decode(node.run(f"cat /etc/shadow | grep {username} | cut -d ':' -f2").stdout).strip()
        else:
            password_hash = user_attrs.get('password_hash', no_password)

        directories[home] = {
            'owner': username,
            'group': username,
            'mode': "0751",
        }

        users[username] = {
            'home': home,
            'password_hash': password_hash,
            'shell': user_attrs.get('shell', default_shell),
            'groups': add_groups,
            'needs': ['pkg_apt:zsh'],
        }

        if 'full_name' in user_attrs:
            users[username]['full_name'] = user_attrs['full_name']
