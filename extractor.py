# frame extractor from video
# Author: Abul Al Arabi

# create the gui using pyqt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLineEdit, QLabel, QSlider, QFormLayout, QComboBox
# error message box
from PyQt5.QtWidgets import QMessageBox
# progress bar
from PyQt5.QtWidgets import QProgressBar

# for video processing
import cv2
import os
'''
    - in the gui: there will be a file selector
    - there will be a field to enter the frame rate (FPS)
    - there will be a start time and a end time field
    - there will be a destination folder selector
    - there will be a button to start the process
    - there will be a button to stop the process
'''

class FrameExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Frame Extractor')
        self.setGeometry(100, 100, 300, 300)

        # create a layout
        layout = QFormLayout()

        # create a container
        container = QWidget()
        container.setStyleSheet("border: 1px solid black;")

        # create a layout for the container
        containerLayout = QVBoxLayout()

        # add a title
        title = QLabel('Frame Extractor by Abul Al Arabi')
        title.setStyleSheet("font-weight: bold; font-size: 16px;")

        # add a description
        description = QLabel('This program extracts frames from a video file.')
        description.setWordWrap(True)

        # create a box layout
        boxLayout = QVBoxLayout()
        boxLayout.addWidget(title)
        boxLayout.addWidget(description)

        # add the box layout to the container layout
        containerLayout.addLayout(boxLayout)

        # add a description
        containerLayout.addWidget(QLabel('You can specify the frame rate, start time and end time.'))
        containerLayout.addWidget(QLabel('The frames will be saved in the destination folder.'))
        containerLayout.addWidget(QLabel('Click on Start Process to start the process.'))
        containerLayout.addWidget(QLabel('Click on Stop Process to stop the process.'))
        containerLayout.addWidget(QLabel('The frames will be saved with the frame number as prefix.'))
        containerLayout.addWidget(QLabel('The frames will be saved in jpg format.'))

        # set the container layout
        container.setLayout(containerLayout)

        # add the container to the main layout
        layout.addRow(container)
        

        # create a file selector
        self.fileSelector = QPushButton('Select Video File')
        self.fileSelector.clicked.connect(self.fileSelectorClicked)
        layout.addRow(QLabel('Select Video File:'), self.fileSelector)

        # add a label for the selected file
        self.selectedFile = QLabel('No file selected')
        layout.addRow(self.selectedFile)


        # create a frame rate field
        self.frameRate = QLineEdit()
        layout.addRow(QLabel('Frame Rate:'), self.frameRate)

        # create a start time field
        self.startTime = QLineEdit()
        layout.addRow(QLabel('Start Time:'), self.startTime)

        # create a end time field
        self.endTime = QLineEdit()
        layout.addRow(QLabel('End Time:'), self.endTime)

        # create a destination folder selector
        self.destinationFolder = QPushButton('Select Destination Folder')
        self.destinationFolder.clicked.connect(self.destinationFolderClicked)
        layout.addRow(QLabel('Destination Folder:'), self.destinationFolder)

        # create a button to start the process
        self.startProcess = QPushButton('Start Process')
        self.startProcess.clicked.connect(self.startProcessClicked)
        layout.addRow(self.startProcess)

        # create a button to stop the process
        self.stopProcess = QPushButton('Stop Process')
        self.stopProcess.clicked.connect(self.stopProcessClicked)
        layout.addRow(self.stopProcess)

        # create a progress bar
        self.progressBar = QProgressBar()
        layout.addRow(self.progressBar)


        self.run = False

        self.setLayout(layout)
        self.show()

    def fileSelectorClicked(self):
        self.videoFile = QFileDialog.getOpenFileName(self, 'Select Video File', os.getenv('HOME'), 'Video Files (*.mp4 *.avi *.mkv)')[0]
        self.selectedFile.setText(self.videoFile)
        # set the start time to 0
        self.startTime.setText('0')
        # set the end time to the duration of the video
        cap = cv2.VideoCapture(self.videoFile)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
        self.endTime.setText(str(duration))

        # set the frame rate to the fps
        self.frameRate.setText(str(fps))


    def destinationFolderClicked(self):
        self.destinationFolder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder', os.getenv('HOME'))
        print(self.destinationFolder)

    def startProcessClicked(self):
        # get the frame rate
        frameRate = int(float(self.frameRate.text()))

        # get the start time
        startTime = int(float(self.startTime.text()))

        # get the end time
        endTime = int(float(self.endTime.text()))

        # get the video file
        videoFile = self.videoFile
        # get the destination folder
        destinationFolder = self.destinationFolder

        # check if the destination folder is selected
        if not destinationFolder:
            # show an error message using a message box
            QMessageBox.critical(self, 'Error', 'Please select a destination folder.')
            return


        # check if the destination folder exists
        if not os.path.exists(destinationFolder):
            os.makedirs(destinationFolder)

        # read the video file
        cap = cv2.VideoCapture(videoFile)
        
        # extract the frames from startTime to endTime and save with frame number prefix
        frameNumber = 0
        self.run = True
        
        # disable the start process button
        self.startProcess.setEnabled(False)
        
        while cap.isOpened() and self.run:
            ret, frame = cap.read()
            if not ret:
                break
            frameNumber += 1
            if frameNumber < startTime * frameRate:
                continue
            if frameNumber > endTime * frameRate:
                break
            if not self.run:
                break
            cv2.imwrite(destinationFolder + '/' + str(frameNumber) + '.jpg', frame)
            
            # update the progress bar
            progress = int((frameNumber / (endTime * frameRate)) * 100)
            self.progressBar.setValue(progress)
            QApplication.processEvents()

        # enable the start process button
        self.startProcess.setEnabled(True)
    

    def stopProcessClicked(self):
        # stop the process 
        self.run = False
        # enable the start process button
        self.startProcess.setEnabled(True)

if __name__ == '__main__':
    app = QApplication([])
    frameExtractor = FrameExtractor()
    app.exec_()