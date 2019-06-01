@metadata_processor
def add_restic_rules(metadata):
    if node.has_bundle('restic'):
        backup_folders = ['/root', ]

        for username, user_attrs in metadata['users'].items():
            backup_folders += ["/home/{}".format(username), ]

        if 'restic' not in metadata:
            metadata['restic'] = {}

        metadata['restic']['backup_folders'] = metadata['restic'].get('backup_folders', []) + backup_folders

    return metadata, DONE
