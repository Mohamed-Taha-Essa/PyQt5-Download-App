import os

import setuptools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
import sys
import urllib.request
# import pafy
from PyQt5 import QtCore
from pytube import YouTube ,Playlist
from threading import *


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.perc_dl = 0
        self.video_resolutions = []
        self.videos = []
        self.resolution = None
        uic.loadUi('main.ui', self)
        self.my_video = None
        self.Handle_ui()
        self.Handle_button()
        self.comboBox.setPlaceholderText("--Choose One--")


    ####################################################################
    def Handle_ui(self):
        self.setWindowTitle("Taha Downloader")
        self.setFixedSize(555, 300)


    def Handle_button(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_browse)
        self.pushButton_3.clicked.connect(self.Handle_browse_1)
        self.pushButton_5.clicked.connect(self.Handle_browse_1)
        self.pushButton_7.clicked.connect(self.Get_Youtube_Video_1)
        self.pushButton_4.clicked.connect(self.Download_Youtube_Video_1)
        self.pushButton_6.clicked.connect(self.thread)
        # self.lineEdit_3.textChanged.connect(self.Resolution)

        # self.comboBox.activated[str].connect(self.onSelected)

    def Handle_browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        text = str(save_place)
        # name =name.split(',')[0]
        # name=name[2:-1]
        name = (text[2:].split(',')[0].replace("'", ''))
        self.lineEdit_2.setText(name)
        # if self.sender() ==self.pushButton_2:
        #     self.lineEdit_2.setText(name)
        #
        # elif self.sender() == self.pushButton_3:
        #     self.lineEdit_4.setText(name)
        #
        # elif self.sender() == self.pushButton_5:
        #     self.lineEdit_6.setText(name)
        #
        # else:
        #     pass


    def Handle_progress_bar(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percentage = read * 100 / totalsize
            self.progressBar.setValue(percentage)
            QApplication.processEvents()  # to solve problem of not responding insteadof thread

    def Download(self):
        # url   - save location ,size of file
        url = self.lineEdit.text()

        save_location = self.lineEdit_2.text()
        try:
            urllib.request.urlretrieve(url, save_location, self.Handle_progress_bar)
        except Exception:
            QMessageBox.warning(self, "Error Message", "download failed")
            return

        QMessageBox.information(self, "Download completed", "download finished")
        self.progressBar.setValue(0)
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")

######################################### Page 2 ##################################################################
    def Handle_progress_bar_1(self,stream, chunk, bytes_remaining):
        curr = stream.filesize - bytes_remaining
        per_downloaded = round((curr / stream.filesize) * 100)
        self.perc_dl = per_downloaded
        self.progressBar_2.setValue(int(self.perc_dl))
        QApplication.processEvents()

    def Get_Youtube_Video_1(self):
        self.my_video = YouTube(self.lineEdit_3.text() )
        self.my_video.check_availability()
        QApplication.processEvents()
        print("meta = ", self.my_video.metadata)
        print("streams = ", self.my_video.streams)
        try:
            for stream in self.my_video.streams.filter(progressive=True).order_by('resolution'):
                self.video_resolutions.append(stream.resolution)
                self.videos.append(stream)
                # print(stream.mime_type)
                data ='{} {} {} {}'.format(stream.mime_type ,stream.resolution,", size = ",stream.filesize_mb)
                self.comboBox.addItem(data)

        except:
            print("An error has occurred")
        print("click start to start download")

    def Handle_browse_1(self):
        save_location =QFileDialog.getExistingDirectory(self,"Selet Download directory")
        self.lineEdit_4.setText(save_location)
        self.lineEdit_6.setText(save_location)

    def Download_Youtube_Video_1(self):
        self.my_video.register_on_progress_callback(self.Handle_progress_bar_1)
        path =self.lineEdit_4.text()
        index =self.comboBox.currentIndex()
        print(self.videos[index].filesize/(1024*1024), "MB")
        self.videos[index].download(path)

        QMessageBox.information(self, "Download completed", "download finished")
        self.progressBar_2.setValue(0)
        self.lineEdit_3.setText("")
        self.comboBox.Clear()

    ##############################-Download playlist-####################################################################
    def Handle_progress_bar_2(self,stream, chunk, bytes_remaining):
        curr = stream.filesize - bytes_remaining
        per_downloaded = round((curr / stream.filesize) * 100)
        perc_dl = per_downloaded
        self.progressBar_3.setValue(int(perc_dl))


    def thread(self):
        t1 = Thread(target=self.Download_Youtube_Playlist)
        t1.start()
        # t2 =Thread(target =self.Handle_progress_bar_2)
        # t2.start()
    def Download_Youtube_Playlist(self):
        playlist_url =self.lineEdit_5.text()
        save_location =self.lineEdit_6.text()
        p = Playlist(playlist_url)
        os.chdir(save_location)
        if os.path.exists(str(p.title)):
            os.chdir(str(p.title))
        else :
            os.mkdir(str(p.title))
            os.chdir(str(p.title))
        for video in p.videos:
            highresvid = video.streams.get_highest_resolution()
            video.register_on_progress_callback(self.Handle_progress_bar_2)
            print(highresvid.filesize_mb)
            highresvid.download()

            # for stream in video.streams.filter(file_extension='mp4'):
            #     # self.video_resolutions.append(stream.resolution)
            #     # self.videos.append(stream)
            #     print(stream.mime_type ,type(stream.resolution))
            #     data = '{} {} {} {}'.format(stream.mime_type, stream.resolution, ", size = ", stream.filesize_mb)
            #     if stream.resolution =='720p':
            #         self.comboBox_2.addItem(data)
            #         continue
            #     elif stream.resolution =='360p':
            #         self.comboBox_2.addItem(data)
            #
        QMessageBox.information(self, "Download completed", "download finished")
        self.progressBar_3.setValue(0)
        self.lineEdit_5.setText("")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
