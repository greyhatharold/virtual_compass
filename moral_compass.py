from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPolygonF
import math
from models import Decision, MoralDimension
from logger import get_logger

logger = get_logger(__name__, log_level="DEBUG")

class MoralCompass(QWidget):
    def __init__(self, decision: Decision):
        super().__init__()
        self.decision = decision
        self.setMinimumSize(400, 400)
        logger.debug("MoralCompass initialized", decision=decision)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_compass_face(painter)
        self.draw_moral_dimensions(painter)
        self.draw_decision_arrow(painter)

    def draw_compass_face(self, painter):
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.setBrush(QColor(240, 240, 240))
        painter.drawEllipse(10, 10, self.width() - 20, self.height() - 20)

    def draw_moral_dimensions(self, painter):
        center_x, center_y = self.width() / 2, self.height() / 2
        radius = min(center_x, center_y) - 20
        num_dimensions = len(MoralDimension)

        for i, dimension in enumerate(MoralDimension):
            angle = i * 2 * math.pi / num_dimensions
            score = self.decision.get_dimension_score(dimension)
            normalized_score = (score + 10) / 20  # Normalize from -10:10 to 0:1

            x = int(center_x + math.cos(angle) * radius * normalized_score)
            y = int(center_y + math.sin(angle) * radius * normalized_score)

            # Draw dimension line
            painter.setPen(QPen(QColor(0, 100, 200), 2))
            painter.drawLine(int(center_x), int(center_y), x, y)

            # Draw dimension marker
            painter.setPen(QPen(QColor(200, 50, 50), 4))
            painter.drawPoint(x, y)

            # Draw dimension label
            painter.setPen(QColor(0, 0, 0))
            painter.setFont(QFont('Arial', 10))
            label_x = int(center_x + math.cos(angle) * (radius + 20))
            label_y = int(center_y + math.sin(angle) * (radius + 20))
            painter.drawText(label_x - 50, label_y, 100, 20, Qt.AlignCenter, dimension.value)

    def draw_decision_arrow(self, painter):
        center_x, center_y = self.width() / 2, self.height() / 2
        radius = min(center_x, center_y) - 40
        goodness = self.decision.goodness
        angle = math.pi * (1 - goodness) / 2

        x = int(center_x + math.sin(angle) * radius)
        y = int(center_y - math.cos(angle) * radius)

        # Draw arrow line
        painter.setPen(QPen(QColor(200, 50, 50), 3))
        painter.drawLine(int(center_x), int(center_y), x, y)

        # Draw arrowhead
        arrowhead_size = 15
        arrowhead = QPolygonF([
            QPointF(x, y),
            QPointF(x - arrowhead_size * math.cos(angle - math.pi/6),
                    y - arrowhead_size * math.sin(angle - math.pi/6)),
            QPointF(x - arrowhead_size * math.cos(angle + math.pi/6),
                    y - arrowhead_size * math.sin(angle + math.pi/6))
        ])
        painter.setBrush(QColor(200, 50, 50))
        painter.drawPolygon(arrowhead)

    def update_decision(self, new_decision: Decision):
        self.decision = new_decision
        self.update()
