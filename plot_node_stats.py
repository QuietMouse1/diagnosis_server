import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import sys, os
from helper_funcs import format_scandir_output
import collections
# The nodes logs directory contains directories
# Each of the directory is the name of the ros node 
# Inside each directory contains a CPU usage file and memory usage file

def generate_node_logs():

    # Find nodeslogs directory
    # Find the latest logs directory
    whereami = 'NodesLogs/'

    out = os.scandir(whereami)
    dirs_dct = {}
    file_dct = {}
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

    # Report directory
    # Create a new directory to store all the reports
    # The name will be dependent on the newwest logs directory
    report_directory = "Report/Nodes_logs_"
    new_directory = report_directory + newest_directory
    try:
        os.mkdir(new_directory)
    except Exception as e:
        print(e) # directory already exist ?

    # loop through all the directories the NodesLogs directory 
    # in each directories, generate a graph of cpu and mem usage

    directory_containing_all_nodes = os.scandir(whereami + newest_directory)
    for entry in directory_containing_all_nodes:
        if entry.is_dir():
            file_entries = os.scandir(whereami + newest_directory + entry.name)
            node_name_dir = entry.name + "/"
            for file in file_entries:
                if substring_exist_in_filename(file.name, "cpu_usage.csv"):
                    cpu_df = pd.read_csv(whereami + newest_directory + node_name_dir + file.name, sep= ",")
                    cpu_df = cpu_df.iloc[1:,:]
                if substring_exist_in_filename(file.name, "mem_usage.csv"):
                    mem_df = pd.read_csv(whereami + newest_directory + node_name_dir + file.name, sep= ",")
                    mem_df = mem_df.iloc[1:,:]
            print(cpu_df)
            plt_handler = plot_cpu_mem_image(cpu_df, mem_df, new_directory, entry.name)

    return plt_handler, newest_directory

def plot_cpu_mem_image(cpu_df, ram_df, directory_to_save_them, node_name):
    ### Ram and CPU
    # print(df.columns)
    # cpu_df = 100 - df['%idle']
    # Ignore first row, always 0 output
    average_cpu = str(cpu_df.iloc[:,0].mean())
    average_ram = str(ram_df.iloc[:,0].mean())
    print("Average CPU usage is {}".format(average_cpu))
    print("Average memory usage is {}".format(average_ram))

    figure, (axis1, axis2, axis3) = plt.subplots(3, 1)
    figure.suptitle(node_name + '_CPU and RAM Usage Graph')
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

    plt.xlabel('''Average CPU {}%,
    Average Mem{}%'''.format(average_cpu, average_ram))

    # Wtf no pixel format?
    figure.set_size_inches(10,15)
    figure.savefig(directory_to_save_them + node_name + '_mem_cpu_usage_graph.png', dpi = 200)

    return plt

def substring_exist_in_filename(file_name, substring):
    if substring in file_name:
        return True
    else:
        return False

if __name__ == "__main__":
    plt_handler, newest_directory = generate_node_logs()
    # plt_handler.show()