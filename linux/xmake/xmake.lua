set_languages("cxx17", "C99")

-- add_requires("fmt", {system=false})
add_requires("fmt", {configs = {header_only = true, vs_runtime = "MD"}})

-- add_requires("spdlog", {configs = {header_only = true, fmt_external=true, vs_runtime = "MD"}})
add_requires("spdlog", {configs = {header_only = true, fmt_external=false, vs_runtime = "MD"}})

  local s = format("工程目录: $(projectdir), $(curdir)")
  -- print(s)

if is_mode("debug") then
    set_configvar("LOG_ACTIVE_LEVEL", 0)  -- 激活的日志级别
else
    set_configvar("LOG_ACTIVE_LEVEL", 2)  -- 激活的日志级别
end
set_configvar("USE_SPDLOG_LOGGER", 1) -- 是否使用spdlog作为日志输出
set_configvar("USE_SPDLOG_ASYNC_LOGGER", 0) -- 使用异步的spdlog
set_configvar("CHECK_ACCESS_BOUND", 1)
if is_plat("macosx") then
    set_configvar("SUPPORT_SERIALIZATION", 0)
else
    set_configvar("SUPPORT_SERIALIZATION", is_mode("release") and 1 or 0)
  end
set_configvar("SUPPORT_TEXT_ARCHIVE", 0)
set_configvar("SUPPORT_XML_ARCHIVE", 1)
set_configvar("SUPPORT_BINARY_ARCHIVE", 1)
set_configvar("HKU_DISABLE_ASSERT", 0)

target("test")
    if is_mode("debug") then
        -- set_kind("static")
        set_kind("binary")
    else
        set_kind("binary")
    end
    add_packages("fmt", "spdlog")
    set_configdir("./")
    add_configfiles("$(projectdir)/config.h.in")
    add_includedirs("..")
    add_files("*.cpp")
target_end()

before_build(function(target)
  -- do what before before_build
  print(s)
end)
