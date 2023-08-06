=======
mystiko
=======

Collect Kubernetes secrets into a python dictionary.  For use by python
applications running in Docker containers.


-------
Install
-------
Install package::

    pip install mystiko


-----
Usage
-----
Assuming you have given Kubernetes a secret with key "db-password"::

    from mystiko import k8s
    k8s_secrets = k8s.get_secrets()
    db_pwd = k8s_secrets['DB_PASSWORD']

The default secrets directory is `/etc/secrets/`.  If you are using a different
directory, supply it to the `get_secrets` function::

    from mystiko import k8s
    k8s_secrets = k8s.get_secrets(directory='/your/directory/')


----
Name
----
"Kubernetes" is Greek for "helmsman" or "pilot."  Following that theme,
"mystiko" is Greek for "secret."

