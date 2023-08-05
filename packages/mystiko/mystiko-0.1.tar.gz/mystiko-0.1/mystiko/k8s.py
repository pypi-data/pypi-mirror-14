import os

def get_secrets(directory='/etc/secrets/'):

    secret_dict = {}

    # make sure the directory has the trailing slash
    if directory[-1] != '/':
        directory = directory + '/'

    for s_key in os.listdir(directory):
        with open(directory + s_key, 'r') as sf:
            s_value = sf.read()
            secret_dict[s_key] = s_value.strip()

    return secret_dict

