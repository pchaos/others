-- xmake.lua
-- Modified: 2024-11-04 20:37:05
-- 定义目标
target("run_tests")
set_kind("education") -- 设置为虚拟目标，不生成实际文件

-- 在构建时执行 pytest 命令
on_build(function()
  os.exec("pytest --headless -vvv test_genTABHTML.py::TestGenPchaosGitIo")
end)

target("copy_files")
set_kind("education") -- 设置为虚拟目标，不生成实际文件

-- 在构建时执行文件复制命令
on_build(function()
  os.exec(
    "cp -v --update script.js styles.tab.css styles.tab.phone.css ${HOME}/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/")
  os.exec("cp -v /tmp/index.html /tmp/index_phone.html ${HOME}/myDocs/YUNIO/tmp/gupiao/pchaos.github.io/")
end)

-- 定义默认目标
target("default")
set_kind("education")
add_deps("run_tests") -- 默认执行测试和复制文件的目标
add_deps("copy_files") -- 复制文件的目标依赖于测试完成
