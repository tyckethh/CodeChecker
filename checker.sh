#!/bin/bash

## 获取当前路径
BASE_PATH=$(cd `dirname $0`; pwd)
#echo 'BASE_PATH: '$BASE_PATH

echo "开始进行本次提交检查"

# 此处修改成你电脑的 python3 解释器路径
#/var/data/py_env/p4git/bin/python3.9 $BASE_PATH/main.py $BASE_PATH
python3 $BASE_PATH/main.py $BASE_PATH

if [[ $? == 1 ]]; then
    echo "本次提交不通过，请修改后提交！"
    exit 1
fi

echo "恭喜，你的提交通过测试，继续保持呦~"
exit 0
