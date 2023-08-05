ceph-workbench
==============

`ceph-workbench
<http://ceph-workbench.dachary.org/root/ceph-workbench>`_ is a
:ref:`GPLv3+ Licensed <gplv3>` command-line toolbox for `Ceph <http://ceph.com>`_.

Installation
------------

* Install Docker http://docs.docker.com/engine/installation/

* Copy the following shell function to ``~/.bashrc``::

    function ceph-workbench() {
       mkdir -p $HOME/.ceph-workbench
       sudo docker run --rm -ti \
           -v $HOME/.ceph-workbench:/opt/.ceph-workbench \
           -v /var/run/docker.sock:/run/docker.sock \
           -v $(which docker):/bin/docker \
           $(w=$(git rev-parse --show-toplevel 2>/dev/null) && echo "-v $w:$w -w $w") \
           --env USER_ID=$(id -u) --env USER_NAME=$(id -un) \
           dachary/ceph-workbench \
           ceph-workbench "$@"
    }

* Verify that it works::

    ceph-workbench --help

* Optionally copy your OpenStack ``$PROJECT-openrc.sh`` file to
  ``~/.ceph-workbench/openrc.sh``: the ``ceph-qa-suite`` subcommand will
  use it.
    
User Guide
----------

The document `Contributing to Ceph: A Guide for Developers
<http://docs.ceph.com/docs/master/dev/>`_ explains the context in
which ``ceph-workbench`` can be used.

Contributor Guide
-----------------

If you want to contribute to ``ceph-workbench``, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 1

   dev/philosophy
   dev/authors
