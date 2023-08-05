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

    db_pwd = k8s_secrets['db-password']


----
Name
----
"Kubernetes" is Greek for "helmsman" or "pilot."  Following that theme,
"mystiko" is Greek for "secret."

