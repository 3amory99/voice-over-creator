from PyQt5 import uic
import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from app_module import *
from ui_splash_screen import Ui_SplashScreen
from playsound import playsound
import threading
from langdetect import detect

counter = 0

speech_config = SpeechConfig(subscription="06ee11a748eb4523b8ae1dd8739d0023", region="eastus")
# speech_recognition_language="en-US")
languages = {"en": "English",
             "ar": "Arabic",
             "fr": "French",
             "de": "German",
             "es": "Spanish"
             }
lang_Directory = {"en": ["Sara", "Guy", "Amber"],
                  "ar": ["Hamed", "Salma", "Hoda"],
                  "fr": ["Denise", "Henri", "Hortense"],
                  "de": ["Katja", "Hedda", "Conrad"],
                  "es": ["Alvaro", "Helena", "Elvira"]
                  }
lang_codes = {"en": ["en-US-SaraNeural", "en-US-GuyNeural", "en-US-AmberNeural"],
              "ar": ["ar-SA-HamedNeural", "ar-EG-SalmaNeural", "ar-EG-HodaNeural"],
              "fr": ["fr-FR-DeniseNeural", "fr-FR-HenriNeural", "fr-FR-HortenseNeural"],
              "de": ["de-GER-KatjaNeural", "de-GER-HeddaNeural", "de-GER-ConradNeural"],
              "es": ["AlvaroNeural", "HelenaNeural", "ElviraNeural"]
              }


class GUIWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.playBackgroundSound()
        ## PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle('Voice Over Creator')
        UIFunctions.labelTitle(self, 'Voice Over Creator')
        UIFunctions.labelDescription(self, 'New demo version is released, text to speech')
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        self.ui.pushButton.clicked.connect(lambda: self.extract_file())
        self.ui.checkButton.clicked.connect(lambda: self.goVoice(text))

        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "Splash", "btn_home", "url(icons/20x20/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "Home", "btn_widgets", "url(icons/20x20/cil-voice-over-record.png)", True)
        UIFunctions.addNewMenu(self, "Details", "details_wedgit", "url(icons/20x20/cil-newspaper.png)", True)
        UIFunctions.addNewMenu(self, "Exit", "btn_exit", "url(icons/24x24/cil-exit-to-app.png)",
                               False)

        UIFunctions.selectStandardMenu(self, "btn_home")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        UIFunctions.userIcon(self, "OM", "", True)

        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        UIFunctions.uiDefinitions(self)
        self.show()

    def extract_file(self):
        global text
        global langCode

        print("done")
        fileName = QFileDialog.getOpenFileName(self, "Open text file", "/home/jana")
        print(fileName[0])
        # print(self.ui.comboBox_2.currentText())

        if fileName[0]:
            text_array = readInputFile(fileName[0])
            text = self.convert_list_to_string(text_array)
            self.ui.lineEdit.setText(fileName[0])
            self.ui.plainTextEdit.setPlainText(text)
            langCode = detect(self.ui.plainTextEdit.toPlainText())
            print(langCode)
            self.config_inputs(langCode)
        return text

    def config_inputs(self, langCode):
        if langCode is not None:
            self.ui.comboBox.removeItem(0)
            self.ui.comboBox.addItem(languages[langCode])
            for key in languages:
                if key != langCode:
                    self.ui.comboBox.addItem(languages[key])
            voices = lang_Directory[langCode]
            self.ui.comboBox_2.removeItem(0)
            for j in voices:
                self.ui.comboBox_2.addItem(j)

    def convert_list_to_string(self, mix_list, seperator=' '):
        """ Convert list to string, by joining all item in list with given separator.
            Returns the concatenated string """
        return seperator.join([str(elem) for elem in mix_list])

    def playBackgroundSound(self):
        playsound("welcome.mp3")

    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Splash")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE NEW USER
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_exit":
            self.close()

        if btnWidget.objectName() == "details_wedgit":
            self.ui.stackedWidget.setCurrentWidget(self.ui.details_wedgit)
            UIFunctions.resetStyle(self, "details_wedgit")
            UIFunctions.labelPage(self, "Plagiarism Report Details")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            # name = QFileDialog.getOpenFileName(self, 'Open File')
            # print(name)
            # self.image = QtGui.QImage(name[0])

            # self.setValuee(self, self.ui.labelPercentageGPU, self.ui.circularProgressGPU, "rgba(85, 170, 255, 255)", 30)
            # self.setValuee(self, self.ui.labelPercentageRAM, self.ui.circularProgressRAM, "rgba(85, 170, 255, 255)", 70)

    def setValuee(self, labelPercentage, progressBarName, color, sliderValue):

        # GET SLIDER VALUE
        # value = slider.value()

        # CONVERT VALUE TO INT
        # sliderValue = 50

        # HTML TEXT PERCENTAGE
        htmlText = """<p align="center"><span style=" font-size:50pt;">{VALUE}</span><span style=" font-size:40pt; vertical-align:super;">%</span></p>"""
        labelPercentage.setText(htmlText.replace("{VALUE}", str(sliderValue)))

        # CALL DEF progressBarValue
        self.progressBarValue(self, sliderValue, progressBarName, color)

    def progressBarValue(self, value, widget, color):

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
        	border-radius: 110px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} {COLOR});
        }
        """

        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # FIX MAX VALUE
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2).replace("{COLOR}", color)

        # APPLY STYLESHEET WITH NEW VALUES
        widget.setStyleSheet(newStylesheet)

    # def file_action(self):
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())

    ########################################################################

    def resizeEvent(self, event):
        self.resizeFunction()
        return super(GUIWindow, self).resizeEvent(event)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))

    def goVoice(self, text):

        outputVoice = ""
        if langCode is not None:
            voices = lang_codes[langCode]
            for voice in voices:
                print(voice, "--> ", "is selected")
                if voice.__contains__(self.ui.comboBox_2.currentText()):
                    outputVoice = voice
                    break
        try:
            # speech_config.speech_synthesis_voice_name = "ar-EG-ShakirNeural"
            speech_config.speech_synthesis_voice_name = outputVoice
            audio_config = AudioOutputConfig(filename="output.wav")
            synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            # synthesizer.speak_text_async(text)
            # audio_config = AudioOutputConfig(use_default_speaker=True)
            result = synthesizer.speak_text_async(text).get()
            stream = AudioDataStream(result)
            return stream
        except:
            print("error")


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)


        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> MODEL"))
        QtCore.QTimer.singleShot(3000,
                                 lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        global counter

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()
            self.main = GUIWindow()

            playSoundTone = threading.Thread(target=self.playBackgroundSound())
            playSoundTone.start()
            # SHOW MAIN WINDOW

            # with concurrent.futures.ThreadPoolExecutor() as exector:
            #     exector.map(self.goApp(), self.playBackgroundSound())

            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1

    def playBackgroundSound(self):
        playsound("welcome.mp3")

    # def goApp(self):
    #     self.main = GUIWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = SplashScreen()
    sys.exit(app.exec_())
