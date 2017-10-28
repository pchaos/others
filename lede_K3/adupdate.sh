#!/bin/bash  
# adbyby update Script
# By viagram
# 

i=1
DATA_PATH='/usr/share/adbyby/data'
TMP_PATH='/tmp'

function uprule(){
    local parstr=$1
    if [[ "$parstr" == "lazy" ]] || [[ "$parstr" == "video" ]];then
        echo
        echo -e "\033[32m    正在更新: ${parstr}规则,请稍等...\033[0m"
        if [[ -f $TMP_PATH/adbyby-rule.tmp ]]; then
            rm -f $TMP_PATH/adbyby-rule.tmp
        fi
        if command -v wget >/dev/null 2>&1; then
            url="http://update.adbyby.com/rule3/${1}.jpg"
            wget --no-check-certificate -t3 -T5 -c ${url} -O $TMP_PATH/adbyby-rule.tmp  >/dev/null 2>&1
            if ! head -1 $TMP_PATH/adbyby-rule.tmp | egrep -io '[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}[[:space:]*][0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'; then
                rm -f $TMP_PATH/adbyby-rule.tmp
                url="https://raw.githubusercontent.com/kysdm/adbyby/master/xwhyc-rules/${1}.txt"
                wget --no-check-certificate -t3 -T5 -c ${url} -O $TMP_PATH/adbyby-rule.tmp  >/dev/null 2>&1
            fi
        elif command -v curl >/dev/null 2>&1; then
            url="http://update.adbyby.com/rule3/${1}.jpg"
            curl -sk ${url} -o $TMP_PATH/adbyby-rule.tmp --retry 3 >/dev/null 2>&1
            if ! head -1 $TMP_PATH/adbyby-rule.tmp | egrep -io '[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}[[:space:]*][0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'; then
                rm -f $TMP_PATH/adbyby-rule.tmp
                url="https://raw.githubusercontent.com/kysdm/adbyby/master/xwhyc-rules/${1}.txt"
                curl -sk ${url} -o $TMP_PATH/adbyby-rule.tmp --retry 3 >/dev/null 2>&1
            fi
        fi
        if [[ $? -ne 0 ]]; then
            echo -e "\033[41;37m    下载 $url 失败 $? \033[0m"
            exit $?
        fi
    else
        echo -e "\033[41;37m    未知规则:${parstr}\033[0m"
        exit 1
    fi
    OLD_STR=$(head -1 $DATA_PATH/$parstr.txt | egrep -io '[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}[[:space:]*][0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}')
    OLD_INT=$(date -d "${OLD_STR}" +%s)
    NEW_STR=$(head -1 $TMP_PATH/adbyby-rule.tmp | egrep -io '[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}[[:space:]*][0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}')
    NEW_INT=$(date -d "${NEW_STR}" +%s)
    echo -e "\033[32m    规则地址: $url \033[0m"
    echo -e "\033[32m    本地版本: $OLD_STR \033[0m"
    echo -e "\033[32m    在线版本: $NEW_STR \033[0m"
    if [[ -z $NEW_STR ]]; then
        echo -e "\033[41;37m    更新结果: 获取错误.\033[0m"
        exit 1
    fi
    if [[ $OLD_INT -lt $NEW_INT  ]]; then
        \cp -f $TMP_PATH/adbyby-rule.tmp $DATA_PATH/$parstr.txt
        if [[ $? -ne 0  ]]; then
            rm -f $TMP_PATH/adbyby-rule.tmp
            echo -e "\033[32m    Error: $? \033[0m"
            exit $?
        fi
        rm -f $TMP_PATH/adbyby-rule.tmp
        echo -e "\033[32m    更新结果: 更新成功.\033[0m"
        ((i++))
        if [[ $i -gt 2 ]]; then
            /etc/init.d/adbyby restart 2>/dev/null
        fi
    else
        echo -e "\033[32m    更新结果: 规则已是最新版本.\033[0m"
    fi
}


Install_UP
if [[ -n $(ps | grep -v grep | grep -i '/adbyby') ]]; then
    uprule lazy
    uprule video
fi
