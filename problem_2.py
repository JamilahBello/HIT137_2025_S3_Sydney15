import csv
import os

# folder_path = "E:\\0.0_CDU\\1.Software_now_course_resources\\Group_assingment_2\\nazia_assingment_2_syd_15\\HIT137_2025_S3_Sydney15\\temperatures"  # local directory

folder_path = "..\\HIT137_2025_S3_Sydney15\\temperatures"
#helper function : calculates the average
def calculate_average(temps):
    return round(float(sum(temps)) / int(len(temps)), 2) #i.e in [7]

#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#function 01
def seasonal_average():
    summer_temperature = []
    winter_temperature = []
    autumn_temperature = []
    spring_temperature = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"): #i.e in [1]
            file_path = os.path.join(folder_path, filename)
            with (open(file_path, mode="r", encoding="utf-8") as file): #i.e in [2]
                reader = csv.DictReader(file) #i.e in [3]
                for row in reader:
                    for i in row["December"], row["January"], row["February"]:
                        summer_temperature.append(float(i))
                    for j in row["March"], row["April"], row["May"]:
                        autumn_temperature.append(float(j))
                    for k in row["June"], row["July"], row["August"]:
                        winter_temperature.append(float(k))
                    for l in row["September"], row["October"], row["November"]:
                        spring_temperature.append(float(l)) #i.e in [5]

                averege_temperature_all_season ={
                    "Summer  " :calculate_average(summer_temperature),
                    "Autumn  " :calculate_average(autumn_temperature),
                    "Winter  " :calculate_average(winter_temperature),
                    "Spring  " :calculate_average(spring_temperature),
                }
                with open('average_temp.txt', 'w', encoding="utf-8") as file:
                    for season, temperature in averege_temperature_all_season.items():
                        file.write(f"{season}: {temperature}\u00B0C \n") #i.e in [6] , i.e in [7]

#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------

#function 2 : find the range of temperature station wise and returns the max
def temperature_range_func():
    #reading files in directory
    for filename in os.listdir(folder_path): #i.e in [1]
        if filename.endswith(".csv"): #will only read csv files
            file_path = os.path.join(folder_path, filename)
            with (open(file_path, mode="r", encoding="utf-8") as file):#i.e in [1]
                reader = csv.DictReader(file) #i.e in [2]
                station_wise_temps = {}
                for row in reader:
                    station_name = row['STATION_NAME'] #i.e in [4] # put the station names into an array
                    temperatures = []
                    for month, value in row.items():
                        if month not in {"STATION_NAME", "STN_ID", "LAT","LON"}:  # we only need the station name and the temperature values, no need for other values
                            try:
                                temperatures.append(float(value))  # if the values cannot be converted into float, that means these are station names
                            except ValueError:  # when we find values that can be converted into floats , we put them in temps
                                pass

                    station_wise_temps[station_name] = temperatures #i.e in [4]

                # this block rearranges the data : iterates through every station and their temperature though out the month and
                # temp_difference : Holds the maximum , minimum and the difference of temperature for each station
                temp_difference = {}
                for key, value in station_wise_temps.items():
                    temp_difference[key] = {
                        "max_temperature": round(max(value), 2),  # dictionary of dictionary to hold the max
                        "min_temperature": round(min(value), 2),  # min
                        "temperature_difference": round(max(value) - min(value), 2)  # difference of max and min rounded by 2
                    } #i.e in [4]

                temperature_range = {}  # holds the final result : The maximum range and the min,max temperature of the station
                largest_tmp_range = -1.00
                largest_station_name = None

                # temperature_range={} : holds the final result : The maximum range and the min,max temperature of the station
                # this loop finds the maximum gap between the highest and lowest temperature of a particular station(s) and then stores the value into a dictionary
                for station_names, values in temp_difference.items():
                    if values["temperature_difference"] > largest_tmp_range:
                        largest_tmp_range = values["temperature_difference"] #i.e in [4]
                        largest_station_name = station_names
                        temperature_range = {
                            "Station_name": largest_station_name,
                            "Range": largest_tmp_range,
                            "Max": values["max_temperature"],
                            "Min": values["min_temperature"]
                        } #i.e in [4]
                    # this condition checks if there are any other station has the same temperature range difference
                    elif values["temperature_difference"] == largest_tmp_range:
                        temperature_range = {
                            "Station_name": largest_station_name,
                            "Range": largest_tmp_range,
                            "Max": values["max_temperature"],
                            "Min": values["min_temperature"]
                        }
                with open('largest_temp_range_station.txt', 'w', encoding="utf-8") as file:
                    file.write(
                        f"{temperature_range["Station_name"]}: Range:{temperature_range['Range']}\u00B0C(Max:{temperature_range['Max']}\u00B0C ,Min:{temperature_range['Min']}\u00B0C) \n"
                    ) #i.e in [7]



#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#function 3 : find the smallest and largest standard deviation , station wise

def temperature_stability():
    #reading files in directory
    for filename in os.listdir(folder_path): #i.e in [1]
        if filename.endswith(".csv"): #will only read csv files
            file_path = os.path.join(folder_path, filename)
            with (open(file_path, mode="r", encoding="utf-8") as file): #i.e in [1]
                reader = csv.DictReader(file) #i.e in [2]
                station_wise_temps = {}
                for row in reader:
                    station_name = row['STATION_NAME']  # put the station names into an array
                    temperatures = []
                    for month, value in row.items():
                        if month not in {"STATION_NAME", "STN_ID", "LAT","LON"}:  # we only need the station name and the temperature values, no need for other values
                            try:
                                temperatures.append(float(value))  # if the values cannot be converted into float, that means these are station names
                            except ValueError:  # when we find values that can be converted into floats , we put them in temps
                                pass

                    station_wise_temps[station_name] = temperatures

    #steps dor std (standard deviation)
    #1 : Find mean of each station's temperatures
    station_wise_std={}
    mean_temperature = {}
    all_station_std=[]

    for key, value in station_wise_temps.items():
        mean_temperature[key] = {
            "station_name": key,
            "temperatures" : value,
            "mean_temperature": round(sum(value) / len(value), 2)  # dictionary of dictionary to hold the mean of each station
             } #i.e in [8]
    for  temperatures, mean_temperature in mean_temperature.items():
            station=mean_temperature["station_name"] 
            all_temperatures=mean_temperature["temperatures"]  #only the temperatures value keeping in a variable
            mean_value = mean_temperature["mean_temperature"]   #the mean of all temperature

            sum_of_squared_diff =0
            for i in all_temperatures:
                difference = i - mean_value
                sum_of_squared_diff += difference * difference

                length = len(all_temperatures)
                variance = sum_of_squared_diff / (length - 1)
                standard_var = variance ** 0.5
                station_wise_std={
                    "station_name" : station,
                    "std" : round(standard_var,2) #i.e in [6]
                }
            all_station_std.append(station_wise_std)



    #find the max and min std station wise
    #definifn first value as the min and max, later we will find the actual min , max
    min_std=all_station_std[0]
    max_std=all_station_std[0]


    for values in all_station_std:
        if values["std"]>max_std['std'] :
            max_std=values
        if values["std"]<min_std['std']:
            min_std=values

    #this block of code handles if there are ties (multiple min or max) standard deviation,
    for data in all_station_std:
        if data["std"]==max_std['std']:
            max_std['station_name']=all_station_std[0]['station_name']
            max_std['std']=data["std"] #i.e in [6]

        if data["std"]==min_std['std']:
            min_std['station_name']=all_station_std[0]['station_name']
            min_std['std']=data["std"] #i.e in [6]

    print(min_std,min_std)

    with open("temperature_stability_stations.tx", 'w', encoding="utf-8") as file:
        file.write(
             "Most Stable:Station:" f"{min_std["station_name"]}: StdDev {min_std['std']}\u00B0C Most Variable:Station:{max_std["station_name"]}: StdDev {max_std['std']}\u00B0C"
        ) #i.e in [6]

seasonal_average()
temperature_range_func()
temperature_stability()
