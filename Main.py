from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import windowbar
import SpotifyAPI
import colorPicker
    
class Window(QWidget):
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        brush = QBrush(QColor(37, 40, 49, 255))
        painter.setBrush(brush)

        pen = QPen(Qt.black)
        painter.setPen(pen)

        painter.drawRoundedRect(rect, 20, 20)
        
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        width = 575
        height = 275
        
        
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        
        self.window_bar = windowbar.MyBar(self)
        self.main_layout.addWidget(self.window_bar)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_widget.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_widget)
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignVCenter)
        self.label.setStyleSheet("color: rgb(197, 196, 204); font-size: 15px;")
        self.content_layout.addWidget(self.label)
        
        self.update_track_info()
        self.show()

        # Update track info every second
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_track_info)
        self.timer.start(1000)
        
    def update_track_info(self):
        track_info = SpotifyAPI.SpotifyClient.get_current_playback()
        if track_info:
            track_name = track_info['track_name']
            track_artists = track_info['track_artists']
            track_length = track_info['track_length']
            current_time = track_info['current_time']
            thumbnail = track_info['thumbnail']
            progress = (current_time / track_length) * 100
            
            #Change color
            global last_track_name
            global highlightAscent
            if last_track_name != track_name:
                last_track_name = track_name
                
                # print("\nNow played:",track_name)
                color = colorPicker.Colorpicker.getColorFromThumbnail(thumbnail)
                highlightAscent = color
                

            track_length_str = f"{track_length // 60:02d}:{track_length % 60:02d}"
            current_time_str = f"{current_time // 60:02d}:{current_time % 60:02d}"
            

            self.label.setText(self.get_colored_text(track_name, track_artists, current_time_str, track_length_str, progress))
        else:
            self.label.setText("<div style='font-family: \"JetBrains Mono SemiBold\"; font-size: 20px; color: rgb(230, 230, 230);'>No track is currently playing.</div>")

    def get_colored_text(self, title, artist, current_time, total_time, progress):
        global highlightAscent 
        progress_bar_length = 40
        progress_filled = int(progress_bar_length * progress / 100)
        progress_empty = progress_bar_length - progress_filled
        
        return f"""
                <div style="font-family: 'JetBrains Mono SemiBold', 'Noto Sans Thai SemiBold'; font-size: 20px;">
                <p style="color:rgb{highlightAscent}; ">WhySo@Spotify<span style="color:rgb(197, 196, 204);">:<span style="color:rgb(75, 128, 213);">~</span>$ </span> <span style="color:rgb(230, 180, 170);">./shelltify</span> <span style="color:rgb(197, 196, 204);">--nowplaying</span></p>
	            <p style="color:rgb(230, 230, 230)";>Title: {title}</p>
	            <p style="color:rgb(230, 230, 230)";>Artist: {artist}</p>
                <p style="color:rgb(230, 230, 230)";>[<span style="color:rgb{highlightAscent};">{"#"*(progress_filled+1)}</span><span style="color:rgb(197, 196, 204;">{"-"*(progress_empty-1)}</span>]</p>
	            <p style="color:rgb(230, 230, 230)"; >{current_time} - {total_time}</p>
                </div>
        """

global highlightAscent 
global last_track_name 
highlightAscent = '(255, 85, 85)'
last_track_name = ''

app = QApplication(sys.argv)

id = QFontDatabase.addApplicationFont("res\\fonts\\JetbrainMono\\static\\JetBrainsMono-SemiBold.ttf")
QFontDatabase.addApplicationFont("res\\fonts\\Noto_Sans_Thai\\static\\NotoSansThai-SemiBold.ttf")
_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
_font = QFont(_fontstr, 13)
app.setFont(_font)

window = Window()
sys.exit(app.exec())