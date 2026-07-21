import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QTextEdit, QGroupBox,
    QGridLayout, QScrollArea, QMessageBox, QSplitter, QSizePolicy,
    QMenuBar, QMenu, QListWidget, QListWidgetItem,
    QFileDialog
)
from PyQt6.QtGui import QColor, QPalette, QFont, QAction
from PyQt6.QtCore import Qt, pyqtSignal

from i18n import t, set_language
from main import (
    find_font_files, ensure_directories, check_font_supports_char,
    generate_map_art, MINECRAFT_COLORS, MINECRAFT_BLOCK_TYPES, get_color_key,
    render_text_to_image
)
from preview import PreviewWindow

SYMBOL_CATEGORIES = {
    'punctuation': [
        (',', 'english_comma'), ('，', 'chinese_comma'),
        ('.', 'english_period'), ('。', 'chinese_period'),
        ('?', 'english_question'), ('？', 'chinese_question'),
        ('!', 'english_exclamation'), ('！', 'chinese_exclamation'),
        (':', 'english_colon'), ('：', 'chinese_colon'),
        (';', 'english_semicolon'), ('；', 'chinese_semicolon'),
        ('、', 'enumeration_comma'), ('…', 'ellipsis'),
    ],
    'quotes': [
        ('"', 'english_double_quote'), ('“', 'chinese_left_double_quote'), ('”', 'chinese_right_double_quote'),
        ("'", 'english_single_quote'), ('‘', 'chinese_left_single_quote'), ('’', 'chinese_right_single_quote'),
        ('「', 'left_corner_single_quote'), ('」', 'right_corner_single_quote'),
        ('『', 'left_corner_double_quote'), ('』', 'right_corner_double_quote'),
    ],
    'parentheses': [
        ('(', 'english_left_parenthesis'), (')', 'english_right_parenthesis'),
        ('（', 'chinese_left_parenthesis'), ('）', 'chinese_right_parenthesis'),
        ('[', 'english_left_bracket'), (']', 'english_right_bracket'),
        ('【', 'chinese_left_bracket'), ('】', 'chinese_right_bracket'),
        ('{', 'left_curly_bracket'), ('}', 'right_curly_bracket'),
        ('<', 'less_than'), ('>', 'greater_than'),
        ('《', 'chinese_left_bookmark'), ('》', 'chinese_right_bookmark'),
    ],
    'math': [
        ('+', 'plus'), ('-', 'hyphen'), ('=', 'equals'),
        ('×', 'multiply_sign'), ('÷', 'divide_sign'), ('±', 'plus_minus_sign'),
        ('√', 'square_root'), ('π', 'pi_sign'), ('°', 'degree_sign'),
        ('∞', 'infinity_sign'), ('∫', 'integral_sign'), ('∑', 'sum_sign'),
        ('∏', 'product_sign'), ('θ', 'theta_sign'), ('φ', 'phi_sign'),
    ],
    'operators': [
        ('*', 'asterisk'), ('/', 'forward_slash'), ('\\', 'backward_slash'),
        ('^', 'caret'), ('~', 'tilde'), ('`', 'backtick'),
        ('|', 'vertical_bar'), ('&', 'ampersand'), ('@', 'at_sign'),
        ('#', 'hash'), ('%', 'percent'), ('_', 'underscore'),
    ],
    'currency': [
        ('$', 'dollar_sign'), ('¥', 'yuan_sign'),
        ('€', 'euro_sign'), ('£', 'pound_sign'),
    ],
    'symbols': [
        ('★', 'filled_star'), ('☆', 'empty_star'),
        ('●', 'filled_circle'), ('○', 'empty_circle'),
        ('▲', 'filled_triangle'), ('△', 'empty_triangle'),
        ('■', 'filled_square'), ('□', 'empty_square'),
        ('♠', 'spade_sign'), ('♥', 'heart_sign'),
        ('♦', 'diamond_sign'), ('♣', 'club_sign'),
        ('→', 'right_arrow'), ('←', 'left_arrow'),
        ('↑', 'up_arrow'), ('↓', 'down_arrow'),
        ('©', 'copyright_sign'), ('®', 'registered_sign'),
        ('™', 'trademark_sign'), ('§', 'section_sign'),
    ],
}

CATEGORY_TRANSLATION_KEYS = {
    'punctuation': 'punctuation',
    'quotes': 'quotes',
    'parentheses': 'parentheses',
    'math': 'math',
    'operators': 'operators',
    'currency': 'currency',
    'symbols': 'symbols',
}

PREVIEW_MODES = {
    'map': {'name': 'map_art', 'label': 'Map Art Preview'},
    'build_2d': {'name': 'build_2d', 'label': '2D Build Preview'},
}


class SymbolButton(QPushButton):
    clicked_with_symbol = pyqtSignal(str)

    def __init__(self, symbol, label, parent=None):
        super().__init__(symbol, parent)
        self.symbol = symbol
        self.setToolTip(label)
        self.clicked.connect(self.emit_symbol)

    def emit_symbol(self):
        self.clicked_with_symbol.emit(self.symbol)


class ColorButton(QPushButton):
    clicked_with_color = pyqtSignal(str)

    def __init__(self, color_key, color_info, parent=None):
        super().__init__(parent)
        self.color_key = color_key
        self.color_info = color_info
        self.setFixedSize(40, 40)
        self.update_color()
        self.clicked.connect(self.emit_color)

    def update_color(self):
        rgb = self.color_info['rgb']
        color_str = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_str};
                border: 1px solid #333;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {color_str};
            }}
            QPushButton:pressed {{
                background-color: {color_str};
            }}
        """)
        self.setToolTip(f"{t(self.color_info['name'])} ({self.color_info['abbr']})")

    def emit_color(self):
        self.clicked_with_color.emit(self.color_key)


class MapArtGeneratorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.dirname(__file__)
        self.font_files = []
        self.selected_font_path = None
        self.selected_font_name = None
        self.selected_color_key = None
        self.selected_block_type = 'concrete'
        self.default_block_type = 'concrete'
        self.default_preview_mode = 'map'
        self.default_font = ''
        self.generated_files = []
        
        self.load_settings()
        self.init_ui()
        self.load_fonts()
        self.apply_defaults()
        self.update_ui_text()

    def init_ui(self):
        self.setWindowTitle(t('app_name'))
        self.setGeometry(100, 100, 1000, 700)

        menubar = self.menuBar()
        
        settings_action = QAction(f"{t('settings')} (Settings)", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        menubar.addAction(settings_action)
        
        language_menu = menubar.addMenu(f"{t('language')} (Language)")
        lang_action_zh = QAction(t('chinese'), self)
        lang_action_zh.triggered.connect(lambda: self.change_language('zh_cn'))
        language_menu.addAction(lang_action_zh)
        lang_action_en = QAction(t('english'), self)
        lang_action_en.triggered.connect(lambda: self.change_language('en'))
        language_menu.addAction(lang_action_en)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(10, 10, 10, 10)

        self.font_group = QGroupBox()
        font_layout = QVBoxLayout(self.font_group)
        font_layout.setSpacing(5)
        
        self.font_combo = QComboBox()
        self.font_combo.currentIndexChanged.connect(self.on_font_changed)
        self.font_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        font_layout.addWidget(self.font_combo)
        
        left_layout.addWidget(self.font_group)

        self.text_group = QGroupBox()
        text_layout = QVBoxLayout(self.text_group)
        text_layout.setSpacing(5)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText(t('input_text'))
        self.text_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        text_layout.addWidget(self.text_input)
        
        left_layout.addWidget(self.text_group)

        self.block_type_group = QGroupBox()
        block_type_layout = QVBoxLayout(self.block_type_group)
        block_type_layout.setSpacing(5)
        
        self.block_type_combo = QComboBox()
        for block_key, block_info in MINECRAFT_BLOCK_TYPES.items():
            self.block_type_combo.addItem(t(block_info['name']), block_key)
        self.block_type_combo.currentIndexChanged.connect(self.on_block_type_changed)
        block_type_layout.addWidget(self.block_type_combo)
        
        left_layout.addWidget(self.block_type_group)

        self.color_group = QGroupBox()
        color_layout = QGridLayout(self.color_group)
        color_layout.setSpacing(5)
        self.color_buttons = []
        
        row, col = 0, 0
        for color_key, color_info in MINECRAFT_COLORS.items():
            btn = ColorButton(color_key, color_info)
            btn.clicked_with_color.connect(self.on_color_selected)
            self.color_buttons.append(btn)
            color_layout.addWidget(btn, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
        
        self.selected_color_label = QLabel(t('select_color'))
        color_layout.addWidget(self.selected_color_label, row + 1, 0, 1, 4)
        
        left_layout.addWidget(self.color_group)

        self.symbol_group = QGroupBox()
        symbol_layout = QVBoxLayout(self.symbol_group)
        symbol_layout.setSpacing(5)
        
        self.symbol_category_combo = QComboBox()
        for cat_key in SYMBOL_CATEGORIES:
            self.symbol_category_combo.addItem(t(CATEGORY_TRANSLATION_KEYS[cat_key]), cat_key)
        self.symbol_category_combo.currentIndexChanged.connect(self.update_symbol_buttons)
        symbol_layout.addWidget(self.symbol_category_combo)
        
        self.symbol_scroll = QScrollArea()
        self.symbol_scroll.setWidgetResizable(True)
        self.symbol_container = QWidget()
        self.symbol_grid = QGridLayout(self.symbol_container)
        self.symbol_grid.setSpacing(3)
        self.symbol_scroll.setWidget(self.symbol_container)
        self.symbol_scroll.setMaximumHeight(120)
        symbol_layout.addWidget(self.symbol_scroll)
        
        left_layout.addWidget(self.symbol_group)

        self.generate_btn = QPushButton(t('generate_button'))
        self.generate_btn.clicked.connect(self.on_generate)
        self.generate_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        left_layout.addWidget(self.generate_btn)
        
        left_panel.setMinimumWidth(300)
        left_panel.setMaximumWidth(400)
        left_panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        splitter.addWidget(left_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)
        
        self.file_list_group = QGroupBox()
        file_list_layout = QVBoxLayout(self.file_list_group)
        
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.file_list.doubleClicked.connect(self.on_file_double_click)
        file_list_layout.addWidget(self.file_list)
        
        right_layout.addWidget(self.file_list_group)
        
        self.log_group = QGroupBox()
        log_layout = QVBoxLayout(self.log_group)
        
        self.clear_log_btn = QPushButton(t('clear_log'))
        self.clear_log_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(self.clear_log_btn)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)
        log_layout.addWidget(self.log_text)
        right_layout.addWidget(self.log_group)
        
        splitter.addWidget(right_panel)
        
        main_layout.addWidget(splitter)

        self.update_symbol_buttons()
        self.load_existing_files()

    def load_settings(self):
        config_file = os.path.join(self.base_dir, 'config.json')
        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    settings = config.get('settings', {})
                    self.default_block_type = settings.get('default_block_type', 'concrete')
                    self.default_preview_mode = settings.get('default_preview_mode', 'map')
                    self.default_font = settings.get('default_font', '')
            except:
                pass

    def save_settings(self):
        config_file = os.path.join(self.base_dir, 'config.json')
        try:
            import json
            config = {
                'settings': {
                    'default_block_type': self.default_block_type,
                    'default_preview_mode': self.default_preview_mode,
                    'default_font': self.default_font
                },
                'language': self.language
            }
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except:
            pass

    def apply_defaults(self):
        idx = self.block_type_combo.findData(self.default_block_type)
        if idx >= 0:
            self.block_type_combo.setCurrentIndex(idx)
        
        if self.default_font:
            for i in range(self.font_combo.count()):
                if self.font_combo.itemText(i) == self.default_font:
                    self.font_combo.setCurrentIndex(i)
                    break

    def open_settings_dialog(self):
        dialog = QWidget()
        dialog.setWindowTitle(t('settings'))
        dialog.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout(dialog)
        
        block_type_label = QLabel(t('default_block_type'))
        layout.addWidget(block_type_label)
        block_type_combo = QComboBox()
        for block_key, block_info in MINECRAFT_BLOCK_TYPES.items():
            block_type_combo.addItem(t(block_info['name']), block_key)
        idx = block_type_combo.findData(self.default_block_type)
        if idx >= 0:
            block_type_combo.setCurrentIndex(idx)
        layout.addWidget(block_type_combo)
        
        preview_mode_label = QLabel(t('default_preview_mode'))
        layout.addWidget(preview_mode_label)
        preview_mode_combo = QComboBox()
        for mode_key, mode_info in PREVIEW_MODES.items():
            preview_mode_combo.addItem(t(mode_info['name']), mode_key)
        idx = preview_mode_combo.findData(self.default_preview_mode)
        if idx >= 0:
            preview_mode_combo.setCurrentIndex(idx)
        layout.addWidget(preview_mode_combo)
        
        font_label = QLabel(t('default_font'))
        layout.addWidget(font_label)
        font_combo = QComboBox()
        font_combo.addItem(t('none'), '')
        for font_path in self.font_files:
            font_name = os.path.splitext(os.path.basename(font_path))[0]
            font_combo.addItem(font_name, font_path)
        for i in range(font_combo.count()):
            if font_combo.itemText(i) == self.default_font:
                font_combo.setCurrentIndex(i)
                break
        layout.addWidget(font_combo)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton(t('ok'))
        ok_btn.clicked.connect(lambda: self.save_settings_from_dialog(dialog, block_type_combo, preview_mode_combo, font_combo))
        button_layout.addWidget(ok_btn)
        cancel_btn = QPushButton(t('cancel'))
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.show()

    def save_settings_from_dialog(self, dialog, block_type_combo, preview_mode_combo, font_combo):
        self.default_block_type = block_type_combo.currentData()
        self.default_preview_mode = preview_mode_combo.currentData()
        self.default_font = font_combo.currentText()
        self.save_settings()
        dialog.close()
        QMessageBox.information(self, t('success'), t('settings_saved'))

    def load_fonts(self):
        ensure_directories(self.base_dir)
        self.font_files = find_font_files(self.base_dir)
        
        self.font_combo.clear()
        if not self.font_files:
            self.log(t('no_font_found'))
            return
        
        for font_path in self.font_files:
            font_name = os.path.splitext(os.path.basename(font_path))[0]
            self.font_combo.addItem(font_name, font_path)
        
        if self.font_files:
            self.on_font_changed(0)

    def load_existing_files(self):
        litematic_dir = os.path.join(self.base_dir, 'litematic')
        if os.path.exists(litematic_dir):
            for filename in sorted(os.listdir(litematic_dir)):
                if filename.endswith('.litematic'):
                    item = QListWidgetItem(filename)
                    item.setData(Qt.ItemDataRole.UserRole, os.path.join(litematic_dir, filename))
                    self.file_list.addItem(item)

    def on_font_changed(self, index):
        if index >= 0 and index < len(self.font_files):
            self.selected_font_path = self.font_files[index]
            self.selected_font_name = os.path.splitext(os.path.basename(self.selected_font_path))[0]

    def on_block_type_changed(self, index):
        self.selected_block_type = self.block_type_combo.currentData()

    def on_color_selected(self, color_key):
        self.selected_color_key = color_key
        color_info = MINECRAFT_COLORS[color_key]
        self.selected_color_label.setText(f"{t(color_info['name'])} ({color_info['abbr']})")
        
        for btn in self.color_buttons:
            rgb = btn.color_info['rgb']
            color_str = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
            if btn.color_key == color_key:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color_str};
                        border: 3px solid #000000;
                        border-radius: 4px;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color_str};
                        border: 1px solid #333;
                        border-radius: 4px;
                    }}
                """)

    def update_symbol_buttons(self):
        while self.symbol_grid.count():
            child = self.symbol_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        category = self.symbol_category_combo.currentData()
        symbols = SYMBOL_CATEGORIES.get(category, [])
        
        row, col = 0, 0
        for symbol, label_key in symbols:
            btn = SymbolButton(symbol, t(label_key))
            btn.clicked_with_symbol.connect(self.on_symbol_clicked)
            btn.setFixedSize(35, 35)
            self.symbol_grid.addWidget(btn, row, col)
            col += 1
            if col == 10:
                col = 0
                row += 1

    def on_symbol_clicked(self, symbol):
        current_text = self.text_input.text()
        self.text_input.setText(current_text + symbol)

    def change_language(self, lang):
        set_language(lang)
        self.update_ui_text()

    def update_ui_text(self):
        self.setWindowTitle(t('app_name'))
        
        self.font_group.setTitle(t('font_selection'))
        self.text_group.setTitle(t('text_input'))
        self.block_type_group.setTitle(t('block_type_selection'))
        self.color_group.setTitle(t('color_selection'))
        self.symbol_group.setTitle(t('symbol_selection'))
        self.log_group.setTitle(t('log_output'))
        self.file_list_group.setTitle(t('generated_files'))
        
        self.text_input.setPlaceholderText(t('input_text'))
        self.selected_color_label.setText(t('select_color'))
        self.generate_btn.setText(t('generate_button'))
        self.clear_log_btn.setText(t('clear_log'))
        
        for block_key, block_info in MINECRAFT_BLOCK_TYPES.items():
            idx = self.block_type_combo.findData(block_key)
            if idx >= 0:
                self.block_type_combo.setItemText(idx, t(block_info['name']))
        
        for cat_key in SYMBOL_CATEGORIES:
            idx = self.symbol_category_combo.findData(cat_key)
            if idx >= 0:
                self.symbol_category_combo.setItemText(idx, t(CATEGORY_TRANSLATION_KEYS[cat_key]))
        
        for btn in self.color_buttons:
            btn.update_color()
        
        self.update_symbol_buttons()

    def log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def clear_log(self):
        self.log_text.clear()

    def on_file_double_click(self, index):
        item = self.file_list.itemFromIndex(index)
        if item:
            file_path = item.data(Qt.ItemDataRole.UserRole)
            if file_path and os.path.exists(file_path):
                self.open_preview(file_path)

    def open_preview(self, file_path):
        preview_window = PreviewWindow(file_path, self.base_dir, self)
        preview_window.show()

    def on_generate(self):
        if not self.selected_font_path:
            QMessageBox.warning(self, t('error'), t('no_font_found'))
            return
        
        text = self.text_input.text().strip()
        if not text:
            QMessageBox.warning(self, t('error'), t('empty_input'))
            return
        
        if not self.selected_color_key:
            QMessageBox.warning(self, t('error'), t('select_color'))
            return
        
        unsupported_chars = []
        for char in text:
            if not check_font_supports_char(self.selected_font_path, char):
                unsupported_chars.append(char)
        
        if unsupported_chars:
            QMessageBox.warning(self, t('error'), t('font_not_support', font_name=self.selected_font_name, chars=', '.join(unsupported_chars)))
            return
        
        self.log(t('start_generation', count=len(text)))
        
        litematic_dir = os.path.join(self.base_dir, 'litematic')
        
        total_blocks = 0
        generated_files = []
        
        for i, char in enumerate(text):
            self.log(t('generating', current=i+1, total=len(text), char=char))
            result = generate_map_art(char, self.selected_color_key, self.selected_font_path, self.selected_font_name, litematic_dir, self.selected_block_type)
            
            if result[0] is False:
                self.log(t('generation_failed'))
                continue
            
            output_path, block_count = result
            total_blocks += block_count
            generated_files.append(output_path)
            
            self.log(t('generation_success', path=output_path))
            self.log(t('block_count', count=block_count))
            
            filename = os.path.basename(output_path)
            item = QListWidgetItem(filename)
            item.setData(Qt.ItemDataRole.UserRole, output_path)
            self.file_list.addItem(item)
        
        self.log("")
        self.log("=" * 60)
        self.log(t('generation_complete', count=len(generated_files)))
        self.log(t('total_blocks', count=total_blocks))
        self.log("=" * 60)


def main():
    app = QApplication(sys.argv)
    window = MapArtGeneratorUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()