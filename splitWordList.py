#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import platform
import sys
import subprocess

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Word List Splitter'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 240

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label1 = QLabel(self)
        label1.setText('Enter number of words (integer)')
        label1.move(80, 40)
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(360, 40)
        self.textbox1.resize(150, 40)
        self.textbox1.setText('10')

        label2 = QLabel(self)
        label2.setText("Enter delimiter(\',\' or \';\' or \'|\', etc.)")
        label2.move(80, 100)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(360, 100)
        self.textbox2.resize(150, 40)
        self.textbox2.setText(',')

        button = QPushButton('Select Word List', self)
        button.setToolTip('Select the long list you want to split')
        button.resize(150, 40)
        button.move(240, 160)
        button.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Select a word list...', 'All Files (*);;Comma-separated Values(*.csv)', options=options)
        if filename:
            self.popUp_confirmation(filename)

    def popUp_confirmation(self, filename):
        buttonReply = QMessageBox.question(
            self, 'Confirmation', 'Split ' + filename + '?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            numOfWords = int(self.textbox1.text())
            delimiter = self.textbox2.text()
            res = split_list(filename, 'group', numOfWords, delimiter)
            if res:
                QMessageBox.about(
                    self, 'Splitted!', 'Splitted files are saved in group folder under current directory.')
                open_dir('group')
            else:
                QMessageBox.about(
                    self, 'Failure!', 'Either word list cannot be loaded or wrong settings, please try again.')


# Read a word list, remove NaN and flatten to a 1D list
def split_list(csvfile, savepath, numOfWords, delimiter):
    print(numOfWords)
    try:
        df = pd.read_csv(csvfile, delimiter=delimiter)
        words = df.values.ravel()
        wordList = [word for word in words if str(word) != 'nan']

        # Shuffle the list
        totalWords = len(wordList)
        randomInd = np.arange(totalWords, dtype=int)
        np.random.shuffle(randomInd)

        # Split into small lists
        if not os.path.isdir(savepath):
            os.mkdir(savepath)
        for i in range(totalWords // numOfWords):
            ind = randomInd[i * numOfWords:(i+1) * numOfWords]
            selectedWord = [wordList[i].lower() for i in ind]
            writeWords = '\n'.join(selectedWord)
            f = open(savepath + '/wordList' + str(i) + '.txt', 'w')
            f.write(writeWords)
            f.close()

        return True
    except:
        return False


def open_dir(path):
    if platform.system() == "Windows":
        subprocess.Popen(["explorer", path])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
