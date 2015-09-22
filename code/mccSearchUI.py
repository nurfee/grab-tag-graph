'''
# Wizard for running the mccSearch program
'''

import os
import subprocess

import networkx as nx

#mccSearch modules
import mccSearch
import utils
import plotting
import metrics
import iomethods

def main():
    CEGraph = nx.DiGraph()
    prunedGraph = nx.DiGraph()
    MCCList =[]
    MCSList=[]
    MCSMCCNodesList =[]
    allMCSsList =[]
    allCETRMMList =[]
    #DIRS={}
    DIRS={
               "mainDirStr" : "/Users/nsagitap/output/devel/",
                "TRMMdirName" : None,
                "CEoriDirName" : "/Users/nsagitap/data/MTSAT/Indonesia/200702/S8"
    #          mainDirStr= "/directory/to/where/to/store/outputs"
    #          TRMMdirName = "/directory/to/the/TRMM/netCDF/files"
    #          CEoriDirName = "/directory/to/the/MERG/netCDF/files"
             }
    preprocessing = ''
    rawMERG = ''
    startDateTime   = '200702010030'
    endDateTime     = '200702010630'

    #for GrADs
    subprocess.call('export DISPLAY=:0.0', shell=True)


    print "Running MCCSearch ..... \n"
    # Main Directory
    if not 'mainDirStr' in DIRS.keys():
        DIRS['mainDirStr'] = raw_input("> Please enter working directory: \n" )   # This is where data created will be stored
    else:
        print "> Working directory : ", DIRS['mainDirStr']

    preprocessing = raw_input ("> Do you need to preprocess the MERG files? [y/n]: \n")
    while preprocessing.lower() != 'n':
        if preprocessing.lower() == 'y':
            #get location for raw files
            rawMERG = raw_input("> Please enter the directory to the RAW MERG (.Z) files: \n")
            #run preprocessing
            utils.preprocessing_merg(rawMERG)
            continue
        elif preprocessing.lower() == 'n' :
            pass
        else:
            print "Error! Invalid choice "
            preprocessing = raw_input ("> Do you need to preprocess the MERG files? [y/n]: \n")


    #get the location of the MERG and TRMM data
    ## MERG.nc directory
    if not 'CEoriDirName' in DIRS.keys():
        DIRS['CEoriDirName'] = raw_input("> Please enter the directory to the MERG netCDF files: \n")
    else:
        print "> Directory of MERG netCDF files: ", DIRS['CEoriDirName']
    try:
        if not os.path.exists(DIRS['CEoriDirName']):
            print "Error! MERG invalid path!"
            DIRS['CEoriDirName'] = raw_input("> Please enter the directory to the MERG netCDF files: \n")
    except:
        print "..."


    ## TRMM.nc directory
    if not 'TRMMdirName' in DIRS.keys():
        DIRS['TRMMdirName'] = raw_input("> Please enter the location to the raw TRMM netCDF files: \n")
    else:
        print "> Directory of raw TRMM netCDF files: ", DIRS['TRMMdirName']
    try:
        if not os.path.exists(DIRS['TRMMdirName']):
            print "Error: TRMM invalid path!"
            DIRS['TRMMdirName'] = raw_input("> Please enter the location to the raw TRMM netCDF files: \n")
    except:
        pass

    #get the dates for analysis
    ## Start date time
    if not startDateTime:
        startDateTime = raw_input("> Please enter the start date and time yyyymmddhrmm: \n")
    else:
        print "> Start date time: ", startDateTime
    #check validity of time
    while utils.valid_date(startDateTime) != True:
        print "Invalid time entered for startDateTime!"
        startDateTime = raw_input("> Please enter the start date and time yyyymmddhrmm: \n")

    ## End date time
    if not endDateTime:
        endDateTime = raw_input("> Please enter the end date and time yyyymmddhrmm: \n")
    else:
        print "> End date time: ", endDateTime
    while utils.valid_date(endDateTime) != True:
        print "Invalid time entered for endDateTime!"
        endDateTime = raw_input("> Please enter the end date and time yyyymmddhrmm: \n")

    #check if all the files exisits in the MERG and TRMM directories entered
    #test,_ = iomethods.check_for_files(startDateTime, endDateTime, DIRS['TRMMdirName'], 2)
    if DIRS['TRMMdirName']:
        test,_ = iomethods.check_for_files(DIRS['TRMMdirName'], startDateTime, endDateTime, 3, 'hour')
        if test == False:
            print "Error with files in the original TRMM directory entered. Please check your files before restarting. "
            return
    #test,filelist = iomethods.check_for_files(startDateTime, endDateTime, DIRS['CEoriDirName'],1)
    test,filelist = iomethods.check_for_files(DIRS['CEoriDirName'], startDateTime, endDateTime, 1, 'hour')
    if test == False:
        print "Error with files in the original MERG directory entered. Please check your files before restarting. "
        return

    #create main directory and file structure for storing intel
    DIRS['mainDirStr'] = iomethods.create_main_directory(DIRS['mainDirStr'])
    TRMMCEdirName = DIRS['mainDirStr']+'/TRMMnetcdfCEs'
    CEdirName = DIRS['mainDirStr']+'/IRnetcdfCEs'

    # for doing some postprocessing with the clipped datasets instead of running the full program, e.g.
    postprocessing = raw_input("> Do you wish to postprocess data? [y/n] \n")
    while postprocessing.lower() != 'n':
        if postprocessing.lower() == 'y':
            option = postprocessing_plot_menu(DIRS)
            return
        elif postprocessing.lower() == 'n':
            pass
        else:
            print "\n Invalid option."
            postprocessing = raw_input("> Do you wish to postprocess data? [y/n] \n")
    # -------------------------------------------------------------------------------------------------
    # Getting started. Make it so number one!
    print ("-"*80)
    print "\t\t Starting the MCCSearch Analysis "
    print ("-"*80)
    print "\n -------------- Reading MERG and TRMM Data ----------"
#    mergImgs, timeList, LAT, LON = iomethods.read_data(DIRS['CEoriDirName'],'ch4','latitude','longitude', filelist)
    mergImgs, timeList, LAT, LON = iomethods.read_data(DIRS['CEoriDirName'],'tbb','lat','lon', filelist)
    print "\n -------------- findCloudElements ----------"
    CEGraph = mccSearch.find_cloud_elements(mergImgs,timeList,DIRS['mainDirStr'], LAT,LON,DIRS['TRMMdirName'])
    #theList = CEGraph.successors(node)
    #if the TRMMdirName wasnt entered for whatever reason, you can still get the TRMM data this way
    # CEGraph = mccSearch.findCloudElements(mergImgs,timeList)
    # allCETRMMList=mccSearch.findPrecipRate(DIRS['TRMMdirName'],timeList)
    # ----------------------------------------------------------------------------------------------
    print "\n -------------- findCloudClusters ----------"
    prunedGraph = mccSearch.find_cloud_clusters(CEGraph)
    print "\n -------------- findMCCs ----------"
    MCCList,MCSList = mccSearch.find_MCC(prunedGraph)
    #now ready to perform various calculations/metrics
    print ("-"*80)
    print "\n -------------- METRICS ----------"
    print ("-"*80)
    #some calculations/metrics that work that work
    print "creating the MCC userfile ", metrics.create_text_file(MCCList,1, DIRS['mainDirStr'], 80000.0, 1)
    print "creating the MCS userfile ", metrics.create_text_file(MCSList,2, DIRS['mainDirStr'], 80000.0, 1)
    plot_menu(MCCList, MCSList, DIRS)

    #Let's get outta here! Engage!
    print ("-"*80)
#*********************************************************************************************************************
def plot_menu(MCCList, MCSList, DIRS):
    '''
    Purpose:: The flow of plots for the user to choose

    Input:: MCCList: a list of directories representing a list of nodes in the MCC
            MCSList: a list of directories representing a list of nodes in the MCS
            DIRS: a dictionary indicating the paths to data, both original and generated

    Output:: None
    '''
    option = display_plot_menu()
    while option != 0:
        #try:
        if option == 1:
            print "Generating Accumulated Rainfall from TRMM for the entire period ...\n"
            plotting.plot_accu_TRMM(MCSList, DIRS['mainDirStr'])
        if option == 2:
            startDateTime = raw_input("> Please enter the start date and time yyyy-mm-dd_hr:mm:ss format: \n")
            endDateTime = raw_input("> Please enter the end date and time yyyy-mm-dd_hr:mm:ss format: \n")
            print "Generating acccumulated rainfall between ", startDateTime," and ", endDateTime, " ... \n"
            plotting.plot_accu_in_time_range(startDateTime, endDateTime, DIRS['mainDirStr'], 1.0)
        if option == 3:
            print "Generating area distribution plot ... \n"
            plotting.display_size(MCSList, DIRS['mainDirStr'])
        if option == 4:
            print "Generating precipitation and area distribution plot ... \n"
            plotting.display_precip(MCSList, DIRS['mainDirStr'])
        if option == 5:
            try:
                print "Generating histogram of precipitation for each time ... \n"
                plotting.plot_precip_histograms(MCSList, DIRS['mainDirStr'])
            except:
                pass
        # except:
        #     print "Invalid option. Please try again, enter 0 to exit \n"

        option = display_plot_menu()
    return
#*********************************************************************************************************************
def display_plot_menu():
    '''
    Purpose:: Display the plot Menu Options

    Input:: None

    Output:: option: an integer representing the choice of the user
    '''
    print "**************** PLOTS ************** \n"
    print "0. Exit \n"
    print "1. Accumulated TRMM precipitation \n"
    print "2. Accumulated TRMM precipitation between dates \n"
    print "3. Area distribution of the system over time \n"
    print "4. Precipitation and area distribution of the system \n"
    print "5. Histogram distribution of the rainfall in the area \n"
    option = int(raw_input("> Please enter your option for plots: \n"))
    return option
#*********************************************************************************************************************
def display_postprocessing_plot_menu():
    '''
    Purpose:: Display the plot Menu Options

    Input:: None

    Output:: option: an integer representing the choice of the user
    '''
    print "**************** POST PROCESSING PLOTS ************** \n"
    print "0. Exit \n"
    print "1. Map plots of the original MERG data \n"
    print "2. Map plots of the cloud elements using IR data \n"
    print "3. Map plots of the cloud elements rainfall accumulations using TRMM data \n"
    #print "4. Accumulated TRMM precipitation \n"
    #print "5. Accumulated TRMM precipitation between dates \n"

    option = int(raw_input("> Please enter your option for plots: \n"))
    return option
#*********************************************************************************************************************
def postprocessing_plot_menu(DIRS):
    '''
    Purpose:: The flow of plots for the user to choose

    Input:: DIRS a dictionary of directories
    #       DIRS={
    #          mainDirStr= "/directory/to/where/to/store/outputs"
    #          TRMMdirName = "/directory/to/the/TRMM/netCDF/files"
    #          CEoriDirName = "/directory/to/the/MERG/netCDF/files"
    #         }

    Output:: None
    '''
    TRMMCEdirName = DIRS['mainDirStr']+'/TRMMnetcdfCEs'
    CEdirName = DIRS['mainDirStr']+'/IRnetcdfCEs'

    option = display_postprocessing_plot_menu()
    while option != 0:
        try:
            if option == 1:
                print "Generating images from the original MERG dataset ... \n"
                utils.post_processing_netcdf(3, DIRS['CEoriDirName'])
            if option == 2:
                print "Generating images from the cloud elements using MERG IR data ... \n"
                utils.post_processing_netcdf(1, CEdirName)
            if option == 3:
                print "Generating precipitation accumulation images from the cloud elements using TRMM data ... \n"
                utils.post_processing_netcdf(2, TRMMCEdirName)
            # if option == 4:
            #     print "Generating Accumulated TRMM rainfall from cloud elements for each MCS ... \n"
            #     featureType = int(raw_input("> Please enter type of MCS MCC-1 or MCS-2: \n"))
            #     if featureType == 1:
            #         filename = DIRS['mainDirStr']+'/textFiles/MCCPostProcessing.txt'
            #         try:
            #             if os.path.isfile(filename):
            #             #read each line as a list
            #         plotting.plotAccTRMM(DIRS['mainDirStr'])
            # if option == 5:
            #     mccSearch.plotAccuInTimeRange()
        except:
            print "Invalid option, please try again"
        option = display_postprocessing_plot_menu()
    return
#*********************************************************************************************************************

main()

