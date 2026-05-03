import sys
import random
import math
from PIL import Image, ImageDraw
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class MagicCircleGenerator:
    def __init__(self, size=128):
        self.size = size
        self.center = size // 2
        self.margin = size // 10
        self.max_radius = (size // 2) - self.margin

    def generate(self):
        # Create a transparent background (0,0,0,0) or black (0,0,0)
        # We'll use RGBA to allow transparency, drawing in pure White
        image = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Decide on a symmetry factor (e.g., 4, 6, 8, 12)
        symmetry = random.choice([4, 6, 8, 12])
        
        # Layering layers
        num_layers = random.randint(3, 6)
        radii = sorted([random.randint(self.size // 6, self.max_radius) for _ in range(num_layers)])

        for i, r in enumerate(radii):
            style = random.choice(['circle', 'polygon', 'star', 'runes', 'spokes'])
            
            if style == 'circle':
                self._draw_circle(draw, r)
                # Sometimes draw a double circle
                if random.random() > 0.7:
                    self._draw_circle(draw, r - 2)

            elif style == 'polygon':
                self._draw_polygon(draw, r, symmetry)

            elif style == 'star':
                self._draw_star(draw, r, symmetry)

            elif style == 'spokes':
                self._draw_spokes(draw, r, radii[i-1] if i > 0 else 0, symmetry)

            elif style == 'runes':
                self._draw_runes(draw, r, symmetry)

        return image

    def _draw_circle(self, draw, r):
        draw.ellipse([self.center - r, self.center - r, self.center + r, self.center + r], outline="white", width=1)

    def _draw_polygon(self, draw, r, n):
        points = []
        for i in range(n):
            angle = math.radians(i * (360 / n))
            x = self.center + r * math.cos(angle)
            y = self.center + r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, outline="white")

    def _draw_star(self, draw, r, n):
        points = []
        inner_r = r * 0.5
        for i in range(n * 2):
            curr_r = r if i % 2 == 0 else inner_r
            angle = math.radians(i * (360 / (n * 2)))
            x = self.center + curr_r * math.cos(angle)
            y = self.center + curr_r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, outline="white")

    def _draw_spokes(self, draw, r_outer, r_inner, n):
        for i in range(n):
            angle = math.radians(i * (360 / n))
            x1 = self.center + r_inner * math.cos(angle)
            y1 = self.center + r_inner * math.sin(angle)
            x2 = self.center + r_outer * math.cos(angle)
            y2 = self.center + r_outer * math.sin(angle)
            draw.line([(x1, y1), (x2, y2)], fill="white", width=1)

    def _draw_runes(self, draw, r, n):
        # Draws abstract small lines/dots around the perimeter
        for i in range(n * 2):
            angle = math.radians(i * (360 / (n * 2)) + 15)
            x = self.center + r * math.cos(angle)
            y = self.center + r * math.sin(angle)
            
            rune_type = random.choice(['dot', 'line', 'cross'])
            size = self.size // 32
            if rune_type == 'dot':
                draw.ellipse([x-1, y-1, x+1, y+1], fill="white")
            elif rune_type == 'line':
                draw.line([(x-size, y), (x+size, y)], fill="white")
            elif rune_type == 'cross':
                draw.line([(x-size, y-size), (x+size, y+size)], fill="white")
                draw.line([(x+size, y-size), (x-size, y+size)], fill="white")

class MagicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procedural Magic Circle Gen")
        self.current_image = None
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Preview Label
        self.preview_label = QLabel("Click Generate")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedSize(400, 400)
        self.preview_label.setStyleSheet("background-color: #1a1a1a; border: 2px solid #555;")
        layout.addWidget(self.preview_label)

        # Controls
        controls = QHBoxLayout()
        
        self.res_combo = QComboBox()
        self.res_combo.addItems(["32", "64", "128", "256"])
        self.res_combo.setCurrentText("128")
        
        gen_btn = QPushButton("✨ Generate")
        gen_btn.clicked.connect(self.generate_circle)
        
        save_btn = QPushButton("💾 Save PNG")
        save_btn.clicked.connect(self.save_circle)

        controls.addWidget(QLabel("Res:"))
        controls.addWidget(self.res_combo)
        controls.addWidget(gen_btn)
        controls.addWidget(save_btn)
        
        layout.addLayout(controls)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def generate_circle(self):
        res = int(self.res_combo.currentText())
        gen = MagicCircleGenerator(res)
        self.current_image = gen.generate()
        
        # Convert PIL to QPixmap for preview
        # We scale it up so it's not tiny in the UI
        data = self.current_image.tobytes("raw", "RGBA")
        qimg = QImage(data, res, res, QImage.Format.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaled(380, 380, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        self.preview_label.setPixmap(scaled_pixmap)

    def save_circle(self):
        if self.current_image:
            path, _ = QFileDialog.getSaveFileName(self, "Save Image", "magic_circle.png", "PNG Files (*.png)")
            if path:
                self.current_image.save(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MagicApp()
    window.show()
    sys.exit(app.exec())