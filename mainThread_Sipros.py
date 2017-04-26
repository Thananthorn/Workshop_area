"""

Copyright 2017 GISTDA


The Software is written by Dr. Teerasit Kasetkasem from Kasetsart University, Thailand, aa a part of the cooperation
between GISTDA and Kasetsart University under the SIPROs project.

GISTDA retains the right to use, copy, modify, merge, publish, distribute, sublicense, and/or shell copies of the
Software. Any distribution, use, copy, modification, publication of this Software must be explicitly granted by GISTDA.
However, Dr. Teerasit Kasetkasem retains the right to use, copy, modify, merge, publish, and/or shell copies of the
Software without any permission from GISTDA for the following conditions:
1) Correction and maintenance of the Software
2) Educational activities
3) Research activities

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import shutil
import traceback
import time
import sys

from PyQt4.QtGui import QApplication , QFileDialog , QMessageBox

import CompleteLevel1A as level1asystem
import CompleteLevel2A as level2asystem
import digitalElevationModel as demservice

import cpf_logic as CP
import scene_info as SI

# SYSTEM CONSTANTS
class demDirectory:
    # The absolute directories to all DEM Databses.
    # Fail to add correct directories may result in high positioning error.

    #Open this if Sipros Linux system.
    SRTM30 = None
    # SRTM90 = "/home/sipros/Application_1A_2A/Sipros_System/DEM/SRTM_90"
    # GLOBE = "/home/sipros/Application_1A_2A/Sipros_System/DEM/GLOBE"
    # THEOS = "/home/sipros/Application_1A_2A/Sipros_System/DEM/THEOS_DEM"

    #Open this if Asuna Linux system.
    # SRTM30 = None
    # SRTM90 = "/home/asuna/worker_Lab/Sipros_System/DEM/SRTM_90"
    # GLOBE = "/home/asuna/worker_Lab/Sipros_System/DEM/GLODE"
    # THEOS = "/home/asuna/worker_Lab/Sipros_System/DEM/THEOS_DEM"

    #Open this if Sipros Windows system.
    # SRTM30 = None
    SRTM90 = "C:/Worker/Support-Worker/Sipros_system/DEM/SRTM_90"
    GLOBE = "C:/Worker/Support-Worker/Sipros_system/DEM/GLOBE"
    THEOS = "C:/Worker/Support-Worker/Sipros_system/DEM/THEOS_DEM"

class processingLevel:
    LEVEL1A = "1A"
    LEVEL2A = "2A"

class sensorType:
    PAN ="PAN"
    MS = "MS"

# SCENE INFORMATION TO USED
class sceneInfo:
    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    in this class I call value from {if __name__ == "__main__"} look at it say sceneinfo.[variable] .
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
    ger_dir = ""
    cpf_file = ""
    begin_lines = []
    start_sample = 1
    im_width = 0
    im_height = 0
    info_dir = ""
    target_dir = ""
    rev_num = ""
    grid_id = ""
    line_shifted = 0

# PROCESSING LEVEL AND DATA TYPE
class processSetup:

    processing_level = ""
    # Choose Between LEVEL2A & LEVEL1A
    sensor = ""
    # Choose Between PAN & MS (going look in {if __name__ == "__main__"} [paragraph 9 - 10 for PAN] , [paragraph 14 - 16 for MS] )
    dem_interpolation = demservice.digitalElevationModel.CUBIC
    # Choose between NEAREST, LINEAR, CUBIC, KRIGING and RBF (KRIGING & RBF ARE VERY SLOW)
    dem_type = demservice.THEOS_DEM
    # Choose between THEOS_DEM, GLOBE_DEM, SRTM90_DEM & SRTM30_DEM (SRTM30 may be very slow)

    # Open this line if Sipros Linux System.
    # apf_file = "/home/sipros/Application_1A_2A/Sipros_System/APF/THEOS_nominal.APF"
    # LOCATION OF APF FILE

    # Open this line if asuna Linux System.
    # apf_file = "/home/asuna/worker_Lab/Sipros_System/APF/THEOS_nominal.APF"
    # LOCATION OF APF FILE

    # Open this line if Sipros Windows System.
    apf_file = r"C:\Worker\Support-Worker\Sipros_system\APF\THEOS_nominal.APF"
    # LOCATION OF APF FILE


def callProcessingSystem(scene_info, process_setup):  # main call thread of the main process
    ger_directory = scene_info.ger_dir
    cpf_file = scene_info.cpf_file
    apf_file = process_setup.apf_file
    begin_lines = scene_info.begin_lines
    dem_type = process_setup.dem_type
    info_directory = scene_info.info_dir
    destination_directory = scene_info.target_dir
    rev_num = scene_info.rev_num
    grid_ref = scene_info.grid_id
    dem_interpolation_method = process_setup.dem_interpolation
    line_shifted = scene_info.line_shifted
    start_sample = scene_info.start_sample
    im_width = scene_info.im_width
    im_height = scene_info.im_height
    dem_dir = demDirectory

    if processSetup.processing_level == processingLevel.LEVEL1A:
        level1asystem.buildLevel1AImage(processSetup.sensor, ger_directory, cpf_file, apf_file, begin_lines, dem_type,
                                        info_directory, destination_directory, rev_num, grid_ref,dem_dir,
                                        dem_interpolation=dem_interpolation_method, line_shifted=line_shifted,
                                        start_sample=start_sample, im_width=im_width, im_height=im_height,
                                        force_run=False)
    elif processSetup.processing_level == processingLevel.LEVEL2A:
        level2asystem.buildLevel2AImage(processSetup.sensor, ger_directory, cpf_file, apf_file, begin_lines, dem_type,
                                        info_directory, destination_directory, rev_num, grid_ref,dem_dir,
                                        dem_interpolation=dem_interpolation_method, line_shift=line_shifted,
                                        start_sample=start_sample, im_width=im_width, im_height=im_height,
                                        force_run=False)


if __name__ == "__main__":
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        The process should be like this.

        Process from [scene_info.py]
        A. Get zip file of CUF.
        B. Extract zip file for get CUF file and browse strip image.
        C. Get values from CUF and Cut browse strip image to browse scene image.
        D. Values from CUF use to create command_files.

        Process in this script.
        A. Get command_file or many command_file.
        B. Append A to list and count value that list for use in for loop.
        C. Seclect Level to process 1A or 2A.
        D. Get values for use in product process.
            D.1. Get CPF file by use process from [cpf_logic.py]
        E. Repeat C by use count value from B.
        F. Get Product files.
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
    app = QApplication(sys.argv)
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Sipros_system_path = Path of all system.
        CUF_path = Local path to keep CUF File use for know data from CUF file. [look at scene_info.py]
        GERALD_keep = Network path to keep GERALD files. (* this path keep GERALD files copy from old system)
        GERALD_local = Local path for copy GERALD files from GERALD_keep for use in product process.
        GERALD_info = Local path for keep extraction files from GERALD file. (Actually those file use in All product process)
        Product_keep = Local path for keep products from product process. (Product : ICON.JPG , IMAGERY.tif , LOGO.JPG , PREVIEW.JPG
                                STYLE.XSL , PDF file.)
        CPF_directory = Path of all CPF file use in [cpf_logic process].
        CPF_index = Path of all CPF index file use in [cpf_logic process].
        Log_directory = Path for keep log files from product process.
        product_detail = Path of all command files [.cmp] create from [scene_info.py]
        * .cmp or command files use for tell about product to process [gerald directory name , beginline , grid ref , revolution number].
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
    # This in path system use on windows environment
    Sipros_system_path = "C:/Worker/Support-Worker/Sipros_system"

    # This in path system use on Sipros linux environment
    # Sipros_system_path = "/home/sipros/Application_1A_2A/Sipros_System"

    # This in path system use on Asuna linux environment
    # Sipros_system_path = "/home/asuna/worker_Lab/Sipros_System"

    CUF_path = Sipros_system_path + "/CUF_PROCESSING"

    GERALD_keep = "//172.27.188.123/thaichote_gerald/GERALD" # windows center drive
    # GERALD_keep = "/mnt/GERALD_002/GERALD" # Server center drive who keep GERALD file.
    # GERALD_keep = "/home/asuna/worker_Lab/Sipros_System/GERALD_SIM" # Asuna drive who keep GERALD file.

    GERALD_local = Sipros_system_path + "/GERALD"

    GERALD_info = Sipros_system_path + "/EXTRACTION_FILES"
    Product_keep = Sipros_system_path + "/PRODUCT_FILES"

    CPF_directory = Sipros_system_path + "/CPF_PROCESSING/CPF_FILE"
    CPF_index = Sipros_system_path + "/CPF_PROCESSING/CPF_INDEX"

    Log_path = Sipros_system_path + "/LOG"
    product_detail = Sipros_system_path + "/COMMAND_FILES"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
         Level = get value from keyboard.
            If 1 as process level 1A.
            If 2 as process level 2A.
            else program will terminated.

        CUF_zip = Call open file dialog for open zip file
        cufzip_file_path = get path of cuf file [a zip file where keep cuf and browse image]
        SI.ReadData = call function read CUF file from [scene_info.py]

        I use try except to catch error value from SI.
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
    Level = int(input("Level processing : "))
    if (Level == 1) or (Level == 2):
        pass
    else :
        sys.exit("input worng processing level.")

    try :
        CUF_zip = QFileDialog.getOpenFileName(None , "Open CUF zip File" , CUF_path , "*.zip")
        cufzip_file_path = str(CUF_zip)
        SI.ReadData(cufzip_file_path, product_detail)
        print "Finish."
    except IOError :
        QMessageBox.warning(None , "Warning !" , "Create catalog file is about by user.")
        print traceback.format_exc()
        sys.exit("Terminate becase worng CUF File type.")
    except :
         QMessageBox.critical(None , "Critical" , "Cann't open cuf file.")
         print traceback.format_exc()
         sys.exit("Terminate becase worng CUF File type.")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Browse_command_files_list = List of filename command files. [.cmp]
        Browse_command_file = Call Open file dialog for open cmp files to read command for product process

        for command_filenames is loop for get command file name from Browse_command_file

        count_command = count value of command files.
     ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
    try :
        Browse_command_files_list = []
        Browse_command_file = QFileDialog.getOpenFileNames(None,"Browse command files" ,product_detail, "*.cmp")
        for command_filenames in Browse_command_file:
            command_filename = str(command_filenames)
            Browse_command_files_list.append(command_filename)

        count_command = len(Browse_command_files_list)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            this for loop product process by count command files. It mean number of repeat product process.

            command_list = list of value in command files
            then program will be open command file and read value in command file and keep it in to command_list.
        ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
        for i in range(count_command):
            command_list = []
            open_command_file = open(Browse_command_files_list[i],"r")
            for j in range(64):
                get_pre_command = open_command_file.readline()
                pre_command = get_pre_command.strip("\n")
                command_value = str(pre_command)
                command_list.append(command_value)
            open_command_file.close()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                get valiable name for value from command file.

                Now I use {Revolution_number  , Gerald_name , SpectralMode , band_offset_Bx
                , scene_count , scene_rank , Grid_ref , Center_scene_viewing_date , Center_scene_viewing_time} for product process.

                Set condition by
                If SpectralMode = MS : dsr_begin will be list like [beginline_b1 , beginline_b2 , beginline_b3 , beginline_b4].
                If SpectralMode = PAN : dsr_begin will be int of beginline.
            ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
            # Begin_reception_date = int(command_list[0])
            # Begin_reception_time = float(command_list[1])
            # End_reception_date = int(command_list[2])
            # End_reception_time = float(command_list[3])
            # Orbit_cycle = str(command_list[4])
            Revolution_number = str(command_list[5])
            # Mission = str(command_list[6])
            # Satellite = str(command_list[7])
            # Passrank = str(command_list[8])
            # PassID = str(command_list[9])
            # Segment_count = int(command_list[10])
            # Segment_info = str(command_list[11])
            # FileName = str(command_list[12])
            Gerald_name = str(command_list[13])
            # Segment_rank = int(command_list[14])
            # Instrument = str(command_list[15])
            # Transmission_mode = str(command_list[16])
            # Segment_quality = str(command_list[17])
            # Begin_segment_viewing_date = int(command_list[18])
            # Begin_segment_viewing_time = float(command_list[19])
            # End_segment_viewing_date = int(command_list[20])
            # End_segment_viewing_time = float(command_list[21])
            # Compression_ratio = float(command_list[22])
            SpectralMode = str(command_list[23])
            band_offset_B1 = int(command_list[24])
            band_offset_B2 = int(command_list[25])
            band_offset_B3 = int(command_list[26])
            band_offset_B4 = int(command_list[27])
            # Reference_Band = str(command_list[28])
            # Along_track_viewing_angle = float(command_list[29])
            # Across_track_viewing_angle = float(command_list[30])
            # ABS_Gain = float(command_list[31])
            # scene_info = str(command_list[32])
            scene_count = int(command_list[33])
            scene_rank = int(command_list[34])
            Grid_ref = str(command_list[35])
            # Technical_quality = str(command_list[36])
            # Cloud_cover = str(command_list[37])
            # Snow_cover = str(command_list[38])
            Center_scene_viewing_date = str(command_list[39])
            Center_scene_viewing_time = str(command_list[40])
            # Begin_scene_viewing_date = int(command_list[41])
            # Begin_scene_viewing_time = float(command_list[42])
            # End_scene_viewing_date = int(command_list[43])
            # End_scene_viewing_time = float(command_list[44])
            # Coupling_mode = str(command_list[45])
            # Orientation_angle = float(command_list[46])
            # Incidence_angle = float(command_list[47])
            # Sun_elevation = float(command_list[48])
            # Sun_azimuth = float(command_list[49])
            # Latitude_NW = float(command_list[50])
            # Longitude_NW = float(command_list[51])
            # Latitude_NE = float(command_list[52])
            # Longitude_NE = float(command_list[53])
            # Latitude_SW = float(command_list[54])
            # Longitude_SW = float(command_list[55])
            # Latitude_SE = float(command_list[56])
            # Longitude_SE = float(command_list[57])
            # Center_scene_latitude = float(command_list[58])
            # Center_scene_longitude = float(command_list[59])
            if SpectralMode == "MS":
                dsr_begin = [int(command_list[60]) , int(command_list[61]) , int(command_list[62]) , int(command_list[63])]
            elif SpectralMode == "PAN":
                dsr_begin = int(command_list[60])
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                Set EXAMPLE as SpectralMode.
                job_time as time in that moment product process has start. It use to set PDF name , directory who keep product , zip file name.

                Set condition by
                if EXAMPLE = PAN
                ger_keep = GERALD directory network path.
                ger_dir = GERALD directory local path.
                Gerald_filelist = list use to get GERALD file name from [ger_keep].
                for loop to get all file in [ger_keep].
                set check in [ger_keep] has .GER file if not .GER file will show error message.

                Gerald_file_pan = GERALD file from [ger_keep].
                set condition to check has GERALD file has exist if has pass if not has program will terminated. by get error message.
            ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
            EXAMPLE = SpectralMode

            job_time = time.time()
            if EXAMPLE == "PAN":

                ger_keep = "%s/%s"%(GERALD_keep , Gerald_name)
                ger_dir = "%s/%s"%(GERALD_local , Gerald_name)
                Gerald_filelist = []
                for root , directory , files in os.walk(ger_keep , topdown = False):
                    for filename in files:
                        Gerald_filename = os.path.join(root , filename)
                        if Gerald_filename.endswith(".GER"):
                            Gerald_filelist.append(Gerald_filename)
                            Gerald_filelist.sort()
                        elif not Gerald_filename.endswith(".GER"):
                            error_value_gerald = str(traceback.format_exc())
                            print error_value_gerald
                            QMessageBox.warning(None ,"Warning", error_value_gerald)

                Gerald_file_pan = Gerald_filelist[0]
                if os.path.exists(Gerald_file_pan):
                    pass
                elif not os.path.exists(Gerald_file_pan):
                    sys.exit("Gerald file has without exist.")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    Set condition :
                    If [GERALD_local] path without Gerald directory then create directory in [GERALD_local] path as Gerald directory name.
                    Copy GERALD file in Gerald directory in [GERALD_local] path.

                    If [GERALD_local] path has Gerald directory then check has GERALD file in there
                    If Gerald directory has GERALD file pass to another process.
                    If Gerald directory without GERALD file or another file remove this Gerald directory and re create it and copy
                    GERALD file from [ger_keep] in to it

                    If process has not  work on flow show error message and terminated program.
                ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                try :
                    if not os.path.exists(ger_dir):
                        os.mkdir(ger_dir)
                        print "create gerald local"
                        shutil.copy(Gerald_file_pan , ger_dir)
                        print "copy gerald from center dirve."
                    elif os.path.exists(ger_dir):
                        for local_root , local_directory , local_files in os.walk(ger_dir , topdown = False):
                            for local_filename in local_files:
                                Gerald_local_filename = os.path.join(local_root , local_filename)
                                if Gerald_local_filename.endswith(".GER"):
                                    pass
                                elif not Gerald_local_filename.endswith(".GER"):
                                    shutil.rmtree(ger_dir)
                                    print "Delete gerald local."
                                    os.mkdir(ger_dir)
                                    print "Recreate gerald local."
                                    shutil.copy(Gerald_file_pan , ger_dir)
                                    print "copy gerald from center dirve."
                except :
                    QMessageBox.warning(None ,"Warning", str(traceback.format_exc()))
                    sys.exit(traceback.format_exc())
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                     cpf_file = root path of CPF file. [like C:/CPF/THOES_XXX_XXX.CPF]
                     cpf_name = CPF base name. [like THOES_XXX_XXX.CPF]
                     CPF process is import from [cpf_logic.py].

                     ger_info_dir = [GERALD_info] + Gerald_name.
                     If ger_info_dir has not exist create ger_info_dir in [GERALD_info].
                     If ger_info_dir has exist pass to another process.

                     out_path = [Product_keep]

                     job_ID = get job_time in UTC format.
                     job_ID_year = job_ID.tm_year {mean get year from job_ID - 2000} return 2 digit for set [pan_out_name].
                     job_ID_month = job_ID.tm_mon {mean get month from job_ID} return 2 digit for set [pan_out_name].
                     job_ID_day = job_ID.tm_mday {mean get date from job_ID} return 2 digit for set [pan_out_name].
                     job_ID_hour = job_ID.tm_hour {mean get hour from job_ID} return 2 digit for set [pan_out_name].
                     job_ID_min = job_ID.tm_min {mean get minute from job_ID} return 2 digit for set [pan_out_name].
                     job_ID_sec = job_ID.tm_sec {mean get second from job_ID} return 2 digit for set [pan_out_name].
                     job_ID_millisec = int((job_time%1)*1000) {calculate millisec from job_time} return 2 digit for set [pan_out_name].

                     call sensor type as [PAN] from class sensorType.

                     Set condition get value from keyboard.
                     If Level = 1 call processing_level from class  processingLevel as LEVEL1A and set pan_out_name =
                                        TH_CAT_[job_ID_year][job_ID_month][job_ID_day][ job_ID_hour][ job_ID_min][job_ID_sec][job_ID_millisec]_1_1P {1P mean Level 1A PAN}.

                     If Level = 2 call processing_level from class  processingLevel as LEVEL2A and set pan_out_name =
                                        TH_CAT_[job_ID_year][job_ID_month][job_ID_day][ job_ID_hour][ job_ID_min][job_ID_sec][job_ID_millisec]_1_2P {2P mean Level 2A PAN}.

                     out_dir = [out_path] + [pan_out_name].
                     If out_dir has not exist create out_dir directory.
                     If out_dir has exist delete old out_dir directory and re create out_dir.
                ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                cpf_file , cpf_name = CP.comparecufandcpf(Center_scene_viewing_date , CPF_directory , CPF_index)
                # absolute location of cpf file

                ger_info_dir = GERALD_info + "/" + Gerald_name# absolute directory containing all extracted information from ger files.
                if not os.path.exists(ger_info_dir):
                    os.mkdir(ger_info_dir)
                    print "Gerald info has create."
                elif os.path.exists(ger_info_dir):
                    print "Gerald info has already exist."
                    pass

                out_path = Product_keep # absolute directory to keep product in

                job_ID = time.gmtime(job_time)
                job_ID_year = job_ID.tm_year-2000
                job_ID_month = job_ID.tm_mon
                job_ID_day = job_ID.tm_mday
                job_ID_hour = job_ID.tm_hour
                job_ID_min = job_ID.tm_min
                job_ID_sec = job_ID.tm_sec
                job_ID_millisec = int((job_time%1)*1000)

                processSetup.sensor = sensorType.PAN

                if Level == 1:
                    processSetup.processing_level = processingLevel.LEVEL1A
                    pan_out_name = "TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec) + "_R%sP1A_%s_%s"%(Revolution_number,Center_scene_viewing_date,Center_scene_viewing_time)
                    level = "Level 1A"

                elif Level == 2:
                    processSetup.processing_level = processingLevel.LEVEL2A
                    pan_out_name = "TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec) +  "_R%sP2A_%s_%s"%(Revolution_number,Center_scene_viewing_date,Center_scene_viewing_time)
                    level = "Level 2A"

                out_dir = out_path + "/" + pan_out_name
                if not os.path.exists(out_dir):
                    os.mkdir(out_dir)
                    print "Product path has create."
                elif os.path.exists(out_dir):
                    shutil.rmtree(out_dir)
                    print "Delete old product path."
                    os.mkdir(out_dir)
                    print "Create new product path."
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    Set condition by use scene_rank and scene_count.
                    If scene_rank != scene_count set like this.
                    sceneInfo.cpf_file = give [cpf_file] in to class sceneInfo.
                    sceneInfo.ger_dir = give [ger_dir] and get it in to class sceneInfo.
                    sceneInfo.begin_lines = [dsr_begin] give beginline from command_file by list

                    sceneInfo.im_width = int 12000 is standart for PAN image product.
                    sceneInfo.im_height = int 12000 is standart for PAN image product.
                    Those two line mean PAN image has standart as 12000 X 12000.

                    sceneInfo.info_dir = [ger_info_dir] where do you want to keep extraction files.
                    sceneInfo.target_dir = [out_dir] where do you want to keep product.
                    sceneInfo.rev_num = [Revolution_number] give revolution number from command_file by string.
                    sceneInfo.grid_id = [Grid_ref] give grid reference from command_file by string.
                    sceneInfo = class that mean I set those value in class sceneInfo from here.

                    Set scene_info = class sceneInfo.
                    Set process_setup = class processSetup.
                    callProcessingSystem = activate product process function.

                    then when processing product has finish take [out_dir] to create archive process.

                    I use try except process to check the product process has working at right flow.
                    If it working well it will finish and create Success log file.
                    If it working not well the product process will not finish and it will pass to create Failure log file.
                    [Success log] = log file tell information about product.
                    [Failure log] = log file tell information about product and error message : reason product can not create.
                    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                if scene_rank != scene_count:
                    try:
                        start_time = time.clock()
                        sceneInfo.cpf_file = cpf_file
                        sceneInfo.ger_dir  = ger_dir
                        sceneInfo.begin_lines = [dsr_begin]
                        sceneInfo.im_width = 12000
                        sceneInfo.im_height = 12000
                        sceneInfo.info_dir = ger_info_dir
                        sceneInfo.target_dir = out_dir
                        sceneInfo.rev_num = Revolution_number
                        sceneInfo.grid_id = Grid_ref
                        scene_info = sceneInfo
                        process_setup = processSetup
                        callProcessingSystem(scene_info, process_setup)
                        end_time = float((time.clock() - start_time)/60)

                        os.mkdir(out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/ICON.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/PREVIEW.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/IMAGERY.tif" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/METADATA.DIM" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/STYLE.XSL" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))

                        print "Create archive."
                        shutil.make_archive(out_dir , "zip" , out_dir)
                        print "product completed."

                        Log_pan_name = Log_path + "/Success/" + pan_out_name + "_Success.log"
                        Log_pan_file = open(Log_pan_name,"w")
                        Log_pan_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_pan_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_pan_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_pan_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_pan_file.write(str(level) + "\n")
                        Log_pan_file.write("Begin line : " + str(dsr_begin) + "\n")
                        Log_pan_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_pan_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_pan_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_pan_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_pan_file.write("Status : completed.\n")
                        Log_pan_file.write("Time to use : " + str(end_time) + "mn")
                        Log_pan_file.close()

                    except:
                        Log_pan_name = Log_path + "/Failure/" + pan_out_name + "_Failure.log"
                        Log_pan_file = open(Log_pan_name,"w")
                        Log_pan_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_pan_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_pan_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_pan_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_pan_file.write(str(level) + "\n")
                        Log_pan_file.write("Begin line : " + str(dsr_begin) + "\n")
                        Log_pan_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_pan_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_pan_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_pan_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_pan_file.write("Status : uncompleted.\n")
                        Log_pan_file.write("Error value is : \n" + str(traceback.format_exc()))
                        Log_pan_file.close()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    Set condition by use scene_rank and scene_count.
                    If scene_rank = scene_count
                    [dsr_begin] in command_file is useless.

                    Calculate new begin line from GDB file so that mean you have to extract gerald befor get new begin line (in this case I recommend solution :
                    order scene befor lastscene and then order lastscene so you get extraction files then you can use GDB for calculate new begin line.)

                    Solution to calculate New_dsr_begin is like this.
                    A. Get last line of [GDB file] in extraction directory.
                    B. Then get last [word] of data from A.(this [word] is number of all line in that gerald file have or in the another word you can say
                        it is the last Gerald line can process product.)
                    C. Take data from B to find [New_dsr_begin] by this : [ Use_GDB_last_line_list[0] ](last Gerald line) - 11999 (the standart of PAN 12000 -1)
                    D. Last Use data from C to be [bandline].
                    E. Process product by [bandline].
                    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                elif scene_rank == scene_count:
                    Use_GDB_last_line_list = []
                    GDB_directory = ger_info_dir
                    for root_gdb , directory_gdb , file_gdb in os.walk(GDB_directory , topdown = False):
                        for filepath in file_gdb:
                            GDB_path = os.path.abspath(os.path.join(root_gdb , filepath))
                            if GDB_path.endswith(".gdb"):
                                GDB_data_file = open(GDB_path , "r")
                                GDB_data_list = GDB_data_file.readlines()
                                GDB_data_file.close()

                                Pre_GDB_Endline = GDB_data_list[len(GDB_data_list)-1]
                                Pre_GDB_End_line_data = Pre_GDB_Endline.split( )
                                count_Pre_GDB_End_line_data = len(Pre_GDB_End_line_data)
                                GDB_last_line = int(Pre_GDB_End_line_data[count_Pre_GDB_End_line_data - 1])
                                Use_GDB_last_line_list.append(GDB_last_line)

                    bandline = Use_GDB_last_line_list[0] - 11999  # begining line of PAN image
                    try:
                        start_time = time.clock()
                        sceneInfo.cpf_file = cpf_file
                        sceneInfo.ger_dir  = ger_dir
                        sceneInfo.begin_lines = [bandline]
                        sceneInfo.im_width = 12000
                        sceneInfo.im_height = 12000
                        sceneInfo.info_dir = ger_info_dir
                        sceneInfo.target_dir = out_dir
                        sceneInfo.rev_num = Revolution_number
                        sceneInfo.grid_id = Grid_ref
                        scene_info = sceneInfo
                        process_setup = processSetup
                        callProcessingSystem(scene_info, process_setup)
                        end_time = float((time.clock() - start_time)/60)

                        os.mkdir(out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/ICON.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/PREVIEW.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/IMAGERY.tif" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/METADATA.DIM" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/STYLE.XSL" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))

                        print "Create archive."
                        shutil.make_archive(out_dir , "zip" , out_dir)
                        print "product completed."

                        Log_pan_name = Log_path + "/Success/" + pan_out_name + "_Success.log"
                        Log_pan_file = open(Log_pan_name,"w")
                        Log_pan_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_pan_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_pan_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_pan_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_pan_file.write(str(level) + "\n")
                        Log_pan_file.write("Begin line : " + str(bandline) + "\n")
                        Log_pan_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_pan_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_pan_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_pan_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_pan_file.write("Status : completed.\n")
                        Log_pan_file.write("Time to use : " + str(end_time) + "mn")
                        Log_pan_file.close()

                    except:
                        Log_pan_name = Log_path + "/Failure/" + pan_out_name + "_Failure.log"
                        Log_pan_file = open(Log_pan_name,"w")
                        Log_pan_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_pan_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_pan_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_pan_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_pan_file.write(str(level) + "\n")
                        Log_pan_file.write("Begin line : " + str(bandline) + "\n")
                        Log_pan_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_pan_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_pan_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_pan_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_pan_file.write("Status : uncompleted.\n")
                        Log_pan_file.write("Error value is : \n" + str(traceback.format_exc()))
                        Log_pan_file.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                if EXAMPLE = MS
                ger_keep = GERALD directory network path.
                ger_dir = GERALD directory local path.
                Gerald_filelist = list use to get GERALD file name from [ger_keep].
                for loop to get all file in [ger_keep].
                set check in [ger_keep] has .GER file if not .GER file will show error message.

                Gerald_file_Bx = GERALD file from GERALD directory.[Gerald_filelist has 4 files in MS so x is (1 - 4)]
                set condition to check has GERALD file has exist if has pass if not has program will terminated. by get error message.
                ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
            elif EXAMPLE == "MS":
                ger_keep = GERALD_keep + "/" + Gerald_name
                ger_dir = GERALD_local + "/" + Gerald_name
                Gerald_filelist = []
                for root , directory , files in os.walk(ger_keep , topdown = False):
                    for filename in files:
                        Gerald_filename = os.path.join(root , filename)
                        if Gerald_filename.endswith(".GER"):
                            Gerald_filelist.append(Gerald_filename)
                            Gerald_filelist.sort()
                        elif not Gerald_filename.endswith(".GER"):
                            error_value_gerald = str(traceback.format_exc())
                            print error_value_gerald
                            QMessageBox.warning(None ,"Warning", error_value_gerald)

                Gerald_file_B1 = Gerald_filelist[0]
                Gerald_file_B2 = Gerald_filelist[1]
                Gerald_file_B3 = Gerald_filelist[2]
                Gerald_file_B4 = Gerald_filelist[3]

                print "%s\n%s\n%s\n%s"%(Gerald_file_B1,Gerald_file_B2,Gerald_file_B3,Gerald_file_B4)

                if (os.path.exists(Gerald_file_B1)) and (os.path.exists(Gerald_file_B2)) and (os.path.exists(Gerald_file_B3)) and (os.path.exists(Gerald_file_B4)):
                    pass
                elif not (os.path.exists(Gerald_file_B1) and os.path.exists(Gerald_file_B2) and os.path.exists(Gerald_file_B3) and os.path.exists(Gerald_file_B4)):
                    sys.exit("Gerald file without exist.")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    Set condition :
                    If [GERALD_local] path without Gerald directory then create directory in [GERALD_local] path as Gerald directory name.
                    Copy GERALD file in Gerald directory in [GERALD_local] path.

                    If [GERALD_local] path has Gerald directory then check has GERALD file in there
                    If Gerald directory has GERALD file pass to another process.
                    If Gerald directory without GERALD file or another file remove this Gerald directory and re create it and copy
                    GERALD file from [ger_keep] in to it

                    If process has not  work on flow show error message and terminated program.
                    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                try :
                    if not os.path.exists(ger_dir):
                        os.mkdir(ger_dir)
                        print "create gerald local"
                        shutil.copy(Gerald_file_B1 , ger_dir)
                        print "copy gerald band 1 from center dirve."
                        shutil.copy(Gerald_file_B2 , ger_dir)
                        print "copy gerald band 2 from center dirve."
                        shutil.copy(Gerald_file_B3 , ger_dir)
                        print "copy gerald band 3 from center dirve."
                        shutil.copy(Gerald_file_B4 , ger_dir)
                        print "copy gerald band 4 from center dirve."

                    elif os.path.exists(ger_dir):
                        for local_root , local_directory , local_files in os.walk(ger_dir , topdown = False):
                            for local_filename in local_files:
                                Gerald_local_filename = os.path.join(local_root , local_filename)
                                if Gerald_local_filename.endswith(".GER"):
                                    pass
                                elif not Gerald_local_filename.endswith(".GER"):
                                    shutil.rmtree(ger_dir)
                                    print "Delete gerald local."
                                    os.mkdir(ger_dir)
                                    print "Recreate gerald local."
                                    shutil.copy(Gerald_file_B1 , ger_dir)
                                    print "copy gerald band 1 from center dirve."
                                    shutil.copy(Gerald_file_B2 , ger_dir)
                                    print "copy gerald band 2 from center dirve."
                                    shutil.copy(Gerald_file_B3 , ger_dir)
                                    print "copy gerald band 3 from center dirve."
                                    shutil.copy(Gerald_file_B4 , ger_dir)
                                    print "copy gerald band 4 from center dirve."
                except :
                    QMessageBox.warning(None ,"Warning", str(traceback.format_exc()))
                    sys.exit(traceback.format_exc())
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                     cpf_file = root path of CPF file. [like C:/CPF/THOES_XXX_XXX.CPF]
                     cpf_name = CPF base name. [like THOES_XXX_XXX.CPF]
                     CPF process is import from [cpf_logic.py].

                     ger_info_dir = [GERALD_info] + Gerald_name.
                     If ger_info_dir has not exist create ger_info_dir in [GERALD_info].
                     If ger_info_dir has exist pass to another process.

                     out_path = [Product_keep]

                     job_ID = get job_time in UTC format.
                     job_ID_year = job_ID.tm_year {mean get year from job_ID - 2000} return 2 digit for set [ms_out_name].
                     job_ID_month = job_ID.tm_mon {mean get month from job_ID} return 2 digit for set [ms_out_name].
                     job_ID_day = job_ID.tm_mday {mean get date from job_ID} return 2 digit for set [ms_out_name].
                     job_ID_hour = job_ID.tm_hour {mean get hour from job_ID} return 2 digit for set [ms_out_name].
                     job_ID_min = job_ID.tm_min {mean get minute from job_ID} return 2 digit for set [ms_out_name].
                     job_ID_sec = job_ID.tm_sec {mean get second from job_ID} return 2 digit for set [ms_out_name].
                     job_ID_millisec = int((job_time%1)*1000) {calculate millisec from job_time} return 2 digit for set [ms_out_name].

                     call sensor type as [MS] from class sensorType.

                     Set condition get value from keyboard.
                     If Level = 1 call processing_level from class  processingLevel as LEVEL1A and set ms_out_name =
                                        TH_CAT_[job_ID_year][job_ID_month][job_ID_day][ job_ID_hour][ job_ID_min][job_ID_sec][job_ID_millisec]_1_1M {1M mean Level 1A MS}.

                     If Level = 2 call processing_level from class  processingLevel as LEVEL2A and set ms_out_name =
                                        TH_CAT_[job_ID_year][job_ID_month][job_ID_day][ job_ID_hour][ job_ID_min][job_ID_sec][job_ID_millisec]_1_2M {2M mean Level 2A MS}.

                     out_dir = [out_path] + [ms_out_name].
                     If out_dir has not exist create out_dir directory.
                     If out_dir has exist delete old out_dir directory and re create out_dir.
                ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                cpf_file , cpf_name = CP.comparecufandcpf(Center_scene_viewing_date , CPF_directory , CPF_index)

                ger_info_dir = GERALD_info + "/" + Gerald_name
                if not os.path.exists(ger_info_dir):
                    os.mkdir(ger_info_dir)
                    print "Gerald info has create."
                elif os.path.exists(ger_info_dir):
                    print "Gerald info has already exist."
                    pass

                out_path = Product_keep

                job_ID = time.gmtime(job_time)
                job_ID_year = job_ID.tm_year-2000
                job_ID_month = job_ID.tm_mon
                job_ID_day = job_ID.tm_mday
                job_ID_hour = job_ID.tm_hour
                job_ID_min = job_ID.tm_min
                job_ID_sec = job_ID.tm_sec
                job_ID_millisec = int((job_time%1)*1000)

                processSetup.sensor = sensorType.MS

                if Level == 1:
                    processSetup.processing_level = processingLevel.LEVEL1A
                    ms_out_name = "TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec) + "_R%sM1A_%s_%s"%(Revolution_number,Center_scene_viewing_date,Center_scene_viewing_time)
                    level = "Level 1A"

                elif Level == 2:
                    processSetup.processing_level = processingLevel.LEVEL2A
                    ms_out_name = "TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec) + "_R%sM2A_%s_%s"%(Revolution_number,Center_scene_viewing_date,Center_scene_viewing_time)
                    level = "Level 2A"

                out_dir = out_path + "/" + ms_out_name
                if not os.path.exists(out_dir):
                    os.mkdir(out_dir)
                    print "Product path has create."
                elif os.path.exists(out_dir):
                    shutil.rmtree(out_dir)
                    print "Delete old product path."
                    os.mkdir(out_dir)
                    print "Create new product path."
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    Set condition by use scene_rank and scene_count.
                    If scene_rank != scene_count set like this.
                    sceneInfo.cpf_file = give [cpf_file] in to class sceneInfo.
                    sceneInfo.ger_dir = give [ger_dir] and get it in to class sceneInfo.
                    sceneInfo.begin_lines = [dsr_begin] give beginline from command_file by list

                    sceneInfo.im_width = int 6000 is standart for MS image product.
                    sceneInfo.im_height = int 6000 is standart for MS image product.
                    Those two line mean MS image has standart as 6000 X 6000.

                    sceneInfo.info_dir = [ger_info_dir] where do you want to keep extraction files.
                    sceneInfo.target_dir = [out_dir] where do you want to keep product.
                    sceneInfo.rev_num = [Revolution_number] give revolution number from command_file by string.
                    sceneInfo.grid_id = [Grid_ref] give grid reference from command_file by string.
                    sceneInfo = class that mean I set those value in class sceneInfo from here.

                    Set scene_info = class sceneInfo.
                    Set process_setup = class processSetup.
                    callProcessingSystem = activate product process function.

                    then when processing product has finish take [out_dir] to create archive process.

                    I use try except process to check the product process has working at right flow.
                    If it working well it will finish and create Success log file.
                    If it working not well the product process will not finish and it will pass to create Failure log file.
                    [Success log] = log file tell information about product.
                    [Failure log] = log file tell information about product and error message : reason product can not create.
                ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                if scene_rank != scene_count:
                    try:
                        start_time = time.clock()
                        sceneInfo.cpf_file = cpf_file
                        sceneInfo.ger_dir  = ger_dir
                        sceneInfo.begin_lines = dsr_begin
                        sceneInfo.im_width = 6000
                        sceneInfo.im_height = 6000
                        sceneInfo.info_dir = ger_info_dir
                        sceneInfo.target_dir = out_dir
                        sceneInfo.rev_num = Revolution_number
                        sceneInfo.grid_id = Grid_ref
                        scene_info = sceneInfo
                        process_setup = processSetup
                        callProcessingSystem(scene_info, process_setup)
                        end_time = float((time.clock() - start_time)/60.0)

                        os.mkdir(out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/ICON.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/PREVIEW.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/IMAGERY.tif" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/METADATA.DIM" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/STYLE.XSL" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))

                        print "Create archive."
                        shutil.make_archive(out_dir , "zip" , out_dir)
                        print "product completed."

                        Log_ms_name = Log_path + "/Success/" + ms_out_name + "_Success.log"
                        Log_ms_file = open(Log_ms_name,"w")
                        Log_ms_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_ms_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_ms_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_ms_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_ms_file.write(str(level) + "\n")
                        Log_ms_file.write("Begin line : " + str(dsr_begin) + "\n")
                        Log_ms_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_ms_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_ms_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_ms_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_ms_file.write("Status : completed.\n")
                        Log_ms_file.write("Time to use : " + str(end_time) + "mn")
                        Log_ms_file.close()

                    except :
                        Log_ms_name = Log_path + "/Failure/" + ms_out_name + "_Failure.log"
                        Log_ms_file = open(Log_ms_name,"w")
                        Log_ms_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_ms_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_ms_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_ms_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_ms_file.write(str(level) + "\n")
                        Log_ms_file.write("Begin line : " + str(dsr_begin) + "\n")
                        Log_ms_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_ms_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_ms_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_ms_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_ms_file.write("Status : uncompleted.\n")
                        Log_ms_file.write("Error value is : \n" + str(traceback.format_exc()))
                        Log_ms_file.close()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    """/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    Set condition by use scene_rank and scene_count.
                    If scene_rank = scene_count
                    [dsr_begin] in command_file is useless.

                    Calculate new begin line from band 4 GDB file so that mean you have to extract gerald befor get new begin line (in this case I recommend solution :
                    order scene befor lastscene and then order lastscene so you get extraction files then you can use band 4 GDB for calculate new begin line.)

                    Solution to calculate New_dsr_begin is like this.
                    A. Get last line of [band 4 GDB file] in extraction directory.
                    B. Then get last [word] of data from A.(this [word] is number of all line in that gerald file have or in the another word you can say
                        it is the last Gerald line can process product.)
                    C. Take data from B to find [New_dsr_begin] by this : [ Use_GDB_last_line_list[0] ](last Gerald line) - 5999 (the standart of PAN 6000 -1)
                    D. Last Use data from C to be [New_dsr_begin_B4].
                    F. Find [New_dsr_begin_B3] by use [New_dsr_beginB4] - [band_offset_B4] .
                    G. Find [New_dsr_begin_B2] by use [New_dsr_beginB3] + [band_offset_B2] .
                    H. Find [New_dsr_begin_B1] by use [New_dsr_beginB3] + [band_offset_B1] .
                    I. Get [New_dsr_begin_Bx ] into list name [bandlines].
                    J.Process product by [bandlines].
                    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
                elif scene_rank == scene_count:
                    Use_GDB_last_line_list = []
                    GDB_directory = ger_info_dir
                    for root_gdb , directory_gdb , file_gdb in os.walk(GDB_directory , topdown = False):
                        for filepath in file_gdb:
                            GDB_path = os.path.abspath(os.path.join(root_gdb , filepath))
                            if GDB_path.endswith("B4.gdb"):
                                GDB_data_file = open(GDB_path , "r")
                                GDB_data_list = GDB_data_file.readlines()
                                GDB_data_file.close()

                                Pre_GDB_Endline = GDB_data_list[len(GDB_data_list)-1]
                                Pre_GDB_End_line_data = Pre_GDB_Endline.split( )
                                count_Pre_GDB_End_line_data = len( Pre_GDB_End_line_data)
                                GDB_last_line = int(Pre_GDB_End_line_data[count_Pre_GDB_End_line_data - 1])
                                Use_GDB_last_line_list.append(GDB_last_line)

                    New_dsr_beginB4 = Use_GDB_last_line_list[0] - 5999
                    New_dsr_beginB3 = New_dsr_beginB4 - band_offset_B4
                    New_dsr_beginB2 = New_dsr_beginB3 + band_offset_B2
                    New_dsr_beginB1 = New_dsr_beginB3 + band_offset_B1

                    bandlines = [New_dsr_beginB1 , New_dsr_beginB2 , New_dsr_beginB3 , New_dsr_beginB4]  # begining line of MS image

                    try:
                        start_time = time.clock()
                        sceneInfo.cpf_file = cpf_file
                        sceneInfo.ger_dir  = ger_dir
                        sceneInfo.begin_lines = bandlines
                        sceneInfo.im_width = 6000
                        sceneInfo.im_height = 6000
                        sceneInfo.info_dir = ger_info_dir
                        sceneInfo.target_dir = out_dir
                        sceneInfo.rev_num = Revolution_number
                        sceneInfo.grid_id = Grid_ref
                        scene_info = sceneInfo
                        process_setup = processSetup
                        callProcessingSystem(scene_info, process_setup)
                        end_time = float((time.clock() - start_time)/60.0)

                        os.mkdir(out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/ICON.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/PREVIEW.JPG" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/IMAGERY.tif" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/METADATA.DIM" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))
                        shutil.move(out_dir + "/STYLE.XSL" , out_dir + "/TH_CAT_%02d%02d%02d"%(job_ID_year , job_ID_month , job_ID_day) + "%02d%02d%02d%03d"%(job_ID_hour , job_ID_min , job_ID_sec , job_ID_millisec))

                        print "Create archive."
                        shutil.make_archive(out_dir , "zip" , out_dir)
                        print "product completed."

                        Log_ms_name = Log_path + "/Success/" + ms_out_name + "_Success.log"
                        Log_ms_file = open(Log_ms_name,"w")
                        Log_ms_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_ms_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_ms_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_ms_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_ms_file.write(str(level) + "\n")
                        Log_ms_file.write("Begin line : " + str(bandlines) + "\n")
                        Log_ms_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_ms_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_ms_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_ms_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_ms_file.write("Status : completed.\n")
                        Log_ms_file.write("Time to use : " + str(end_time) + "mn")
                        Log_ms_file.close()

                    except:
                        Log_ms_name = Log_path + "/Failure/" + ms_out_name + "_Failure.log"
                        Log_ms_file = open(Log_ms_name,"w")
                        Log_ms_file.write("Revolution : " +str(Revolution_number) + "\n")
                        Log_ms_file.write("Gerald directory name : " + str(Gerald_name) + "\n")
                        Log_ms_file.write("Spectral Mode : " + str(SpectralMode) + "\n")
                        Log_ms_file.write("CPF file : " + str(cpf_name) + "\n")
                        Log_ms_file.write(str(level) + "\n")
                        Log_ms_file.write("Begin line : " + str(bandlines) + "\n")
                        Log_ms_file.write("Scene rank : " + str(scene_rank) + "\n")
                        Log_ms_file.write("Date : " + str(Center_scene_viewing_date) + "\n")
                        Log_ms_file.write("Time : " + str(Center_scene_viewing_time) + "\n")
                        Log_ms_file.write("Grid ref : " + str(Grid_ref) + "\n")
                        Log_ms_file.write("Status : uncompleted.\n")
                        Log_ms_file.write("Error value is : \n" + str(traceback.format_exc()))
                        Log_ms_file.close()

    except IOError :
        QMessageBox.warning(None , "Warnig" , "Command abort by User.")

    except:
        error_value_process = str(traceback.format_exc())
        QMessageBox.warning(None ,"Warning", error_value_process)

    sys.exit("End Process.")
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
