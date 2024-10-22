/**
 * @class       : script
 * @author      : user (user@fedora)
 * @created     : 星期五 10月 18, 2024 10:29:51 WITA
 * Modified    : 2024-10-21 00:22:21
 * @description : script
 */


document.addEventListener("DOMContentLoaded", function() {
  // html中记住最后一次点击的tab,下次打开同样的url,自动切换到最后记录的tab
    const lastTab = localStorage.getItem('activeTab') || 'index' || 'main';
  console.log("最后保存的tab：",lastTab);
    activateTab(lastTab);
        // 为每个导航标题添加点击事件
    document.querySelectorAll('.navI-radio').forEach(link => {
        link.addEventListener('click', function() {
            const tabId = this.getAttribute('id');
            activateTab(tabId);
            localStorage.setItem('activeTab', tabId); // 保存当前选中的标签到 localStorage
        });
    });
});

function activateTab(tabId) {
    // 检查 tabId 是否有效
    const tabContent = document.getElementById(tabId);
    if (!tabContent) {
        console.error(`无效的 tabId: ${tabId}`);
        return; // 如果 tabId 无效，则退出函数
    }

    // 隐藏所有标签内容
    document.querySelectorAll('.navI-radio').forEach(tab => {
        tab.classList.remove('active');
    });

    // 移除所有标签链接的激活状态
    document.querySelectorAll('.navI-radio').forEach(link => {
        link.classList.remove('active');
    });

    // 显示当前选中的标签内容并激活对应链接
    tabContent.classList.add('active');

    const activeLink = document.querySelector(`.navI-radio[id="${tabId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    } else {
        console.warn(`未找到对应的链接: ${tabId}`);
    }
}

  function isMobileBrowser() {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
  console.log(userAgent);
    return /android|iphone|ipad|ipod|blackberry|iemobile|opera mini|AppleWebKit/i.test(userAgent);
}

  function redirectToMobile() {
            const userAgent = navigator.userAgent || navigator.vendor || window.opera;
            const currentUrl = window.location.href;

            // 检测是否为移动设备
    if (isMobileBrowser()) {
                // 检查当前 URL 是否已经是 index_phone.html
                if (!currentUrl.includes("index_phone.html")) {
                    // 重定向到手机页面
                    window.location.href = "index_phone.html";
                }
            }
        }

    function changeStylesheet() {
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.id = "stylesheet";
        link.href = "styles.tab.phone.css";
        // 获取 link 标签
            var oldLink = document.getElementById("stylesheet");
            if (oldLink) {
        document.getElementById("stylesheet").setAttribute("href", "styles.tab.phone.css");
                // oldLink.parentNode.removeChild(oldLink);
                console.log("已替换旧样式文件");
 document.head.appendChild(link);
            }
    }

function loadMobileStyles() {
    if (isMobileBrowser()) {
        console.log("检测到使用手机浏览器，准备加载样式文件...");
        
        changeStylesheet();

        var link = document.getElementById("stylesheet");
if (link) {
    console.log("已删除旧样式文件");
    console.log(link.href);
        link.onload = function() {
            console.log("样式文件加载成功！");
        };

        link.onerror = function() {
            console.error("样式文件加载失败！");
        };
    }

    } else {
        console.log("不是手机浏览器，不加载样式文件。");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");
loadMobileStyles();
});

  function myOnLoad() {
redirectToMobile();
  }

          // 页面加载时执行重定向检查
        window.onload = myOnLoad;
