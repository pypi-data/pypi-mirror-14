import os
import re


def get_kubernetes_secrets_file_dicts(directory):
    """
    Retrieves secrets files from the given directory that match the hyphenated
    Kubernetes naming convention.

    Args:
        directory: The directory the Kubernetes secrets are located in.

    Yields:
        A dictionary with the filename as uppercase with underscores
        (secret-key becomes SECRET_KEY) as the key and the value contained
        within the file as the value per file.
    """
    kubernetes_secret_re = re.compile(r'^[a-z]+(-[a-z]+)*$')

    for filename in os.listdir(directory):
        # Make sure we only look at files, not directories
        if not os.path.isfile(os.path.join(directory, filename)):
            continue

        # Does the file name match the hyphenated Kubernetes naming convention?
        if not kubernetes_secret_re.match(filename):
            continue

        with open(os.path.join(directory, filename)) as secret_file:
            # Convert the filename to uppercase with underscores
            constant = filename.replace('-', '_').upper()

            # Yield the constant as the key, and the stripped
            yield {constant: secret_file.read().strip()}


def get_secrets(directory='/etc/secrets/'):
    """
    Args:
        directory: The directory the Kubernetes secrets are located in.

    Returns:
        A dictionary with the filename as uppercase with underscores
        (secret-key becomes SECRET_KEY) as the key and the value contained
        within the file as the value.
    """
    # Make sure the directory has the trailing slash
    directory = os.path.join(directory, '')

    # Make sure the directory exists
    if not os.path.exists(directory):
        raise ValueError('Directory "{}" does not exist'.format(directory))

    secrets = {}

    for secret_dict in get_kubernetes_secrets_file_dicts(directory):
        secrets.update(secret_dict)

    return secrets
