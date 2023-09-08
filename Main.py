from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

import requests
import time
import json
import Res_rc
import copy
import pyqtgraph as pg
#import matplotlib.pyplot as plt
#import sys

colors = {}
last_clicked_label = None
plotLen = 20
valArr = [20] * plotLen
plot = None

def led1 (checked):
    if checked:
        form.pushButton_2.setText("Выкл")
        print("I'm worked too much")
        form.label_24.hide()
        form.label_20.show()          
    else:
        form.label_20.hide()
        form.label_24.show()
        form.pushButton_2.setText("Вкл")
        print ("I'm worked too")

def led2 (checked):
    if checked:
        form.pushButton_3.setText("Выкл")
        print("I'm worked too much")
        form.label_27.hide()
        form.label_26.show()       
    else:
        form.label_26.hide()
        form.label_27.show()
        form.pushButton_3.setText("Вкл")
        print ("I'm worked too")

def led3 (checked):
    if checked:
        form.pushButton_4.setText("Выкл")
        print("I'm worked too much")
        form.label_31.hide()
        form.label_29.show()
        #state =  form.label_24.isVisible() 
                  
    else:
        form.label_29.hide()
        form.label_31.show()
        form.pushButton_4.setText("Вкл")
        print ("I'm worked too")

        
def updateLCD():
    global temp 
    form.lcdNumber.display(temp) 

def sed ():
    print ("I'm worked!")
  
led_data = {
    "leds1": {"red": 0, "green": 0, "blue": 0},
    "leds2": {"red": 0, "green": 0, "blue": 0},
    "leds3": {"red": 0, "green": 0, "blue": 0},
    "leds4": {"red": 0, "green": 0, "blue": 0},
    "leds5": {"red": 0, "green": 0, "blue": 0},
    "leds6": {"red": 0, "green": 0, "blue": 0},
    "leds7": {"red": 0, "green": 0, "blue": 0},
    "leds8": {"red": 0, "green": 0, "blue": 0},
}

def vkl():
     for led in form.leds:
            #caution! Naming will be the same for a Led and JSON led objects
            led.setStyleSheet(f"background-color: yellow;")
            led_data[led.objectName()]["red"] = 255
            led_data[led.objectName()]["green"] = 255
            led_data[led.objectName()]["blue"] = 0

def vikl():
        for led in form.leds:
            #caution! Naming will be the same for a Led and JSON led objects
            led.setStyleSheet(f"background-color: black;")
            led_data[led.objectName()]["red"] = 0
            led_data[led.objectName()]["green"] = 0
            led_data[led.objectName()]["blue"] = 0

def color():
        color = QColorDialog.getColor()
        if color.isValid():
            palette = QPalette()
            palette.setColor(QPalette.Button, color)
            form.color_b.setPalette(palette)
            for led in form.leds:
                led.setStyleSheet(f"background-color: {color.name()};")
                led_data[led.objectName()]["red"] = color.red()
                led_data[led.objectName()]["green"] = color.green()
                led_data[led.objectName()]["blue"] = color.blue()

def led_clicked(event):
       colors = led.palette().color(QPalette.Background)
       sender= QApplication.widgetAt(event.globalPos()) #QApplication.widgetAt() для получения текущего виджета, на котором было совершено действие
       color = QColorDialog.getColor()
       if color.isValid():
               #caution! Naming will be the same for a Led and JSON led objects
              sender.setStyleSheet(f"background-color: {color.name()};")
              led_data[sender.objectName()]["red"] = color.red()
              led_data[sender.objectName()]["green"] = color.green()
              led_data[sender.objectName()]["blue"] = color.blue()
       else:
             form.leds.setStyleSheet(" ")
    
def sendMessage():
    url = form.lineEdit.text()
    labels_dict = {}
    labels_dict["LED1"] = form.label_20.isVisible()
    labels_dict["LED2"] = form.label_26.isVisible()
    labels_dict["LED3"] = form.label_29.isVisible()

    json_data = {}
    json_data.update(led_data)
    json_data.update(labels_dict)
    json_str = json.dumps(json_data, separators=(',', ':'))
    
    data_str = 'Я отправляю текст на: ' + url + '\n'+ json_str
    form.textEdit.setPlainText(data_str)
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #заголовки запроса
    response = requests.post(url, json=json_data, headers=headers) #отправка POST запроса

    # обрабатываем ответ и выводим его в поле вывода
    if response.status_code == 200:
        form.textEdit.append('О, все прошло успешно!\n') #выводим значение в line_edit
    else:
        form.textEdit.append('Ошибка при получении данных')



def getValueFromMacket():
    url = form.lineEdit_2.text()
    response = requests.get(url) #отправка POST запроса

    # обрабатываем ответ и выводим его в поле вывода
    if response.status_code == 200:
        data=response.json() #функция преобразования данных в объект питон
        #Parse the date
        form.textEdit.append(json.dumps(data)) #выводим значение в line_edit
        form.textEdit.append(str(data["temperature"]))
        
        bs = list()
        bs.append(data["button1State"])
        bs.append(data["button2State"])
        bs.append(data["button3State"])
        update_button(bs)

        update_pressure(data["pressure"])
        
        form.lcdNumber_7.display(data["ambient_light"])
        form.lcdNumber_2.display (data["red_light"])
        form.lcdNumber_3.display (data["green_light"])
        form.lcdNumber_4.display (data["blue_light"])
        form.lcdNumber_8.display (data["lightness"])
        
        form.lcdNumber_5.display(data['acceleration_x'])
        form.lcdNumber_9.display (data['acceleration_y'])
        form.lcdNumber_6.display (data['acceleration_z'])

        led1(data['LED1'])
        led2(data['LED2'])
        led3(data['LED3'])
        valArr.pop(0)
        valArr.append(data["temperature"])
        print(valArr)
        UpdatePlot(plot, valArr)
    else:
        form.textEdit.append('Ошибка при получении данных')


#json.load(file) @ACHT! Method to convert Str to JSON


def update_pressure(p):
    form.lcd_pressure.display(p)

def update_button (bs):
    for i in range(1, 4):
         button_state = bs[i-1]
         if button_state == 'True':
             getattr(form, f'on_{i}').show()
             getattr(form, f'off_{i}').hide()
         else:
             getattr(form, f'on_{i}').hide()
             getattr(form, f'off_{i}').show()


def UpdatePlot(plot, val):
    x = list(range(1, len(valArr)+1))
    bargraph = pg.BarGraphItem(x = x, height = val, width = 0.6, brush ='g')
    plot.clear()
    plot.addItem(bargraph)
    
def Plots(form, valArr):
    widget = QWidget()
    plot = pg.plot() #создает объект PlotWidget из библиотеки PyqtGraph
    
    x = list(range(1, len(valArr)+1))
    bargraph = pg.BarGraphItem(x = x, height = valArr, width = 0.6, brush ='g')
    plot.addItem(bargraph)
    
    # Creating a grid layout
    layout = QGridLayout()
    layout.addWidget(plot, 0,0)
    form.plotwidget.setLayout(layout)

    return plot
    

if __name__ == "__main__":
    # Opening JSON file
    f = open('config.json') #открывает файл 'config.json', загружает его содержимое в переменную 'conf' в формате словаря (dictionary) при помощи функции 'json.load()', а затем выводит все ключи словаря 'conf' при помощи цикла 'for'.
    conf = json.load(open('config.json'))
    f.close()

    print("Find an arguments:")
    for i in conf:
        print(i)
        
    import sys

    Form, Window = uic.loadUiType(conf['uiPath'] + conf['uiFileName'])

    app = QApplication(sys.argv)# Создаем экземпляр QApplication и передаем параметры командной строки 
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show() # Окна скрыты по умолчанию!
    window.setWindowTitle('Lr4')  #nazvanie
    form.pushButton.clicked.connect(sendMessage) #привязываем функцию к кнопке Отправить
    form.lineEdit.setText("http://" + conf['defaultMDNSname'] + conf['defaultPostRoute'])
    form.lineEdit_2.setText("http://" + conf['defaultMDNSname'] + conf['defaultGetRoute'])
    form.pushButton_5.clicked.connect(getValueFromMacket) #привязываем функцию к кнопке Отправить GET запрос
    

    form.pushButton_2.setCheckable(True) #вкл режим перекл
    form.pushButton_2.setChecked(False) #нач значение
    form.label_20.hide()
    form.pushButton_2.toggled["bool"].connect(led1)

    form.pushButton_3.setCheckable(True) #вкл режим перекл
    form.pushButton_3.setChecked(False) #нач значение
    form.label_26.hide()
    form.pushButton_3.toggled["bool"].connect(led2)

    form.pushButton_4.setCheckable(True) #вкл режим перекл
    form.pushButton_4.setChecked(False) #нач значение
    form.label_29.hide()
    form.pushButton_4.toggled["bool"].connect(led3)
    
    form.on_1.hide()
    form.on_2.hide()
    form.on_3.hide()

    form.lcdNumber.display(45)

    
    form.leds = [form.leds1, form.leds2, form.leds3, form.leds4, form.leds5, form.leds6, form.leds7, form.leds8]


    for led in form.leds:
            led.mousePressEvent = led_clicked
        
    timer = QTimer()
    timer.setInterval(1000)

    #Connect the timer to the update_pressure function
    #TODO connect to getSensValue from macket
    #timer.timeout.connect(update_pressure)
    #timer.timeout.connect (update_button)
    #timer.timeout.connect (update_light)
    #timer.timeout.connect (update_acceleration)

    timer.start()

    form.vkl_b.clicked.connect(vkl)
    form.vikl_b.clicked.connect(vikl)
    form.color_b.clicked.connect(color)
    
    plot = Plots(form, valArr)
    
    sys.exit (app.exec_()) # Запуск цикла событий
