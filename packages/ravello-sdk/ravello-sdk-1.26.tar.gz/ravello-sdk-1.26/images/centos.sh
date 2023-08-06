#!/bin/bash
#
# Based on centos.sh from libguestfs.
# Copyright (C) 2013-2014 Red Hat Inc. GPL licensed.
#
# Adapted by Ravello Systems, Inc.

set -e
set -x

if [ $# -ne 1 ]; then
    echo "$0 VERSION"
    exit 1
fi

version=$1
output=centos-$version.img
tmpname=tmp-$(tr -cd 'a-f0-9' < /dev/urandom | head -c 8)
tree=http://mirror.centos.org/centos/$version/os/x86_64/

rm -f $output

# Generate the kickstart to a temporary file.
tmpdir=$(mktemp -d)
ks=$tmpdir/ks.cfg
cat > $ks <<'EOF'
install
text
reboot
lang en_US.UTF-8
keyboard us
network --bootproto dhcp
rootpw ravelloCloud
firewall --enabled --ssh
selinux --enforcing
timezone --utc America/New_York
bootloader --location=mbr --timeout=2 --append="nomodeset rd_NO_PLYMOUTH"
zerombr
clearpart --all --initlabel
part /     --fstype=ext4 --size=1024 --grow --asprimary

# Halt the system once configuration has finished.
poweroff

%packages
@core
%end

%post
# Show logging information on tty6 (ALT-F6)
exec >/dev/tty6 2>&1

rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
yum -y install cloud-utils cloud-init dracut-modules-growroot
# XXX: if "yum update" doesn't install a new kernel then the dracut growroot
# module will not end up in the initramfs.
yum -y update

sed -i -e 's/cloud-user/ravello/' /etc/cloud/cloud.cfg
sed -i -e 's/NM_CONTROLLED=.*/NM_CONTROLLED=no/' /etc/sysconfig/network-scripts/ifcfg-eth0
%end
EOF

# Clean up function.
cleanup ()
{
    rm -f $ks
    rmdir $tmpdir
    virsh undefine $tmpname ||:
}
trap cleanup INT QUIT TERM EXIT ERR

qemu-img create -f qcow2 $output 2G

virt-install \
    --name=$tmpname \
    --ram=2048 \
    --cpu=host --vcpus=2 \
    --os-type=linux --os-variant=rhel$version \
    --initrd-inject=$ks \
    --extra-args="ks=file:/ks.cfg console=tty0 console=ttyS0,115200 proxy=$http_proxy" \
    --disk $(pwd)/$output \
    --serial pty \
    --location=$tree \
    --nographics \
    --noreboot

virt-sysprep -a $output
virt-sparsify $output $output.sparse
mv -f $output.sparse $output
