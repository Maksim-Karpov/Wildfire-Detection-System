from abc import ABC, abstractmethod
#import numpy as np
#from keras.models import load_model
#import tensorflow
import json

#Abstract class for surveilance devices
class SurveilanceDevice(ABC):
    def __init__(self, id, X, Y, battery_charge, marker_color):
        self._device_id = id
        self._coordinate_x = X
        self._coordinate_y = Y
        self._battery_charge = battery_charge
        self._marker_color = marker_color
    
    #@abstractmethod
    def SetCoordinates(self, X, Y):
        self._coordinate_x = X
        self._coordinate_y = Y
    def GetCoordinates(self): #Sending location of any subsequent device
        coordinates = {"X": self._coordinate_x, "Y": self._coordinate_y}
        return coordinates
    def GetMarkerColor(self):
        return self._marker_color
    def SetBatteryCharge(self, charge_level):
        self._battery_charge = charge_level
    def GetBatteryCharge(self):
        return self._battery_charge
    def GetId(self):
        return self._device_id
    
#Temperature sensor class, to handle the temperature data of surrounding environment
class TemperatureSensor(SurveilanceDevice):
    def __init__(self, id, X, Y, battery_charge, marker_color, temperature_data):
        super().__init__(id, X, Y, battery_charge, marker_color)
        self.__current_temperature = temperature_data

    def SetTemperature(self, temperature_data): #Updating tmeperature
        self.__current_temperature = temperature_data

    def GetTemperature(self):
        return self.__current_temperature

#Humidity sensor class to handle surrounding humidity
class HumiditySensor(SurveilanceDevice):
    def __init__(self, id, X, Y, battery_charge, marker_color, humidity_data):
        super().__init__(id, X, Y, battery_charge, marker_color)
        self.__current_humidity=humidity_data
    
    def SetHumidity(self, humidity_data):
        self.__current_humidity = humidity_data
        
    def GetHumidity(self):
        return self.__current_humidity

#Anemometer (wind speed sensor) to handle the wind speed data in the environment
class WindGauge(SurveilanceDevice):
    def __init__(self, id, X, Y, battery_charge, marker_color, wind_speed_data):
        super().__init__(id, X, Y, battery_charge, marker_color)
        self.__current_wind_speed = wind_speed_data
    
    def SetWindSpeed(self, wind_speed_data):
        self.__current_wind_speed = wind_speed_data
        
    def GetWindSpeed(self):
        return self.__current_wind_speed

#UAV class to work with data from drones monitoring the area
class AutonomousDrone(SurveilanceDevice):
    def __init__(self, id,  X, Y, battery_charge, marker_color, status):
        super().__init__(id,  X, Y, battery_charge, marker_color)
        self.__status = status
        
    def GetStatus(self):
        return self.__status

