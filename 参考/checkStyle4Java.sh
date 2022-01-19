#!/bin/bash

##脚本提供功能：JAVA代码规范是否符合统一规范

##分三个部分：
# 1.变量定义部分
# 2.校验部分：代码分析
# 3.初始化入口

##校验流程：
# 1.最后代码规范校验

##其他：
# 1.官方文档说明：https://docs.gitlab.com/ee/administration/server_hooks.html#chained-hooks

####### 初始化变量部分 #########
## 定义 JAVA_HOME 变量 
JAVA_HOME=/usr

## 获取当前路径
BASE_PATH=$(cd `dirname $0`; pwd)
#echo 'BASE_PATH: '$BASE_PATH

####### 初始化变量部分 #########


####### 校验部分：JAVA代码分析 ###########
## 代码校验
validate_code_rules()
{
    echo 'Start code analysis for java!'
    oldrev=$(git rev-parse $1)
    newrev=$(git rev-parse $2)
    refname="$3"
    #echo 'Old version: '$oldrev
    #echo 'New version: '$newrev
    #echo 'Branch: '$refname
    
    isPassed=0
    # 只判断 .java 的代码
    #echo `git config --global --list`
    FILES=`git diff --name-only ${oldrev} ${newrev} | grep -e "\.java$"`
    echo ${FILES}
    if [ -n "$FILES" ]; then
        TEMPDIR=$BASE_PATH/"tmp"
        
        # 修改文件分隔符设置，将空格去掉
        SALVEIFS=$IFS
        IFS=$(echo -en "\n\b")
        
        for FILE in ${FILES}; do
          echo $FILE
          mkdir -p "${TEMPDIR}/`dirname ${FILE}`" >/dev/null
          git show $newrev:$FILE > ${TEMPDIR}/${FILE}
        done;
        
        # 还原文件分隔符设置
        IFS=$SAVEIFS

        ## 需要阿里云P3C的插件包p3c-pmd-2.1.0.jar与该脚本在同级目录下
        echo 'Aliyun p3c-pmd checking code...'
        $JAVA_HOME/bin/java -Dpmd.language=en -cp $BASE_PATH/p3c-pmd-2.1.0.jar net.sourceforge.pmd.PMD -d $TEMPDIR -R rulesets/java/ali-comment.xml,rulesets/java/ali-concurrent.xml,rulesets/java/ali-constant.xml,rulesets/java/ali-exception.xml,rulesets/java/ali-flowcontrol.xml,rulesets/java/ali-naming.xml,rulesets/java/ali-oop.xml,rulesets/java/ali-other.xml,rulesets/java/ali-set.xml -f text
        
        RESULT=$?
        #echo $RESULT
        if [ $RESULT -gt 0 ]; then
            isPassed=1
        fi
        
    else
        echo 'No java file, skip.....'
    fi
    
    # 删除临时目录，
    rm -rf $TEMPDIR
    echo 'End java code analysis!'
    if [[ $isPassed == 1 ]]; then
        exit 1
    fi
}

####### 校验部分：JAVA代码分析 ###########

####### 执行入口###########
pre_receive()
{
    validate_code_rules $1 $2 $3
}

# update hook触发会带参数执行if逻辑
# pre-receive hooks脚本触发无参数执行else逻辑
if [ -n "$1" -a -n "$2" -a -n "$3" ]; then
    # Output to the terminal in command line mode - if someone wanted to
    # resend an email; they could redirect the output to sendmail
    # themselves
    pre_receive $2 $3 $1
    #echo $1'+'$2'+'$3
else
    while read oldrev newrev refname
    do
        pre_receive $oldrev $newrev $refname
        #echo $oldrev' '$newrev' '$refname
    done
fi
####### 执行入口###########

echo '恭喜，你的提交通过测试！'
exit 0
