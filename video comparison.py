import sys
import os
from PyQt5.QtCore import QUrl, QTimer, QTime,Qt,QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,QSizePolicy,QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video1_folder = ''
        self.video2_folder = ''
        self.settings = QSettings("YourOrganizationName", "Video Comparison")  # Use a unique organization name
        self.video1_folder = self.settings.value("input_folder1", "")
        self.video2_folder = self.settings.value("input_folder2", "")

        self.player1 = QMediaPlayer(self)
        self.player2 = QMediaPlayer(self)

        self.video_widget1 = QVideoWidget(self)
        self.video_widget2 = QVideoWidget(self)

        self.label_elapsed1 = QLabel("00:00", self)
        
        self.label_elapsed2 = QLabel("00:00", self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_elapsed_time)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.sliderMoved.connect(self.seek_both_videos)

        self.init_ui()

        # Set the minimum sizes for player1 and player2
        self.video_widget1.setMinimumSize(400, 400)  # Adjust the values as per your requirements
        self.video_widget2.setMinimumSize(400, 400)  # Adjust the values as per your requirements


    def init_ui(self):
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 450)

        layout = QVBoxLayout()

        video_layout = QHBoxLayout()
        video_layout.addWidget(self.video_widget1)
        video_layout.addWidget(self.video_widget2)
        layout.addLayout(video_layout)
        
        elapsed_layout = QHBoxLayout()
        elapsed_layout.addWidget(self.label_elapsed1, 1, alignment=Qt.AlignLeft | Qt.AlignTop)
        elapsed_layout.addWidget(self.label_elapsed2, 1, alignment=Qt.AlignRight | Qt.AlignTop)
        layout.addLayout(elapsed_layout)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider)
        layout.addLayout(slider_layout) 

        openButton_layout = QHBoxLayout()
        self.open_button1 = QPushButton("Open Video 1", self)
        self.open_button1.clicked.connect(self.open_video1)
        openButton_layout.addWidget(self.open_button1, 2)

        self.open_button2 = QPushButton("Open Video 2", self)
        self.open_button2.clicked.connect(self.open_video2)
        openButton_layout.addWidget(self.open_button2, 2)
        layout.addLayout(openButton_layout)

        control_layout = QHBoxLayout()
        self.play_button = QPushButton("Play", self)
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.play_videos)
        control_layout.addWidget(self.play_button, 2)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.pause_videos)
        control_layout.addWidget(self.pause_button, 2)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_videos)
        control_layout.addWidget(self.stop_button, 2)

        layout.addLayout(control_layout)

        # Set size policy for video widgets to expand with the window
        self.video_widget1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_widget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add some spacing around the widgets to reduce crowding
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        print(self.video1_folder)
        print(self.video2_folder)

    def open_video1(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File 1", self.video1_folder, "Video Files (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.mpeg *.mpg *.m4v *.ts);;All Files (*)")

        if file_name:
            self.video1_folder = os.path.dirname(file_name) or '.'  # Update the folder location with a fallback to current directory
            self.settings.setValue("input_folder1", self.video1_folder)
            media_content = QMediaContent(QUrl.fromLocalFile(file_name))
            self.player1.setMedia(media_content)
            self.player1.setVideoOutput(self.video_widget1)
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            print(self.video1_folder)

            self.timer.start(1000)

    def open_video2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File 2", self.video2_folder, "Video Files (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.mpeg *.mpg *.m4v *.ts);;All Files (*)")

        if file_name:
            self.video2_folder = os.path.dirname(file_name) or '.'  # Update the folder location with a fallback to current directory
            self.settings.setValue("input_folder2", self.video2_folder)
            media_content = QMediaContent(QUrl.fromLocalFile(file_name))
            self.player2.setMedia(media_content)
            self.player2.setVideoOutput(self.video_widget2)
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            print(self.video2_folder)

            self.timer.start(1000)

    def seek_both_videos(self, position):
        self.player1.setPosition(position)
        self.player2.setPosition(position)

    def play_videos(self):
        self.player1.play()
        self.player2.play()

    def pause_videos(self):
        self.player1.pause()
        self.player2.pause()

    def stop_videos(self):
        self.player1.stop()
        self.player2.stop()
        self.timer.stop()

    def update_elapsed_time(self):
        self.update_elapsed_label(self.label_elapsed1, self.player1, self.slider)
        self.update_elapsed_label(self.label_elapsed2, self.player2, self.slider)

    def update_elapsed_label(self, label, player, slider):
        position = player.position()
        elapsed_time = QTime(0, position // 60000, (position // 1000) % 60)
        label.setText(elapsed_time.toString("mm:ss"))

        # Get the maximum duration of both players
        max_duration = max(self.player1.duration(), self.player2.duration())
        slider.setMaximum(max_duration)
        slider.setValue(position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())