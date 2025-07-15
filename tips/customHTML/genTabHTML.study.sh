#!/usr/bin/env bash
# Modified: 2025-07-15 13:04:24

# 是否启用详细模式的参数是 -v
verbose_mode=false

# 遍历所有传入的参数
for arg in "$@"; do
  if [[ "$arg" == "-v" ]]; then
    verbose_mode=true
    break
  fi
done

# 根据是否启用详细模式来执行不同的语句
if $verbose_mode; then
  echo "Verbose mode activated"
  # 使用 -s 参数来禁用标准输出捕获，print 的输出就会在测试运行时显示出来
  pytest -s --headless -vvv test_genTABHTML.py::TestGenPchaosGitIo
else
  传入"-v"参数,显示更多内容
  # pytest test_genTABHTML.py
  pytest --headless -vvv test_genTABHTML.py::TestGenPchaosGitIo
  # pytest --headless -vvv test_genTABHTML.py::TestGenPchaosGitIo::test_genHTML_phone
fi
echo copy files ... $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/index.html index_phone.html
cp -v --update script.js styles.tab.css styles.tab.phone.css $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/
cp -v /tmp/index.html /tmp/index_phone.html $HOME/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/

echo Done

# 从生成的文件中提取text url
# pytest -vvv -s test_genTABHTML.py::TestUnGenHTML > /tmp/url.txt

# 更新index.html，并且推送到github
#if [ "$(basename "$PWD")" != "customHTML" ]; then z custom; fi && ./genTabHTML.study.sh && z gupiao pchaos && git add . && git cm "update" && git push && cd -
