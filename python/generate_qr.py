#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红色福字二维码生成器
======================

功能：
    生成红色二维码，中间带有大大的文字（默认"福"字），可选金色边框

使用方式：
    python3 generate_qr.py "你的URL"
    python3 generate_qr.py "你的URL" -t "福"
    python3 generate_qr.py "你的URL" -t "财" -o my_qrcode
    python3 generate_qr.py "你的URL" --border-color white

输出文件：
    - {prefix}.png              (无边框版本)
    - {prefix}_with_border.png  (白色边框版本)
    - {prefix}_gold_border.png  (金色边框版本)

依赖：
    pip install qrcode pillow

作者: Prometheus
日期: 2026-02-16
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode


def find_font():
    """查找系统中可用的中文字体"""
    candidates = [
        "/usr/share/fonts/wps-office/msyhbd.ttc",
        "/usr/share/fonts/wps-office/msyh.ttc",
        "/usr/share/fonts/wps-office/simhei.ttf",
        "/usr/share/fonts/wps-office/Deng.ttf",
        "/usr/share/fonts/SarasaGothicSC-TTF/SarasaGothicSC-Bold.ttf",
        "/usr/share/fonts/SarasaGothicSC-TTF/SarasaGothicSC-Regular.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.otf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def generate_qr(url, center_text="福", output_prefix="fu_qrcode", border_color="gold"):
    """生成中心带文字的二维码"""
    font_path = find_font()
    
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="red", back_color="white").convert("RGBA")
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")
    
    overlay_size = int(min(w, h) * 0.28)
    left = (w - overlay_size) // 2
    top = (h - overlay_size) // 2
    right = left + overlay_size
    bottom = top + overlay_size
    radius = int(overlay_size * 0.25)
    draw.rounded_rectangle(
        [(left, top), (right, bottom)],
        radius=radius,
        fill=(255, 255, 255, 255)
    )
    
    text = center_text
    if font_path is None:
        font = ImageFont.load_default()
    else:
        font_size = int(overlay_size * 0.72)
        font = ImageFont.truetype(font_path, font_size)
    
    try:
        bbox = font.getbbox(text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        text_w, text_h = font.getsize(text)
    
    text_x = left + (overlay_size - text_w) // 2
    text_y = top + (overlay_size - text_h) // 2 - int(overlay_size * 0.05)
    draw.text((text_x, text_y), text, font=font, fill=(255, 0, 0, 255))
    
    outputs = []
    
    out_png = f"/tmp/{output_prefix}.png"
    img.save(out_png, format="PNG")
    outputs.append(out_png)
    
    border = 20
    w2 = w + 2 * border
    h2 = h + 2 * border
    
    if border_color == "gold":
        img_border = Image.new("RGBA", (w2, h2), (255, 215, 0, 255))
        out_border = f"/tmp/{output_prefix}_gold_border.png"
    elif border_color == "white":
        img_border = Image.new("RGBA", (w2, h2), (255, 255, 255, 255))
        out_border = f"/tmp/{output_prefix}_with_border.png"
    else:
        outputs.append(None)
        return outputs
    
    img_border.paste(img, (border, border))
    img_border.save(out_border, format="PNG")
    outputs.append(out_border)
    
    return outputs


def main():
    parser = argparse.ArgumentParser(
        description="生成红色福字/文字二维码",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 generate_qr.py "https://example.com"
  python3 generate_qr.py "https://example.com" -t "福"
  python3 generate_qr.py "https://example.com" -t "财" -o caishen
  python3 generate_qr.py "https://example.com" -t "喜" --border-color white
        """
    )
    parser.add_argument("url", nargs="?", help="二维码内容 URL")
    parser.add_argument("-t", "--text", default="福", help="中间显示的文字 (默认: 福)")
    parser.add_argument("-o", "--output", default="fu_qrcode", help="输出文件前缀 (默认: fu_qrcode)")
    parser.add_argument("--border-color", choices=["gold", "white", "none"], default="gold",
                        help="边框颜色 (默认: gold)")
    
    args = parser.parse_args()
    
    if not args.url:
        print("请提供二维码内容 URL")
        print("使用方法: python3 generate_qr.py <url>")
        print("运行: python3 generate_qr.py -h 查看帮助")
        return
    
    print(f"正在生成二维码，中间文字: {args.text}...")
    outputs = generate_qr(args.url, args.text, args.output, args.border_color)
    
    print("生成完成!")
    for f in outputs:
        if f:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
