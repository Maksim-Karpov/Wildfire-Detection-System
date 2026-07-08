#loading models related packages
import tensorflow

#User created modules
import LoadAIModels
import ISClasses
from ComposeClasses import CreateSamples
from AUXModules import (AdjustTableHeaders,
                         AddToTable,
                           DrawPoints,
                             UpdateAllData,
                               GiveRandomSignal,
                                 AssignToCluster,
                                   random_images_arr)

#loading interface Qt related stuff
from PyQt6 import QtWidgets, QtGui, QtMultimedia
from PyQt6.QtWidgets import ( 
    QMessageBox, QApplication, QVBoxLayout,
    QTableWidget, QHBoxLayout, QFileDialog,
    QTableWidgetItem
    )
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, pyqtSignal, QObject

#Importing elements to draw the map
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import sys
from pynput import keyboard
from datetime import datetime
import json
import numpy as np
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

#Not the best solution but as temporary
image_preview_path = ""
info_label = ""

#System class for button input handling (doesn't work)
class BridgeInput(QObject):
    key_pressed = pyqtSignal(str)

#+++++++++Creating windows for the system+++++++++++
#login & password input
class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui_windows\\LoginWindow.ui", self)
        self.setWindowTitle("Authorization window")
        self.enterbutton.clicked.connect(self.GoToMainWindow)
        self.exitbutton.clicked.connect(self.ExitSystem)
        self.setMinimumSize(850, 350)
        #self.width = 850
        #self.height = 350

    def GoToMainWindow(self):
        #for debug
        #self.loginedit.setText("testuser")
        #self.passwordedit.setText("testp4ssword")

        if self.loginedit.text() == "testuser" and self.passwordedit.text() == "testpassword":
            widgets_pack.setCurrentIndex(widgets_pack.currentIndex()+1)
        elif self.loginedit.text() != "testuser":
            QMessageBox.question(self, 'Security alert',
                                  "Incorrect login or password!")
            self.loginedit.setText("")
        elif self.passwordedit.text() != "testpassword":
            QMessageBox.question(self, 'Security alert', 
                                 "Incorrect login or password!")
            self.passwordedit.setText("")
    def ExitSystem(self):
        widgets_pack.close()

#Main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui_windows\\MainWindow.ui", self)
        self.setWindowTitle("Main Form")
        #windows size
        self.setMinimumSize(850, 350)
        #Main form creation and setting
        self.canvas = FigureCanvasQTAgg(Figure(figsize=(15, 15), layout="constrained"))
        self.canvas.figure.tight_layout(pad=0.0)
        self.map_image = plt.imread("ui_windows\\SupervisedRegion.png")
        self.ax = self.canvas.figure.add_subplot()
        self.img_area = [10, 35, 5, 50] #xmin-max, ymin-max
        self.ax.imshow(self.map_image, extent=self.img_area, aspect="auto", zorder=-1)
        self.ax.set_xticks(np.arange(10, 35, 1.5))
        self.ax.set_yticks(np.arange(5, 51, 1.5))
        self.ax.tick_params(labelsize=7)
        self.ax.grid(visible=True, color='white',zorder=1, alpha=0.5)
        plt.show()

        #Preparing the canvas for Qt display
        layout = QVBoxLayout(self.map_area)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.map_area.setContentsMargins(0,0,0,0)
        layout.addWidget(self.canvas)

        #Setting up the width and height for the table
        #Thermometer
        AdjustTableHeaders(self.therm_sens_table)
        #Gigrometer
        AdjustTableHeaders(self.humid_sens_table)
        #Anemometer
        AdjustTableHeaders(self.wind_sens_table)
        #UAV
        AdjustTableHeaders(self.drone_table)
        #Threats
        AdjustTableHeaders(self.threats_table)
        #ImageDetection
        AdjustTableHeaders(self.detections_table)

        #++++++++Adding Initialazation Data++++++
        #++++++++++++Addong monitoring devices+++++++++
        self.drones_dict, self.temperature_dict, self.humid_dict, self.wind_dict = CreateSamples()
        #print("DATA: ", self.drones_dict, self.temperature_dict, self.humid_dict, self.wind_dict)
        #++++++++++++++Loading starting data to the table++++++++++++++++
        AddToTable(self.therm_sens_table, self.temperature_dict, "thermal", "init")
        AddToTable(self.humid_sens_table, self.humid_dict, "humid", "init")
        AddToTable(self.wind_sens_table, self.wind_dict, "wind", "init")
        AddToTable(self.drone_table, self.drones_dict, "drone", "init")

        #Initial drawing of points on the map
        DrawPoints(self.therm_sens_table, self.temperature_dict, self)
        DrawPoints(self.humid_sens_table, self.humid_dict, self)
        DrawPoints(self.wind_sens_table, self.wind_dict, self)
        DrawPoints(self.drone_table, self.drones_dict, self)

        #++++++++++++Loading AI models+++++++++++++
        try:
            self.status, self.weather_parameter_model, self.image_classification_model = LoadAIModels.LoadModels()
            if self.status == False:
                print("Models successfully loaded!")
            else:
                print("Failed to lood models or other problem occured")
        except Exception as e:
            print("Unexpected error occured when loading the model!", e)
        #++++++++++++Loading AI models+++++++++++++

        #----------Buttong handling---------
        self.mainexitbutton.clicked.connect(self.ExitMain)
        #!!!!! Was done to imitate the receival of the signal from the external device in the network !!!!!
        #!!!!! Since no devices are available, the imitation was done via small menu with buttons !!!!!!!!
        self.update_data_btn.clicked.connect(self.UpdateData)
        self.check_detections_btn.clicked.connect(self.CheckDetections)

    def CheckDetections(self):
        _, _ = QFileDialog.getOpenFileName(self, "File browsing", "overlook_images", filter="Images (*.jpg *.png)")

    def ExitMain(self):
        widgets_pack.setCurrentIndex(widgets_pack.currentIndex()-1)
    
    def UpdateData(self):
        #CNN model image handling
        if self.check_image_rad.isChecked():
            #IMITATION of system receiving an image from UAV
            print("\nImage Classification Model")
            input_image_path, detection_loc = GiveRandomSignal(random_images_arr)
            print("Received Signal !")
            probability, predicted_class, self.image = LoadAIModels.FireImagePredict(self.image_classification_model, input_image_path)
            print(f'{format(probability[0][0], '.3f')}, {predicted_class[0][0]}')
            #----Adding to table--------  0 - is fire
            if predicted_class == 0: #Model detected a fire
                row_position = self.detections_table.rowCount()
                self.detections_table.insertRow(row_position)
                det_id = "00"+str(row_position)
                self.detections_table.setItem(row_position, 0, QTableWidgetItem(det_id))
                self.detections_table.setItem(row_position, 1, QTableWidgetItem(str(detection_loc['X'])))
                self.detections_table.setItem(row_position, 2, QTableWidgetItem(str(detection_loc['Y'])))
                self.detections_table.setItem(row_position, 3, QTableWidgetItem(input_image_path))

                #Saving detections to logs
                try:
                    t = time.localtime()
                    curr_time = time.strftime("%d_%m_%Y %H-%M-%S", t)
                    report = {"Position Occured": detection_loc, "Date": curr_time, "Storage": input_image_path}
                    #json_report = json.dumps(report)
                    filename = "(" + curr_time + ")" + ".json"
                    print(filename)
                    folder = Path("reports")
                    with open(folder / filename, "w", encoding='utf-8') as file:
                        json.dump(report, file)

                except Exception as e:
                    print("Error when saving report", e)

                global image_preview_path
                image_preview_path = input_image_path
                global info_label
                info_label = detection_loc
                print("Opening in new window")
                image_view.ChangeImage(image_preview_path, info_label)
                widgets_pack.setCurrentIndex(widgets_pack.currentIndex()+1)
            
        #Handling the weather data via secondary FNN model
        elif self.check_cluster_rad.isChecked():
            print("Weather Decision Model")
            clust_objects_arr = [self.temperature_dict, self.humid_dict, self.wind_dict]
            cluster_zones = AssignToCluster(clust_objects_arr)
            print(cluster_zones)
            #CollectData(cluster_zones)
            try:
                for i in range(len(cluster_zones)):
                    arr = [0,0,0]
                    zone = cluster_zones[i]
                    id = "zone_" + str(i+1)
                    obj_arr = zone[id]["objects"]
                    for obj in obj_arr:
                        #print(type(obj))
                        if isinstance(obj, ISClasses.TemperatureSensor):
                            #print(obj.GetTemperature())
                            arr[1] = obj.GetTemperature()
                        elif isinstance(obj, ISClasses.HumiditySensor):
                            arr[0] = obj.GetHumidity()
                        elif isinstance(obj, ISClasses.WindGauge):
                            arr[2] = obj.GetWindSpeed()
                        else:
                            print("couldn't find data")
                        print("Collected data:", arr)
                    input_arr = np.array([arr], dtype=np.float32)    
                    probability, predicted_class = LoadAIModels.FireWeatherPredict(self.weather_parameter_model, input_arr)
                    print(f'{format(probability[0][0], '.3f')}, {predicted_class[0][0]}')
                    # For this FNN model 1 - is a fire class
                    if predicted_class == 1:
                        print("Fire risk is possible")
                        row_position = self.threats_table.rowCount()
                        self.threats_table.insertRow(row_position)
                        thr_id = "00"+str(row_position)
                        print(zone[id]["x_min"])
                        self.threats_table.setItem(row_position, 0, QTableWidgetItem(thr_id))
                        self.threats_table.setItem(row_position, 2, QTableWidgetItem(str(zone[id]["x_min"])))
                        self.threats_table.setItem(row_position, 3, QTableWidgetItem(str(zone[id]["x_max"])))
                        self.threats_table.setItem(row_position, 4, QTableWidgetItem(str(zone[id]["y_min"])))
                        self.threats_table.setItem(row_position, 5, QTableWidgetItem(str(zone[id]["y_max"])))
                        print("reached here")
                        self.threats_table.setItem(row_position, 6, QTableWidgetItem(str(f'{arr[0]}C, {arr[1]}%, {arr[2]} км/ч')))
                        diff = abs(predicted_class - probability)
                        if diff <= 0.1:
                            probability = "Extremely high risk"
                        elif diff >= 0.1 and diff <= 0.3:
                            probability = "High risk"
                        elif diff >= 0.3 and diff <= 0.5:
                            probability = "Fire risk"
                        else:
                            probability = "Potential fire risk"
                        print(probability)
                        self.threats_table.setItem(row_position, 1, QTableWidgetItem(probability))
            except Exception as e:
                print("Error occured when adding to table:", e)       
        #Updating the UAV positions and parameters for the surveilance devices
        elif self.update_all_data_rad.isChecked():
            print("Update Data Chosen")
            #Updating the data
            UpdateAllData(self.drones_dict, self.temperature_dict, self.humid_dict, self.wind_dict)
            print("Classes updated")
            #Updating the tables
            print("Updating tables")
            AddToTable(self.therm_sens_table, self.temperature_dict, "thermal", "update")
            AddToTable(self.humid_sens_table, self.humid_dict, "humid", "update")
            AddToTable(self.wind_sens_table, self.wind_dict, "wind", "update")
            AddToTable(self.drone_table, self.drones_dict, "drone", "update")
            #Updating points of the map
            print("After updated data, to draw points, chack if values changed !")
            plt.clf()
            self.ax.clear()
            self.ax.imshow(self.map_image, extent=self.img_area, aspect="auto", zorder=-1)
            self.ax.set_xticks(np.arange(10, 35, 1.5))
            self.ax.set_yticks(np.arange(5, 51, 1.5))
            self.ax.tick_params(labelsize=7)
            self.ax.grid(visible=True, color='white',zorder=1, alpha=0.5)
            DrawPoints(self.therm_sens_table, self.temperature_dict, self)
            DrawPoints(self.humid_sens_table, self.humid_dict, self)
            DrawPoints(self.wind_sens_table, self.wind_dict, self)
            DrawPoints(self.drone_table, self.drones_dict, self)
            self.canvas.draw_idle()            

class ImageViewWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print("Inside window viewer")
        loadUi("ui_windows\\ImageView.ui", self)
        self.setWindowTitle("Image view")
        self.resize(650, 450)
        self.setMinimumSize(450, 450)
        self.back_btn.clicked.connect(self.GoBack)
        print("Loading image")
        print("Image loaded")

    def ChangeImage(self, image_path, info):
        pixmap = QPixmap(image_path)
        #self.image_frame = plt.imread(image_path)
        self.image_frame.setPixmap(pixmap)
        self.info_label.setText(str(info))

    def GoBack(self):
        widgets_pack.setCurrentIndex(widgets_pack.currentIndex()-1)

if __name__ == "__main__":        
    #Adding objects on startup
    fire_detection_programm = QApplication(sys.argv)
    widgets_pack = QtWidgets.QStackedWidget()
    login_form = LoginWindow()
    main_interface = MainWindow()
    image_view = ImageViewWindow()

    #adding widgets to a pack for navigation
    widgets_pack.addWidget(login_form) #1
    widgets_pack.addWidget(main_interface) #2
    widgets_pack.addWidget(image_view)
    #Displaying UI to user
    widgets_pack.show()
        
    try:        
        #Exitying the program handling
        print("Starting the program")
        sys.exit(fire_detection_programm.exec())
    except:
        print("Exiting Programm")