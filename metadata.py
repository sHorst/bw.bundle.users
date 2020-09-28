@metadata_reactor
def add_restic_rules(metadata):
    if not node.has_bundle("restic"):
        raise DoNotRunAgain

    add_folders = ['/root', ]

    for username, user_attrs in metadata.get('users').items():
        add_folders += ["/home/{}".format(username), ]

    return {
        'restic': {
            'backup_folders':add_folders
        }
    }
