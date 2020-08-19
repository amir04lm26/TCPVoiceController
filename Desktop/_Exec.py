# -*- coding: utf-8 -*-
#!/usr/bin/env python3
##############$#################
# REVIEW HouseController By Am_H_M
##############$#################
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep
from threading import Thread
from queue import Queue
import speech_recognition as sr
import socket

from main import Ui_MainWindow as MainScreen
from socket import SHUT_RDWR

Connected = 0
SendList = []
Connection_Close = 'Img/connection-off.png'
Connectino_Open = 'Img/connection-on.png'
Fan_Off = 'Img/fan-off.png'
Fan_On = 'Img/fan-on.png'
Lamp_Off = 'Img/lightbulb-off.png'
Lamp_On = 'Img/lightbulb-on.png'
Voice = 'Img/voiceAssistant.gif'

Lamp_VoiceCommands = ['نور', 'لامپ', 'چراغ', 'مهتابی', 'روشنایی']
Lamp_On_VoiceCommands = ['روشن', 'زیاد']
Lamp_Off_VoiceCommands = ['خاموش', 'کم']
Fan_VoiceCommands = ['فن', 'تهویه', 'چیلر', 'کولر', 'باد']
Fan_On_VoiceCommands = ['روشن', 'زیاد']
Fan_Off_VoiceCommands = ['خاموش', 'کم']

# * TCP
TCP_IP = '192.168.1.138'
TCP_PORT = 8085
BUFFER_SIZE = 1024
Connection = 1

mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class MainWindow_Exec():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.Main = QtWidgets.QMainWindow()
        self.MainUI = MainScreen()
        self.MainUI.setupUi(self.Main)
        # SECTION Configuration
        # ? IP Validator
        # Part of the regular expression
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        # Regulare expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange +
                          "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self.MainUI.lineEdit)
        self.MainUI.lineEdit.setValidator(ipValidator)
        # ? Port Validator
        rx = QRegExp('^[1-9]\d{3}$')
        validator = QRegExpValidator(rx)
        self.MainUI.lineEditPort.setValidator(validator)
        # ? Button Def Config
        self.MainUI.pushButton.setStyleSheet(
            """QPushButton{background-color: #00aaff;color: rgb(255, 255, 255); border-radius: 2px; font: 12pt \"B Nazanin\"; padding: 5px;}\n
                 QPushButton:hover{background-color: #9ee35d; border: 1px solid rgb(255, 85, 127);}\n
                 QPushButton:pressed{outline: none;}\n
                 QPushButton:focus{outline: none;}""")
        self.MainUI.clearLog.setStyleSheet(
            """QPushButton{background-color: #FF5733;color: rgb(255, 255, 255); border-radius: 2px; font: 12pt \"Arial\"; padding: 5px;}\n
                 QPushButton:hover{background-color: #CE4212; border: 1px solid rgb(255, 255, 255);}\n
                 QPushButton:pressed{outline: none;}\n
                 QPushButton:focus{outline: none;}""")
        global Connection_Close, Fan_Off, Lamp_Off
        self.MainUI.connection.setScaledContents(True)
        self.MainUI.connection.setPixmap(QPixmap(Connection_Close))
        self.MainUI.lamp.setScaledContents(True)
        self.MainUI.lamp.setPixmap(QPixmap(Lamp_Off))
        self.MainUI.fan.setScaledContents(True)
        self.MainUI.fan.setPixmap(QPixmap(Fan_Off))
        # SECTION Set Connections
        self.MainUI.pushButton.clicked.connect(self.ButtonClicked)
        self.MainUI.clearLog.clicked.connect(
            lambda: self.MainUI.textBrowser.clear())
        # SECTION Show the Screen
        self.Main.show()
        sys.exit(app.exec_())

    def ButtonClicked(self):
        global Connected, Connectino_Open, Connection_Close, Voice, TCP_IP, TCP_PORT
        if Connected == 0:
            TCP_IP = self.MainUI.lineEdit.text()
            print(type(self.MainUI.lineEdit.text()),
                  self.MainUI.lineEdit.text())
            TCP_PORT = int(self.MainUI.lineEditPort.text())
            print(type(self.MainUI.lineEditPort.text()),
                  self.MainUI.lineEditPort.text())
            self.MainUI.pushButton.setText('قطع اتصال')
            self.MainUI.pushButton.setStyleSheet(
                """QPushButton{background-color: #00aaff;color: rgb(255, 255, 255); border-radius: 2px; font: 12pt \"B Nazanin\"; padding: 5px;}\n
                 QPushButton:hover{background-color: #C70039; border: 1px solid #DAF7A6;}\n
                 QPushButton:pressed{outline: none;}\n
                 QPushButton:focus{outline: none;}""")
            # ? Start Voice Thread
            self.VoiceDetectionThread_Start()
            # ? Start Connection Thread
            self.ConnectionThread_Start()
            # ? Set Icons & gif
            movie = QMovie(Voice)
            self.MainUI.voice.setMovie(movie)
            self.MainUI.voice.setScaledContents(True)
            movie.setCacheMode(QMovie.CacheAll)
            movie.start()
            movie.loopCount()
            self.setConsumer(Fan_Off, Lamp_Off)
            Connected = 1
        else:
            self.MainUI.pushButton.setText('اتصال')
            self.MainUI.pushButton.setStyleSheet(
                """QPushButton{background-color: #00aaff;color: rgb(255, 255, 255); border-radius: 2px; font: 12pt \"B Nazanin\"; padding: 5px;}\n
                 QPushButton:hover{background-color: #9ee35d; border: 1px solid rgb(255, 85, 127);}\n
                 QPushButton:pressed{outline: none;}\n
                 QPushButton:focus{outline: none;}""")
            # ? Start Voice Thread
            self.mVoiceDetectionThread.stop()
            # ? Start Connection Thread
            self.mConnectionThread.stop()
            # ? Set Icons & gif
            self.MainUI.voice.setScaledContents(True)
            self.MainUI.voice.setPixmap(QPixmap())
            self.setConsumer(Fan_Off, Lamp_Off)
            Connected = 0

    def txtAdd(self, text):
        self.MainUI.textBrowser.append(
            '<p align="right" style="margin-right:5px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; color:#ffffff;">$ ' + text + '</span></p>')

    def txtFailerAdd(self, text):
        self.MainUI.textBrowser.append(
            '<p align="right" style="margin-right:5px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; color:#DE401D;">$ ' + text + '</span></p>')

    def txtSuccessAdd(self, text):
        self.MainUI.textBrowser.append(
            '<p align="right" style="margin-right:5px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt; color:#12CE42 ;">$ ' + text + '</span></p>')

    def setConsumer(self, fan, lamp):
        self.MainUI.lamp.setPixmap(QPixmap(lamp))
        self.MainUI.fan.setPixmap(QPixmap(fan))

    def VoiceDetectionThread_Start(self):
        self.mVoiceDetectionThread = VoiceDetectionThread(parent=None)
        self.mVoiceDetectionThread.start()
        self.mVoiceDetectionThread.voiceData.connect(
            self.VoiceThreadDataInitilizer)     # REVIEW Recieve the signal

    def ConnectionThread_Start(self):
        self.mConnectionThread = ConnectionThread(parent=None)
        self.mConnectionThread.start()
        self.mConnectionThread.connectionData.connect(
            self.ConnectionThreadDataInitilizer)     # REVIEW Recieve the signal

    def VoiceThreadDataInitilizer(self, data):
        global Lamp_VoiceCommands, Lamp_On_VoiceCommands, Lamp_Off_VoiceCommands, Fan_VoiceCommands, Fan_On_VoiceCommands, Fan_VoiceCommands, SendList
        if data == 'VER':
            self.txtFailerAdd("نمی تونم تشخیص بدم چی گفتید")
        elif data == 'GER':
            self.txtFailerAdd('در تشخیص صدای شما مشکلی به وجود آمده است')
        else:
            self.txtAdd('فکر می کنم گفتید:' + data)
            # SECTION Command Detection
            if any(x in data for x in Lamp_VoiceCommands) and any(x in data for x in Lamp_On_VoiceCommands):
                self.txtSuccessAdd('درخواست شما ارسال شد')
                SendList.append('VCLOVC')
            elif any(x in data for x in Lamp_VoiceCommands) and any(x in data for x in Lamp_Off_VoiceCommands):
                self.txtSuccessAdd('درخواست شما ارسال شد')
                SendList.append('VCLFVC')
            if any(x in data for x in Fan_VoiceCommands) and any(x in data for x in Fan_On_VoiceCommands):
                self.txtSuccessAdd('درخواست شما ارسال شد')
                SendList.append('VCFOVC')
            elif any(x in data for x in Fan_VoiceCommands) and any(x in data for x in Fan_Off_VoiceCommands):
                self.txtSuccessAdd('درخواست شما ارسال شد')
                SendList.append('VCFFVC')

    def ConnectionThreadDataInitilizer(self, data):
        if data == 'connecting':
            self.txtAdd('در حال اتصال به سرور ...')
        elif data == 'connected':
            self.MainUI.connection.setScaledContents(True)
            self.MainUI.connection.setPixmap(QPixmap(Connectino_Open))
            self.txtSuccessAdd('ارتباط برقرار شد')
        elif data == 'disconnected':
            self.MainUI.connection.setScaledContents(True)
            self.MainUI.connection.setPixmap(QPixmap(Connection_Close))
            self.txtFailerAdd('ارتباط قطع شد')
        elif data == 'responceok':
            self.txtSuccessAdd('درخواست شما با موفقیت انجام شد')
        elif data == 'responcefl':
            self.txtFailerAdd('درخواست شما با خطا مواجه شد')
        # TODO State
        elif 'state' in data:
            res = data.find('state')
            if res != -1:
                state = data[res:]
                _lamp = ''
                _fan = ''
                if state[5] == 'O':
                    _lamp = Lamp_On
                # elif state[5] == 'F':
                else:
                    _lamp = Lamp_Off
                if state[6] == 'O':
                    _fan = Fan_On
                # elif state[6] == 'F':
                else:
                    _fan = Fan_Off
                self.setConsumer(_fan, _lamp)


class VoiceDetectionThread(QThread):
    # SECTION Define new Signal
    voiceData = QtCore.pyqtSignal(str)

    # SECTION Initilizer
    def __init__(self, parent=None):
        super(VoiceDetectionThread, self).__init__(parent)

    # SECTION Run thread
    def run(self):
        r = sr.Recognizer()
        audio_queue = Queue()
        while True:
            def recognize_worker():
                # this runs in a background thread
                while True:
                    audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
                    if audio is None:
                        break  # stop processing if the main thread is done

                    # received audio data, now we'll recognize it using Google Speech Recognition
                    try:
                        # for testing purposes, we're just using the default API key
                        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                        # instead of `r.recognize_google(audio)`

                        # print("فکر می کنم گفتید:" +
                        #       r.recognize_google(audio, language="fa-IR"))
                        self.voiceData.emit(
                            r.recognize_google(audio, language="fa-IR"))
                    except sr.UnknownValueError:
                        # print("نمی تونم تشخیص بدم چی گفتید")
                        self.voiceData.emit("VER")
                    except sr.RequestError as e:
                        # print(
                        #     "Could not request results from Google Speech Recognition service; {0}".format(e))
                        #print('در تشخیص صدای شما مشکلی به وجود آمده است')
                        self.voiceData.emit('GER')
                    audio_queue.task_done()  # mark the audio processing job as completed in the queue

            # start a new thread to recognize audio, while this thread focuses on listening
            recognize_thread = Thread(target=recognize_worker)
            recognize_thread.daemon = True
            recognize_thread.start()
            with sr.Microphone() as source:
                try:
                    while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
                        audio_queue.put(r.listen(source))
                except:
                    pass
                # except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
                #     pass

            audio_queue.join()  # block until all current audio processing jobs are done
            audio_queue.put(None)  # tell the recognize_thread to stop
            recognize_thread.join()  # wait for the recognize_thread to actually stop

    # SECTION Stop thread
    def stop(self):
        self.terminate()


class ConnectionThread(QThread):
    # SECTION Define new Signal
    connectionData = QtCore.pyqtSignal(str)

    # SECTION Initilizer
    def __init__(self, parent=None):
        super(ConnectionThread, self).__init__(parent)

    # SECTION Run thread
    def run(self):
        global mSocket
        while True:
            self.connectionData.emit('connecting')
            sleep(1)
            try:
                try:
                    mSocket.connect((TCP_IP, TCP_PORT))
                    mSocket.settimeout(0.1)
                    self.connectionData.emit('connected')
                    data = b''
                    while True:
                        # ? Send Data
                        if len(SendList) != 0:
                            mSocket.send(bytes(SendList[0] + '\r\n', 'utf8'))
                            SendList.remove(SendList[0])
                        # ? Try To Get Data
                        try:
                            data += mSocket.recv(BUFFER_SIZE)
                        except:
                            pass
                        # ? Check Collected Data
                        if (b"\n" in data and b'VC' in data):
                            try:
                                res = data.find(b'VC')
                                if res != -1:
                                    data = data[res:]
                                    accknow = ''
                                    try:
                                        accknow = data[0:6].decode('utf-8')
                                        if (accknow[2] == 'O' or accknow[2] == 'F') and (accknow[3] == 'O' or accknow[3] == 'F'):
                                            self.connectionData.emit(
                                                'state' + accknow[2] + accknow[3])
                                        elif accknow[2] == 'O' and accknow[3] == 'K':
                                            self.connectionData.emit(
                                                'responceok')
                                        elif accknow[2] == 'F' and accknow[3] == 'L':
                                            self.connectionData.emit(
                                                'responcefl')
                                    except:
                                        print('DataType Error.')
                                    data = b''
                            except:
                                pass
                        elif len(data) > BUFFER_SIZE:
                            data = b''
                    mSocket.close()
                    self.connectionData.emit('disconnected')
                except Exception as ex:
                    mSocket.close()
                    print(ex)
            except Exception as ex:
                print(ex)

    # SECTION Stop thread
    def stop(self):
        global mSocket
        try:
            # mSocket.shutdown(SHUT_RDWR)
            # mSocket.close()
            mSocket.shutdown(1)
            mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as ex:
            print(
                'An exception has been occured while trying to close the socket:r\r\n', ex)
        self.terminate()
        self.connectionData.emit('disconnected')


if __name__ == "__main__":
    MainWindow_Exec()
