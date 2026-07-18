import sys
import os
import argparse
import freetype
from PIL import Image, ImageDraw, ImageFont
from litemapy import Schematic, Region, BlockState

MINECRAFT_CONCRETE_COLORS = {
    'white': {'name': '白色', 'abbr': 'W', 'rgb': (255, 255, 255), 'block': 'minecraft:white_concrete'},
    'orange': {'name': '橙色', 'abbr': 'O', 'rgb': (255, 163, 0), 'block': 'minecraft:orange_concrete'},
    'magenta': {'name': '品红色', 'abbr': 'M', 'rgb': (255, 0, 255), 'block': 'minecraft:magenta_concrete'},
    'light_blue': {'name': '淡蓝色', 'abbr': 'LB', 'rgb': (0, 191, 255), 'block': 'minecraft:light_blue_concrete'},
    'yellow': {'name': '黄色', 'abbr': 'Y', 'rgb': (255, 255, 0), 'block': 'minecraft:yellow_concrete'},
    'lime': {'name': '黄绿色', 'abbr': 'L', 'rgb': (0, 255, 0), 'block': 'minecraft:lime_concrete'},
    'pink': {'name': '粉红色', 'abbr': 'P', 'rgb': (255, 192, 203), 'block': 'minecraft:pink_concrete'},
    'gray': {'name': '灰色', 'abbr': 'Gy', 'rgb': (128, 128, 128), 'block': 'minecraft:gray_concrete'},
    'silver': {'name': '淡灰色', 'abbr': 'S', 'rgb': (192, 192, 192), 'block': 'minecraft:light_gray_concrete'},
    'cyan': {'name': '青色', 'abbr': 'C', 'rgb': (0, 255, 255), 'block': 'minecraft:cyan_concrete'},
    'purple': {'name': '紫色', 'abbr': 'V', 'rgb': (128, 0, 128), 'block': 'minecraft:purple_concrete'},
    'blue': {'name': '蓝色', 'abbr': 'B', 'rgb': (0, 0, 255), 'block': 'minecraft:blue_concrete'},
    'brown': {'name': '棕色', 'abbr': 'Br', 'rgb': (165, 42, 42), 'block': 'minecraft:brown_concrete'},
    'green': {'name': '绿色', 'abbr': 'G', 'rgb': (0, 128, 0), 'block': 'minecraft:green_concrete'},
    'red': {'name': '红色', 'abbr': 'R', 'rgb': (255, 0, 0), 'block': 'minecraft:red_concrete'},
    'black': {'name': '黑色', 'abbr': 'Bl', 'rgb': (0, 0, 0), 'block': 'minecraft:black_concrete'},
}

COLOR_ALIASES = {
    '白': 'white', '白色': 'white', 'w': 'white',
    '橙': 'orange', '橙色': 'orange', 'o': 'orange',
    '品红': 'magenta', '品红色': 'magenta', 'm': 'magenta',
    '淡蓝': 'light_blue', '淡蓝色': 'light_blue', '天蓝': 'light_blue', 'lb': 'light_blue',
    '黄': 'yellow', '黄色': 'yellow', 'y': 'yellow',
    '黄绿': 'lime', '黄绿色': 'lime', 'l': 'lime',
    '粉红': 'pink', '粉红色': 'pink', 'p': 'pink',
    '灰': 'gray', '灰色': 'gray', 'gy': 'gray',
    '淡灰': 'silver', '淡灰色': 'silver', '银': 'silver', 's': 'silver',
    '青': 'cyan', '青色': 'cyan', 'c': 'cyan',
    '紫': 'purple', '紫色': 'purple', 'v': 'purple',
    '蓝': 'blue', '蓝色': 'blue', 'b': 'blue',
    '棕': 'brown', '棕色': 'brown', 'br': 'brown',
    '绿': 'green', '绿色': 'green', 'g': 'green',
    '红': 'red', '红色': 'red', 'r': 'red',
    '黑': 'black', '黑色': 'black', 'bl': 'black',
}

SYMBOL_NAMES = {
    ',': '英文逗号', '，': '中文逗号',
    '.': '英文句号', '。': '中文句号',
    '?': '英文问号', '？': '中文问号',
    '!': '英文感叹号', '！': '中文感叹号',
    ':': '英文冒号', '：': '中文冒号',
    ';': '英文分号', '；': '中文分号',
    '"': '英文双引号', '“': '中文左双引号', '”': '中文右双引号',
    '\'': '英文单引号', '‘': '中文左单引号', '’': '中文右单引号',
    '(': '英文左括号', '（': '中文左括号',
    ')': '英文右括号', '）': '中文右括号',
    '[': '英文左方括号', '【': '中文左方括号',
    ']': '英文右方括号', '】': '中文右方括号',
    '{': '左花括号', '}': '右花括号',
    '<': '小于号', '>': '大于号',
    '《': '左书名号', '》': '右书名号',
    '/': '斜杠', '\\': '反斜杠',
    '-': '减号', '—': '破折号',
    '_': '下划线',
    '=': '等号',
    '+': '加号',
    '*': '星号',
    '#': '井号',
    '%': '百分号',
    '&': '与号',
    '@': '艾特号',
    '^': '脱字符',
    '~': '波浪号',
    '`': '反引号',
    '|': '竖线',
    '$': '美元符号',
    '¥': '人民币符号',
    '€': '欧元符号',
    '£': '英镑符号',
    '§': '章节符号',
    '©': '版权符号',
    '®': '注册商标符号',
    '™': '商标符号',
    '°': '度数符号',
    '√': '根号符号',
    'π': '圆周率符号',
    '×': '乘号',
    '÷': '除号',
    '±': '正负号',
    '·': '间隔号',
    '…': '省略号',
    '、': '顿号',
    '「': '左角单引号',
    '」': '右角单引号',
    '『': '左角双引号',
    '』': '右角双引号',
    '–': '短破折号',
    '•': '项目符号',
    '∞': '无穷大符号',
    '∫': '积分符号',
    '∑': '求和符号',
    '∏': '乘积符号',
    'θ': '角度符号',
    'φ': '黄金比例符号',
    '★': '实心星形',
    '☆': '空心星形',
    '●': '实心圆形',
    '○': '空心圆形',
    '▲': '实心三角形',
    '△': '空心三角形',
    '■': '实心方块',
    '□': '空心方块',
    '♠': '黑桃符号',
    '♥': '红心符号',
    '♦': '方块符号',
    '♣': '梅花符号',
    '→': '右箭头',
    '←': '左箭头',
    '↑': '上箭头',
    '↓': '下箭头',
    '↔': '双向箭头',
    '↕': '垂直双向箭头',
    '⇒': '蕴含符号',
    '⇔': '等价符号',
    '⊕': '异或符号',
    '⊗': '张量积符号',
    '⊂': '子集符号',
    '⊃': '超集符号',
    '⊆': '子集或等于符号',
    '⊇': '超集或等于符号',
    '∈': '属于符号',
    '∉': '不属于符号',
    '∪': '并集符号',
    '∩': '交集符号',
    '∅': '空集符号',
    '∀': '全称量词',
    '∃': '存在量词',
    '¬': '否定符号',
    '∧': '合取符号',
    '∨': '析取符号',
    '⊢': '推导符号',
    '⊤': '真值符号',
    '⊥': '假值符号',
}

CORNER_SYMBOLS = {
    '©': 'top_right',
    '®': 'top_right',
    '™': 'top_right',
    '°': 'top_left',
    '§': 'bottom_right',
    '★': 'top_left',
    '☆': 'top_left',
    '●': 'bottom_left',
    '○': 'bottom_left',
}

POSITION_OFFSET = 5


def get_char_display_name(char):
    if char in SYMBOL_NAMES:
        return SYMBOL_NAMES[char]
    return char


def check_font_supports_char(font_path, char):
    try:
        face = freetype.Face(font_path)
        face.set_char_size(48 * 64)
        glyph_index = face.get_char_index(char)
        if glyph_index == 0:
            return False
        face.load_glyph(glyph_index, freetype.FT_LOAD_RENDER)
        bitmap = face.glyph.bitmap
        if bitmap.width == 0 or bitmap.rows == 0:
            return False
        return True
    except Exception:
        return False


def get_color_key(user_input):
    user_input = user_input.strip().lower()
    if user_input in MINECRAFT_CONCRETE_COLORS:
        return user_input
    if user_input in COLOR_ALIASES:
        return COLOR_ALIASES[user_input]
    return None


def rgb_to_concrete_color(rgb):
    min_distance = float('inf')
    best_color = 'white'
    
    for color_key, color_info in MINECRAFT_CONCRETE_COLORS.items():
        cr, cg, cb = color_info['rgb']
        distance = (rgb[0] - cr) ** 2 + (rgb[1] - cg) ** 2 + (rgb[2] - cb) ** 2
        if distance < min_distance:
            min_distance = distance
            best_color = color_key
    
    return best_color


def render_text_to_image(text, font_path, text_color_rgb, image_size=128, position=None):
    img = Image.new('RGBA', (image_size, image_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font_size = 1
    font = None
    
    while True:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if text_width >= image_size - 4 or text_height >= image_size - 4:
            font_size -= 1
            try:
                font = ImageFont.truetype(font_path, font_size)
            except:
                font = ImageFont.load_default()
            break
        
        font_size += 1
    
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if position == 'top_right':
        x = image_size - text_width - POSITION_OFFSET - bbox[0]
        y = POSITION_OFFSET - bbox[1]
    elif position == 'top_left':
        x = POSITION_OFFSET - bbox[0]
        y = POSITION_OFFSET - bbox[1]
    elif position == 'bottom_right':
        x = image_size - text_width - POSITION_OFFSET - bbox[0]
        y = image_size - text_height - POSITION_OFFSET - bbox[1]
    elif position == 'bottom_left':
        x = POSITION_OFFSET - bbox[0]
        y = image_size - text_height - POSITION_OFFSET - bbox[1]
    else:
        x = (image_size - text_width) // 2 - bbox[0]
        y = (image_size - text_height) // 2 - bbox[1]
    
    draw.text((x, y), text, font=font, fill=text_color_rgb)
    
    return img


def create_litematic_from_image(image, text, color_key, font_name, output_dir):
    width, height = image.size
    reg = Region(0, 0, 0, width, 1, height)
    
    text_block = BlockState(MINECRAFT_CONCRETE_COLORS[color_key]['block'])
    air_block = BlockState('minecraft:air')
    
    block_count = 0
    for x in range(width):
        for z in range(height):
            r, g, b, a = image.getpixel((x, z))
            if a > 128:
                reg[x, 0, z] = text_block
                block_count += 1
            else:
                reg[x, 0, z] = air_block
    
    char_name = get_char_display_name(text)
    color_name = MINECRAFT_CONCRETE_COLORS[color_key]['name']
    schem_name = f"{font_name}_{char_name}_{color_name}_{block_count}"
    schem = reg.as_schematic(
        name=schem_name,
        author="MapArtGenerator",
        description=f"128x128 map art of '{text}' in {color_name}, {block_count} blocks"
    )
    
    output_path = os.path.join(output_dir, f"{schem_name}.litematic")
    schem.save(output_path)
    
    return output_path, block_count


def generate_map_art(text, color_input, font_path, font_name, output_dir=None):
    color_key = get_color_key(color_input)
    if color_key is None:
        print(f"错误：不支持的颜色 '{color_input}'！")
        color_list = [f"{v['name']}({v['abbr']})" for v in MINECRAFT_CONCRETE_COLORS.values()]
        print(f"支持的颜色：{', '.join(color_list)}")
        return False
    
    text_color_rgb = MINECRAFT_CONCRETE_COLORS[color_key]['rgb']
    position = CORNER_SYMBOLS.get(text, None)
    image = render_text_to_image(text, font_path, text_color_rgb, position=position)
    
    if output_dir is None:
        output_dir = os.path.dirname(__file__)
    
    output_path, block_count = create_litematic_from_image(image, text, color_key, font_name, output_dir)
    
    return output_path, block_count


def find_font_files(base_dir):
    ttf_dir = os.path.join(base_dir, 'ttf')
    font_files = []
    
    if os.path.exists(ttf_dir):
        for filename in sorted(os.listdir(ttf_dir)):
            if filename.lower().endswith('.ttf'):
                font_files.append(os.path.join(ttf_dir, filename))
    
    return font_files[:10]


def main():
    base_dir = os.path.dirname(__file__)
    
    ttf_dir = os.path.join(base_dir, 'ttf')
    litematic_dir = os.path.join(base_dir, 'litematic')
    
    if not os.path.exists(ttf_dir):
        os.makedirs(ttf_dir)
        print(f"提示：已自动创建字体目录 {ttf_dir}")
    
    if not os.path.exists(litematic_dir):
        os.makedirs(litematic_dir)
        print(f"提示：已自动创建投影文件目录 {litematic_dir}")
    
    font_files = find_font_files(base_dir)
    
    if not font_files:
        print("错误：在 ttf 目录下找不到字体文件！")
        print(f"请将 .ttf 字体文件放入 {ttf_dir} 目录")
        sys.exit(1)
    
    print("=" * 60)
    print("我的世界文字地图画生成器（128×128）")
    print("=" * 60)
    
    if len(font_files) == 1:
        font_path = font_files[0]
        font_name = os.path.splitext(os.path.basename(font_path))[0]
        print(f"检测到唯一字体：{font_name}")
        print(f"已选择字体文件为{os.path.basename(font_path)}")
        print("=" * 60)
    else:
        print("可用字体：")
        for i, font_path in enumerate(font_files):
            font_name = os.path.splitext(os.path.basename(font_path))[0]
            print(f"  [{i}] {font_name}")
        print("=" * 60)
        
        while True:
            choice = input("请选择字体（输入数字 0~9）：").strip()
            
            if not choice.isdigit():
                print("错误：请输入有效的数字！")
                continue
            
            index = int(choice)
            if index < 0 or index >= len(font_files):
                print(f"错误：请输入 0~{len(font_files)-1} 之间的数字！")
                continue
            
            break
        
        font_path = font_files[index]
        font_name = os.path.splitext(os.path.basename(font_path))[0]
        print(f"\n已选择字体：{font_name}")
    color_list = [f"{v['name']}({v['abbr']})" for v in MINECRAFT_CONCRETE_COLORS.values()]
    print(f"支持的颜色：{', '.join(color_list)}")
    print("=" * 60)
    
    while True:
        text = input("请输入要生成的文字（可输入多个字或符号）：").strip()
        
        if len(text) == 0:
            print("错误：输入不能为空！")
            continue
        
        unsupported_chars = []
        for char in text:
            if not check_font_supports_char(font_path, char):
                unsupported_chars.append(char)
        
        if unsupported_chars:
            print(f"错误：字体 '{font_name}' 不支持以下字符：{', '.join(unsupported_chars)}")
            print("请重新输入！")
            continue
        
        break
    
    while True:
        color_input = input("请输入文字颜色（使用上述支持的颜色名称）：").strip()
        color_key = get_color_key(color_input)
        
        if color_key is None:
            print(f"错误：不支持的颜色 '{color_input}'！")
            color_list = [f"{v['name']}({v['abbr']})" for v in MINECRAFT_CONCRETE_COLORS.values()]
            print(f"支持的颜色：{', '.join(color_list)}")
            continue
        
        break
    
    print(f"\n开始生成 {len(text)} 个地图画文件...")
    print("-" * 60)
    
    total_blocks = 0
    generated_files = []
    
    for i, char in enumerate(text):
        print(f"\n[{i+1}/{len(text)}] 正在生成：'{char}'")
        result = generate_map_art(char, color_key, font_path, font_name, litematic_dir)
        
        if result is False:
            print(f"  生成失败！")
            continue
        
        output_path, block_count = result
        total_blocks += block_count
        generated_files.append((char, output_path))
        
        print(f"  成功！投影文件：{output_path}")
        print(f"  方块数量：{block_count}")
    
    print("\n" + "=" * 60)
    print(f"生成完成！共生成 {len(generated_files)} 个文件")
    print(f"总方块数量：{total_blocks}")
    print("=" * 60)
    print("\n使用方法：")
    print("1. 将生成的 .litematic 文件放入 .minecraft/schematics 文件夹")
    print("2. 在游戏中安装 Litematica 投影模组")
    print("3. 使用木棍打开投影菜单，加载文件")
    print("4. 将投影放置在地图区域内即可建造")


if __name__ == '__main__':
    main()