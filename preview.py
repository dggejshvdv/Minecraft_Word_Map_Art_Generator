import os
import numpy as np
from PIL import Image
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QMessageBox,
    QGraphicsView, QGraphicsScene
)
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtCore import Qt

from i18n import t

BLOCK_COLOR_MAP = {
    'white': (255, 255, 255),
    'orange': (255, 163, 0),
    'magenta': (255, 0, 255),
    'light_blue': (0, 191, 255),
    'yellow': (255, 255, 0),
    'lime': (0, 255, 0),
    'pink': (255, 192, 203),
    'gray': (128, 128, 128),
    'silver': (192, 192, 192),
    'cyan': (0, 255, 255),
    'purple': (128, 0, 128),
    'blue': (0, 0, 255),
    'brown': (165, 42, 42),
    'green': (0, 128, 0),
    'red': (255, 0, 0),
    'black': (0, 0, 0),
}

BLOCK_TEXTURE_MAP = {
    'white_concrete': 'white_concrete.png',
    'orange_concrete': 'orange_concrete.png',
    'magenta_concrete': 'magenta_concrete.png',
    'light_blue_concrete': 'light_blue_concrete.png',
    'yellow_concrete': 'yellow_concrete.png',
    'lime_concrete': 'lime_concrete.png',
    'pink_concrete': 'pink_concrete.png',
    'gray_concrete': 'gray_concrete.png',
    'light_gray_concrete': 'light_gray_concrete.png',
    'cyan_concrete': 'cyan_concrete.png',
    'purple_concrete': 'purple_concrete.png',
    'blue_concrete': 'blue_concrete.png',
    'brown_concrete': 'brown_concrete.png',
    'green_concrete': 'green_concrete.png',
    'red_concrete': 'red_concrete.png',
    'black_concrete': 'black_concrete.png',
    'white_wool': 'white_wool.png',
    'orange_wool': 'orange_wool.png',
    'magenta_wool': 'magenta_wool.png',
    'light_blue_wool': 'light_blue_wool.png',
    'yellow_wool': 'yellow_wool.png',
    'lime_wool': 'lime_wool.png',
    'pink_wool': 'pink_wool.png',
    'gray_wool': 'gray_wool.png',
    'light_gray_wool': 'light_gray_wool.png',
    'cyan_wool': 'cyan_wool.png',
    'purple_wool': 'purple_wool.png',
    'blue_wool': 'blue_wool.png',
    'brown_wool': 'brown_wool.png',
    'green_wool': 'green_wool.png',
    'red_wool': 'red_wool.png',
    'black_wool': 'black_wool.png',
    'white_carpet': 'white_carpet.png',
    'orange_carpet': 'orange_carpet.png',
    'magenta_carpet': 'magenta_carpet.png',
    'light_blue_carpet': 'light_blue_carpet.png',
    'yellow_carpet': 'yellow_carpet.png',
    'lime_carpet': 'lime_carpet.png',
    'pink_carpet': 'pink_carpet.png',
    'gray_carpet': 'gray_carpet.png',
    'light_gray_carpet': 'light_gray_carpet.png',
    'cyan_carpet': 'cyan_carpet.png',
    'purple_carpet': 'purple_carpet.png',
    'blue_carpet': 'blue_carpet.png',
    'brown_carpet': 'brown_carpet.png',
    'green_carpet': 'green_carpet.png',
    'red_carpet': 'red_carpet.png',
    'black_carpet': 'black_carpet.png',
    'white_terracotta': 'white_terracotta.png',
    'orange_terracotta': 'orange_terracotta.png',
    'magenta_terracotta': 'magenta_terracotta.png',
    'light_blue_terracotta': 'light_blue_terracotta.png',
    'yellow_terracotta': 'yellow_terracotta.png',
    'lime_terracotta': 'lime_terracotta.png',
    'pink_terracotta': 'pink_terracotta.png',
    'gray_terracotta': 'gray_terracotta.png',
    'light_gray_terracotta': 'light_gray_terracotta.png',
    'cyan_terracotta': 'cyan_terracotta.png',
    'purple_terracotta': 'purple_terracotta.png',
    'blue_terracotta': 'blue_terracotta.png',
    'brown_terracotta': 'brown_terracotta.png',
    'green_terracotta': 'green_terracotta.png',
    'red_terracotta': 'red_terracotta.png',
    'black_terracotta': 'black_terracotta.png',
}

PREVIEW_MODES = {
    'map': {'name': 'map_art', 'label': 'Map Art Preview'},
    'build_2d': {'name': 'build_2d', 'label': '2D Build Preview'},
}


class PreviewWindow(QMainWindow):
    def __init__(self, litematic_path, base_dir, parent=None):
        super().__init__(parent)
        self.litematic_path = litematic_path
        self.base_dir = base_dir
        self.preview_mode = 'map'
        self.zoom = 1.0
        self.data = []
        self.width = 0
        self.height = 0
        
        self.setWindowTitle(t('preview_window_title') + f": {os.path.basename(litematic_path)}")
        self.setGeometry(200, 200, 800, 600)
        
        self.init_ui()
        self.load_litematic_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.setMinimumSize(400, 400)
        
        toolbar = QHBoxLayout()
        
        self.mode_combo = QComboBox()
        for mode_key, mode_info in PREVIEW_MODES.items():
            self.mode_combo.addItem(t(mode_info['name']), mode_key)
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        toolbar.addWidget(self.mode_combo)
        
        self.zoom_in_btn = QPushButton(t('zoom_in'))
        self.zoom_in_btn.clicked.connect(lambda: self.set_zoom(self.zoom * 1.2))
        toolbar.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton(t('zoom_out'))
        self.zoom_out_btn.clicked.connect(lambda: self.set_zoom(self.zoom / 1.2))
        toolbar.addWidget(self.zoom_out_btn)
        
        self.reset_btn = QPushButton(t('reset_view'))
        self.reset_btn.clicked.connect(self.reset_view)
        toolbar.addWidget(self.reset_btn)
        
        layout.addLayout(toolbar)
        
        self.graphics_view = QGraphicsView()
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graphics_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.graphics_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.graphics_view.wheelEvent = self.on_wheel_event
        layout.addWidget(self.graphics_view)
        
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

    def load_litematic_data(self):
        from litemapy import Schematic
        try:
            schem = Schematic.load(self.litematic_path)
            region = schem.regions[list(schem.regions.keys())[0]]
            
            xrange = region.xrange
            zrange = region.zrange
            
            if callable(xrange):
                xrange = xrange()
            if callable(zrange):
                zrange = zrange()
            
            self.width = xrange.stop - xrange.start
            self.height = zrange.stop - zrange.start
            self.data = []
            
            for x in range(self.width):
                row = []
                for z in range(self.height):
                    block = region[x, 0, z]
                    block_name = str(block)
                    if block_name != 'minecraft:air':
                        row.append(block_name.split(':')[1])
                    else:
                        row.append(None)
                self.data.append(row)
            
            self.render_preview()
        except Exception as e:
            QMessageBox.warning(self, t('error'), t('preview_load_failed', error=str(e)))

    def render_preview(self):
        self.scene.clear()
        
        if self.preview_mode == 'map':
            self.render_map_preview()
        elif self.preview_mode == 'build_2d':
            self.render_build_2d_preview()

    def render_map_preview(self):
        image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        for x in range(self.width):
            for z in range(self.height):
                block_name = self.data[x][z]
                if block_name:
                    color_key = block_name.replace('_concrete', '').replace('_wool', '').replace('_carpet', '').replace('_terracotta', '')
                    color_key = color_key.replace('light_gray', 'silver')
                    if color_key in BLOCK_COLOR_MAP:
                        rgb = BLOCK_COLOR_MAP[color_key]
                        image.putpixel((x, z), rgb + (255,))
        
        qimage = QImage(image.tobytes("raw", "RGBA"), self.width, self.height, QImage.Format.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        self.scene.addPixmap(pixmap)
        
        self.graphics_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom = self.graphics_view.transform().m11()

    def render_build_2d_preview(self):
        tile_size = 16
        image = Image.new('RGBA', (self.width * tile_size, self.height * tile_size), (0, 0, 0, 0))
        
        textures = self.load_textures()
        
        for x in range(self.width):
            for z in range(self.height):
                block_name = self.data[x][z]
                if block_name:
                    texture_key = block_name.replace('light_gray', 'silver')
                    if texture_key in BLOCK_TEXTURE_MAP:
                        texture_name = BLOCK_TEXTURE_MAP[texture_key]
                        texture = textures.get(texture_name)
                        if texture:
                            for tx in range(min(tile_size, texture.width)):
                                for ty in range(min(tile_size, texture.height)):
                                    pixel = texture.getpixel((tx, ty))
                                    image.putpixel((x * tile_size + tx, z * tile_size + ty), pixel)
                    else:
                        color_key = block_name.replace('_concrete', '').replace('_wool', '').replace('_carpet', '').replace('_terracotta', '')
                        color_key = color_key.replace('light_gray', 'silver')
                        if color_key in BLOCK_COLOR_MAP:
                            rgb = BLOCK_COLOR_MAP[color_key]
                            for tx in range(tile_size):
                                for ty in range(tile_size):
                                    image.putpixel((x * tile_size + tx, z * tile_size + ty), rgb + (255,))
        
        qimage = QImage(image.tobytes("raw", "RGBA"), image.width, image.height, QImage.Format.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        self.scene.addPixmap(pixmap)
        
        self.graphics_view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom = self.graphics_view.transform().m11()

    def load_textures(self):
        textures = {}
        assets_dir = os.path.join(self.base_dir, 'assets', 'minecraft', 'textures', 'block')
        
        if not os.path.exists(assets_dir):
            return textures
        
        for texture_name in BLOCK_TEXTURE_MAP.values():
            texture_path = os.path.join(assets_dir, texture_name)
            if os.path.exists(texture_path):
                try:
                    textures[texture_name] = Image.open(texture_path).convert('RGBA')
                except:
                    pass
        
        return textures

    def on_mode_changed(self, index):
        self.preview_mode = self.mode_combo.currentData()
        self.render_preview()

    def on_wheel_event(self, event):
        delta = event.angleDelta().y()
        
        if delta > 0:
            self.set_zoom(self.zoom * 1.1)
        else:
            self.set_zoom(self.zoom / 1.1)

    def set_zoom(self, zoom):
        self.zoom = max(0.1, min(50.0, zoom))
        
        view_rect = self.graphics_view.viewport().rect()
        center_pos = view_rect.center()
        
        old_center = self.graphics_view.mapToScene(center_pos)
        
        current_scale = self.graphics_view.transform().m11()
        if current_scale > 0:
            scale_ratio = self.zoom / current_scale
            self.graphics_view.scale(scale_ratio, scale_ratio)
        
        new_center = self.graphics_view.mapFromScene(old_center)
        delta_x = center_pos.x() - new_center.x()
        delta_y = center_pos.y() - new_center.y()
        self.graphics_view.translate(delta_x, delta_y)

    def reset_view(self):
        self.render_preview()

    def resizeEvent(self, event):
        size = event.size()
        min_dim = min(size.width(), size.height())
        if size.width() != min_dim or size.height() != min_dim:
            self.resize(min_dim, min_dim)
            return
        super().resizeEvent(event)