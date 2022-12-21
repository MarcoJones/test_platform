 #!/bin/bash
base_dir=/home/jones/interface_test_platform
res='ls -A $base_dir'
jenkins_dir=$WORKSPACE/interface_test_platform
# 判断部署目录是否为空
if [-z $res];then
# 如果为空直接拷贝部署文件到部署目录
cp -r $jenkins_dir/* $base_dir/
echo pwd
cd $base_dir/
python3 manage.py runserver
else
# 不为空先清理部署目录再拷贝部署
rm -rf $base_dir/*
cp -r $jenkins_dir/* $base_dir/
echo pwd
cd $base_dir/
fi
nohup python manage.py runserver 0.0.0.0:8000 > /dev/null   2>&1 &
