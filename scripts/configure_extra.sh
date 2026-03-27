#!/bin/sh

make_ifcfg_file()
{
	IPADDR=$1
	DEVICE_NAME=$2

	HWADDR=`ifconfig ${DEVICE_NAME} |awk '/ether/{print $2}'`
	HWADDR=$(echo $HWADDR | tr '[a-z]' '[A-Z]')
	UUID=`nmcli connection show |grep ${DEVICE_NAME}|grep ethernet|awk '{print $2}'`

	# Base name of the interface configuration files.
	BASENAME=/etc/sysconfig/network-scripts
	#BASENAME=/home/users/if

	# Build ifcfg-en* files here
	FILE=${BASENAME}/ifcfg-${DEVICE_NAME}
	echo $FILE
	cat >$FILE <<EOF
TYPE=Ethernet
NAME=${DEVICE_NAME}
ONBOOT=yes
BOOTPROTO=static
UUID=${UUID}
HWADDR=${HWADDR}
IPADDR0=${IPADDR}
PREFIX0=24
EOF
}

make_vlan_ifcfg_file()
{
	IPADDR=$1
	DEVICE_NAME=$2
	VLAN=$3

	HWADDR=`ifconfig ${DEVICE_NAME} |awk '/ether/{print $2}'`
	HWADDR=$(echo $HWADDR | tr '[a-z]' '[A-Z]')
	NETWORK=`echo ${IPADDR}|cut -d . -f 1,2,3`
	UUID=`nmcli connection show |grep ${DEVICE_NAME}|grep ethernet|awk '{print $2}'`

	# Base name of the interface configuration files.
	BASENAME=/etc/sysconfig/network-scripts
	#BASENAME=/home/users/if

	# Build ifcfg-en* files here
	FILE=$BASENAME/ifcfg-$DEVICE_NAME
	echo $FILE
	cat >$FILE <<EOF
TYPE=Ethernet
NAME=${DEVICE_NAME}
ONBOOT=yes
BOOTPROTO=none
UUID=${UUID}
HWADDR=${HWADDR}
EOF

	FILE=${BASENAME}/ifcfg-${DEVICE_NAME}.${VLAN}
	echo $FILE
	cat >$FILE <<EOF
DEVICE=${DEVICE_NAME}.${VLAN}
ONBOOT=yes
BOOTPROTO=none
IPADDR0=${IPADDR}
PREFIX0=24
NETWORK=${NETWORK}.0
VLAN=yes
EOF

}

IPADDR=$1
INTERFACE=$2

if [ "$IPADDR" = "" ] || [ "$INTERFACE" = "" ]
then
	echo "Usage:  sh configure_extra.sh ipaddress interface" 
	echo "eg:     sh configure_extra.sh 169.15.1.1 ens2f0"
	echo "The shell is only for ADS-B Center System!"
	exit
fi

make_ifcfg_file $IPADDR $INTERFACE


