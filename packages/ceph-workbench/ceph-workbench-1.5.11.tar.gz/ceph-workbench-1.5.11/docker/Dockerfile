FROM ubuntu:14.04
MAINTAINER Loic Dachary "loic@dachary.org"

# nova.clouds will redirect to the fastest mirror
RUN sed -i -e 's|http://archive.ubuntu|http://nova.clouds.archive.ubuntu|' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python-virtualenv git
RUN echo 'ALL ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN cd /opt ; git clone -b openstack http://github.com/dachary/teuthology
RUN cd /opt/teuthology ; ./bootstrap install
RUN cd /opt/teuthology ; python setup.py install
RUN pip install ceph-workbench
# the requests version installed by default system wide is not good enough (<= 2.8.1)
#  and will be used by default unless the package is removed
RUN pip install --upgrade --force-reinstall requests pip ; apt-get remove --purge -y python-requests
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
