from ISClasses import SurveilanceDevice, WindGauge, AutonomousDrone, TemperatureSensor, HumiditySensor
import json

def LoadObjects(file_path):
    objects_arr = []
    with open(file_path) as f:
        objects_arr = json.load(f)
    return objects_arr

drone_js_arr = LoadObjects("surveilance_devices\\drone_objects.json")
humid_js_arr = LoadObjects("surveilance_devices\\humid_sensors.json")
temp_js_arr = LoadObjects("surveilance_devices\\thermal_sensors.json")
wind_js_arr = LoadObjects("surveilance_devices\\wind_sensors.json")

def CreateSamples():
    #--------------Adding UAVs-------------------------
    drones_dict = {}
    for i in drone_js_arr:
        tmp_obj = AutonomousDrone(id=i["device_id"],
                                X=i["location_x"],
                                Y=i["location_y"],
                                battery_charge=i["battery_charge"],
                                marker_color=i["marker_color"],
                                status=i["status"])
        drones_dict[tmp_obj._device_id] = tmp_obj
    #for debug
    #print(drones_dict["dr0001"].GetStatus())

    #-------------Adding thermometers-------------
    temperature_dict = {}
    for i in temp_js_arr:
        tmp_obj = TemperatureSensor(id=i["device_id"],
                                X=i["location_x"],
                                Y=i["location_y"],
                                battery_charge=i["battery_charge"],
                                marker_color=i["marker_color"],
                                temperature_data=i["temperature"])
        temperature_dict[tmp_obj._device_id] = tmp_obj
    #debug
    #print(temperature_dict["th0002"].GetTemperature())

    #-------------Adding gigrometers (humidity)------------------
    humid_dict = {}
    for i in humid_js_arr:
        tmp_obj = HumiditySensor(id=i["device_id"],
                                X=i["location_x"],
                                Y=i["location_y"],
                                battery_charge=i["battery_charge"],
                                marker_color=i["marker_color"],
                                humidity_data=i["humidity"])
        humid_dict[tmp_obj._device_id] = tmp_obj
    #debug
    #print(humid_dict["hm0003"].GetMarkerColor())

    #-------------Adding anemometers (wind gauge)----------------
    wind_dict = {}
    for i in wind_js_arr:
        tmp_obj = WindGauge(id=i["device_id"],
                                X=i["location_x"],
                                Y=i["location_y"],
                                battery_charge=i["battery_charge"],
                                marker_color=i["marker_color"],
                                wind_speed_data=i["wind_speed"])
        wind_dict[tmp_obj._device_id] = tmp_obj
    #debug
    #print(wind_dict["wn0005"].GetCoordinates()['X'])
    
    return drones_dict, temperature_dict, humid_dict, wind_dict
