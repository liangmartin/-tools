#!/bin/bash
set -e
[ $(id -u) -gt 0 ] && exit 1

#cpu超过多少限制
PEC_CPU=80

LIMIT_CPU=85

LOG_DIR=/var/log/cpulimit/

# 超过阀值进程pid
PIDARG=$(ps -aux |awk -v CPU=${PEC_CPU} '{if($3 > CPU) print $2}')
CPULIMITCMD=$(which cpulimit)

install_cpulimit() {
	[ ! -d /tmp ] && mkdir /tmp || cd /tmp
	wget -c https://github.com/opsengine/cpulimit/archive/v0.2.tar.gz
	tar -zxf v0.2.tar.gz
	cd cpulimit-0.2 && make
	[ $? -eq 0 ] && cp src/cpulimit /usr/bin/
}


do_cpulimit() {
[ ! -d ${LOG_DIR} ] && mkdir -p ${LOG_DIR}
for i in ${PIDARG};
do
        MSG=$(ps -aux |awk -v pid=$i '{if($2 == pid) print $0}')
        echo ${MSG}
	[ ! -d /tmp ] && mkdir /tmp || cd /tmp
	nohup ${CPULIMITCMD} -p $i -l ${LIMIT_CPU} &
        echo "$(date) -- ${MSG}" >> ${LOG_DIR}$(date +%F).log
done
}

main() {

	hash cpulimit
	if [ $? -eq 0 ];then
		do_cpulimit
	else
		install_cpulimit && do_cpulimit
	fi
}

main
