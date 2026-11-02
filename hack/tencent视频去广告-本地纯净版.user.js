// ==UserScript==
// @name         腾讯视频去广告（本地纯净版）
// @namespace    local
// @version      1.0.0
// @description  提炼自"网盘下载助手"：仅保留本地去广告（CSS 隐藏 + 播放器响应剥离广告/水印），零网络请求，不读取不上传 Cookie
// @match        https://v.qq.com/*
// @grant        GM_addStyle
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        unsafeWindow
// @run-at       document-body
// @noframes
// ==/UserScript==

(function () {
  "use strict";

  /* ---------- 1. CSS 隐藏广告/推广元素（纯本地） ---------- */
  GM_addStyle(
    ".txp-layer.txp-layer-dynamic-above-control,.playlist-overlay-minipay," +
    ".client_download,.nav-policy-wrap,.txp-layer:has(.txp-little-tip)," +
    ".mod_quick>div:not(:last-child),.icon_vip_pic,.adv_report," +
    ".playlist-video-modules-union,.txp-little-tip,.video-card-wrap[element-id]" +
    "{display: none !important}"
  );

  /* ---------- 本地缓存（GM 存储，无网络） ---------- */
  const load = k => { try { return JSON.parse(GM_getValue(k, "null") ?? "null"); } catch { return null; } };

  /* ---------- 2. 拦截播放器 XHR：剥离广告/水印（纯本地） ---------- */
  unsafeWindow.XMLHttpRequest = new Proxy(XMLHttpRequest, {
    construct(target) {
      let url = "", payload = "";
      return new Proxy(new target(), {
        set(t, p, v) { return Reflect.set(t, p, v); },
        get(t, p) {
          let value = t[p];

          // 拦截 open/send，捕捉 url 与 body，并把"广告信息"请求伪装成"仅视频信息"
          if (typeof value === "function") {
            value = function () {
              if (p === "open") url = arguments[1];
              if (p === "send") {
                payload = arguments[0];
                try {
                  if (url.includes("/proxyhttp")) {
                    const obj = JSON.parse(payload);
                    if (obj.buid === "vinfoad") {
                      obj.buid = "onlyvinfo";
                      payload = JSON.stringify(obj);
                      arguments[0] = payload;
                    }
                  }
                } catch { /* 非 JSON body（如 FormData）：保持原请求不动 */ }
              }
            };
          }

          // 改写响应
          if (p === "response" && url.endsWith("/proxyhttp")) {
            if (payload.includes("onlyad")) value = '{"errCode":1}'; // 广告请求直接报错
            if (payload.includes("onlyvinfo")) {
              try {
                const cache = load("vi");
                const obj = JSON.parse(payload);
                const vid = new URLSearchParams(obj.vinfoparam).get("vid");
                if (vid === cache?.vid) {
                  value = cache.doc; // 命中本地缓存，直接复用
                } else {
                  const d = JSON.parse(value);
                  const vinfo = JSON.parse(d.vinfo);
                  if (Object.hasOwn(vinfo, "dltype")) {
                    vinfo.preview = Number.parseInt(vinfo.vl.vi[0].td); // 试看时长=总时长
                    vinfo.vl.vi[0].ad = null; // 去广告
                    vinfo.vl.vi[0].wl = null; // 去水印
                    vinfo.fl.cnt = 1;
                    d.vinfo = JSON.stringify(vinfo);
                    value = JSON.stringify(d);
                    save("vi", { vid, doc: value });
                  }
                }
              } catch { /* 腾讯返回非 JSON（错误页等）：原样返回，不打乱播放器 */ }
            }
          }
          return value;
        },
      });
    },
  });
})();