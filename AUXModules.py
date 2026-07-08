from PyQt6 import QtCore
from PyQt6.QtWidgets import QTableWidgetItem
import numpy as np
import random
import ISClasses

#As imitaion of receiving images froms UAVs, sample images are preloaded
#for demonstarion of the processing via CNN
random_images_arr = [ 
    "overlook_images\\drone3\\dr0003, 24, 30.jpg",
    "overlook_images\\drone4\\dr0004, 26, 34.jpg",
    "overlook_images\\drone4\\dr0004, 43, 40.jpg",
    "overlook_images\\drone2\\dr0002, 30, 35.jpg",
    "overlook_images\\drone1\\dr0001, 12, 24.jpg",
    "overlook_images\\drone1\\dr0001, 15, 20.jpg",
    "overlook_images\\drone1\\dr0001, 17, 21.jpg",
    "overlook_images\\drone1\\dr0001, 39, 40.jpg",
    "overlook_images\\drone2\\dr0002, 21, 12.jpg",
    "overlook_images\\drone2\\dr0002, 25, 12.jpg",
    "overlook_images\\drone2\\dr0002, 26, 14.jpg",
    "overlook_images\\drone3\\dr0003, 45, 8.jpg",
    "overlook_images\\drone3\\dr0003, 24, 34.jpg",
    "overlook_images\\drone4\\dr0004, 37, 19.jpg",
    "overlook_images\\drone4\\dr0004, 7, 14.jpg",
    "overlook_images\\drone4\\dr0004, 39, 47.jpg"
]

#Borders of zones with weather sensors for
#determing the fire hazard in the area where devices are located as a cluster
cluster_zones = [{"zone_1":{"x_min": 10.0, "x_max": 17.5, "y_min": 5.0, "y_max": 14.0, "objects": []}},
                 {"zone_2":{"x_min": 25.0, "x_max": 32.5, "y_min": 5.0, "y_max": 14.0, "objects": []}},
                 {"zone_3":{"x_min": 10.0, "x_max": 17.5, "y_min": 39.5, "y_max": 50.0, "objects": []}},
                 {"zone_4":{"x_min": 26.5, "x_max": 31.5, "y_min": 38.0, "y_max": 50.0, "objects": []}},
                 {"zone_5":{"x_min": 17.5, "x_max": 23.5, "y_min": 23.0, "y_max": 35.5, "objects": []}}]

#Checking which device goes to which cluster
def AssignToCluster(obj_dict_arr):
    try:
        for dict in obj_dict_arr:
            for obj in dict:
                obj_coord = dict[obj].GetCoordinates()
                obj_x = obj_coord["X"]
                obj_y = obj_coord["Y"]
                print(f'Obj coordinates: {obj_x, obj_y}')
                for i in range(len(cluster_zones)):
                    zone = cluster_zones[i]
                    id = "zone_" + str(i+1)
                    print(f'zone coordinates: {zone[id]['x_min']} -> {zone[id]['x_max']} {zone[id]['y_min']} -> {zone[id]['y_max']}')
                    #print(zone[id])
                    #print(zone[id]["x_max"])
                    if (obj_x >= zone[id]["x_min"] and obj_x <= zone[id]["x_max"] 
                        and obj_y >= zone[id]["y_min"] and obj_y <= zone[id]["y_max"]):
                        print("Object in zone: ", id)
                        zone[id]["objects"].append(dict[obj])
        return cluster_zones
    
    except Exception as e:
        print("Exception when assigning to clusters:", e)
        
#Imitation of getting the data as well image from the UAV drone
def GiveRandomSignal(random_images_arr):
    rng = np.random.default_rng()
    rand_img_ind = rng.integers(low=0, high=len(random_images_arr), size=1)
    #print("Index:", rand_img_ind)
    filepath = random_images_arr[rand_img_ind[0]]
    #print("FilePath: ", filepath)
    subset = filepath.split('\\')
    location = subset[-1]
    tmp_str = location.replace(" ", "").replace(".jpg","").split(',')
    #print("TMP", tmp_str)
    detect_loc = {"drone": str(tmp_str[0]), 'X': float(tmp_str[1]), 'Y': float(tmp_str[2])}
    #print("Location: ", detect_loc)

    return filepath, detect_loc

#Adjusting the UI tables
def AdjustTableHeaders(table):
    if table.objectName() == "threats_table":
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        table.setColumnWidth(0, 90)
        table.setColumnWidth(1, 90)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 150)
        table.setColumnWidth(4, 150)
        table.setColumnWidth(5, 150)
        table.setColumnWidth(6, 220)
    elif table.objectName() == "detections_table":
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 50)
        table.setColumnWidth(2, 50)
        table.setColumnWidth(3, 200)
    else:
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        table.setColumnWidth(0, 90)
        table.setColumnWidth(1, 70)
        table.setColumnWidth(2, 70)
        table.setColumnWidth(3, 80)
        table.setColumnWidth(4, 70)

#Adding the data from class samples to the UI table
def AddToTable(table, dictionary, type, flag):
    if flag == "init":
        for key in dictionary:
            obj = dictionary[key]
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(obj.GetId())))
            table.setItem(row_position, 1, QTableWidgetItem(str(obj.GetCoordinates()["X"])))
            table.setItem(row_position, 2, QTableWidgetItem(str(obj.GetCoordinates()["Y"])))
            #Drawing points on the map on app startup
            #main_interface.ax.scatter(obj.GetCoordinates()["X"], obj.GetCoordinates()["Y"], color=obj.GetMarkerColor())
            if type == "thermal":
                table.setItem(row_position, 3, QTableWidgetItem(str(obj.GetTemperature())))
            elif type == "humid":
                table.setItem(row_position, 3, QTableWidgetItem(str(obj.GetHumidity())))
            elif type == "wind":
                table.setItem(row_position, 3, QTableWidgetItem(str(obj.GetWindSpeed())))
            elif type == "drone":
                table.setItem(row_position, 3, QTableWidgetItem(str(obj.GetStatus())))
            table.setItem(row_position, 4, QTableWidgetItem(str(obj.GetBatteryCharge())))
    elif flag == "update":
        row = 0
        for key in dictionary:
            obj = dictionary[key]
            table.item(row, 1).setText(str(obj.GetCoordinates()['X']))
            table.item(row, 2).setText(str(obj.GetCoordinates()['Y']))
            table.item(row, 4).setText(str(obj.GetBatteryCharge()))
            if type == "thermal":
                table.setItem(row, 3, QTableWidgetItem(str(obj.GetTemperature())))
            elif type == "humid":
                table.setItem(row, 3, QTableWidgetItem(str(obj.GetHumidity())))
            elif type == "wind":
                table.setItem(row, 3, QTableWidgetItem(str(obj.GetWindSpeed())))
            elif type == "drone":
                table.setItem(row, 3, QTableWidgetItem(str(obj.GetStatus())))
            row += 1
    
#Drawing points on the map on updates
def DrawPoints(table, obj_dict, interface):
    rows_number = table.rowCount()
    if rows_number == 0:
        print("The table is empty")
        pass
    else:
        for i in range(rows_number):
            object_id = table.item(i, 0).text()
            marker_color = obj_dict[object_id].GetMarkerColor()
            coordinates = obj_dict[object_id].GetCoordinates()
            interface.ax.scatter(coordinates["X"], coordinates["Y"], color=marker_color)

#Imitating the decrease of device battery charge with time to imitate the real-time updates
def SubstractBattery(dict, obj, battery_subs):
    diff = dict[obj].GetBatteryCharge()-battery_subs
    if diff <= 0:
        dict[obj].SetBatteryCharge(0)
    else:
        dict[obj].SetBatteryCharge(dict[obj].GetBatteryCharge()-battery_subs)

#Updating the data of all devices to imitate the work of system in realtime upon "receiving the signal"
def UpdateAllData(dr_dict, therm_dict, humid_dict, wind_dict):
    drone_positions = [{"dr0001":[{"X":28.0, "Y":18.5},{"X":26.5, "Y":41.0},{"X":16.6, "Y":33.5}]},
                       {"dr0002":[{"X":25.5, "Y":26.0},{"X":22.0, "Y":12.5},{"X":11.5, "Y":24.5}]},
                       {"dr0003":[{"X":13.0, "Y":47.0},{"X":22.0, "Y":46.0},{"X":34.0, "Y":45.5}]},
                       {"dr0004":[{"X":31.5, "Y":9.5},{"X":33.0, "Y":11.0},{"X":33.5, "Y":38.0}]}]
    #Random data generation
    rng = np.random.default_rng()
    temperature_data = rng.integers(low=10, high=31, size=7)
    humidity_data = rng.integers(low=20, high=80, size=7)
    wind_speed_data = rng.integers(low=3, high=20, size=7)
    
    #Drone location update
    #rand_index = random.randint(0, 6)
    counter = 0
    for dr_obj in dr_dict:
        print("Input object: ", dr_dict[dr_obj])
        dr_position_arr = drone_positions[counter]
        #print(dr_position_arr)
        counter+=1
        positions_arr = dr_position_arr[dr_obj]
        #print(positions_arr)
        set_position = positions_arr[random.randint(0, 2)]
        dr_dict[dr_obj].SetCoordinates(set_position['X'], set_position['Y'])
        print("coordinates set")
        print("Current coord: ", dr_dict[dr_obj].GetCoordinates())
        print("Obj battery: ", dr_dict[dr_obj].GetBatteryCharge())
        SubstractBattery(dr_dict, dr_obj, random.randint(1, 3)) #ТУТ ОШИБКА !!!
        print(f'drone {dr_obj} updated')
    #Temperature data update
    for th_sens in therm_dict:
        therm_dict[th_sens].SetTemperature(temperature_data[random.randint(0, 6)])
        SubstractBattery(therm_dict, th_sens, random.randint(1, 3))
    #Humidity data update
    for hm_sens in humid_dict:
        humid_dict[hm_sens].SetHumidity(humidity_data[random.randint(0, 6)])
        SubstractBattery(humid_dict, hm_sens, random.randint(1, 3))
    #Wind speed data update
    for ws_sens in wind_dict:
        wind_dict[ws_sens].SetWindSpeed(wind_speed_data[random.randint(0, 6)])
        SubstractBattery(wind_dict, ws_sens, random.randint(1, 3))
