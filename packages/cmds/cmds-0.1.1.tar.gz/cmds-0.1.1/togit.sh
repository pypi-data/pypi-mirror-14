#/bin/sh

nowdate=`date -d"today" +%Y%m%d%H%M%S`

srcproj=cmds
srcdir=/home/albert/git_projects/${srcproj}

destproj=cmds
destdir=/home/qiueer/github/$destproj

echo "=== BACKUP"
cp $destdir /tmp/${destproj}_{nowdate} -R

echo "=== COPY TO"
cp ${srcdir}/* ${destdir}/ -R
rm ${destdir}/togit.sh -fr
chown qiueer.qiueer ${destdir} -R