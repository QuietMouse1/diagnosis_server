import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys, os
from helper_funcs import format_scandir_output
from filenames import Filenames
import collections

def generate_logs():

    filename = Filenames()
    whereami = 'Logs/'
    out = os.scandir(whereami)
    dirs_dct = {}
    for entry in out:
        if entry.is_dir():
            dirs_dct[os.path.getctime(entry)] = entry.name # sorting by key is easier (?) than sorting by values
            print (os.path.getctime(entry), entry.name)
    
    sorted_dirs_dct = collections.OrderedDict(sorted(dirs_dct.items())) # sort them using ordered dict
    print("Sorting out directory")
    for k, v in sorted_dirs_dct.items():
        print(k, v)
    newest_directory = list(sorted_dirs_dct.values())[-1] # get the latest value
    print("Logs Newest_directory is " + newest_directory)

    report_directory = "Report/"
    new_directory = report_directory + newest_directory

    try:
        os.mkdir(new_directory)
    except Exception as e:
        print(e) # directory already exist ?

    drone_number = os.getenv('DRONE_NUMBER')

    if drone_number == "1":
        ping_file_name = filename.ping1_2
    if drone_number == "2":
        ping_file_name = filename.ping2_3
    if drone_number == "3":
        ping_file_name = filename.ping3_1


    cpu_df = pd.read_csv(whereami + newest_directory + filename.cpu, sep= ",")
    ram_df = pd.read_csv(whereami + newest_directory + filename.ram, sep= ",")
    ping_df = pd.read_csv(whereami + newest_directory + ping_file_name, sep= ",")
    wifi_df = pd.read_csv(whereami + newest_directory + filename.wifi, sep= ",")

    ### Ram and CPU
    # print(df.columns)
    # cpu_df = 100 - df['%idle']
    average_cpu = cpu_df.iloc[:,0].mean()
    average_ram = ram_df.iloc[:,0].mean()
    print("Average CPU usage is {}".format(average_cpu))
    print("Average memory usage is {}".format(average_ram))

    figure, (axis1, axis2, axis3) = plt.subplots(3, 1)
    figure.suptitle('CPU and RAM Usage Graph')
    #format the time column
    ram_time_column = ram_df.iloc[:,1]
    ram_column = ram_df.iloc[:,0]
    ram_date_time_in_pandas = pd.to_datetime(ram_time_column)
    axis1.set_title('RAM usage graph')
    axis1.plot(ram_date_time_in_pandas, ram_column)
    axis1.set_ylabel("RAM (%)")
    axis1.set_xlabel("Time (24h)")

    cpu_time_column = cpu_df.iloc[:,1]
    cpu_column = cpu_df.iloc[:,0]
    cpu_date_time_in_pandas = pd.to_datetime(cpu_time_column)
    axis2.set_title('Average CPU thread usage graph')
    axis2.plot(cpu_date_time_in_pandas, cpu_column)
    axis2.set_ylabel("Average CPU usage (%)")
    axis2.set_xlabel("Time (24h)")

    axis3.plot(cpu_date_time_in_pandas, cpu_column)
    axis3.plot(ram_date_time_in_pandas, ram_column)
    axis3.set_title('CPU & RAM graph')
    axis3.set_ylabel("CPU & RAM usage (%)")
    axis3.set_xlabel("Time (24h)")
    axis3.legend(["CPU", "RAM"])

    # Wtf no pixel format?
    figure.set_size_inches(10,15)
    figure.savefig(new_directory + 'mem_cpu_usage_graph.png', dpi = 200)

    ## Ping
    figure1, (axis4, axis5) = plt.subplots(2,1)
    figure1.suptitle('CPU and Ping graph')
    ping_time_column = ping_df.iloc[:,1]
    ping_column = ping_df.iloc[:,0]
    ping_date_time_in_pandas = pd.to_datetime(ping_time_column)
    axis4.scatter(ping_date_time_in_pandas, ping_column)
    axis4.set_title('Ping graph')
    axis4.set_ylabel("Ping (ms)")
    axis4.set_xlabel("Time (24h)")

    axis5.plot(cpu_date_time_in_pandas, cpu_column)
    axis5.set_title('CPU graph')
    axis5.set_ylabel("Average CPU thread usage graph (%)")
    axis5.set_xlabel("Time (24h)")

    figure1.set_size_inches(10,15)
    plt.xlabel('''Average CPU {}%,
    Average Mem{}%'''.format(average_cpu, average_ram))

    figure1.savefig(new_directory + 'ping_graph.png', dpi = 200)

    ## wifi
        # bit_rate = out[11] # Rate=866.7 units are in Mb/s
        # Tx_power = out[13] # Tx-Power=22 units are in dbm
        # signal_level = out[29] # level=-51 units are in dBm

    figure2, (axis6, axis7) = plt.subplots(2,1)
    figure2.suptitle('Wifi graph')
    wifi_time_column = wifi_df.iloc[:,3]
    bit_rate_column = wifi_df.iloc[:,0]
    tx_power = wifi_df.iloc[:,1]
    signal_strength = wifi_df.iloc[:,2]

    ping_column = ping_df.iloc[:,0]
    wifi_time_column_in_pandas = pd.to_datetime(wifi_time_column)

    axis6.plot(wifi_time_column_in_pandas, tx_power)
    axis6.plot(wifi_time_column_in_pandas, signal_strength)
    axis6.set_title('TX power Signal Strength graph')
    axis6.legend(["TX power", "Signal Strength"])
    axis6.set_ylabel("Gain (dBm)")
    axis6.set_xlabel("Time (24h)")

    axis7.plot(wifi_time_column_in_pandas, bit_rate_column)
    axis7.set_title('Bit rate graph')
    axis7.set_ylabel("Bit rate (Mb/s)")
    axis7.set_xlabel("Time (24h)")

    figure2.set_size_inches(10,15)
    figure2.savefig(new_directory + 'wifi_stats.png', dpi = 200)
    return plt, newest_directory

if __name__ == "__main__":
    plt_handler, direct = generate_logs()
    plt_handler.show()