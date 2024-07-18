from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.setFixedHeight(50)
        self.setStyleSheet("""
                           border-top-left-radius: 20px; 
                           border-top-right-radius: 20px; 
                           background-color: rgb(31, 31, 39);
                           """)
        
        self.main_layout = QStackedLayout()
        self.setLayout(self.main_layout)

        self.title_layout = QHBoxLayout()
        self.title = QLabel("WhySo@Spotify")
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.title.setStyleSheet("color: rgb(197, 196, 204);")
        self.title_layout.addWidget(self.title)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch()
        
        button_style = """
            QPushButton {
                background-color: none;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: rgb(92, 62, 24);
            }
        """

        self.minimize_button = QPushButton()
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setIcon(QIcon(resource_path('res\\drawable\\minimize_white.png')))
        self.minimize_button.setIconSize(QSize(20, 20))
        self.minimize_button.setStyleSheet("background-color: none; border: none;")
        self.minimize_button.setStyleSheet(button_style)
        self.minimize_button.clicked.connect(self.minimize_window)

        self.close_button = QPushButton()
        self.close_button.setFixedSize(30, 30)
        self.close_button.setIcon(QIcon(resource_path('res\\drawable\\close2_white.png')))
        self.close_button.setIconSize(QSize(20, 20))
        self.close_button.setStyleSheet("background-color: none; border: none;")
        self.close_button.setStyleSheet(button_style)
        self.close_button.clicked.connect(self.close_window)

        self.buttons_layout.addWidget(self.minimize_button)
        self.buttons_layout.addWidget(self.close_button)

        self.title_widget = QWidget()
        self.title_widget.setLayout(self.title_layout)

        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(self.buttons_layout)
        self.buttons_widget.setAttribute(Qt.WA_TranslucentBackground)
        
        self.main_layout.addWidget(self.buttons_widget)
        self.main_layout.addWidget(self.title_widget)

        self.main_layout.setStackingMode(QStackedLayout.StackAll)

        self.start = QPoint(0, 0)
        self.pressing = False
        

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.move(self.mapToGlobal(self.movement))
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
        
    def minimize_window(self):
        self.parent.showMinimized()

    def close_window(self):
        self.parent.close()