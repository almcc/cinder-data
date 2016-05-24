FROM centos:7

MAINTAINER Alastair McClelland <alastair.mcclelland@gmail.com>

RUN \
  yum install -y epel-release http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm ;\
  yum install -y python-pip ;\
  yum clean all ;\
  pip install --upgrade pip

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
