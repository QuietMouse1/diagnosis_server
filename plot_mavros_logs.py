import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os 
from filenames import Filenames
import collections

# Adjust frequency of time interval in the x axis

def generate_mavros_logs():

    filename = Filenames()
    whereami = 'MavrosLogs/'

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
        print("Directory already exist, skipping mkdir")

    mavros_pose_df = pd.read_csv(whereami + newest_directory + filename.mavros_pose, sep= ",")
    setpoint_df = pd.read_csv(whereami + newest_directory + filename.setpoint_pose , sep= ",")
    assigned_df = pd.read_csv(whereami + newest_directory + filename.assigned_pose, sep= ",")
    aloam_df = pd.read_csv(whereami + newest_directory + filename.aloam, sep= ",")
    vision_df = pd.read_csv(whereami + newest_directory + filename.mavros_vision, sep= ",")

    figure, (axis, axis2, axis3) = plt.subplots(3,1)
    figure.suptitle('Setpoint vs mavros_pose graph')
    x_mavros_pose_column = mavros_pose_df.iloc[:,0]
    y_mavros_pose_column = mavros_pose_df.iloc[:,1]
    z_mavros_pose_column = mavros_pose_df.iloc[:,2]
    time_mavros_pose_column = mavros_pose_df.iloc[:,3]
    mavros_pose_date_time_in_pandas = pd.to_datetime(time_mavros_pose_column)

    x_setpointpose_column = setpoint_df.iloc[:,0]
    y_setpointpose_column = setpoint_df.iloc[:,1]
    z_setpointpose_column = setpoint_df.iloc[:,2]
    time_setpointpose_column = setpoint_df.iloc[:,3]
    setpoint_date_time_in_pandas = pd.to_datetime(time_setpointpose_column)

    x_assignedpose_column = assigned_df.iloc[:,0]
    y_assignedpose_column = assigned_df.iloc[:,1]
    z_assignedpose_column = assigned_df.iloc[:,2]
    time_assignedpose_column = assigned_df.iloc[:,3]
    assignedpose_date_time_in_pandas = pd.to_datetime(time_assignedpose_column)

    x_aloam_column = aloam_df.iloc[:,0]
    y_aloam_column = aloam_df.iloc[:,1]
    z_aloam_column = aloam_df.iloc[:,2]
    time_aloam_column = aloam_df.iloc[:,3]
    aloam_date_time_in_pandas = pd.to_datetime(time_aloam_column)

    x_vision_column = vision_df.iloc[:,0]
    y_vision_column = vision_df.iloc[:,1]
    z_vision_column = vision_df.iloc[:,2]
    time_vision_column = vision_df.iloc[:,3]
    vision_date_time_in_pandas = pd.to_datetime(time_vision_column)

    axis.plot(mavros_pose_date_time_in_pandas, x_mavros_pose_column)
    axis.plot(setpoint_date_time_in_pandas, x_setpointpose_column)
    axis.plot(assignedpose_date_time_in_pandas, x_assignedpose_column)
    axis.plot(aloam_date_time_in_pandas, x_aloam_column, linestyle= 'dashed')
    axis.plot(vision_date_time_in_pandas, x_vision_column, linestyle= 'dotted')

    axis.set_title('X')
    axis.legend(["Mavros pose", "Setpoint pose", "Assigned pose", "Aloam odom", "Mavros vision"])
    axis.set_ylabel("Position (m)")
    axis.set_xlabel("Time (24h)")

    axis2.plot(mavros_pose_date_time_in_pandas, y_mavros_pose_column)
    axis2.plot(setpoint_date_time_in_pandas, y_setpointpose_column)
    axis2.plot(assignedpose_date_time_in_pandas, y_assignedpose_column)
    axis2.plot(aloam_date_time_in_pandas, y_aloam_column, linestyle= 'dashed')
    axis2.plot(vision_date_time_in_pandas, y_vision_column, linestyle= 'dotted')
    axis2.set_title('Y')
    axis2.legend(["Mavros pose", "Setpoint pose", "Assigned pose", "Aloam odom", "Mavros vision"])
    axis2.set_ylabel("Position (m)")
    axis2.set_xlabel("Time (24h)")

    axis3.plot(mavros_pose_date_time_in_pandas, z_mavros_pose_column)
    axis3.plot(setpoint_date_time_in_pandas, z_setpointpose_column)
    axis3.plot(assignedpose_date_time_in_pandas, z_assignedpose_column)
    axis3.plot(aloam_date_time_in_pandas, z_aloam_column, linestyle= 'dashed')
    axis3.plot(vision_date_time_in_pandas, z_vision_column, linestyle= 'dotted')

    axis3.set_title('Z')
    axis3.legend(["Mavros pose", "Setpoint pose", "Assigned pose", "Aloam odom", "Mavros vision"])
    axis3.set_ylabel("Position (m)")
    axis3.set_xlabel("Time (24h)")

    # Wtf no pixel format?
    figure.set_size_inches(10,15)
    figure.savefig(new_directory + '/mavros_local_vs_setpoint_vs_assigned.png', dpi = 200)
    return plt, newest_directory

if __name__ == "__main__":
    plt_handler, direct = generate_mavros_logs()
    plt_handler.show()