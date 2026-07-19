import sys
import os
import freetype
from PIL import Image, ImageDraw, ImageFont
from litemapy import Schematic, Region, BlockState
from i18n import t

MINECRAFT_CONCRETE_COLORS = {
    'white': {'name': 'white', 'abbr': 'W', 'rgb': (255, 255, 255), 'block': 'minecraft:white_concrete'},
    'orange': {'name': 'orange', 'abbr': 'O', 'rgb': (255, 163, 0), 'block': 'minecraft:orange_concrete'},
    'magenta': {'name': 'magenta', 'abbr': 'M', 'rgb': (255, 0, 255), 'block': 'minecraft:magenta_concrete'},
    'light_blue': {'name': 'light_blue', 'abbr': 'LB', 'rgb': (0, 191, 255), 'block': 'minecraft:light_blue_concrete'},
    'yellow': {'name': 'yellow', 'abbr': 'Y', 'rgb': (255, 255, 0), 'block': 'minecraft:yellow_concrete'},
    'lime': {'name': 'lime', 'abbr': 'L', 'rgb': (0, 255, 0), 'block': 'minecraft:lime_concrete'},
    'pink': {'name': 'pink', 'abbr': 'P', 'rgb': (255, 192, 203), 'block': 'minecraft:pink_concrete'},
    'gray': {'name': 'gray', 'abbr': 'Gy', 'rgb': (128, 128, 128), 'block': 'minecraft:gray_concrete'},
    'silver': {'name': 'silver', 'abbr': 'S', 'rgb': (192, 192, 192), 'block': 'minecraft:light_gray_concrete'},
    'cyan': {'name': 'cyan', 'abbr': 'C', 'rgb': (0, 255, 255), 'block': 'minecraft:cyan_concrete'},
    'purple': {'name': 'purple', 'abbr': 'V', 'rgb': (128, 0, 128), 'block': 'minecraft:purple_concrete'},
    'blue': {'name': 'blue', 'abbr': 'B', 'rgb': (0, 0, 255), 'block': 'minecraft:blue_concrete'},
    'brown': {'name': 'brown', 'abbr': 'Br', 'rgb': (165, 42, 42), 'block': 'minecraft:brown_concrete'},
    'green': {'name': 'green', 'abbr': 'G', 'rgb': (0, 128, 0), 'block': 'minecraft:green_concrete'},
    'red': {'name': 'red', 'abbr': 'R', 'rgb': (255, 0, 0), 'block': 'minecraft:red_concrete'},
    'black': {'name': 'black', 'abbr': 'Bl', 'rgb': (0, 0, 0), 'block': 'minecraft:black_concrete'},
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
    ',': 'english_comma', '，': 'chinese_comma',
    '.': 'english_period', '。': 'chinese_period',
    '?': 'english_question', '？': 'chinese_question',
    '!': 'english_exclamation', '！': 'chinese_exclamation',
    ':': 'english_colon', '：': 'chinese_colon',
    ';': 'english_semicolon', '；': 'chinese_semicolon',
    '"': 'english_double_quote', '“': 'chinese_left_double_quote', '”': 'chinese_right_double_quote',
    '\'': 'english_single_quote', '‘': 'chinese_left_single_quote', '’': 'chinese_right_single_quote',
    '(': 'english_left_parenthesis', '（': 'chinese_left_parenthesis',
    ')': 'english_right_parenthesis', '）': 'chinese_right_parenthesis',
    '[': 'english_left_bracket', '【': 'chinese_left_bracket',
    ']': 'english_right_bracket', '】': 'chinese_right_bracket',
    '{': 'left_curly_bracket', '}': 'right_curly_bracket',
    '<': 'less_than', '>': 'greater_than',
    '《': 'chinese_left_bookmark', '》': 'chinese_right_bookmark',
    '/': 'forward_slash', '\\': 'backward_slash',
    '-': 'hyphen', '—': 'em_dash',
    '_': 'underscore',
    '=': 'equals',
    '+': 'plus',
    '*': 'asterisk',
    '#': 'hash',
    '%': 'percent',
    '&': 'ampersand',
    '@': 'at_sign',
    '^': 'caret',
    '~': 'tilde',
    '`': 'backtick',
    '|': 'vertical_bar',
    '$': 'dollar_sign',
    '¥': 'yuan_sign',
    '€': 'euro_sign',
    '£': 'pound_sign',
    '§': 'section_sign',
    '©': 'copyright_sign',
    '®': 'registered_sign',
    '™': 'trademark_sign',
    '°': 'degree_sign',
    '√': 'square_root',
    'π': 'pi_sign',
    '×': 'multiply_sign',
    '÷': 'divide_sign',
    '±': 'plus_minus_sign',
    '·': 'middle_dot',
    '…': 'ellipsis',
    '、': 'enumeration_comma',
    '「': 'left_corner_single_quote',
    '」': 'right_corner_single_quote',
    '『': 'left_corner_double_quote',
    '』': 'right_corner_double_quote',
    '–': 'en_dash',
    '•': 'bullet_point',
    '∞': 'infinity_sign',
    '∫': 'integral_sign',
    '∑': 'sum_sign',
    '∏': 'product_sign',
    'θ': 'theta_sign',
    'φ': 'phi_sign',
    '★': 'filled_star',
    '☆': 'empty_star',
    '●': 'filled_circle',
    '○': 'empty_circle',
    '▲': 'filled_triangle',
    '△': 'empty_triangle',
    '■': 'filled_square',
    '□': 'empty_square',
    '♠': 'spade_sign',
    '♥': 'heart_sign',
    '♦': 'diamond_sign',
    '♣': 'club_sign',
    '→': 'right_arrow',
    '←': 'left_arrow',
    '↑': 'up_arrow',
    '↓': 'down_arrow',
    '↔': 'left_right_arrow',
    '↕': 'up_down_arrow',
    '⇒': 'implies_sign',
    '⇔': 'equivalent_sign',
    '⊕': 'xor_sign',
    '⊗': 'tensor_product',
    '⊂': 'subset_sign',
    '⊃': 'superset_sign',
    '⊆': 'subset_or_equal',
    '⊇': 'superset_or_equal',
    '∈': 'element_of',
    '∉': 'not_element_of',
    '∪': 'union_sign',
    '∩': 'intersection_sign',
    '∅': 'empty_set',
    '∀': 'for_all',
    '∃': 'exists',
    '¬': 'negation_sign',
    '∧': 'conjunction_sign',
    '∨': 'disjunction_sign',
    '⊢': 'derivation_sign',
    '⊤': 'true_sign',
    '⊥': 'false_sign',
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
        return t(SYMBOL_NAMES[char])
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
    color_name = t(MINECRAFT_CONCRETE_COLORS[color_key]['name'])
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
        return False, t('unsupported_color', color=color_input)
    
    text_color_rgb = MINECRAFT_CONCRETE_COLORS[color_key]['rgb']
    position = CORNER_SYMBOLS.get(text, None)
    image = render_text_to_image(text, font_path, text_color_rgb, position=position)
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'litematic')
    
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


def ensure_directories(base_dir):
    ttf_dir = os.path.join(base_dir, 'ttf')
    litematic_dir = os.path.join(base_dir, 'litematic')
    
    if not os.path.exists(ttf_dir):
        os.makedirs(ttf_dir)
        return {'ttf_created': True, 'ttf_dir': ttf_dir}
    
    if not os.path.exists(litematic_dir):
        os.makedirs(litematic_dir)
        return {'litematic_created': True, 'litematic_dir': litematic_dir}
    
    return {'created': False}


if __name__ == '__main__':
    print("请通过 ui.py 启动本程序！")
    print("Usage: python ui.py")