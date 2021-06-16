#import PyQt5
#from PyQt5 import QtCore
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import os
#from os import path
import urllib.request
import pafy
import humanize

uiFile, _ = loadUiType('main.ui')
Ui_MainWindow, _ = loadUiType('subWindow.ui')

################ Main Class ##########################
class MainApp(QMainWindow, uiFile):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_userInterface()


################## open the second window ########
    def open_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
##################################################


    def setup_userInterface(self):
        self.setWindowTitle('Joud Download Manager')
        self.setFixedSize(654, 294)
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
        self.pushButton_8.clicked.connect(self.get_videoData)
        self.pushButton_12.clicked.connect(self.download_yt_playlist)
        self.pushButton_6.clicked.connect(self.download_youtube_video)
        self.pushButton_7.clicked.connect(self.setup_browse_forVideo)
        self.pushButton_13.clicked.connect(self.browse_forList)
        self.pushButton_9.clicked.connect(self.playList_data)
        self.pushButton_10.clicked.connect(self.open_window)

#################################################
###### Download any file:########################
    def setup_progress_bar(self, blocknum, blocksize, totalsize):
        red = blocknum * blocksize
        if totalsize > 0:
            percent = red * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()

    def download_file(self):
        url = self.lineEdit.text()
        location = self.lineEdit_2.text()

        if url == '' or location == '':
            QMessageBox.warning(self, 'Empty Field', 'Enter a valid URL and Location ...... !!!')

        else:
            try:
                urllib.request.urlretrieve(url, location, self.setup_progress_bar)
            except Exception:
                QMessageBox.warning(self, 'Download Error', 'The Download Failed')
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')
                self.progressBar.setValue(0)
                return

            QMessageBox.information(self, 'Download Completed', 'The Download Finished Successfully')
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.progressBar.setValue(0)

    def setup_browse_file(self):
        location = QFileDialog.getExistingDirectory(self, 'Save To')
        self.lineEdit_2.setText(location)
#################################################

######### Download a video from youtube:#########
    def get_videoData(self):
        url = self.lineEdit_4.text()

        if url == '':
            QMessageBox.warning(self, 'Empty Field', 'Enter a valid URL ...... !!!')

        else:
            vid = pafy.new(url)
            info = '{} ({})'.format(vid.title, vid.duration)
            self.textEdit_2.setPlainText(info)

            vid_streams = vid.allstreams
            for s in vid_streams:
                size = humanize.naturalsize(s.get_filesize())
                data = '{}, ({}), {}, {}'.format(s.mediatype, s.extension,  s.quality, size)
                self.comboBox.addItem(data)

    def download_youtube_video(self):
        url = self.lineEdit_4.text()
        location = self.lineEdit_3.text()
        if url == '' or location == '':
            QMessageBox.warning(self, 'Empty Field', 'Enter a valid URL, and Choose the  Location directory\n and Select the Quality...... !!!')
        else:
            vid = pafy.new(url)
            vid_stream = vid.allstreams
            quality = self.comboBox.currentIndex()
            try:
                download = vid_stream[quality].download(filepath=location)
            except Exception:
                QMessageBox.warning(self, 'Download Error', 'The Download Failed')
                self.lineEdit_3.setText('')
                self.lineEdit_4.setText('')
                self.progressBar.setValue(0)
                return

            QMessageBox.information(self, 'Download Complete', 'The Download Finished Successfully')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')

    def setup_browse_forVideo(self):
        location = QFileDialog.getExistingDirectory(self, 'Save To')
        self.lineEdit_3.setText(location)
##################################################

###### Download a playlist from youtube:##########
    def playList_data(self):
        url = self.lineEdit_10.text()
        if url == '':
            QMessageBox.warning(self, 'Empty Field', 'Enter a valid URL ...... !!!')
        else:
            list = pafy.get_playlist(url)
            list_title = list['title']
            self.textEdit.setPlainText(list_title)

    def download_yt_playlist(self):
        url = self.lineEdit_10.text()
        location = self.lineEdit_9.text()

        if url == '' or location == '':
            QMessageBox.warning(self, 'Empty Field', 'Enter a valid URL and Location directory ...... !!!')
        else:
            list = pafy.get_playlist(url)
            list['title']
            videos = list['items']

            os.chdir(location)
            # To Create a folder for playlist videos:
            #os.mkdir(str(list['title']))
            #os.chdir(str(list['title']))

            for vid in videos:
                p = vid['pafy']
                down = p.getbest(preftype='mp4')
                down.download()

            QMessageBox.information(self, 'Download Complete', 'The Download Finished Successfully')

    def browse_forList(self):
        location = QFileDialog.getExistingDirectory(self, 'Save To')
        self.lineEdit_9.setText(location)
##################################################


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
