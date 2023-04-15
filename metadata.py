global metadata_reactor, node, DoNotRunAgain


@metadata_reactor
def add_restic_rules(metadata):
    if not node.has_bundle("restic"):
        raise DoNotRunAgain

    add_folders = {'/root', }

    for username, user_attrs in metadata.get('users').items():
        if user_attrs.get('delete', False) or user_attrs.get('exclude_backup', False):
            continue
        add_folders.add(user_attrs.get('home', f"/home/{username}"))

    return {
        'restic': {
            'backup_folders': add_folders
        }
    }
