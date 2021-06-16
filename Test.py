from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import os
from os import path
import urllib.request
import pafy

uiFile, _ = loadUiType('main.ui')


class MainApp(QMainWindow, uiFile):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_userInterface()


    def setup_userInterface(self):
        self.setWindowTitle('Joud Download Manager')
        self.setup_buttons()
        self.tabWidget.tabBar().setVisible(False)


################################################
######## UI CHanges Methods ####################

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube_video(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Youtube_list(self):
        self.tabWidget.setCurrentIndex(3)

################################################

    def setup_buttons(self):
        self.pushButton.clicked.connect(self.download_file)
        self.pushButton_3.clicked.connect(self.Open_Home)
        self.pushButton_4.clicked.connect(self.Open_Download)
        self.pushButton_5.clicked.connect(self.Open_Youtube_video)
        self.pushButton_14.clicked.connect(self.Open_Youtube_list)
        self.pushButton_2.clicked.connect(self.setup_browse_file)
        self.pushButton_6.clicked.connect(self.download_yt_video)
        self.pushButton_12.clicked.connect(self.download_yt_playlist)
        self.pushButton_7.clicked.connect(self.setup_browse_forVideo)
        self.pushButton_13.clicked.connect(self.setup_browse_forList)


#######################################
###### Download any file:##############

    def setup_progress_bar(self, blocknum, blocksize, totalsize):
        red = blocknum * blocksize
        if totalsize > 0:
            percent = red * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()


    def download_file(self):
        url = self.lineEdit.text()
        location = self.lineEdit_2.text()

        try:
            urllib.request.urlretrieve(url, location, self.setup_progress_bar)
        except Exception:
            QMessageBox.warning(self, 'Download Error', 'The Download Failed')
            return
        QMessageBox.information(self, 'Download Completed', 'The Download Finished')


        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    def setup_browse_file(self):
        location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(location[0]))


#################################################
######### Download a video from youtube:#########

    def download_yt_video(self):
        vid_url = self.lineEdit_4.text()
        location = self.lineEdit_3.text()
        try:
            vid = pafy.new(vid_url)
            print(vid.title)
            print(vid.duration)
            print(vid.rating)
            print(vid.author)
            print(vid.length)
            print(vid.viewcount)

        except Exception:
            QMessageBox.warning(self, 'Download Error', 'The Download Failed')
            return
        QMessageBox.information(self, 'Download Completed', 'The Download Finished')

        self.lineEdit_4.setText('')
        self.lineEdit_3.setText('')
        self.progressBar.setValue(0)

    def setup_browse_forVideo(self):
        location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_3.setText(str(location[0]))



##################################################
###### Download a playlist from youtube:##########
    def download_yt_playlist(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
