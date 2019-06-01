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

        directories["/home/{}".format(username)] = {
            'owner': username,
            'group': username,
            'mode': "0751",
        }

        home = user_attrs.get('home', "/home/{}".format(username))
        password_hash = user_attrs.get('password_hash', no_password)
        shell = user_attrs.get('shell', default_shell)

        users[username] = {
            'home': user_attrs.get('home', "/home/{}".format(username)),
            'password_hash': user_attrs.get('password_hash', no_password),
            'shell': user_attrs.get('shell', default_shell),
            'groups': add_groups,
            'needs': ['pkg_apt:zsh'],
        }

        if 'full_name' in user_attrs:
            users[username]['full_name'] = user_attrs['full_name']
