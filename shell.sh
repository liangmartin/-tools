#!/bin/bash

#查看内存使用百分比
free | sed -n '2p' | gawk 'x = int(( $3 / $2 ) * 100) {print x}' | sed 's/$/%/'

#查看磁盘实用百分比
df -h /dev/sda1 | sed -n '/% \//p' | gawk '{ print $5 }'


