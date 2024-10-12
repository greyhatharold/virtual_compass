import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QScrollArea, QFrame, QSplitter)
from PyQt5.QtGui import QFont, QPainter, QColor, QLinearGradient, QPen, QIcon
from PyQt5.QtCore import Qt, QRect
from moral_compass import MoralCompass
from models import Decision, MoralDimension
from response_generator import ResponseGenerator
from input_analysis import ConversationAnalyzer

class MedievalScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet("""
            QScrollArea {
                border: 2px solid #8B4513;
                border-radius: 10px;
                background-color: #FFF8DC;
            }
            QScrollBar:vertical {
                border: none;
                background: #D2B48C;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #8B4513;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

class MedievalButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Times New Roman", 12, QFont.Bold))
        self.setFixedSize(200, 50)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Button shape
        rect = self.rect().adjusted(2, 2, -2, -2)
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, QColor("#D2B48C"))
        gradient.setColorAt(1, QColor("#8B4513"))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor("#4A2601"), 2))
        painter.drawRoundedRect(rect, 10, 10)

        # Text
        painter.setPen(QColor("#FFF8DC"))
        painter.drawText(rect, Qt.AlignCenter, self.text())

        # Highlight effect
        if self.underMouse():
            painter.setBrush(QColor(255, 255, 255, 30))
            painter.drawRoundedRect(rect, 10, 10)

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ye Olde Decision Analysis Toole")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                                  stop:0 #F4A460, stop:1 #D2691E);
            }
        """)

        self.response_generator = ResponseGenerator()
        self.conversation_analyzer = ConversationAnalyzer()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        main_layout.addWidget(self.create_header())

        # Create a splitter for the main content
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)

        # Left side: Input, buttons, and output
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(self.create_input_section())
        left_layout.addWidget(self.create_button_section())
        left_layout.addWidget(self.create_output_section())
        content_splitter.addWidget(left_widget)

        # Right side: Moral Compass
        # Create an initial Decision with neutral moral scores
        initial_moral_scores = {dim: 0 for dim in MoralDimension}
        initial_decision = Decision("Initial Decision", "No decision made yet", initial_moral_scores)

        self.moral_compass = MoralCompass(initial_decision)
        content_splitter.addWidget(self.moral_compass)

        # Set the initial sizes of the splitter
        content_splitter.setSizes([600, 400])

    def create_header(self):
        header = QLabel("Ye Olde Decision Analysis Toole")
        header.setStyleSheet("""
            font-size: 36px;
            color: #FFF8DC;
            font-family: 'Times New Roman';
            font-weight: bold;
            padding: 20px;
            background-color: rgba(139, 69, 19, 0.7);
            border-radius: 15px;
        """)
        header.setAlignment(Qt.AlignCenter)
        return header

    def create_input_section(self):
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 248, 220, 0.7);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)

        input_label = QLabel("Enter your query:")
        input_label.setStyleSheet("""
            font-size: 18px;
            color: #8B4513;
            font-family: 'Times New Roman';
            font-weight: bold;
            margin-bottom: 10px;
        """)
        input_layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFF8DC;
                color: #8B4513;
                border: 2px solid #DAA520;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Times New Roman';
                font-size: 14px;
            }
        """)
        self.input_text.setFixedHeight(100)
        input_layout.addWidget(self.input_text)

        return input_frame

    def create_button_section(self):
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(20)

        analyze_button = MedievalButton("Analyze")
        analyze_button.clicked.connect(self.analyze_input)
        button_layout.addWidget(analyze_button)

        clear_button = MedievalButton("Clear")
        clear_button.clicked.connect(self.clear_input)
        button_layout.addWidget(clear_button)

        return button_frame

    def create_output_section(self):
        output_frame = QFrame()
        output_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 248, 220, 0.7);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        output_layout = QVBoxLayout(output_frame)

        output_label = QLabel("Analysis Results:")
        output_label.setStyleSheet("""
            font-size: 18px;
            color: #8B4513;
            font-family: 'Times New Roman';
            font-weight: bold;
            margin-bottom: 10px;
        """)
        output_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFF8DC;
                color: #8B4513;
                border: 2px solid #DAA520;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Times New Roman';
                font-size: 14px;
            }
        """)

        scroll_area = MedievalScrollArea()
        scroll_area.setWidget(self.output_text)
        scroll_area.setFixedHeight(200)
        output_layout.addWidget(scroll_area)

        return output_frame

    def analyze_input(self):
        input_text = self.input_text.toPlainText()
        
        # Use ConversationAnalyzer to get detailed analysis
        analysis_result = self.conversation_analyzer.analyze_input(input_text)
        
        # Generate response using ResponseGenerator
        response = self.response_generator.generate_response(input_text)
        
        # Display the response
        self.output_text.setPlainText(response)

        # Update the Moral Compass
        new_decision = analysis_result['decision']
        self.moral_compass.decision = new_decision
        self.moral_compass.update()

        # Display additional analysis information
        additional_info = f"""
Sentiment: {analysis_result['sentiment']['compound']:.2f}
Dominant Emotion: {max(analysis_result['emotions'], key=analysis_result['emotions'].get)}
Key Phrases: {', '.join(analysis_result['key_phrases'][:5])}  # Display top 5 key phrases
Entities: {', '.join([e['text'] for e in analysis_result['entities'][:5]])}  # Display top 5 entities
        """
        self.output_text.append("\n\nAdditional Analysis:")
        self.output_text.append(additional_info)

    def clear_input(self):
        self.input_text.clear()
        self.output_text.clear()
        # Reset the Moral Compass to its initial state
        initial_moral_scores = {dim: 0 for dim in MoralDimension}
        self.moral_compass.decision = Decision("Initial Decision", "No decision made yet", initial_moral_scores)
        self.moral_compass.update()
