from PyQt4.QtGui import QApplication , QFileDialog , QMessageBox
import os , shutil , traceback , cv2 , zipfile
import sys
import xml.dom.minidom
import utm
import numpy as np

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
								{ Slave function	}
This function use to extract zip file who keep CUF file and Browse strip images. To make this function  work  you have to get
2 thing to it.

[cufzip_file_path] = CUF zip file full path.
[Product_detail] = Path where you want extract CUF zip file.

The operator of this function.
A. Locate CUF zip file path.
B. Set extract directory path.
C. Check extract directory path has exist.
If extract directory path has not exist. Create extract directory.
If extract directory path has exist. Delete old extract directory and re-create extract directory.
D. Open CUF zip file and extract zip file in extract directory.
F. Return CUF file path and extract directory.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
def cufopertor(cufzip_file_path , Product_detail):
	cufzipfile = cufzip_file_path
	cufzipdir = Product_detail + "/Extract_CUF"
	if not os.path.exists(cufzipdir):
		os.mkdir(cufzipdir)
	elif os.path.exists(cufzipdir):
		shutil.rmtree(cufzipdir)
		os.mkdir(cufzipdir)

	zip_file = open(cufzipfile , "rb")
	cuf_file = zipfile.ZipFile(zip_file)
	for fileread in cuf_file.namelist():
		cuf_file.extractall(cufzipdir)
	zip_file.close()

	for cuf_root , cuf_directory , cuf_filename in os.walk(cufzipdir , topdown=False):
		for cuf_name in cuf_filename :
			if cuf_name.endswith(".CUF"):
				cuf_path = os.path.abspath(os.path.join(cuf_root , cuf_name))
			else : pass

	return  cuf_path , cufzipdir
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""/------------------------------------------------------------------------------------------------------------------------------------------------------------------------
								{ Master function }
This function use to  get catalog date from CUF file for generate command files[.cmp] and cut browse files from strip to scene by scene.
To make this function work you have to get 2 thing to it.
[cufzip_file_path] = CUF zip file full path.
[Product_detail] = Path where you create command files.

The operator of this function.
A. Get return from cufopertor function.
B.  Read value from CUF file.
C. Create command files.
D. Create browse image files {by scene} from browse image files {by strip}.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
def ReadData(cufzip_file_path , Product_detail) :

	print "\nCreate command files [.cmp] from Catalog file."

	cuf_file , cufdir = cufopertor(cufzip_file_path , Product_detail)
	# Get CUF file and extract path from cufopertor function.

	"""/-------------------------------------------------------------------------------------------------------------------------------------------------------------
	Get CUF file for return document handler.
	Get root document.

	Fix directory path to keep command files.
	Set condition.
	If path to keep command files has not exist script will create that directory.
	If path to keep command files has exist script will delete that and recreate it.
	-------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
	CUF_Data = xml.dom.minidom.parse(cuf_file)
	root_CUF = CUF_Data.documentElement

	FIlename_path = Product_detail + "/Filename"
	Date_time_path = Product_detail + "/Date_time"
	Corner_path = Product_detail + "/Lat_long_4Corner"
	Center_path = Product_detail + "/Lat_long_Center"

	if not os.path.exists(FIlename_path):
		os.mkdir(FIlename_path)
	elif os.path.exists(FIlename_path):
		shutil.rmtree(FIlename_path)
		os.mkdir(FIlename_path)

	if not os.path.exists(Date_time_path):
		os.mkdir(Date_time_path)
	elif os.path.exists(Date_time_path):
		shutil.rmtree(Date_time_path)
		os.mkdir(Date_time_path)

	if not os.path.exists(Corner_path):
		os.mkdir(Corner_path)
	elif os.path.exists(Corner_path):
		shutil.rmtree(Corner_path)
		os.mkdir(Corner_path)

	if not os.path.exists(Center_path):
		os.mkdir(Center_path)
	elif os.path.exists(Center_path):
		shutil.rmtree(Center_path)
		os.mkdir(Center_path)

	"""/-------------------------------------------------------------------------------------------------------------------------------------------------------------
	Get root document element from CUF file.

	create list name [SceneCount_list] for keep total scene count in this CUF file.
	-------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
	# Get revolution number from CUF file.
	Pre_RevolutionNumber = root_CUF.getElementsByTagName("revolutionNumber")[0]
	Pre_RevolutionNumber_unicode = Pre_RevolutionNumber.childNodes[0].data
	Pre_RevolutionNumber_value = Pre_RevolutionNumber_unicode.strip("\n")
	RevolutionNumber_value = str(Pre_RevolutionNumber_value)

	# Get mission from CUF file.
	Pre_Mission = root_CUF.getElementsByTagName("mission")[0]
	Pre_Mission_unicode = Pre_Mission.childNodes[0].data
	Pre_Mission_value = Pre_Mission_unicode.strip("\n")
	Mission_value = str(Pre_Mission_value)

	# Get satellite Id from CUF file.
	Pre_SatelliteIdt = root_CUF.getElementsByTagName("satelliteIdt")[0]
	Pre_SatelliteIdt_unicode = Pre_SatelliteIdt.childNodes[0].data
	Pre_SatelliteIdt_value = Pre_SatelliteIdt_unicode.strip("\n")
	SatelliteIdt_value = str(Pre_SatelliteIdt_value)

	# Get pass rank from CUF file
	Pre_PassRank = root_CUF.getElementsByTagName("passRank")[0]
	Pre_PassRank_unicode = Pre_PassRank.childNodes[0].data
	Pre_PassRank_value = Pre_PassRank_unicode.strip("\n")
	PassRank_value = str(Pre_PassRank_value)

	# Get pass Id from CUF file
	Pre_PassId = root_CUF.getElementsByTagName("passId")[0]
	Pre_PassId_unicode = Pre_PassId.childNodes[0].data
	Pre_PassId_value = Pre_PassId_unicode.strip("\n")
	PassId_value = str(Pre_PassId_value)

	# Get begin downlink time from CUF file.
	Pre_BeginReception = root_CUF.getElementsByTagName("beginReception")[0]
	Pre_BeginReception_unicode = Pre_BeginReception.childNodes[0].data
	Pre_BeginReception_value = Pre_BeginReception_unicode.strip("\n")
	BeginReception_value = str(Pre_BeginReception_value)
	BeginReception_year = str(BeginReception_value[:-14])
	BeginReception_month = str(BeginReception_value[4:-12])
	BeginReception_date = str(BeginReception_value[6:-10])
	BeginReception_hour = str(BeginReception_value[8:-8])
	BeginReception_min = str(BeginReception_value[10:-6])
	BeginReception_sec = str(BeginReception_value[12:])

	# Get end downlink time from CUF file.
	Pre_EndReception = root_CUF.getElementsByTagName("endReception")[0]
	Pre_EndReception_unicode = Pre_EndReception.childNodes[0].data
	Pre_EndReception_value = Pre_EndReception_unicode.strip("\n")
	EndReception_value = str(Pre_EndReception_value)
	EndReception_year = str(EndReception_value[:-14])
	EndReception_month = str(EndReception_value[4:-12])
	EndReception_date = str(EndReception_value[6:-10])
	EndReception_hour = str(EndReception_value[8:-8])
	EndReception_min = str(EndReception_value[10:-6])
	EndReception_sec = str(EndReception_value[12:])

	# Get orbit number from CUF file.
	Pre_OrbitCycle = root_CUF.getElementsByTagName("orbitCycle")[0]
	Pre_OrbitCycle_unicode = Pre_OrbitCycle.childNodes[0].data
	Pre_OrbitCycle_value = Pre_OrbitCycle_unicode.strip("\n")
	OrbitCycle_value = str(Pre_OrbitCycle_value)

	# Get Segment count from CUF file
	Pre_SegmentCount = root_CUF.getElementsByTagName("segmentsCount")[0]
	Pre_SegmentCount_unicode = Pre_SegmentCount.childNodes[0].data
	Pre_SegmentCount_value = Pre_SegmentCount_unicode.strip("\n")
	SegmentCount_value = int(Pre_SegmentCount_value)

	SceneCount_list = []

	"""/-------------------------------------------------------------------------------------------------------------------------------------------------------------
	Set Segment to root tag by use tag segment from CUF file for use for loop.
	Get value from Segment loop.
	A. Get spectral mode from CUF file.
	B. Get  browse image filename for get browse image file path {image by strip}.
	C. Use spectral mode for set condition.
	-------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
	Segment = root_CUF.getElementsByTagName("segment")
	for segment in Segment:

		# Get SpectralMode from CUF file to use it split MS or PAN
		Pre_SpectralMode = segment.getElementsByTagName("spectralMode")[0]
		Pre_SpectralMode_unicode = Pre_SpectralMode.childNodes[0].data
		Pre_SpectralMode_value = Pre_SpectralMode_unicode.strip("\n")
		SpectralMode_value = str(Pre_SpectralMode_value)

		Pre_browseFileName = segment.getElementsByTagName("browseFileName")[0]
		Pre_browseFileName_unicode = Pre_browseFileName.childNodes[0].data
		Pre_browseFileName_value = Pre_browseFileName_unicode.strip("\n")
		browseFileName_value = cufdir + "/" + str(os.path.basename(cufzip_file_path)).strip(".zip") + "/" + str(Pre_browseFileName_value)

		# If spectral mode = MS
		if SpectralMode_value == "MS":

			# Get Gerald filename from CUF file.
			Pre_FileNameMS = segment.getElementsByTagName("fileName")[0]
			Pre_FileNameMS_unicode = Pre_FileNameMS.childNodes[0].data
			Pre_FileNameMS_value = Pre_FileNameMS_unicode.strip("\n")
			FileNameMS_value = str(Pre_FileNameMS_value)

			# Get segment rank from CUF file.
			Pre_MSSegmentRank = segment.getElementsByTagName("segmentRank")[0]
			Pre_MSSegmentRank_unicode = Pre_MSSegmentRank.childNodes[0].data
			Pre_MSSegmentRank_value = Pre_MSSegmentRank_unicode.strip("\n")
			MSSegmentRank_value = int(Pre_MSSegmentRank_value)

			# Get transmissionMode from CUF file.
			Pre_TransmissionModeMS = segment.getElementsByTagName("transmissionMode")[0]
			Pre_TransmissionModeMS_unicode = Pre_TransmissionModeMS.childNodes[0].data
			Pre_TransmissionModeMS_value = Pre_TransmissionModeMS_unicode.strip("\n")
			TransmissionModeMS_value = str(Pre_TransmissionModeMS_value)

			# Get instrument type from CUF file.
			Pre_InstrumentTypeMS = segment.getElementsByTagName("instrumentType")[0]
			Pre_InstrumentTypeMS_unicode = Pre_InstrumentTypeMS.childNodes[0].data
			Pre_InstrumentTypeMS_value = Pre_InstrumentTypeMS_unicode.strip("\n")
			InstrumentTypeMS_value = str(Pre_InstrumentTypeMS_value)

			# Get instrument ID from CUF file.
			Pre_InstrumentIDMS = segment.getElementsByTagName("instrumentIdt")[0]
			Pre_InstrumentIDMS_unicode = Pre_InstrumentIDMS.childNodes[0].data
			Pre_InstrumentIDMS_value = Pre_InstrumentIDMS_unicode.strip("\n")
			InstrumentIDMS_value = str(Pre_InstrumentIDMS_value)

			# Get segment quality from CUF file
			Pre_MSsegmenquality = segment.getElementsByTagName("segmentQuality")[0]
			Pre_MSsegmenquality_unicode = Pre_MSsegmenquality.childNodes[0].data
			Pre_MSsegmenquality_value = Pre_MSsegmenquality_unicode.strip("\n")
			MSsegmentquality_value = str(Pre_MSsegmenquality_value)

			#  Get begin {year , month , date , hour , minute} from begin viewing date in CUF file.
			Pre_BeginViewingDateMS_segment = segment.getElementsByTagName("beginViewingDate")[0]
			Pre_BeginViewingDateMS_segment_unicode = Pre_BeginViewingDateMS_segment.childNodes[0].data
			Pre_BeginViewingDateMS_segment_value = Pre_BeginViewingDateMS_segment_unicode.strip("\n")
			BeginViewingDateMS_segment_value = str(Pre_BeginViewingDateMS_segment_value)

			Pre_YearMS_segment = BeginViewingDateMS_segment_value [:4]
			YearMS_segment = str(Pre_YearMS_segment)

			Pre_MonthMS_segment = BeginViewingDateMS_segment_value [4:6]
			MonthMS_segment = str(Pre_MonthMS_segment)

			Pre_DateMS_segment = BeginViewingDateMS_segment_value [6:8]
			DateMS_segment = str(Pre_DateMS_segment)

			Pre_HourMS_segment = BeginViewingDateMS_segment_value [8:10]
			HourMS_segment = str(Pre_HourMS_segment)

			Pre_MinMS_segment = BeginViewingDateMS_segment_value [10:12]
			MinMS_segment = str(Pre_MinMS_segment)

			Pre_SecMS_segment = BeginViewingDateMS_segment_value [12:14]
			SecMS_segment = str(Pre_SecMS_segment)

			#  Get end {year , month , date , hour , minute} from end viewing date in CUF file.
			Pre_EndViewingDateMS_segment = segment.getElementsByTagName("endViewingDate")[0]
			Pre_EndViewingDateMS_segment_unicode = Pre_EndViewingDateMS_segment.childNodes[0].data
			Pre_EndViewingDateMS_segment_value = Pre_EndViewingDateMS_segment_unicode.strip("\n")
			EndViewingDateMS_segment_value = str(Pre_EndViewingDateMS_segment_value)

			Pre_EndYearMS_segment = EndViewingDateMS_segment_value [:4]
			EndYearMS_segment = str(Pre_EndYearMS_segment)

			Pre_EndMonthMS_segment = EndViewingDateMS_segment_value [4:6]
			EndMonthMS_segment = str(Pre_EndMonthMS_segment)

			Pre_EndDateMS_segment = EndViewingDateMS_segment_value [6:8]
			EndDateMS_segment = str(Pre_EndDateMS_segment)

			Pre_EndHourMS_segment = EndViewingDateMS_segment_value [8:10]
			EndHourMS_segment = str(Pre_EndHourMS_segment)

			Pre_EndMinMS_segment = EndViewingDateMS_segment_value [10:12]
			EndMinMS_segment = str(Pre_EndMinMS_segment)

			Pre_EndSecMS_segment = EndViewingDateMS_segment_value [12:14]
			EndSecMS_segment = str(Pre_EndSecMS_segment)

			#Get image com pression ratio from CUF file.
			Pre_MSCompression_ratio = segment.getElementsByTagName("compressionRatio")[0]
			Pre_MSCompression_ratio_unicode = Pre_MSCompression_ratio.childNodes[0].data
			Pre_MSCompression_ratio_value = Pre_MSCompression_ratio_unicode.strip("\n")
			MSCompression_ratio_value = str(Pre_MSCompression_ratio_value)

			#Get reference band from CUF file.
			Pre_MSReferenceBand = segment.getElementsByTagName("referenceBand")[0]
			Pre_MSReferenceBand_unicode = Pre_MSReferenceBand.childNodes[0].data
			Pre_MSReferenceBand_value = Pre_MSReferenceBand_unicode.strip("\n")
			MSReferenceBand_value = str(Pre_MSReferenceBand_value)

			#Get along track viewing angle from CUF file.
			Pre_MS_Alongtrackviewingangle = segment.getElementsByTagName("alongTrackViewingAngle")[0]
			Pre_MS_Alongtrackviewingangle_unicode = Pre_MS_Alongtrackviewingangle.childNodes[0].data
			Pre_MS_Alongtrackviewingangle_value = Pre_MS_Alongtrackviewingangle_unicode.strip("\n")
			MS_Alongtrackviewingangle_value = str(Pre_MS_Alongtrackviewingangle_value)

			#Get across track viewing angle from CUF file.
			Pre_MS_Acrosstrackviewingangle = segment.getElementsByTagName("acrossTrackViewingAngle")[0]
			Pre_MS_Acrosstrackviewingangle_unicode = Pre_MS_Acrosstrackviewingangle.childNodes[0].data
			Pre_MS_Acrosstrackviewingangle_value = Pre_MS_Acrosstrackviewingangle_unicode.strip("\n")
			MS_Acrosstrackviewingangle_value = str(Pre_MS_Acrosstrackviewingangle_value)

			#Get absolut gain from CUF file.
			Pre_MS_ABSGain = segment.getElementsByTagName("absGain")[0]
			Pre_MS_ABSGain_unicode = Pre_MS_ABSGain.childNodes[0].data
			Pre_MS_ABSGain_value = Pre_MS_ABSGain_unicode.strip("\n")
			MS_ABSGain_value = str(Pre_MS_ABSGain_value)

			#In MS we use Offset from CUF file in product process so then we create list name [Offset_value] for keep band offset.
			Offset_value = []

			# Get offset band 1 from CUF file.
			Pre_Offset_1 = segment.getElementsByTagName("offsetB1")[0]
			Pre_Offset_1_unicode = Pre_Offset_1.childNodes[0].data
			Pre_Offset_1_value = Pre_Offset_1_unicode.strip("\n")
			Offset_1_value = int(Pre_Offset_1_value)

			# Get offset band 2 from CUF file.
			Pre_Offset_2 = segment.getElementsByTagName("offsetB2")[0]
			Pre_Offset_2_unicode = Pre_Offset_2.childNodes[0].data
			Pre_Offset_2_value = Pre_Offset_2_unicode.strip("\n")
			Offset_2_value = int(Pre_Offset_2_value)

			# Get offset band 3 from CUF file.
			Pre_Offset_3 = segment.getElementsByTagName("offsetB3")[0]
			Pre_Offset_3_unicode = Pre_Offset_3.childNodes[0].data
			Pre_Offset_3_value = Pre_Offset_3_unicode.strip("\n")
			Offset_3_value = int(Pre_Offset_3_value)

			# Get offset band 4 from CUF file.
			Pre_Offset_4 = segment.getElementsByTagName("offsetB4")[0]
			Pre_Offset_4_unicode = Pre_Offset_4.childNodes[0].data
			Pre_Offset_4_value = Pre_Offset_4_unicode.strip("\n")
			Offset_4_value = int(Pre_Offset_4_value)

			# append band offset in to list
			Offset_value.append(Offset_1_value)
			Offset_value.append(Offset_2_value)
			Offset_value.append(Offset_3_value)
			Offset_value.append(Offset_4_value)

			#  Get sceneCount from CUF file for create condition to split Normal scene from Last scene
			Pre_ScenecountMS = segment.getElementsByTagName("scenesCount")[0]
			Pre_ScenecountMS_unicode = Pre_ScenecountMS.childNodes[0].data
			Pre_ScenecountMS_value = Pre_ScenecountMS_unicode.strip("\n")
			ScenecountMS_value = int(Pre_ScenecountMS_value)
			SceneCount_list.append(ScenecountMS_value)

			#  Create GERALD name from by use components from CUF file.
			GERALDMS_name = Mission_value + "_" + SatelliteIdt_value + "_LEVEL0_" + PassRank_value + "_" + PassId_value + "_" + RevolutionNumber_value + "_" + SpectralMode_value + "_" + TransmissionModeMS_value + "_" + InstrumentTypeMS_value + "_" + InstrumentIDMS_value + "_" + FileNameMS_value + "_" + YearMS_segment + "-" + MonthMS_segment + "-" + DateMS_segment + "_" + HourMS_segment + "-" + MinMS_segment + "-" + SecMS_segment

			# Get last index list.
			MSSegmentImageRank_value = MSSegmentRank_value - 1

			#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			"""/-------------------------------------------------------------------------------------------------------------------------------------------------------------
			Read Browse (strip) images and get image shape value from it.

			Get Columns count from CUF file to use it be  Browse image width(both strip and scene).
			-------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
			imgname_MS = os.path.abspath(browseFileName_value)
			imgMS = cv2.imread(imgname_MS)

			Hight_MS , Width_MS , Ch_MS = imgMS.shape
			print "Cut browse image from strip: %s to scene by scene."%imgname_MS

			# Get ColumnsCount for use it in crop browse image
			Pre_ColumnsCountMS = segment.getElementsByTagName("columnsCount")[0]
			Pre_ColumnsCountMS_unicode = Pre_ColumnsCountMS.childNodes[0].data
			Pre_ColumnsCountMS_value = Pre_ColumnsCountMS_unicode.strip("\n")
			ColumnsCountMS_value = int(Pre_ColumnsCountMS_value)
			#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

			# Set SceneMS as root to get elements from tag in scene by for loop
			SceneMS = segment.getElementsByTagName("scene")
			for sceneMS in SceneMS :
				# Get sceneRank from catalog file for use to compare with sceneCount for split Normal and Last scene
				Pre_SceneMSRank = sceneMS.getElementsByTagName("sceneRank")[0]
				Pre_SceneMSRank_unicode = Pre_SceneMSRank.childNodes[0].data
				Pre_SceneMSRank_value = Pre_SceneMSRank_unicode.strip("\n")
				SceneMSRank_value = int(Pre_SceneMSRank_value)

				# create list name DSR_beginMS_list to keep DSR_begin value from CUF file(and we use it in process product).
				DSR_beginMS_list = []

				# create list name DSR_endMS_list to keep DSR_end value from CUF file.
				DSR_endMS_list = []

				# if first scene
				if SceneMSRank_value == 1 :
					# Get centerViewingDate from CUF file .
					Pre_CenterViewingDateMS = sceneMS.getElementsByTagName("centerViewingDate")[0]
					Pre_CenterViewingDateMS_unicode = Pre_CenterViewingDateMS.childNodes[0].data
					Pre_CenterViewingDateMS_value = Pre_CenterViewingDateMS_unicode.strip("\n")

					# Cut centerViewingDate get time value from it.
					CenterViewingDateMS_time = Pre_CenterViewingDateMS_value[8:14]
					CenterViewingDateMS_value = str(CenterViewingDateMS_time)

					# Set form  centerViewingDate value to [hour , min , sec]
					Use_CenterViewingDateMS_value = str(CenterViewingDateMS_time)[:2] + str(CenterViewingDateMS_time)[2:4] + str(CenterViewingDateMS_time)[4:]

					# Get date [year , month , date] from centerViewingdate to use it be [Image_date] in cpf_logic.py
					create_dateMS = Pre_CenterViewingDateMS_value[:8]

					# Get beginViewingDate in scene tag from CUF file.
					Pre_beginViewingDateMS = sceneMS.getElementsByTagName("beginViewingDate")[0]
					Pre_beginViewingDateMS_unicode = Pre_beginViewingDateMS.childNodes[0].data
					Pre_beginViewingDateMS_value = Pre_beginViewingDateMS_unicode.strip("\n")
					BeginViewingDateMS_value = str(Pre_beginViewingDateMS_value)

					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					#Get date [year , month , date] from beginViewingDate value
					Pre_YearBeginMS = BeginViewingDateMS_value [:4]
					YearBeginMS = str(Pre_YearBeginMS)

					Pre_MonthBeginMS = BeginViewingDateMS_value [4:6]
					MonthBeginMS = str(Pre_MonthBeginMS)

					Pre_DateBeginMS = BeginViewingDateMS_value [6:8]
					DateBeginMS = str(Pre_DateBeginMS)
					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					#Get time [hour , min , sec] from beginViewingDate
					Pre_HourBeginMS = BeginViewingDateMS_value [8:10]
					HourBeginMS = str(Pre_HourBeginMS)

					Pre_MinBeginMS = BeginViewingDateMS_value [10:12]
					MinBeginMS = str(Pre_MinBeginMS)

					Pre_SecBeginMS = BeginViewingDateMS_value [12:14]
					SecBeginMS = str(Pre_SecBeginMS)
					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

					# Get endViewingDate in scene tag from CUF file.
					Pre_EndViewingDateMS = sceneMS.getElementsByTagName("endViewingDate")[0]
					Pre_EndViewingDateMS_unicode = Pre_EndViewingDateMS.childNodes[0].data
					Pre_EndViewingDateMS_value = Pre_EndViewingDateMS_unicode.strip("\n")
					EndViewingDateMS_value = str(Pre_EndViewingDateMS_value)

					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					#Get date [year , month , date] from endViewingDate value
					Pre_YearEndMS = EndViewingDateMS_value [:4]
					YearEndMS = str(Pre_YearEndMS)

					Pre_MonthEndMS = EndViewingDateMS_value [4:6]
					MonthEndMS = str(Pre_MonthEndMS)

					Pre_DateEndMS = EndViewingDateMS_value [6:8]
					DateEndMS = str(Pre_DateEndMS)
					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					#Get time [hour , min , sec] from endViewingDate
					Pre_HourEndMS = EndViewingDateMS_value [8:10]
					HourEndMS = str(Pre_HourEndMS)

					Pre_MinEndMS = EndViewingDateMS_value [10:12]
					MinEndMS = str(Pre_MinEndMS)

					Pre_SecEndMS = EndViewingDateMS_value [12:14]
					SecEndMS = str(Pre_SecEndMS)
					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

					# Get beginRangeLine from CUF file
					Pre_BeginRangelineMS = sceneMS.getElementsByTagName("beginRangeLine")[0]
					Pre_BeginRangelineMS_unicode = Pre_BeginRangelineMS.childNodes[0].data
					Pre_BeginRangelineMS_value = Pre_BeginRangelineMS_unicode.strip("\n")
					BeginRangeLineMS_value = int(Pre_BeginRangelineMS_value)

					# Get endRangeLine from CUF file
					Pre_EndRangelineMS = sceneMS.getElementsByTagName("endRangeLine")[0]
					Pre_EndRangeline_unicode = Pre_EndRangelineMS.childNodes[0].data
					Pre_EndRangelineMS_value = Pre_EndRangeline_unicode .strip("\n")
					EndRangeLineMS_value = int(Pre_EndRangelineMS_value)

					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					"""/--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
					Calculate DSR begin for give to be beginline in [mainThread_Sipros.py]
					Calculate DSR End.
					--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
					for i in range(0, 4):
						#  put beginRangeLine + Offset value and put answer in to DSR_begin list
						DSR_beginMS = 1 + (Offset_value[i] + (Offset_value[0] * (-1)))
						DSR_beginMS_list.append(DSR_beginMS)

						#  put endRangeLine + Offset value and put answer in to DSR_end list
						DSR_endMS = (EndRangeLineMS_value + Offset_value[i])
						DSR_endMS_list.append(DSR_endMS)
					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

					# Get KPath from CUF file
					Pre_KPathMS = sceneMS.getElementsByTagName("kPath")[0]
					Pre_KPathMS_unicode = Pre_KPathMS.childNodes[0].data
					Pre_KPathMS_value = Pre_KPathMS_unicode.strip("\n")
					KPathMS_value = str(Pre_KPathMS_value)

					# Get JRow from CUF file
					Pre_JRowMS = sceneMS.getElementsByTagName("jRow")[0]
					Pre_JRowMS_unicode = Pre_JRowMS.childNodes[0].data
					Pre_JRowMS_value = Pre_JRowMS_unicode.strip("\n")
					JRowMS_value = str(Pre_JRowMS_value)

					# Use  KPath and JRow to create grid reference
					Grid_RefMS = KPathMS_value + "-" + JRowMS_value

					# Get texhnoQuality from CUF file.
					Pre_MStechnicalquality = sceneMS.getElementsByTagName("technoQuality")[0]
					Pre_MStechnicalquality_unicode = Pre_MStechnicalquality.childNodes[0].data
					Pre_MStechnicalquality_value = Pre_MStechnicalquality_unicode.strip("\n")
					MStechnicalquality_value = str(Pre_MStechnicalquality_value)

					# Get cloudCover value from CUF file.
					Pre_MScloudCover = sceneMS.getElementsByTagName("cloudCover")[0]
					Pre_MScloudCover_unicode = Pre_MScloudCover.childNodes[0].data
					Pre_MScloudCover_value = Pre_MScloudCover_unicode.strip("\n")
					MScloudCover_value = str(Pre_MScloudCover_value)

					# Get snowCover from CUF file.
					Pre_MSsnowcover = sceneMS.getElementsByTagName("snowCover")[0]
					Pre_MSsnowcover_unicode = Pre_MSsnowcover.childNodes[0].data
					Pre_MSsnowcover_value = Pre_MSsnowcover_unicode.strip("\n")
					MSsnowcover_value = str(Pre_MSsnowcover_value)

					# Check couplingMode (can process pansharpen yet ?) from CUF file.
					Pre_MScouplingmode = sceneMS.getElementsByTagName("couplingMode")[0]
					Pre_MScouplingmode_unicode = Pre_MScouplingmode.childNodes[0].data
					Pre_MScouplingmode_value = Pre_MScouplingmode_unicode.strip("\n")
					MScouplingmode_value = str(Pre_MScouplingmode_value)

					# Get orientationAngle from CUF file.
					Pre_MSorientationAngle = sceneMS.getElementsByTagName("orientationAngle")[0]
					Pre_MSorientationAngle_unicode = Pre_MSorientationAngle.childNodes[0].data
					Pre_MSorientationAngle_value = Pre_MSorientationAngle_unicode.strip("\n")
					MSorientationAngle_value = str(Pre_MSorientationAngle_value)

					# Get incidenceAngle from CUF file.
					Pre_MSIncidenceangle = sceneMS.getElementsByTagName("incidenceAngle")[0]
					Pre_MSIncidenceangle_unicoce = Pre_MSIncidenceangle.childNodes[0].data
					Pre_MSIncidenceangle_value = Pre_MSIncidenceangle_unicoce.strip("\n")
					MSIncidenceangle_value = str(Pre_MSIncidenceangle_value)

					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					"""/--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
					Calculate UTM Lat / Long of [Upper_Left] , [Upper_Right] , [Lower_Left] , [Lower_Right] and [Center_Lat_long].
					In CUF file the coordinates is radian so then we tranfrom it to UTM coordinates by use formula like this :

					Lat_utm = {if N = 1.0 , S = -1.0} * {Lat in degrees + (lat in minute / 60.0) + (lat in second / 3600.0)}
					Long_utm = {if E = 1.0 , W = -1.0} * {Long in degrees + (long in minute / 60.0) + (long in second / 3600.0)}
					--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------/"""
					# Get center latitude from CUF file.
					Pre_MSLatSceneCenter = sceneMS.getElementsByTagName("latSceneCenter")[0]
					Pre_MSLatSceneCenter_unicode = Pre_MSLatSceneCenter.childNodes[0].data
					Pre_MSLatSceneCenter_value = Pre_MSLatSceneCenter_unicode.strip("\n")
					MSLatSceneCenter_value = str(Pre_MSLatSceneCenter_value)

					# Get first character of center latitude.
					Pre_Dec_MSLatSceneCenter_text = MSLatSceneCenter_value[:1]

					# Get second and thrid character of center latitude use for degrees value.
					Pre_Dec_MSLatSceneCenter_Degrees = MSLatSceneCenter_value[1:-4]
					Dec_MSLatSceneCenter_Degrees = np.float64(Pre_Dec_MSLatSceneCenter_Degrees)

					# Get fourth and fifth character of center latitude use for minutes value.
					Pre_Dec_MSLatSceneCenter_minutes = MSLatSceneCenter_value[4:-2]
					Dec_MSLatSceneCenter_minutes = np.float64(Pre_Dec_MSLatSceneCenter_minutes)

					# Get Sixth and still left character of center latitude use for second value.
					Pre_Dec_MSLatSceneCenter_sec = MSLatSceneCenter_value[6:]
					Dec_MSLatSceneCenter_sec = np.float64(Pre_Dec_MSLatSceneCenter_sec)

					# In latitude {if first character is N = 1 , S = -1}.
					if Pre_Dec_MSLatSceneCenter_text == "N" :
						Dec_MSLatSceneCenter_text = 1.0
					elif Pre_Dec_MSLatSceneCenter_text == "S" :
						Dec_MSLatSceneCenter_text = -1.0

					# Calculate center latitude by use formula.
					Use_MSLatSceneCenter_value = np.float64(Dec_MSLatSceneCenter_text * (Dec_MSLatSceneCenter_Degrees + (Dec_MSLatSceneCenter_minutes / 60.0) + (Dec_MSLatSceneCenter_sec / 3600.0)))

 					# Get center longitude from CUF file.
 					Pre_MSLongSceneCenter = sceneMS.getElementsByTagName("longSceneCenter")[0]
 					Pre_MSLongSceneCenter_unicode = Pre_MSLongSceneCenter.childNodes[0].data
 					Pre_MSLongSceneCenter_value = Pre_MSLongSceneCenter_unicode.strip("\n")
 					MSLongSceneCenter_value = str(Pre_MSLongSceneCenter_value)

 					# Get first character of center longitude.
 					Pre_Dec_MSLongSceneCenter_text = MSLongSceneCenter_value[:1]

 					# Get second and thrid character of center longitude use for degrees value.
 					Pre_Dec_MSLongSceneCenter_Degrees = MSLatSceneCenter_value[1:-4]
 					Dec_MSLongSceneCenter_Degrees = np.float64(Pre_Dec_MSLongSceneCenter_Degrees)

 					# Get fourth and fifth character of center latitude use for minutes value.
 					Pre_Dec_MSLongSceneCenter_minutes = MSLongSceneCenter_value[4:-2]
 					Dec_MSLongSceneCenter_minutes = np.float64(Pre_Dec_MSLongSceneCenter_minutes)

 					# Get Sixth and still left character of center latitude use for second value.
 					Pre_Dec_MSLongSceneCenter_sec = MSLongSceneCenter_value[6:]
 					Dec_MSLongSceneCenter_sec = np.float64(Pre_Dec_MSLongSceneCenter_sec)

 					# In longitude {if first character is E = 1 , W = -1}.
 					if Pre_Dec_MSLongSceneCenter_text == "E":
 						Dec_MSLongSceneCenter_text = 1.0
 					elif Pre_Dec_MSLongSceneCenter_text == "W":
 						Dec_MSLongSceneCenter_text = -1.0

 					# Calculate center longitude by use formula.
 					Use_MSLongSceneCenter_value = np.float64(Dec_MSLongSceneCenter_text * (Dec_MSLongSceneCenter_Degrees + (Dec_MSLongSceneCenter_minutes / 60.0) + (Dec_MSLongSceneCenter_sec / 3600.0)))

 					# Get sun elevation from CUF file.
 					Pre_MSSunElevation = sceneMS.getElementsByTagName("sunElevation")[0]
 					Pre_MSSunElevation_unicode = Pre_MSSunElevation.childNodes[0].data
 					Pre_MSSunElevation_value = Pre_MSSunElevation_unicode.strip("\n")
 					MSSunElevation_value = str(Pre_MSSunElevation_value)

 					# Get sun azimuth from CUF file.
 					Pre_MSSunAzimuth = sceneMS.getElementsByTagName("sunAzimuth")[0]
 					Pre_MSSunAzimuth_unicode = Pre_MSSunAzimuth.childNodes[0].data
 					Pre_MSSunAzimuth_value = Pre_MSSunAzimuth_unicode.strip("\n")
 					MSSunAzimuth_value = str(Pre_MSSunAzimuth_value)


 					Pre_MSnwLat = sceneMS.getElementsByTagName("nwLat")[0]
 					Pre_MSnwLat_unicode = Pre_MSnwLat.childNodes[0].data
 					Pre_MSnwLat_value = Pre_MSnwLat_unicode.strip("\n")
 					MSnwLat_value = str(Pre_MSnwLat_value)

 					Pre_Dec_MSnwLat_value_text = MSnwLat_value[:1]
 					Pre_Dec_MSnwLat_Degrees = MSnwLat_value[1:-4]
 					Dec_MSnwLat_Degrees = np.float64(Pre_Dec_MSnwLat_Degrees)
 					Pre_Dec_MSnwLat_minutes = MSnwLat_value[4:-2]
 					Dec_MSnwLat_minutes = np.float64(Pre_Dec_MSnwLat_minutes)
 					Pre_Dec_MSnwLat_sec = MSnwLat_value[6:]
 					Dec_MSnwLat_sec = np.float64(Pre_Dec_MSnwLat_sec)

 					if Pre_Dec_MSnwLat_value_text == "N":
 						Dec_MSnwLat_value_text = 1.0

 					elif Pre_Dec_MSnwLat_value_text == "S":
 						Dec_MSnwLat_value_text = -1.0
 					Use_MSnwLat_value = np.float64(Dec_MSnwLat_value_text * (Dec_MSnwLat_Degrees + (Dec_MSnwLat_minutes / 60.0) + (Dec_MSnwLat_sec / 3600.0)))

 					Pre_MSnwLong = sceneMS.getElementsByTagName("nwLong")[0]
 					Pre_MSnwLong_unicode = Pre_MSnwLong.childNodes[0].data
 					Pre_MSnwLong_value = Pre_MSnwLong_unicode.strip("\n")
 					MSnwLong_value = str(Pre_MSnwLong_value)

 					Pre_Dec_MSnwLong_value_text = MSnwLong_value[:1]
 					Pre_Dec_MSnwLong_Degrees = MSnwLong_value[1:-4]
 					Dec_MSnwLong_Degrees = np.float64(Pre_Dec_MSnwLong_Degrees)
 					Pre_Dec_MSnwLong_minutes = MSnwLong_value[4:-2]
 					Dec_MSnwLong_minutes = np.float64(Pre_Dec_MSnwLong_minutes)
 					Pre_Dec_MSnwLong_sec = MSnwLong_value[6:]
 					Dec_MSnwLong_sec = np.float64(Pre_Dec_MSnwLong_sec)

 					if Pre_Dec_MSnwLong_value_text == "W":
 						Dec_MSnwLong_value_text = 1.0

 					elif Pre_Dec_MSnwLong_value_text == "E":
 						Dec_MSnwLong_value_text = -1.0
 					Use_MSnwLong_value = np.float64(Dec_MSnwLong_value_text * (Dec_MSnwLong_Degrees + (Dec_MSnwLong_minutes / 60.0) + (Dec_MSnwLong_sec / 3600.0)))

 					Pre_MSneLat = sceneMS.getElementsByTagName("neLat")[0]
 					Pre_MSneLat_unicode = Pre_MSneLat.childNodes[0].data
 					Pre_MSneLat_value = Pre_MSneLat_unicode.strip("\n")
 					MSneLat_value = str(Pre_MSneLat_value)

 					Pre_Dec_MSneLat_value_text = MSneLat_value[:1]
 					Pre_Dec_MSneLat_Degrees = MSneLat_value[1:-4]
 					Dec_MSneLat_Degrees = np.float64(Pre_Dec_MSneLat_Degrees)
 					Pre_Dec_MSneLat_minutes = MSneLat_value[4:-2]
 					Dec_MSneLat_minutes = np.float64(Pre_Dec_MSneLat_minutes)
 					Pre_Dec_MSneLat_sec = MSneLat_value[6:]
 					Dec_MSneLat_sec = np.float64(Pre_Dec_MSneLat_sec)

 					if Pre_Dec_MSneLat_value_text == "N":
 						Dec_MSneLat_value_text = 1.0

 					elif Pre_Dec_MSneLat_value_text == "S":
 						Dec_MSneLat_value_text = -1.0
 					Use_MSneLat_value = np.float64(Dec_MSneLat_value_text * (Dec_MSneLat_Degrees + (Dec_MSneLat_minutes / 60.0) + (Dec_MSneLat_sec / 3600.0)))

 					Pre_MSneLong = sceneMS.getElementsByTagName("neLong")[0]
 					Pre_MSneLong_unicode = Pre_MSneLong.childNodes[0].data
 					Pre_MSneLong_value = Pre_MSneLong_unicode.strip("\n")
 					MSneLong_value = str(Pre_MSneLong_value)

 					Pre_Dec_MSneLong_value_text = MSneLong_value[:1]
 					Pre_Dec_MSneLong_Degrees = MSneLong_value[1:-4]
 					Dec_MSneLong_Degrees = np.float64(Pre_Dec_MSneLong_Degrees)
 					Pre_Dec_MSneLong_minutes = MSneLong_value[4:-2]
 					Dec_MSneLong_minutes = np.float64(Pre_Dec_MSneLong_minutes)
 					Pre_Dec_MSneLong_sec = MSneLong_value[6:]
 					Dec_MSneLong_sec = np.float64(Pre_Dec_MSneLong_sec)

 					if Pre_Dec_MSneLong_value_text == "W":
 						Dec_MSneLong_value_text = 1.0

 					elif Pre_Dec_MSneLong_value_text == "E":
 						Dec_MSneLong_value_text = -1.0
 					Use_MSneLong_value = np.float64(Dec_MSneLong_value_text * (Dec_MSneLong_Degrees + (Dec_MSneLong_minutes / 60.0) + (Dec_MSneLong_sec / 3600.0)))

 					Pre_MSswLat = sceneMS.getElementsByTagName("swLat")[0]
 					Pre_MSswLat_unicode = Pre_MSswLat.childNodes[0].data
 					Pre_MSswLat_value = Pre_MSswLat_unicode.strip("\n")
 					MSswLat_value = str(Pre_MSswLat_value)

 					Pre_Dec_MSswLat_value_text = MSswLat_value[:1]
 					Pre_Dec_MSswLat_Degrees = MSswLat_value[1:-4]
 					Dec_MSswLat_Degrees = np.float64(Pre_Dec_MSswLat_Degrees)
 					Pre_Dec_MSswLat_minutes = MSswLat_value[4:-2]
 					Dec_MSswLat_minutes = np.float64(Pre_Dec_MSswLat_minutes)
 					Pre_Dec_MSswLat_sec = MSswLat_value[6:]
 					Dec_MSswLat_sec = np.float64(Pre_Dec_MSswLat_sec)

 					if Pre_Dec_MSswLat_value_text == "N":
 						Dec_MSswLat_value_text = 1.0

 					elif Pre_Dec_MSswLat_value_text == "S":
 						Dec_MSswLat_value_text = -1.0
 					Use_MSswLat_value = np.float64(Dec_MSswLat_value_text * (Dec_MSswLat_Degrees + (Dec_MSswLat_minutes / 60.0) + (Dec_MSswLat_sec / 3600.0)))

 					Pre_MSswLong = sceneMS.getElementsByTagName("swLong")[0]
 					Pre_MSswLong_unicode = Pre_MSswLong.childNodes[0].data
 					Pre_MSswLong_value = Pre_MSswLong_unicode.strip("\n")
 					MSswLong_value = str(Pre_MSswLong_value)

 					Pre_Dec_MSswLong_value_text = MSswLong_value[:1]
 					Pre_Dec_MSswLong_Degrees = MSswLong_value[1:-4]
 					Dec_MSswLong_Degrees = np.float64(Pre_Dec_MSswLong_Degrees)
 					Pre_Dec_MSswLong_minutes = MSswLong_value[4:-2]
 					Dec_MSswLong_minutes = np.float64(Pre_Dec_MSswLong_minutes)
 					Pre_Dec_MSswLong_sec = MSswLong_value[6:]
 					Dec_MSswLong_sec = np.float64(Pre_Dec_MSswLong_sec)

 					if Pre_Dec_MSswLong_value_text == "W":
 						Dec_MSswLong_value_text = 1.0

 					elif Pre_Dec_MSswLong_value_text == "E":
 						Dec_MSswLong_value_text = -1.0
 					Use_MSswLong_value = np.float64(Dec_MSswLong_value_text * (Dec_MSswLong_Degrees + (Dec_MSswLong_minutes / 60.0) + (Dec_MSswLong_sec / 3600.0)))

 					Pre_MSseLat = sceneMS.getElementsByTagName("seLat")[0]
 					Pre_MSseLat_unicode = Pre_MSseLat.childNodes[0].data
 					Pre_MSseLat_value = Pre_MSseLat_unicode.strip("\n")
 					MSseLat_value = str(Pre_MSseLat_value)

 					Pre_Dec_MSseLat_value_text = MSseLat_value[:1]
 					Pre_Dec_MSseLat_Degrees = MSseLat_value[1:-4]
 					Dec_MSseLat_Degrees = np.float64(Pre_Dec_MSseLat_Degrees)
 					Pre_Dec_MSseLat_minutes = MSseLat_value[4:-2]
 					Dec_MSseLat_minutes = np.float64(Pre_Dec_MSseLat_minutes)
 					Pre_Dec_MSseLat_sec = MSseLat_value[6:]
 					Dec_MSseLat_sec = np.float64(Pre_Dec_MSseLat_sec)

 					if Pre_Dec_MSseLat_value_text == "N":
 						Dec_MSseLat_value_text = 1.0

 					elif Pre_Dec_MSseLat_value_text == "S":
 						Dec_MSseLat_value_text = -1.0
 					Use_MSseLat_value = np.float64(Dec_MSseLat_value_text * (Dec_MSseLat_Degrees + (Dec_MSseLat_minutes / 60.0) + (Dec_MSseLat_sec / 3600.0)))

 					Pre_MSseLong = sceneMS.getElementsByTagName("seLong")[0]
 					Pre_MSseLong_unicode = Pre_MSseLong.childNodes[0].data
 					Pre_MSseLong_value = Pre_MSseLong_unicode.strip("\n")
 					MSseLong_value = str(Pre_MSseLong_value)

 					Pre_Dec_MSseLong_value_text = MSseLong_value[:1]
 					Pre_Dec_MSseLong_Degrees = MSseLong_value[1:-4]
 					Dec_MSseLong_Degrees = np.float64(Pre_Dec_MSseLong_Degrees)
 					Pre_Dec_MSseLong_minutes = MSseLong_value[4:-2]
 					Dec_MSseLong_minutes = np.float64(Pre_Dec_MSseLong_minutes)
 					Pre_Dec_MSseLong_sec = MSseLong_value[6:]
 					Dec_MSseLong_sec = np.float64(Pre_Dec_MSseLong_sec)

 					if Pre_Dec_MSseLong_value_text == "W":
 						Dec_MSseLong_value_text = 1.0

 					elif Pre_Dec_MSseLong_value_text == "E":
 						Dec_MSseLong_value_text = -1.0
 					Use_MSseLong_value = np.float64(Dec_MSseLong_value_text * (Dec_MSseLong_Degrees + (Dec_MSseLong_minutes / 60.0) + (Dec_MSseLong_sec / 3600.0)))
 					#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

					# {Set BrowseBeginLine as 1}
					BrowseBeginLineMS_value = 1

					# {Set BrowseEndLine as 499}

					BrowseEndLineMS_value = 499

					# Create catalog file
					Image_FilenameMS = FIlename_path + "/" + RevolutionNumber_value + "_" + SpectralMode_value + "_Filename%s_SceneRank_%s.cmp"%(FileNameMS_value , str(SceneMSRank_value))
					Image_FilenameMS_file = open(Image_FilenameMS, "w")
					Image_FilenameMS_file.write(str(BeginReception_year) + str(BeginReception_month) + str(BeginReception_date) + "\n")
					Image_FilenameMS_file.write(str(BeginReception_hour) + str(BeginReception_min) + str(BeginReception_sec) + "\n")
					Image_FilenameMS_file.write(str(EndReception_year) + str(EndReception_month) + str(EndReception_date) + "\n")
					Image_FilenameMS_file.write(str(EndReception_hour) + str(EndReception_min) + str(EndReception_sec) + "\n")
					Image_FilenameMS_file.write(str(OrbitCycle_value) + "\n")
					Image_FilenameMS_file.write(str(RevolutionNumber_value) + "\n")
					Image_FilenameMS_file.write(str(Mission_value) + "\n")
					Image_FilenameMS_file.write(str(SatelliteIdt_value) + "\n")
					Image_FilenameMS_file.write(str(PassRank_value) + "\n")
					Image_FilenameMS_file.write(str(PassId_value) + "\n")
					Image_FilenameMS_file.write(str(SegmentCount_value) + "\n")
					Image_FilenameMS_file.write(str("Segment info") + "\n")
					Image_FilenameMS_file.write(str(FileNameMS_value) + "\n")
					Image_FilenameMS_file.write(str(GERALDMS_name) + "\n")
					Image_FilenameMS_file.write(str(MSSegmentRank_value) + "\n")
					Image_FilenameMS_file.write(str(InstrumentTypeMS_value) + str(InstrumentIDMS_value) + "\n")
					Image_FilenameMS_file.write(str(TransmissionModeMS_value) + "\n")
					Image_FilenameMS_file.write(str(MSsegmentquality_value) + "\n")
					Image_FilenameMS_file.write(str(YearMS_segment) + str(MonthMS_segment) + str(DateMS_segment) + "\n")
					Image_FilenameMS_file.write(str(HourMS_segment) + str(MinMS_segment) + str(SecMS_segment) + "\n")
					Image_FilenameMS_file.write(str(EndYearMS_segment) + str(EndMonthMS_segment) + str(EndDateMS_segment) + "\n")
					Image_FilenameMS_file.write(str(EndHourMS_segment) + str(EndMinMS_segment) + str(EndSecMS_segment) + "\n")
					Image_FilenameMS_file.write(str(MSCompression_ratio_value) + "\n")
					Image_FilenameMS_file.write(str(SpectralMode_value) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[0]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[1]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[2]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[3]) + "\n")
					Image_FilenameMS_file.write(str(MSReferenceBand_value) + "\n")
					Image_FilenameMS_file.write(str(MS_Alongtrackviewingangle_value) + "\n")
					Image_FilenameMS_file.write(str(MS_Acrosstrackviewingangle_value) + "\n")
					Image_FilenameMS_file.write(str(MS_ABSGain_value) + "\n")
					Image_FilenameMS_file.write(str("Scene info") + "\n")
					Image_FilenameMS_file.write(str(ScenecountMS_value) + "\n")
					Image_FilenameMS_file.write(str(SceneMSRank_value) + "\n")
					Image_FilenameMS_file.write(str(Grid_RefMS) + "\n")
					Image_FilenameMS_file.write(str(MStechnicalquality_value) + "\n")
					Image_FilenameMS_file.write(str(MScloudCover_value) + "\n")
					Image_FilenameMS_file.write(str(MSsnowcover_value) + "\n")
					Image_FilenameMS_file.write(str(create_dateMS[:4]) + str(create_dateMS[4:6]) + str(create_dateMS[6:]) + "\n")
					Image_FilenameMS_file.write(str(Use_CenterViewingDateMS_value) + "\n")
					Image_FilenameMS_file.write(str(YearBeginMS) + str(MonthBeginMS) + str(DateBeginMS) + "\n")
					Image_FilenameMS_file.write(str(HourBeginMS) + str(MinBeginMS) + str(SecBeginMS) + "\n")
					Image_FilenameMS_file.write(str(YearEndMS) + str(MonthEndMS) + str(DateEndMS) + "\n")
					Image_FilenameMS_file.write(str(HourEndMS) + str(MinEndMS) + str(SecEndMS) + "\n")
					Image_FilenameMS_file.write(str(MScouplingmode_value) + "\n")
					Image_FilenameMS_file.write(str(MSorientationAngle_value) + "\n")
					Image_FilenameMS_file.write(str(MSIncidenceangle_value) + "\n")
					Image_FilenameMS_file.write(str(MSSunElevation_value) + "\n")
					Image_FilenameMS_file.write(str(MSSunAzimuth_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSnwLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSnwLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSneLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSneLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSswLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSswLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSseLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSseLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSLatSceneCenter_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSLongSceneCenter_value) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[0]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[1]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[2]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[3]))
					Image_FilenameMS_file.close()

					# # Create catalog file
					Image_Date_timeMS_filename = Date_time_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Date-%s-%s-%s_Time-%s-%s-%s.cmp"%(str(create_dateMS[:4]),str(create_dateMS[4:6]),str(create_dateMS[6:]),Use_CenterViewingDateMS_value[:-4], Use_CenterViewingDateMS_value[2:-2],Use_CenterViewingDateMS_value[4:])
					Image_ConerMS_filename = Corner_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Upper_Left(%.4f , %.4f)_Upper_Right(%.4f , %.4f)_Lower_Left(%.4f , %.4f)_Lower_Right(%.4f , %.4f).cmp"%(Use_MSnwLat_value ,Use_MSnwLong_value ,Use_MSneLat_value , Use_MSneLong_value , Use_MSswLat_value , Use_MSswLong_value , Use_MSseLat_value , Use_MSseLong_value)
					Image_CenterMS_filename = Center_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Center_Lat_long(%.4f , %.4f).cmp"%(Use_MSLatSceneCenter_value , Use_MSLongSceneCenter_value)

					shutil.copy(Image_FilenameMS , Image_Date_timeMS_filename)
					shutil.copy(Image_FilenameMS , Image_ConerMS_filename)
					shutil.copy(Image_FilenameMS , Image_CenterMS_filename)


					crop_img_MS = imgMS[BrowseBeginLineMS_value : 499 + BrowseBeginLineMS_value, 0:ColumnsCountMS_value]
					cv2.imwrite(Image_FilenameMS[:-4] + ".JPG", crop_img_MS)

					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_Date_timeMS_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_ConerMS_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_CenterMS_filename[:-4] + ".JPG")

				# Normal scene condition
				elif SceneMSRank_value != ScenecountMS_value :

					# Get centerViewingDate from CUF file and use it to file name of Image detail file
					Pre_CenterViewingDateMS = sceneMS.getElementsByTagName("centerViewingDate")[0]
					Pre_CenterViewingDateMS_unicode = Pre_CenterViewingDateMS.childNodes[0].data
					Pre_CenterViewingDateMS_value = Pre_CenterViewingDateMS_unicode.strip("\n")
					CenterViewingDateMS_time = Pre_CenterViewingDateMS_value[8:14]
					CenterViewingDateMS_value = str(CenterViewingDateMS_time)
					Use_CenterViewingDateMS_value = str(CenterViewingDateMS_time)[:2] + str(CenterViewingDateMS_time)[2:4] + str(CenterViewingDateMS_time)[4:]
					create_dateMS = Pre_CenterViewingDateMS_value[:8]

					Pre_beginViewingDateMS = sceneMS.getElementsByTagName("beginViewingDate")[0]
					Pre_beginViewingDateMS_unicode = Pre_beginViewingDateMS.childNodes[0].data
					Pre_beginViewingDateMS_value = Pre_beginViewingDateMS_unicode.strip("\n")
					BeginViewingDateMS_value = str(Pre_beginViewingDateMS_value)

					Pre_YearBeginMS = BeginViewingDateMS_value [:4]
					YearBeginMS = str(Pre_YearBeginMS)

					Pre_MonthBeginMS = BeginViewingDateMS_value [4:6]
					MonthBeginMS = str(Pre_MonthBeginMS)

					Pre_DateBeginMS = BeginViewingDateMS_value [6:8]
					DateBeginMS = str(Pre_DateBeginMS)

					Pre_HourBeginMS = BeginViewingDateMS_value [8:10]
					HourBeginMS = str(Pre_HourBeginMS)

					Pre_MinBeginMS = BeginViewingDateMS_value [10:12]
					MinBeginMS = str(Pre_MinBeginMS)

					Pre_SecBeginMS = BeginViewingDateMS_value [12:14]
					SecBeginMS = str(Pre_SecBeginMS)

					Pre_EndViewingDateMS = sceneMS.getElementsByTagName("endViewingDate")[0]
					Pre_EndViewingDateMS_unicode = Pre_EndViewingDateMS.childNodes[0].data
					Pre_EndViewingDateMS_value = Pre_EndViewingDateMS_unicode.strip("\n")
					EndViewingDateMS_value = str(Pre_EndViewingDateMS_value)

					Pre_YearEndMS = EndViewingDateMS_value [:4]
					YearEndMS = str(Pre_YearEndMS)

					Pre_MonthEndMS = EndViewingDateMS_value [4:6]
					MonthEndMS = str(Pre_MonthEndMS)

					Pre_DateEndMS = EndViewingDateMS_value [6:8]
					DateEndMS = str(Pre_DateEndMS)

					Pre_HourEndMS = EndViewingDateMS_value [8:10]
					HourEndMS = str(Pre_HourEndMS)

					Pre_MinEndMS = EndViewingDateMS_value [10:12]
					MinEndMS = str(Pre_MinEndMS)

					Pre_SecEndMS = EndViewingDateMS_value [12:14]
					SecEndMS = str(Pre_SecEndMS)

					""" Get DSR_begin from Normal scene
					first : Get beginRangeLine from catalog file
					second : Use 4 loop to put beginRangeLine + Offset value
					because Offset value as list and it have 4 Index """

					# Get beginRangeLine from CUF file
					Pre_BeginRangelineMS = sceneMS.getElementsByTagName("beginRangeLine")[0]
					Pre_BeginRangelineMS_unicode = Pre_BeginRangelineMS.childNodes[0].data
					Pre_BeginRangelineMS_value = Pre_BeginRangelineMS_unicode.strip("\n")
					BeginRangeLineMS_value = int(Pre_BeginRangelineMS_value)

					Pre_EndRangelineMS = sceneMS.getElementsByTagName("endRangeLine")[0]
					Pre_EndRangelineMS_unicode = Pre_EndRangelineMS.childNodes[0].data
					Pre_EndRangelineMS_value = Pre_EndRangelineMS_unicode.strip("\n")
					EndRangeLineMS_value = int(Pre_EndRangelineMS_value)

					# Create for loop 4 Index
					for i in range(0, 4):
						#  put beginRangeLine + Offset value and put answer in to DSR_begin list
						DSR_beginMS = (BeginRangeLineMS_value + Offset_value[i])
						DSR_beginMS_list.append(DSR_beginMS)

						DSR_endMS = (EndRangeLineMS_value + Offset_value[i])
						DSR_endMS_list.append(DSR_endMS)
					# }

					# { Get KPath and JRow from CUF file and use it to Grid reference
					Pre_KPathMS = sceneMS.getElementsByTagName("kPath")[0]
					Pre_KPathMS_unicode = Pre_KPathMS.childNodes[0].data
					Pre_KPathMS_value = Pre_KPathMS_unicode.strip("\n")
					KPathMS_value = str(Pre_KPathMS_value)

					Pre_JRowMS = sceneMS.getElementsByTagName("jRow")[0]
					Pre_JRowMS_unicode = Pre_JRowMS.childNodes[0].data
					Pre_JRowMS_value = Pre_JRowMS_unicode.strip("\n")
					JRowMS_value = str(Pre_JRowMS_value)

					Grid_RefMS = KPathMS_value + "-" + JRowMS_value
					# }

					Pre_MStechnicalquality = sceneMS.getElementsByTagName("technoQuality")[0]
					Pre_MStechnicalquality_unicode = Pre_MStechnicalquality.childNodes[0].data
					Pre_MStechnicalquality_value = Pre_MStechnicalquality_unicode.strip("\n")
					MStechnicalquality_value = str(Pre_MStechnicalquality_value)

					Pre_MScloudCover = sceneMS.getElementsByTagName("cloudCover")[0]
					Pre_MScloudCover_unicode = Pre_MScloudCover.childNodes[0].data
					Pre_MScloudCover_value = Pre_MScloudCover_unicode.strip("\n")
					MScloudCover_value = str(Pre_MScloudCover_value)

					Pre_MSsnowcover = sceneMS.getElementsByTagName("snowCover")[0]
					Pre_MSsnowcover_unicode = Pre_MSsnowcover.childNodes[0].data
					Pre_MSsnowcover_value = Pre_MSsnowcover_unicode.strip("\n")
					MSsnowcover_value = str(Pre_MSsnowcover_value)

					Pre_MScouplingmode = sceneMS.getElementsByTagName("couplingMode")[0]
					Pre_MScouplingmode_unicode = Pre_MScouplingmode.childNodes[0].data
					Pre_MScouplingmode_value = Pre_MScouplingmode_unicode.strip("\n")
					MScouplingmode_value = str(Pre_MScouplingmode_value)

					Pre_MSorientationAngle = sceneMS.getElementsByTagName("orientationAngle")[0]
					Pre_MSorientationAngle_unicode = Pre_MSorientationAngle.childNodes[0].data
					Pre_MSorientationAngle_value = Pre_MSorientationAngle_unicode.strip("\n")
					MSorientationAngle_value = str(Pre_MSorientationAngle_value)

					Pre_MSIncidenceangle = sceneMS.getElementsByTagName("incidenceAngle")[0]
					Pre_MSIncidenceangle_unicoce = Pre_MSIncidenceangle.childNodes[0].data
					Pre_MSIncidenceangle_value = Pre_MSIncidenceangle_unicoce.strip("\n")
					MSIncidenceangle_value = str(Pre_MSIncidenceangle_value)

					Pre_MSLatSceneCenter = sceneMS.getElementsByTagName("latSceneCenter")[0]
					Pre_MSLatSceneCenter_unicode = Pre_MSLatSceneCenter.childNodes[0].data
					Pre_MSLatSceneCenter_value = Pre_MSLatSceneCenter_unicode.strip("\n")
					MSLatSceneCenter_value = str(Pre_MSLatSceneCenter_value)

					Pre_Dec_MSLatSceneCenter_text = MSLatSceneCenter_value[:1]
					Pre_Dec_MSLatSceneCenter_Degrees = MSLatSceneCenter_value[1:-4]
					Dec_MSLatSceneCenter_Degrees = np.float64(Pre_Dec_MSLatSceneCenter_Degrees)
					Pre_Dec_MSLatSceneCenter_minutes = MSLatSceneCenter_value[4:-2]
					Dec_MSLatSceneCenter_minutes = np.float64(Pre_Dec_MSLatSceneCenter_minutes)
					Pre_Dec_MSLatSceneCenter_sec = MSLatSceneCenter_value[6:]
					Dec_MSLatSceneCenter_sec = np.float64(Pre_Dec_MSLatSceneCenter_sec)

					if Pre_Dec_MSLatSceneCenter_text == "N" :
						Dec_MSLatSceneCenter_text = 1.0
					elif Pre_Dec_MSLatSceneCenter_text == "S" :
						Dec_MSLatSceneCenter_text = -1.0
					Use_MSLatSceneCenter_value = np.float64(Dec_MSLatSceneCenter_text * (Dec_MSLatSceneCenter_Degrees + (Dec_MSLatSceneCenter_minutes / 60.0) + (Dec_MSLatSceneCenter_sec / 3600.0)))

 					Pre_MSLongSceneCenter = sceneMS.getElementsByTagName("longSceneCenter")[0]
 					Pre_MSLongSceneCenter_unicode = Pre_MSLongSceneCenter.childNodes[0].data
 					Pre_MSLongSceneCenter_value = Pre_MSLongSceneCenter_unicode.strip("\n")
 					MSLongSceneCenter_value = str(Pre_MSLongSceneCenter_value)

 					Pre_Dec_MSLongSceneCenter_text = MSLongSceneCenter_value[:1]
 					Pre_Dec_MSLongSceneCenter_Degrees = MSLatSceneCenter_value[1:-4]
 					Dec_MSLongSceneCenter_Degrees = np.float64(Pre_Dec_MSLongSceneCenter_Degrees)
 					Pre_Dec_MSLongSceneCenter_minutes = MSLongSceneCenter_value[4:-2]
 					Dec_MSLongSceneCenter_minutes = np.float64(Pre_Dec_MSLongSceneCenter_minutes)
 					Pre_Dec_MSLongSceneCenter_sec = MSLongSceneCenter_value[6:]
 					Dec_MSLongSceneCenter_sec = np.float64(Pre_Dec_MSLongSceneCenter_sec)

 					if Pre_Dec_MSLongSceneCenter_text == "E":
 						Dec_MSLongSceneCenter_text = 1.0
 					elif Pre_Dec_MSLongSceneCenter_text == "W":
 						Dec_MSLongSceneCenter_text = -1.0
 					Use_MSLongSceneCenter_value = np.float64(Dec_MSLongSceneCenter_text * (Dec_MSLongSceneCenter_Degrees + (Dec_MSLongSceneCenter_minutes / 60.0) + (Dec_MSLongSceneCenter_sec / 3600.0)))

 					Pre_MSSunElevation = sceneMS.getElementsByTagName("sunElevation")[0]
 					Pre_MSSunElevation_unicode = Pre_MSSunElevation.childNodes[0].data
 					Pre_MSSunElevation_value = Pre_MSSunElevation_unicode.strip("\n")
 					MSSunElevation_value = str(Pre_MSSunElevation_value)

 					Pre_MSSunAzimuth = sceneMS.getElementsByTagName("sunAzimuth")[0]
 					Pre_MSSunAzimuth_unicode = Pre_MSSunAzimuth.childNodes[0].data
 					Pre_MSSunAzimuth_value = Pre_MSSunAzimuth_unicode.strip("\n")
 					MSSunAzimuth_value = str(Pre_MSSunAzimuth_value)

 					Pre_MSnwLat = sceneMS.getElementsByTagName("nwLat")[0]
 					Pre_MSnwLat_unicode = Pre_MSnwLat.childNodes[0].data
 					Pre_MSnwLat_value = Pre_MSnwLat_unicode.strip("\n")
 					MSnwLat_value = str(Pre_MSnwLat_value)

 					Pre_Dec_MSnwLat_value_text = MSnwLat_value[:1]
 					Pre_Dec_MSnwLat_Degrees = MSnwLat_value[1:-4]
 					Dec_MSnwLat_Degrees = np.float64(Pre_Dec_MSnwLat_Degrees)
 					Pre_Dec_MSnwLat_minutes = MSnwLat_value[4:-2]
 					Dec_MSnwLat_minutes = np.float64(Pre_Dec_MSnwLat_minutes)
 					Pre_Dec_MSnwLat_sec = MSnwLat_value[6:]
 					Dec_MSnwLat_sec = np.float64(Pre_Dec_MSnwLat_sec)

 					if Pre_Dec_MSnwLat_value_text == "N":
 						Dec_MSnwLat_value_text = 1.0

 					elif Pre_Dec_MSnwLat_value_text == "S":
 						Dec_MSnwLat_value_text = -1.0
 					Use_MSnwLat_value = np.float64(Dec_MSnwLat_value_text * (Dec_MSnwLat_Degrees + (Dec_MSnwLat_minutes / 60.0) + (Dec_MSnwLat_sec / 3600.0)))

 					Pre_MSnwLong = sceneMS.getElementsByTagName("nwLong")[0]
 					Pre_MSnwLong_unicode = Pre_MSnwLong.childNodes[0].data
 					Pre_MSnwLong_value = Pre_MSnwLong_unicode.strip("\n")
 					MSnwLong_value = str(Pre_MSnwLong_value)

 					Pre_Dec_MSnwLong_value_text = MSnwLong_value[:1]
 					Pre_Dec_MSnwLong_Degrees = MSnwLong_value[1:-4]
 					Dec_MSnwLong_Degrees = np.float64(Pre_Dec_MSnwLong_Degrees)
 					Pre_Dec_MSnwLong_minutes = MSnwLong_value[4:-2]
 					Dec_MSnwLong_minutes = np.float64(Pre_Dec_MSnwLong_minutes)
 					Pre_Dec_MSnwLong_sec = MSnwLong_value[6:]
 					Dec_MSnwLong_sec = np.float64(Pre_Dec_MSnwLong_sec)

 					if Pre_Dec_MSnwLong_value_text == "W":
 						Dec_MSnwLong_value_text = 1.0

 					elif Pre_Dec_MSnwLong_value_text == "E":
 						Dec_MSnwLong_value_text = -1.0
 					Use_MSnwLong_value = np.float64(Dec_MSnwLong_value_text * (Dec_MSnwLong_Degrees + (Dec_MSnwLong_minutes / 60.0) + (Dec_MSnwLong_sec / 3600.0)))

 					Pre_MSneLat = sceneMS.getElementsByTagName("neLat")[0]
 					Pre_MSneLat_unicode = Pre_MSneLat.childNodes[0].data
 					Pre_MSneLat_value = Pre_MSneLat_unicode.strip("\n")
 					MSneLat_value = str(Pre_MSneLat_value)

 					Pre_Dec_MSneLat_value_text = MSneLat_value[:1]
 					Pre_Dec_MSneLat_Degrees = MSneLat_value[1:-4]
 					Dec_MSneLat_Degrees = np.float64(Pre_Dec_MSneLat_Degrees)
 					Pre_Dec_MSneLat_minutes = MSneLat_value[4:-2]
 					Dec_MSneLat_minutes = np.float64(Pre_Dec_MSneLat_minutes)
 					Pre_Dec_MSneLat_sec = MSneLat_value[6:]
 					Dec_MSneLat_sec = np.float64(Pre_Dec_MSneLat_sec)

 					if Pre_Dec_MSneLat_value_text == "N":
 						Dec_MSneLat_value_text = 1.0

 					elif Pre_Dec_MSneLat_value_text == "S":
 						Dec_MSneLat_value_text = -1.0
 					Use_MSneLat_value = np.float64(Dec_MSneLat_value_text * (Dec_MSneLat_Degrees + (Dec_MSneLat_minutes / 60.0) + (Dec_MSneLat_sec / 3600.0)))

 					Pre_MSneLong = sceneMS.getElementsByTagName("neLong")[0]
 					Pre_MSneLong_unicode = Pre_MSneLong.childNodes[0].data
 					Pre_MSneLong_value = Pre_MSneLong_unicode.strip("\n")
 					MSneLong_value = str(Pre_MSneLong_value)

 					Pre_Dec_MSneLong_value_text = MSneLong_value[:1]
 					Pre_Dec_MSneLong_Degrees = MSneLong_value[1:-4]
 					Dec_MSneLong_Degrees = np.float64(Pre_Dec_MSneLong_Degrees)
 					Pre_Dec_MSneLong_minutes = MSneLong_value[4:-2]
 					Dec_MSneLong_minutes = np.float64(Pre_Dec_MSneLong_minutes)
 					Pre_Dec_MSneLong_sec = MSneLong_value[6:]
 					Dec_MSneLong_sec = np.float64(Pre_Dec_MSneLong_sec)
 					if Pre_Dec_MSneLong_value_text == "W":
 						Dec_MSneLong_value_text = 1.0

 					elif Pre_Dec_MSneLong_value_text == "E":
 						Dec_MSneLong_value_text = -1.0
 					Use_MSneLong_value = np.float64(Dec_MSneLong_value_text * (Dec_MSneLong_Degrees + (Dec_MSneLong_minutes / 60.0) + (Dec_MSneLong_sec / 3600.0)))

 					Pre_MSswLat = sceneMS.getElementsByTagName("swLat")[0]
 					Pre_MSswLat_unicode = Pre_MSswLat.childNodes[0].data
 					Pre_MSswLat_value = Pre_MSswLat_unicode.strip("\n")
 					MSswLat_value = str(Pre_MSswLat_value)

 					Pre_Dec_MSswLat_value_text = MSswLat_value[:1]
 					Pre_Dec_MSswLat_Degrees = MSswLat_value[1:-4]
 					Dec_MSswLat_Degrees = np.float64(Pre_Dec_MSswLat_Degrees)
 					Pre_Dec_MSswLat_minutes = MSswLat_value[4:-2]
 					Dec_MSswLat_minutes = np.float64(Pre_Dec_MSswLat_minutes)
 					Pre_Dec_MSswLat_sec = MSswLat_value[6:]
 					Dec_MSswLat_sec = np.float64(Pre_Dec_MSswLat_sec)

 					if Pre_Dec_MSswLat_value_text == "N":
 						Dec_MSswLat_value_text = 1.0

 					elif Pre_Dec_MSswLat_value_text == "S":
 						Dec_MSswLat_value_text = -1.0
 					Use_MSswLat_value = np.float64(Dec_MSswLat_value_text * (Dec_MSswLat_Degrees + (Dec_MSswLat_minutes / 60.0) + (Dec_MSswLat_sec / 3600.0)))

 					Pre_MSswLong = sceneMS.getElementsByTagName("swLong")[0]
 					Pre_MSswLong_unicode = Pre_MSswLong.childNodes[0].data
 					Pre_MSswLong_value = Pre_MSswLong_unicode.strip("\n")
 					MSswLong_value = str(Pre_MSswLong_value)

 					Pre_Dec_MSswLong_value_text = MSswLong_value[:1]
 					Pre_Dec_MSswLong_Degrees = MSswLong_value[1:-4]
 					Dec_MSswLong_Degrees = np.float64(Pre_Dec_MSswLong_Degrees)
 					Pre_Dec_MSswLong_minutes = MSswLong_value[4:-2]
 					Dec_MSswLong_minutes = np.float64(Pre_Dec_MSswLong_minutes)
 					Pre_Dec_MSswLong_sec = MSswLong_value[6:]
 					Dec_MSswLong_sec = np.float64(Pre_Dec_MSswLong_sec)

 					if Pre_Dec_MSswLong_value_text == "W":
 						Dec_MSswLong_value_text = 1.0

 					elif Pre_Dec_MSswLong_value_text == "E":
 						Dec_MSswLong_value_text = -1.0
 					Use_MSswLong_value = np.float64(Dec_MSswLong_value_text * (Dec_MSswLong_Degrees + (Dec_MSswLong_minutes / 60.0) + (Dec_MSswLong_sec / 3600.0)))

 					Pre_MSseLat = sceneMS.getElementsByTagName("seLat")[0]
 					Pre_MSseLat_unicode = Pre_MSseLat.childNodes[0].data
 					Pre_MSseLat_value = Pre_MSseLat_unicode.strip("\n")
 					MSseLat_value = str(Pre_MSseLat_value)

 					Pre_Dec_MSseLat_value_text = MSseLat_value[:1]
 					Pre_Dec_MSseLat_Degrees = MSseLat_value[1:-4]
 					Dec_MSseLat_Degrees = np.float64(Pre_Dec_MSseLat_Degrees)
 					Pre_Dec_MSseLat_minutes = MSseLat_value[4:-2]
 					Dec_MSseLat_minutes = np.float64(Pre_Dec_MSseLat_minutes)
 					Pre_Dec_MSseLat_sec = MSseLat_value[6:]
 					Dec_MSseLat_sec = np.float64(Pre_Dec_MSseLat_sec)

 					if Pre_Dec_MSseLat_value_text == "N":
 						Dec_MSseLat_value_text = 1.0

 					elif Pre_Dec_MSseLat_value_text == "S":
 						Dec_MSseLat_value_text = -1.0
 					Use_MSseLat_value = np.float64(Dec_MSseLat_value_text * (Dec_MSseLat_Degrees + (Dec_MSseLat_minutes / 60.0) + (Dec_MSseLat_sec / 3600.0)))

 					Pre_MSseLong = sceneMS.getElementsByTagName("seLong")[0]
 					Pre_MSseLong_unicode = Pre_MSseLong.childNodes[0].data
 					Pre_MSseLong_value = Pre_MSseLong_unicode.strip("\n")
 					MSseLong_value = str(Pre_MSseLong_value)

 					Pre_Dec_MSseLong_value_text = MSseLong_value[:1]
 					Pre_Dec_MSseLong_Degrees = MSseLong_value[1:-4]
 					Dec_MSseLong_Degrees = np.float64(Pre_Dec_MSseLong_Degrees)
 					Pre_Dec_MSseLong_minutes = MSseLong_value[4:-2]
 					Dec_MSseLong_minutes = np.float64(Pre_Dec_MSseLong_minutes)
 					Pre_Dec_MSseLong_sec = MSseLong_value[6:]
 					Dec_MSseLong_sec = np.float64(Pre_Dec_MSseLong_sec)

 					if Pre_Dec_MSseLong_value_text == "W":
 						Dec_MSseLong_value_text = 1.0

 					elif Pre_Dec_MSseLong_value_text == "E":
 						Dec_MSseLong_value_text = -1.0
 					Use_MSseLong_value = np.float64(Dec_MSseLong_value_text * (Dec_MSseLong_Degrees + (Dec_MSseLong_minutes / 60.0) + (Dec_MSseLong_sec / 3600.0)))

					# {Get BrowseBeginLine from CUF file}
					Pre_BrowseBeginLineMS = sceneMS.getElementsByTagName("browseBeginLine")[0]
					Pre_BrowseBeginLineMS_unicode = Pre_BrowseBeginLineMS.childNodes[0].data
					Pre_BrowseBeginLineMS_value = Pre_BrowseBeginLineMS_unicode.strip("\n")
					BrowseBeginLineMS_value = int(Pre_BrowseBeginLineMS_value)

					# {Get BrowseEndLine from CUF file}
					Pre_BrowseEndLineMS = sceneMS.getElementsByTagName("browseEndLine")[0]
					Pre_BrowseEndLineMS_unicode = Pre_BrowseEndLineMS.childNodes[0].data
					Pre_BrowseEndLineMS_value = Pre_BrowseEndLineMS_unicode.strip("\n")
					BrowseEndLineMS_value = int(Pre_BrowseEndLineMS_value)

					# Create catalog file
					Image_FilenameMS = FIlename_path + "/" + RevolutionNumber_value + "_" + SpectralMode_value + "_Filename%s_SceneRank_%s.cmp"%(FileNameMS_value , str(SceneMSRank_value))
					Image_FilenameMS_file = open(Image_FilenameMS, "w")
					Image_FilenameMS_file.write(str(BeginReception_year) + str(BeginReception_month) + str(BeginReception_date) + "\n")
					Image_FilenameMS_file.write(str(BeginReception_hour) + str(BeginReception_min) + str(BeginReception_sec) + "\n")
					Image_FilenameMS_file.write(str(EndReception_year) + str(EndReception_month) + str(EndReception_date) + "\n")
					Image_FilenameMS_file.write(str(EndReception_hour) + str(EndReception_min) + str(EndReception_sec) + "\n")
					Image_FilenameMS_file.write(str(OrbitCycle_value) + "\n")
					Image_FilenameMS_file.write(str(RevolutionNumber_value) + "\n")
					Image_FilenameMS_file.write(str(Mission_value) + "\n")
					Image_FilenameMS_file.write(str(SatelliteIdt_value) + "\n")
					Image_FilenameMS_file.write(str(PassRank_value) + "\n")
					Image_FilenameMS_file.write(str(PassId_value) + "\n")
					Image_FilenameMS_file.write(str(SegmentCount_value) + "\n")
					Image_FilenameMS_file.write(str("Segment info") + "\n")
					Image_FilenameMS_file.write(str(FileNameMS_value) + "\n")
					Image_FilenameMS_file.write(str(GERALDMS_name) + "\n")
					Image_FilenameMS_file.write(str(MSSegmentRank_value) + "\n")
					Image_FilenameMS_file.write(str(InstrumentTypeMS_value) + str(InstrumentIDMS_value) + "\n")
					Image_FilenameMS_file.write(str(TransmissionModeMS_value) + "\n")
					Image_FilenameMS_file.write(str(MSsegmentquality_value) + "\n")
					Image_FilenameMS_file.write(str(YearMS_segment) + str(MonthMS_segment) + str(DateMS_segment) + "\n")
					Image_FilenameMS_file.write(str(HourMS_segment) + str(MinMS_segment) + str(SecMS_segment) + "\n")
					Image_FilenameMS_file.write(str(EndYearMS_segment) + str(EndMonthMS_segment) + str(EndDateMS_segment) + "\n")
					Image_FilenameMS_file.write(str(EndHourMS_segment) + str(EndMinMS_segment) + str(EndSecMS_segment) + "\n")
					Image_FilenameMS_file.write(str(MSCompression_ratio_value) + "\n")
					Image_FilenameMS_file.write(str(SpectralMode_value) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[0]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[1]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[2]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[3]) + "\n")
					Image_FilenameMS_file.write(str(MSReferenceBand_value) + "\n")
					Image_FilenameMS_file.write(str(MS_Alongtrackviewingangle_value) + "\n")
					Image_FilenameMS_file.write(str(MS_Acrosstrackviewingangle_value) + "\n")
					Image_FilenameMS_file.write(str(MS_ABSGain_value) + "\n")
					Image_FilenameMS_file.write(str("Scene info") + "\n")
					Image_FilenameMS_file.write(str(ScenecountMS_value) + "\n")
					Image_FilenameMS_file.write(str(SceneMSRank_value) + "\n")
					Image_FilenameMS_file.write(str(Grid_RefMS) + "\n")
					Image_FilenameMS_file.write(str(MStechnicalquality_value) + "\n")
					Image_FilenameMS_file.write(str(MScloudCover_value) + "\n")
					Image_FilenameMS_file.write(str(MSsnowcover_value) + "\n")
					Image_FilenameMS_file.write(str(create_dateMS[:4]) + str(create_dateMS[4:6]) + str(create_dateMS[6:]) + "\n")
					Image_FilenameMS_file.write(str(Use_CenterViewingDateMS_value) + "\n")
					Image_FilenameMS_file.write(str(YearBeginMS) + str(MonthBeginMS) + str(DateBeginMS) + "\n")
					Image_FilenameMS_file.write(str(HourBeginMS) + str(MinBeginMS) + str(SecBeginMS) + "\n")
					Image_FilenameMS_file.write(str(YearEndMS) + str(MonthEndMS) + str(DateEndMS) + "\n")
					Image_FilenameMS_file.write(str(HourEndMS) + str(MinEndMS) + str(SecEndMS) + "\n")
					Image_FilenameMS_file.write(str(MScouplingmode_value) + "\n")
					Image_FilenameMS_file.write(str(MSorientationAngle_value) + "\n")
					Image_FilenameMS_file.write(str(MSIncidenceangle_value) + "\n")
					Image_FilenameMS_file.write(str(MSSunElevation_value) + "\n")
					Image_FilenameMS_file.write(str(MSSunAzimuth_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSnwLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSnwLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSneLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSneLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSswLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSswLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSseLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSseLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSLatSceneCenter_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSLongSceneCenter_value) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[0]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[1]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[2]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[3]))
					Image_FilenameMS_file.close()

					# # Create catalog file
					Image_Date_timeMS_filename = Date_time_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Date-%s-%s-%s_Time-%s-%s-%s.cmp"%(str(create_dateMS[:4]),str(create_dateMS[4:6]),str(create_dateMS[6:]),Use_CenterViewingDateMS_value[:-4], Use_CenterViewingDateMS_value[2:-2],Use_CenterViewingDateMS_value[4:])
					Image_ConerMS_filename = Corner_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Upper_Left(%.4f , %.4f)_Upper_Right(%.4f , %.4f)_Lower_Left(%.4f , %.4f)_Lower_Right(%.4f , %.4f).cmp"%(Use_MSnwLat_value ,Use_MSnwLong_value ,Use_MSneLat_value , Use_MSneLong_value , Use_MSswLat_value , Use_MSswLong_value , Use_MSseLat_value , Use_MSseLong_value)
					Image_CenterMS_filename = Center_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Center_Lat_long(%.4f , %.4f).cmp"%(Use_MSLatSceneCenter_value , Use_MSLongSceneCenter_value)

					shutil.copy(Image_FilenameMS , Image_Date_timeMS_filename)
					shutil.copy(Image_FilenameMS , Image_ConerMS_filename)
					shutil.copy(Image_FilenameMS , Image_CenterMS_filename)


					crop_img_MS = imgMS[BrowseBeginLineMS_value : 499 + BrowseBeginLineMS_value, 0:ColumnsCountMS_value]
					cv2.imwrite(Image_FilenameMS[:-4] + ".JPG", crop_img_MS)

					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_Date_timeMS_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_ConerMS_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_CenterMS_filename[:-4] + ".JPG")

				# Last scene condition
				elif SceneMSRank_value == ScenecountMS_value :
					# Get centerViewingDate from catalog file and use it to file name of Image detail file
					Pre_CenterViewingDateMS = sceneMS.getElementsByTagName("centerViewingDate")[0]
					Pre_CenterViewingDateMS_unicode = Pre_CenterViewingDateMS.childNodes[0].data
					Pre_CenterViewingDateMS_value = Pre_CenterViewingDateMS_unicode.strip("\n")
					CenterViewingDateMS_time = Pre_CenterViewingDateMS_value[8:14]
					CenterViewingDateMS_value = str(CenterViewingDateMS_time)
					Use_CenterViewingDateMS_value = str(CenterViewingDateMS_time)[:2] + str(CenterViewingDateMS_time)[2:4] + str(CenterViewingDateMS_time)[4:]
					create_dateMS = Pre_CenterViewingDateMS_value[:8]

					Pre_beginViewingDateMS = sceneMS.getElementsByTagName("beginViewingDate")[0]
					Pre_beginViewingDateMS_unicode = Pre_beginViewingDateMS.childNodes[0].data
					Pre_beginViewingDateMS_value = Pre_beginViewingDateMS_unicode.strip("\n")
					BeginViewingDateMS_value = str(Pre_beginViewingDateMS_value)

					Pre_YearBeginMS = BeginViewingDateMS_value [:4]
					YearBeginMS = str(Pre_YearBeginMS)

					Pre_MonthBeginMS = BeginViewingDateMS_value [4:6]
					MonthBeginMS = str(Pre_MonthBeginMS)

					Pre_DateBeginMS = BeginViewingDateMS_value [6:8]
					DateBeginMS = str(Pre_DateBeginMS)

					Pre_HourBeginMS = BeginViewingDateMS_value [8:10]
					HourBeginMS = str(Pre_HourBeginMS)

					Pre_MinBeginMS = BeginViewingDateMS_value [10:12]
					MinBeginMS = str(Pre_MinBeginMS)

					Pre_SecBeginMS = BeginViewingDateMS_value [12:14]
					SecBeginMS = str(Pre_SecBeginMS)

					Pre_EndViewingDateMS = sceneMS.getElementsByTagName("endViewingDate")[0]
					Pre_EndViewingDateMS_unicode = Pre_EndViewingDateMS.childNodes[0].data
					Pre_EndViewingDateMS_value = Pre_EndViewingDateMS_unicode.strip("\n")
					EndViewingDateMS_value = str(Pre_EndViewingDateMS_value)

					Pre_YearEndMS = EndViewingDateMS_value [:4]
					YearEndMS = str(Pre_YearEndMS)

					Pre_MonthEndMS = EndViewingDateMS_value [4:6]
					MonthEndMS = str(Pre_MonthEndMS)

					Pre_DateEndMS = EndViewingDateMS_value [6:8]
					DateEndMS = str(Pre_DateEndMS)

					Pre_HourEndMS = EndViewingDateMS_value [8:10]
					HourEndMS = str(Pre_HourEndMS)

					Pre_MinEndMS = EndViewingDateMS_value [10:12]
					MinEndMS = str(Pre_MinEndMS)

					Pre_SecEndMS = EndViewingDateMS_value [12:14]
					SecEndMS = str(Pre_SecEndMS)

					""" Get DSR_begin from Normal scene
					first  : Get beginRangeLine from catalog file
					second : Use 4 loop to put beginRangeLine + Offset value
							 because Offset value as list and it have 4 Index
					third  : then get pre dsrbegin - 2400 (40% of product line) """

					# {
					# Get beginRangeLine from CUF file
					Pre_BeginRangelineMS = sceneMS.getElementsByTagName("beginRangeLine")[0]
					Pre_BeginRangelineMS_unicode = Pre_BeginRangelineMS.childNodes[0].data
					Pre_BeginRangelineMS_value = Pre_BeginRangelineMS_unicode.strip("\n")
					BeginRangeLineMS_value = int(Pre_BeginRangelineMS_value)

					Pre_EndRangelineMS = sceneMS.getElementsByTagName("endRangeLine")[0]
					Pre_EndRangelineMS_unicode = Pre_EndRangelineMS.childNodes[0].data
					Pre_EndRangelineMS_value = Pre_EndRangelineMS_unicode.strip("\n")
					EndRangeLineMS_value = int(Pre_EndRangelineMS_value)

					# Create for loop 4 Index
					for i in range(0, 4):
						#  put (BeginRangeLineMS_value - 2400) + Offset value and put answer in to DSR_begin list
						DSR_beginMS = int(BeginRangeLineMS_value + Offset_value[i])
						DSR_beginMS_list.append(DSR_beginMS)

						DSR_endMS = (EndRangeLineMS_value + Offset_value[i])
						DSR_endMS_list.append(DSR_endMS)

					# { Get KPath and JRow from CUF file and use it to Grid reference
					Pre_KPathMS = sceneMS.getElementsByTagName("kPath")[0]
					Pre_KPathMS_unicode = Pre_KPathMS.childNodes[0].data
					Pre_KPathMS_value = Pre_KPathMS_unicode.strip("\n")
					KPathMS_value = str(Pre_KPathMS_value)

					Pre_JRowMS = sceneMS.getElementsByTagName("jRow")[0]
					Pre_JRowMS_unicode = Pre_JRowMS.childNodes[0].data
					Pre_JRowMS_value = Pre_JRowMS_unicode.strip("\n")
					JRowMS_value = str(Pre_JRowMS_value)

					Grid_RefMS = KPathMS_value + "-" + JRowMS_value
					# }

					Pre_MStechnicalquality = sceneMS.getElementsByTagName("technoQuality")[0]
					Pre_MStechnicalquality_unicode = Pre_MStechnicalquality.childNodes[0].data
					Pre_MStechnicalquality_value = Pre_MStechnicalquality_unicode.strip("\n")
					MStechnicalquality_value = str(Pre_MStechnicalquality_value)

					Pre_MScloudCover = sceneMS.getElementsByTagName("cloudCover")[0]
					Pre_MScloudCover_unicode = Pre_MScloudCover.childNodes[0].data
					Pre_MScloudCover_value = Pre_MScloudCover_unicode.strip("\n")
					MScloudCover_value = str(Pre_MScloudCover_value)

					Pre_MSsnowcover = sceneMS.getElementsByTagName("snowCover")[0]
					Pre_MSsnowcover_unicode = Pre_MSsnowcover.childNodes[0].data
					Pre_MSsnowcover_value = Pre_MSsnowcover_unicode.strip("\n")
					MSsnowcover_value = str(Pre_MSsnowcover_value)

					Pre_MScouplingmode = sceneMS.getElementsByTagName("couplingMode")[0]
					Pre_MScouplingmode_unicode = Pre_MScouplingmode.childNodes[0].data
					Pre_MScouplingmode_value = Pre_MScouplingmode_unicode.strip("\n")
					MScouplingmode_value = str(Pre_MScouplingmode_value)

					Pre_MSorientationAngle = sceneMS.getElementsByTagName("orientationAngle")[0]
					Pre_MSorientationAngle_unicode = Pre_MSorientationAngle.childNodes[0].data
					Pre_MSorientationAngle_value = Pre_MSorientationAngle_unicode.strip("\n")
					MSorientationAngle_value = str(Pre_MSorientationAngle_value)
					# print "Orientation angle : %.10f"%MSorientationAngle_value

					Pre_MSIncidenceangle = sceneMS.getElementsByTagName("incidenceAngle")[0]
					Pre_MSIncidenceangle_unicoce = Pre_MSIncidenceangle.childNodes[0].data
					Pre_MSIncidenceangle_value = Pre_MSIncidenceangle_unicoce.strip("\n")
					MSIncidenceangle_value = str(Pre_MSIncidenceangle_value)
					# print "Incidence angle : %.10f"%MSIncidenceangle_value

					Pre_MSLatSceneCenter = sceneMS.getElementsByTagName("latSceneCenter")[0]
					Pre_MSLatSceneCenter_unicode = Pre_MSLatSceneCenter.childNodes[0].data
					Pre_MSLatSceneCenter_value = Pre_MSLatSceneCenter_unicode.strip("\n")
					MSLatSceneCenter_value = str(Pre_MSLatSceneCenter_value)

					Pre_Dec_MSLatSceneCenter_text = MSLatSceneCenter_value[:1]
					Pre_Dec_MSLatSceneCenter_Degrees = MSLatSceneCenter_value[1:-4]
					Dec_MSLatSceneCenter_Degrees = np.float64(Pre_Dec_MSLatSceneCenter_Degrees)
					Pre_Dec_MSLatSceneCenter_minutes = MSLatSceneCenter_value[4:-2]
					Dec_MSLatSceneCenter_minutes = np.float64(Pre_Dec_MSLatSceneCenter_minutes)
					Pre_Dec_MSLatSceneCenter_sec = MSLatSceneCenter_value[6:]
					Dec_MSLatSceneCenter_sec = np.float64(Pre_Dec_MSLatSceneCenter_sec)
					# print Pre_Dec_MSLatSceneCenter_sec

					if Pre_Dec_MSLatSceneCenter_text == "N" :
						Dec_MSLatSceneCenter_text = 1.0
					elif Pre_Dec_MSLatSceneCenter_text == "S" :
						Dec_MSLatSceneCenter_text = -1.0
					Use_MSLatSceneCenter_value = np.float64(Dec_MSLatSceneCenter_text * (Dec_MSLatSceneCenter_Degrees + (Dec_MSLatSceneCenter_minutes / 60.0) + (Dec_MSLatSceneCenter_sec / 3600.0)))

 					Pre_MSLongSceneCenter = sceneMS.getElementsByTagName("longSceneCenter")[0]
 					Pre_MSLongSceneCenter_unicode = Pre_MSLongSceneCenter.childNodes[0].data
 					Pre_MSLongSceneCenter_value = Pre_MSLongSceneCenter_unicode.strip("\n")
 					MSLongSceneCenter_value = str(Pre_MSLongSceneCenter_value)
 					Pre_Dec_MSLongSceneCenter_text = MSLongSceneCenter_value[:1]
 					Pre_Dec_MSLongSceneCenter_Degrees = MSLatSceneCenter_value[1:-4]
 					Dec_MSLongSceneCenter_Degrees = np.float64(Pre_Dec_MSLongSceneCenter_Degrees)
 					Pre_Dec_MSLongSceneCenter_minutes = MSLongSceneCenter_value[4:-2]
 					Dec_MSLongSceneCenter_minutes = np.float64(Pre_Dec_MSLongSceneCenter_minutes)
 					Pre_Dec_MSLongSceneCenter_sec = MSLongSceneCenter_value[6:]
 					Dec_MSLongSceneCenter_sec = np.float64(Pre_Dec_MSLongSceneCenter_sec)

 					if Pre_Dec_MSLongSceneCenter_text == "E":
 						Dec_MSLongSceneCenter_text = 1.0
 					elif Pre_Dec_MSLongSceneCenter_text == "W":
 						Dec_MSLongSceneCenter_text = -1.0
 					Use_MSLongSceneCenter_value = np.float64(Dec_MSLongSceneCenter_text * (Dec_MSLongSceneCenter_Degrees + (Dec_MSLongSceneCenter_minutes / 60.0) + (Dec_MSLongSceneCenter_sec / 3600.0)))

 					Pre_MSSunElevation = sceneMS.getElementsByTagName("sunElevation")[0]
 					Pre_MSSunElevation_unicode = Pre_MSSunElevation.childNodes[0].data
 					Pre_MSSunElevation_value = Pre_MSSunElevation_unicode.strip("\n")
 					MSSunElevation_value = str(Pre_MSSunElevation_value)
 					# print "Sun elevation : %.2f"%MSSunElevation_value

 					Pre_MSSunAzimuth = sceneMS.getElementsByTagName("sunAzimuth")[0]
 					Pre_MSSunAzimuth_unicode = Pre_MSSunAzimuth.childNodes[0].data
 					Pre_MSSunAzimuth_value = Pre_MSSunAzimuth_unicode.strip("\n")
 					MSSunAzimuth_value = str(Pre_MSSunAzimuth_value)
 					# print "Sun azimuth : %.2f"%MSSunAzimuth_value

 					Pre_MSnwLat = sceneMS.getElementsByTagName("nwLat")[0]
 					Pre_MSnwLat_unicode = Pre_MSnwLat.childNodes[0].data
 					Pre_MSnwLat_value = Pre_MSnwLat_unicode.strip("\n")
 					MSnwLat_value = str(Pre_MSnwLat_value)

 					Pre_Dec_MSnwLat_value_text = MSnwLat_value[:1]
 					Pre_Dec_MSnwLat_Degrees = MSnwLat_value[1:-4]
 					Dec_MSnwLat_Degrees = np.float64(Pre_Dec_MSnwLat_Degrees)
 					Pre_Dec_MSnwLat_minutes = MSnwLat_value[4:-2]
 					Dec_MSnwLat_minutes = np.float64(Pre_Dec_MSnwLat_minutes)
 					Pre_Dec_MSnwLat_sec = MSnwLat_value[6:]
 					Dec_MSnwLat_sec = np.float64(Pre_Dec_MSnwLat_sec)

 					if Pre_Dec_MSnwLat_value_text == "N":
 						Dec_MSnwLat_value_text = 1.0

 					elif Pre_Dec_MSnwLat_value_text == "S":
 						Dec_MSnwLat_value_text = -1.0
 					Use_MSnwLat_value = np.float64(Dec_MSnwLat_value_text * (Dec_MSnwLat_Degrees + (Dec_MSnwLat_minutes / 60.0) + (Dec_MSnwLat_sec / 3600.0)))

 					Pre_MSnwLong = sceneMS.getElementsByTagName("nwLong")[0]
 					Pre_MSnwLong_unicode = Pre_MSnwLong.childNodes[0].data
 					Pre_MSnwLong_value = Pre_MSnwLong_unicode.strip("\n")
 					MSnwLong_value = str(Pre_MSnwLong_value)
 					Pre_Dec_MSnwLong_value_text = MSnwLong_value[:1]

 					Pre_Dec_MSnwLong_Degrees = MSnwLong_value[1:-4]
 					Dec_MSnwLong_Degrees = np.float64(Pre_Dec_MSnwLong_Degrees)
 					Pre_Dec_MSnwLong_minutes = MSnwLong_value[4:-2]
 					Dec_MSnwLong_minutes = np.float64(Pre_Dec_MSnwLong_minutes)
 					Pre_Dec_MSnwLong_sec = MSnwLong_value[6:]
 					Dec_MSnwLong_sec = np.float64(Pre_Dec_MSnwLong_sec)

 					if Pre_Dec_MSnwLong_value_text == "W":
 						Dec_MSnwLong_value_text = 1.0

 					elif Pre_Dec_MSnwLong_value_text == "E":
 						Dec_MSnwLong_value_text = -1.0
 					Use_MSnwLong_value = np.float64(Dec_MSnwLong_value_text * (Dec_MSnwLong_Degrees + (Dec_MSnwLong_minutes / 60.0) + (Dec_MSnwLong_sec / 3600.0)))

 					Pre_MSneLat = sceneMS.getElementsByTagName("neLat")[0]
 					Pre_MSneLat_unicode = Pre_MSneLat.childNodes[0].data
 					Pre_MSneLat_value = Pre_MSneLat_unicode.strip("\n")
 					MSneLat_value = str(Pre_MSneLat_value)

 					Pre_Dec_MSneLat_value_text = MSneLat_value[:1]
 					Pre_Dec_MSneLat_Degrees = MSneLat_value[1:-4]
 					Dec_MSneLat_Degrees = np.float64(Pre_Dec_MSneLat_Degrees)
 					Pre_Dec_MSneLat_minutes = MSneLat_value[4:-2]
 					Dec_MSneLat_minutes = np.float64(Pre_Dec_MSneLat_minutes)
 					Pre_Dec_MSneLat_sec = MSneLat_value[6:]
 					Dec_MSneLat_sec = np.float64(Pre_Dec_MSneLat_sec)

 					if Pre_Dec_MSneLat_value_text == "N":
 						Dec_MSneLat_value_text = 1.0

 					elif Pre_Dec_MSneLat_value_text == "S":
 						Dec_MSneLat_value_text = -1.0
 					Use_MSneLat_value = np.float64(Dec_MSneLat_value_text * (Dec_MSneLat_Degrees + (Dec_MSneLat_minutes / 60.0) + (Dec_MSneLat_sec / 3600.0)))

 					Pre_MSneLong = sceneMS.getElementsByTagName("neLong")[0]
 					Pre_MSneLong_unicode = Pre_MSneLong.childNodes[0].data
 					Pre_MSneLong_value = Pre_MSneLong_unicode.strip("\n")
 					MSneLong_value = str(Pre_MSneLong_value)

 					Pre_Dec_MSneLong_value_text = MSneLong_value[:1]
 					Pre_Dec_MSneLong_Degrees = MSneLong_value[1:-4]
 					Dec_MSneLong_Degrees = np.float64(Pre_Dec_MSneLong_Degrees)
 					Pre_Dec_MSneLong_minutes = MSneLong_value[4:-2]
 					Dec_MSneLong_minutes = np.float64(Pre_Dec_MSneLong_minutes)
 					Pre_Dec_MSneLong_sec = MSneLong_value[6:]
 					Dec_MSneLong_sec = np.float64(Pre_Dec_MSneLong_sec)

 					if Pre_Dec_MSneLong_value_text == "W":
 						Dec_MSneLong_value_text = 1.0

 					elif Pre_Dec_MSneLong_value_text == "E":
 						Dec_MSneLong_value_text = -1.0
 					Use_MSneLong_value = np.float64(Dec_MSneLong_value_text * (Dec_MSneLong_Degrees + (Dec_MSneLong_minutes / 60.0) + (Dec_MSneLong_sec / 3600.0)))

 					Pre_MSswLat = sceneMS.getElementsByTagName("swLat")[0]
 					Pre_MSswLat_unicode = Pre_MSswLat.childNodes[0].data
 					Pre_MSswLat_value = Pre_MSswLat_unicode.strip("\n")
 					MSswLat_value = str(Pre_MSswLat_value)

 					Pre_Dec_MSswLat_value_text = MSswLat_value[:1]
 					Pre_Dec_MSswLat_Degrees = MSswLat_value[1:-4]
 					Dec_MSswLat_Degrees = np.float64(Pre_Dec_MSswLat_Degrees)
 					Pre_Dec_MSswLat_minutes = MSswLat_value[4:-2]
 					Dec_MSswLat_minutes = np.float64(Pre_Dec_MSswLat_minutes)
 					Pre_Dec_MSswLat_sec = MSswLat_value[6:]
 					Dec_MSswLat_sec = np.float64(Pre_Dec_MSswLat_sec)

 					if Pre_Dec_MSswLat_value_text == "N":
 						Dec_MSswLat_value_text = 1.0

 					elif Pre_Dec_MSswLat_value_text == "S":
 						Dec_MSswLat_value_text = -1.0
 					Use_MSswLat_value = np.float64(Dec_MSswLat_value_text * (Dec_MSswLat_Degrees + (Dec_MSswLat_minutes / 60.0) + (Dec_MSswLat_sec / 3600.0)))

 					Pre_MSswLong = sceneMS.getElementsByTagName("swLong")[0]
 					Pre_MSswLong_unicode = Pre_MSswLong.childNodes[0].data
 					Pre_MSswLong_value = Pre_MSswLong_unicode.strip("\n")
 					MSswLong_value = str(Pre_MSswLong_value)

 					Pre_Dec_MSswLong_value_text = MSswLong_value[:1]
 					Pre_Dec_MSswLong_Degrees = MSswLong_value[1:-4]
 					Dec_MSswLong_Degrees = np.float64(Pre_Dec_MSswLong_Degrees)
 					Pre_Dec_MSswLong_minutes = MSswLong_value[4:-2]
 					Dec_MSswLong_minutes = np.float64(Pre_Dec_MSswLong_minutes)
 					Pre_Dec_MSswLong_sec = MSswLong_value[6:]
 					Dec_MSswLong_sec = np.float64(Pre_Dec_MSswLong_sec)

 					if Pre_Dec_MSswLong_value_text == "W":
 						Dec_MSswLong_value_text = 1.0

 					elif Pre_Dec_MSswLong_value_text == "E":
 						Dec_MSswLong_value_text = -1.0
 					Use_MSswLong_value = np.float64(Dec_MSswLong_value_text * (Dec_MSswLong_Degrees + (Dec_MSswLong_minutes / 60.0) + (Dec_MSswLong_sec / 3600.0)))

 					Pre_MSseLat = sceneMS.getElementsByTagName("seLat")[0]
 					Pre_MSseLat_unicode = Pre_MSseLat.childNodes[0].data
 					Pre_MSseLat_value = Pre_MSseLat_unicode.strip("\n")
 					MSseLat_value = str(Pre_MSseLat_value)

 					Pre_Dec_MSseLat_value_text = MSseLat_value[:1]
 					Pre_Dec_MSseLat_Degrees = MSseLat_value[1:-4]
 					Dec_MSseLat_Degrees = np.float64(Pre_Dec_MSseLat_Degrees)
 					Pre_Dec_MSseLat_minutes = MSseLat_value[4:-2]
 					Dec_MSseLat_minutes = np.float64(Pre_Dec_MSseLat_minutes)
 					Pre_Dec_MSseLat_sec = MSseLat_value[6:]
 					Dec_MSseLat_sec = np.float64(Pre_Dec_MSseLat_sec)

 					if Pre_Dec_MSseLat_value_text == "N":
 						Dec_MSseLat_value_text = 1.0

 					elif Pre_Dec_MSseLat_value_text == "S":
 						Dec_MSseLat_value_text = -1.0
 					Use_MSseLat_value = np.float64(Dec_MSseLat_value_text * (Dec_MSseLat_Degrees + (Dec_MSseLat_minutes / 60.0) + (Dec_MSseLat_sec / 3600.0)))

 					Pre_MSseLong = sceneMS.getElementsByTagName("seLong")[0]
 					Pre_MSseLong_unicode = Pre_MSseLong.childNodes[0].data
 					Pre_MSseLong_value = Pre_MSseLong_unicode.strip("\n")
 					MSseLong_value = str(Pre_MSseLong_value)

 					Pre_Dec_MSseLong_value_text = MSseLong_value[:1]
 					Pre_Dec_MSseLong_Degrees = MSseLong_value[1:-4]
 					Dec_MSseLong_Degrees = np.float64(Pre_Dec_MSseLong_Degrees)
 					Pre_Dec_MSseLong_minutes = MSseLong_value[4:-2]
 					Dec_MSseLong_minutes = np.float64(Pre_Dec_MSseLong_minutes)
 					Pre_Dec_MSseLong_sec = MSseLong_value[6:]
 					Dec_MSseLong_sec = np.float64(Pre_Dec_MSseLong_sec)

 					if Pre_Dec_MSseLong_value_text == "W":
 						Dec_MSseLong_value_text = 1.0

 					elif Pre_Dec_MSseLong_value_text == "E":
 						Dec_MSseLong_value_text = -1.0
 					Use_MSseLong_value = np.float64(Dec_MSseLong_value_text * (Dec_MSseLong_Degrees + (Dec_MSseLong_minutes / 60.0) + (Dec_MSseLong_sec / 3600.0)))

					# {Get BrowseBeginLine from CUF file}
					Pre_BrowseBeginMS = int(Hight_MS)
					BrowseBeginLineMS_value = Pre_BrowseBeginMS - 499

					# {Get BrowseEndLine from CUF file}
					Pre_BrowseEndLineMS = sceneMS.getElementsByTagName("browseEndLine")[0]
					Pre_BrowseEndLineMS_unicode = Pre_BrowseEndLineMS.childNodes[0].data
					Pre_BrowseEndLineMS_value = Pre_BrowseEndLineMS_unicode.strip("\n")
					BrowseEndLineMS_value = int(Pre_BrowseEndLineMS_value)

					# Create catalog file
					Image_FilenameMS = FIlename_path + "/" + RevolutionNumber_value + "_" + SpectralMode_value + "_Filename%s_SceneRank_%s.cmp"%(FileNameMS_value , str(SceneMSRank_value))
					Image_FilenameMS_file = open(Image_FilenameMS, "w")
					Image_FilenameMS_file.write(str(BeginReception_year) + str(BeginReception_month) + str(BeginReception_date) + "\n")
					Image_FilenameMS_file.write(str(BeginReception_hour) + str(BeginReception_min) + str(BeginReception_sec) + "\n")
					Image_FilenameMS_file.write(str(EndReception_year) + str(EndReception_month) + str(EndReception_date) + "\n")
					Image_FilenameMS_file.write(str(EndReception_hour) + str(EndReception_min) + str(EndReception_sec) + "\n")
					Image_FilenameMS_file.write(str(OrbitCycle_value) + "\n")
					Image_FilenameMS_file.write(str(RevolutionNumber_value) + "\n")
					Image_FilenameMS_file.write(str(Mission_value) + "\n")
					Image_FilenameMS_file.write(str(SatelliteIdt_value) + "\n")
					Image_FilenameMS_file.write(str(PassRank_value) + "\n")
					Image_FilenameMS_file.write(str(PassId_value) + "\n")
					Image_FilenameMS_file.write(str(SegmentCount_value) + "\n")
					Image_FilenameMS_file.write(str("Segment info") + "\n")
					Image_FilenameMS_file.write(str(FileNameMS_value) + "\n")
					Image_FilenameMS_file.write(str(GERALDMS_name) + "\n")
					Image_FilenameMS_file.write(str(MSSegmentRank_value) + "\n")
					Image_FilenameMS_file.write(str(InstrumentTypeMS_value) + str(InstrumentIDMS_value) + "\n")
					Image_FilenameMS_file.write(str(TransmissionModeMS_value) + "\n")
					Image_FilenameMS_file.write(str(MSsegmentquality_value) + "\n")
					Image_FilenameMS_file.write(str(YearMS_segment) + str(MonthMS_segment) + str(DateMS_segment) + "\n")
					Image_FilenameMS_file.write(str(HourMS_segment) + str(MinMS_segment) + str(SecMS_segment) + "\n")
					Image_FilenameMS_file.write(str(EndYearMS_segment) + str(EndMonthMS_segment) + str(EndDateMS_segment) + "\n")
					Image_FilenameMS_file.write(str(EndHourMS_segment) + str(EndMinMS_segment) + str(EndSecMS_segment) + "\n")
					Image_FilenameMS_file.write(str(MSCompression_ratio_value) + "\n")
					Image_FilenameMS_file.write(str(SpectralMode_value) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[0]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[1]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[2]) + "\n")
					Image_FilenameMS_file.write(str(Offset_value[3]) + "\n")
					Image_FilenameMS_file.write(str(MSReferenceBand_value) + "\n")
					Image_FilenameMS_file.write(str(MS_Alongtrackviewingangle_value) + "\n")
					Image_FilenameMS_file.write(str(MS_Acrosstrackviewingangle_value) + "\n")
					Image_FilenameMS_file.write(str(MS_ABSGain_value) + "\n")
					Image_FilenameMS_file.write(str("Scene info") + "\n")
					Image_FilenameMS_file.write(str(ScenecountMS_value) + "\n")
					Image_FilenameMS_file.write(str(SceneMSRank_value) + "\n")
					Image_FilenameMS_file.write(str(Grid_RefMS) + "\n")
					Image_FilenameMS_file.write(str(MStechnicalquality_value) + "\n")
					Image_FilenameMS_file.write(str(MScloudCover_value) + "\n")
					Image_FilenameMS_file.write(str(MSsnowcover_value) + "\n")
					Image_FilenameMS_file.write(str(create_dateMS[:4]) + str(create_dateMS[4:6]) + str(create_dateMS[6:]) + "\n")
					Image_FilenameMS_file.write(str(Use_CenterViewingDateMS_value) + "\n")
					Image_FilenameMS_file.write(str(YearBeginMS) + str(MonthBeginMS) + str(DateBeginMS) + "\n")
					Image_FilenameMS_file.write(str(HourBeginMS) + str(MinBeginMS) + str(SecBeginMS) + "\n")
					Image_FilenameMS_file.write(str(YearEndMS) + str(MonthEndMS) + str(DateEndMS) + "\n")
					Image_FilenameMS_file.write(str(HourEndMS) + str(MinEndMS) + str(SecEndMS) + "\n")
					Image_FilenameMS_file.write(str(MScouplingmode_value) + "\n")
					Image_FilenameMS_file.write(str(MSorientationAngle_value) + "\n")
					Image_FilenameMS_file.write(str(MSIncidenceangle_value) + "\n")
					Image_FilenameMS_file.write(str(MSSunElevation_value) + "\n")
					Image_FilenameMS_file.write(str(MSSunAzimuth_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSnwLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSnwLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSneLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSneLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSswLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSswLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSseLat_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSseLong_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSLatSceneCenter_value) + "\n")
					Image_FilenameMS_file.write(str(Use_MSLongSceneCenter_value) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[0]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[1]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[2]) + "\n")
					Image_FilenameMS_file.write(str(DSR_beginMS_list[3]))
					Image_FilenameMS_file.close()

					# # Create catalog file
					Image_Date_timeMS_filename = Date_time_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Date-%s-%s-%s_Time-%s-%s-%s.cmp"%(str(create_dateMS[:4]),str(create_dateMS[4:6]),str(create_dateMS[6:]),Use_CenterViewingDateMS_value[:-4], Use_CenterViewingDateMS_value[2:-2],Use_CenterViewingDateMS_value[4:])
					Image_ConerMS_filename = Corner_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Upper_Left(%.4f , %.4f)_Upper_Right(%.4f , %.4f)_Lower_Left(%.4f , %.4f)_Lower_Right(%.4f , %.4f).cmp"%(Use_MSnwLat_value ,Use_MSnwLong_value ,Use_MSneLat_value , Use_MSneLong_value , Use_MSswLat_value , Use_MSswLong_value , Use_MSseLat_value , Use_MSseLong_value)
					Image_CenterMS_filename = Center_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Center_Lat_long(%.4f , %.4f).cmp"%(Use_MSLatSceneCenter_value , Use_MSLongSceneCenter_value)

					shutil.copy(Image_FilenameMS , Image_Date_timeMS_filename)
					shutil.copy(Image_FilenameMS , Image_ConerMS_filename)
					shutil.copy(Image_FilenameMS , Image_CenterMS_filename)


					crop_img_MS = imgMS[BrowseBeginLineMS_value : 499 + BrowseBeginLineMS_value, 0:ColumnsCountMS_value]
					cv2.imwrite(Image_FilenameMS[:-4] + ".JPG", crop_img_MS)

					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_Date_timeMS_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_ConerMS_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenameMS[:-4] + ".JPG" , Image_CenterMS_filename[:-4] + ".JPG")

			del Offset_value
		# if SpectralMode as PAN
		elif SpectralMode_value == "PAN":

			# Get FileName from catalog file
			Pre_FileNamePAN = segment.getElementsByTagName("fileName")[0]
			Pre_FileNamePAN_unicode = Pre_FileNamePAN.childNodes[0].data
			Pre_FileNamePAN_value = Pre_FileNamePAN_unicode.strip("\n")
			FileNamePAN_value = str(Pre_FileNamePAN_value)

			Pre_PANSegmentRank = segment.getElementsByTagName("segmentRank")[0]
			Pre_PANSegmentRank_unicode = Pre_PANSegmentRank.childNodes[0].data
			Pre_PANSegmentRank_value = Pre_PANSegmentRank_unicode.strip("\n")
			PANSegmentRank_value = int(Pre_PANSegmentRank_value)
			# print "Segment rank : %d"%PANSegmentRank_value

			# Get TransmissionMode from catalog file
			Pre_TransmissionModePAN = segment.getElementsByTagName("transmissionMode")[0]
			Pre_TransmissionModePAN_unicode = Pre_TransmissionModePAN.childNodes[0].data
			Pre_TransmissionModePAN_value = Pre_TransmissionModePAN_unicode.strip("\n")
			TransmissionModePAN_value = str(Pre_TransmissionModePAN_value)
			# print "Transmission Mode : %s"%TransmissionModePAN_value

			# Get Instrument type from catalog file
			Pre_InstrumentTypePAN = segment.getElementsByTagName("instrumentType")[0]
			Pre_InstrumentTypePAN_unicode = Pre_InstrumentTypePAN.childNodes[0].data
			Pre_InstrumentTypePAN_value = Pre_InstrumentTypePAN_unicode.strip("\n")
			InstrumentTypePAN_value = str(Pre_InstrumentTypePAN_value)
			# print "Instrument Type : %s"%InstrumentTypePAN_value

			# Get Instrument ID from catalog file
			Pre_InstrumentIDPAN = segment.getElementsByTagName("instrumentIdt")[0]
			Pre_InstrumentIDPAN_unicode = Pre_InstrumentIDPAN.childNodes[0].data
			Pre_InstrumentIDPAN_value = Pre_InstrumentIDPAN_unicode.strip("\n")
			InstrumentIDPAN_value = str(Pre_InstrumentIDPAN_value)
			# print "Instrument ID : %s"%InstrumentIDPAN_value

			# Get Segment quality from CUF file
			Pre_PANsegmenquality = segment.getElementsByTagName("segmentQuality")[0]
			Pre_PANsegmenquality_unicode = Pre_PANsegmenquality.childNodes[0].data
			Pre_PANsegmenquality_value = Pre_PANsegmenquality_unicode.strip("\n")
			PANsegmentquality_value = str(Pre_PANsegmenquality_value)
			# print "Segment quality : %s"%PANsegmentquality_value

			#  Get BeginViewingDate from catalog file {
			Pre_BeginViewingDatePAN_segment = segment.getElementsByTagName("beginViewingDate")[0]
			Pre_BeginViewingDatePAN_segment_unicode = Pre_BeginViewingDatePAN_segment.childNodes[0].data
			Pre_BeginViewingDatePAN_segment_value = Pre_BeginViewingDatePAN_segment_unicode.strip("\n")
			BeginViewingDatePAN_segment_value = str(Pre_BeginViewingDatePAN_segment_value)

			Pre_YearPAN_segment = BeginViewingDatePAN_segment_value [:4]
			YearPAN_segment = str(Pre_YearPAN_segment)

			Pre_MonthPAN_segment = BeginViewingDatePAN_segment_value [4:6]
			MonthPAN_segment = str(Pre_MonthPAN_segment)

			Pre_DatePAN_segment = BeginViewingDatePAN_segment_value [6:8]
			DatePAN_segment = str(Pre_DatePAN_segment)

			Pre_HourPAN_segment = BeginViewingDatePAN_segment_value [8:10]
			HourPAN_segment = str(Pre_HourPAN_segment)

			Pre_MinPAN_segment = BeginViewingDatePAN_segment_value [10:12]
			MinPAN_segment = str(Pre_MinPAN_segment)

			Pre_SecPAN_segment = BeginViewingDatePAN_segment_value [12:14]
			SecPAN_segment = str(Pre_SecPAN_segment)

			#  Get BeginViewingDate from CUF file and sprint BeginViewingDate to year-month-date {
			Pre_EndViewingDatePAN_segment = segment.getElementsByTagName("endViewingDate")[0]
			Pre_EndViewingDatePAN_segment_unicode = Pre_EndViewingDatePAN_segment.childNodes[0].data
			Pre_EndViewingDatePAN_segment_value = Pre_EndViewingDatePAN_segment_unicode.strip("\n")
			EndViewingDatePAN_segment_value = str(Pre_EndViewingDatePAN_segment_value)

			Pre_EndYearPAN_segment = EndViewingDatePAN_segment_value [:4]
			EndYearPAN_segment = str(Pre_EndYearPAN_segment)

			Pre_EndMonthPAN_segment = EndViewingDatePAN_segment_value [4:6]
			EndMonthPAN_segment = str(Pre_EndMonthPAN_segment)

			Pre_EndDatePAN_segment = EndViewingDatePAN_segment_value [6:8]
			EndDatePAN_segment = str(Pre_EndDatePAN_segment)

			Pre_EndHourPAN_segment = EndViewingDatePAN_segment_value [8:10]
			EndHourPAN_segment = str(Pre_EndHourPAN_segment)

			Pre_EndMinPAN_segment = EndViewingDatePAN_segment_value [10:12]
			EndMinPAN_segment = str(Pre_EndMinPAN_segment)

			Pre_EndSecPAN_segment = EndViewingDatePAN_segment_value [12:14]
			EndSecPAN_segment = str(Pre_EndSecPAN_segment)
			# }

			# print "End viewing date : %s/%s/%s %s:%s:%s"%(EndYearPAN_segment , EndMonthPAN_segment , EndDatePAN_segment , EndHourPAN_segment , EndMinPAN_segment , EndSecPAN_segment)

			Pre_PANCompression_ratio = segment.getElementsByTagName("compressionRatio")[0]
			Pre_PANCompression_ratio_unicode = Pre_PANCompression_ratio.childNodes[0].data
			Pre_PANCompression_ratio_value = Pre_PANCompression_ratio_unicode.strip("\n")
			PANCompression_ratio_value = float(Pre_PANCompression_ratio_value)
			# print "Compression ratio : %f"%PANCompression_ratio_value

			Pre_PANReferenceBand = segment.getElementsByTagName("referenceBand")[0]
			Pre_PANReferenceBand_unicode = Pre_PANReferenceBand.childNodes[0].data
			Pre_PANReferenceBand_value = Pre_PANReferenceBand_unicode.strip("\n")
			PANReferenceBand_value = str(Pre_PANReferenceBand_value)
			# print "Reference Band : %s"%PANReferenceBand_value

			Pre_PAN_Alongtrackviewingangle = segment.getElementsByTagName("alongTrackViewingAngle")[0]
			Pre_PAN_Alongtrackviewingangle_unicode = Pre_PAN_Alongtrackviewingangle.childNodes[0].data
			Pre_PAN_Alongtrackviewingangle_value = Pre_PAN_Alongtrackviewingangle_unicode.strip("\n")
			PAN_Alongtrackviewingangle_value = np.float64(Pre_PAN_Alongtrackviewingangle_value)
			# print "Along track viewing angle : %.10f"%PAN_Alongtrackviewingangle_value

			Pre_PAN_Acrosstrackviewingangle = segment.getElementsByTagName("acrossTrackViewingAngle")[0]
			Pre_PAN_Acrosstrackviewingangle_unicode = Pre_PAN_Acrosstrackviewingangle.childNodes[0].data
			Pre_PAN_Acrosstrackviewingangle_value = Pre_PAN_Acrosstrackviewingangle_unicode.strip("\n")
			PAN_Acrosstrackviewingangle_value = np.float64(Pre_PAN_Acrosstrackviewingangle_value)
			# print "Across track viewing angle : %.10f"%PAN_Acrosstrackviewingangle_value

			Pre_PAN_ABSGain = segment.getElementsByTagName("absGain")[0]
			Pre_PAN_ABSGain_unicode = Pre_PAN_ABSGain.childNodes[0].data
			Pre_PAN_ABSGain_value = Pre_PAN_ABSGain_unicode.strip("\n")
			PAN_ABSGain_value = str(Pre_PAN_ABSGain_value)
			# print "ABS Gain : %.10f"%PAN_ABSGain_value

			#  Get sceneCount from catalog file for create condition to split Normal scene from Last scene
			Pre_ScenecountPAN = segment.getElementsByTagName("scenesCount")[0]
			Pre_ScenecountPAN_unicode = Pre_ScenecountPAN.childNodes[0].data
			Pre_ScenecountPAN_value = Pre_ScenecountPAN_unicode.strip("\n")
			ScenecountPAN_value = int(Pre_ScenecountPAN_value)
			SceneCount_list.append(ScenecountPAN_value)

			#  Get GERAL directory name from components
			GERALDPAN_name = Mission_value + "_" + SatelliteIdt_value + "_LEVEL0_" + PassRank_value + "_" + PassId_value + "_" + RevolutionNumber_value + "_" + SpectralMode_value + "_" + TransmissionModePAN_value + "_" + InstrumentTypePAN_value + "_" + InstrumentIDPAN_value + "_" + FileNamePAN_value + "_" + YearPAN_segment + "-" + MonthPAN_segment + "-" + DatePAN_segment + "_" + HourPAN_segment + "-" + MinPAN_segment + "-" + SecPAN_segment

			PANSegmentImageRank_value = PANSegmentRank_value - 1

			imgname_PAN = os.path.abspath(browseFileName_value)
			imgPAN = cv2.imread(imgname_PAN)

			Hight_PAN , Width_PAN , Ch_PAN = imgPAN.shape
			print "Cut browse image from strip: %s to scene by scene."%imgname_PAN

			# Get ColumnsCount for use it in crop browse image
			Pre_ColumnsCountPAN = segment.getElementsByTagName("columnsCount")[0]
			Pre_ColumnsCountPAN_unicode = Pre_ColumnsCountPAN.childNodes[0].data
			Pre_ColumnsCountPAN_value = Pre_ColumnsCountPAN_unicode.strip("\n")
			ColumnsCountPAN_value = int(Pre_ColumnsCountPAN_value)

			DetailPAN_path = RevolutionNumber_value

			""" Set ScenePAN as root to get elements from tag in scene by for loop"""
			ScenePAN = segment.getElementsByTagName("scene")
			for scenePAN in ScenePAN :

				# Get sceneRank from catalog file for use to compare with sceneCount for split Normal and Last scene
				Pre_SceneRankPAN = scenePAN.getElementsByTagName("sceneRank")[0]
				Pre_SceneRankPAN_unicode = Pre_SceneRankPAN.childNodes[0].data
				Pre_ScenePANRank_value = Pre_SceneRankPAN_unicode.strip("\n")
				ScenePANRank_value = int(Pre_ScenePANRank_value)

				# Create DSR_begin list to get DSR_begin for use to create image
				if ScenePANRank_value == 1:
					# Get centerViewingDate from catalog file and use it to file name of Image detail file
					Pre_CenterViewingDatePAN = scenePAN.getElementsByTagName("centerViewingDate")[0]
					Pre_CenterViewingDatePAN_unicode = Pre_CenterViewingDatePAN.childNodes[0].data
					Pre_CenterViewingDatePAN_value = Pre_CenterViewingDatePAN_unicode.strip("\n")
					CenterViewingDatePAN_time = Pre_CenterViewingDatePAN_value[8:14]
					CenterViewingDatePAN_value = str(CenterViewingDatePAN_time)
					Use_CenterViewingDatePAN_value = str(CenterViewingDatePAN_time)[:2] + str(CenterViewingDatePAN_time)[2:4] + str(CenterViewingDatePAN_time)[4:]
					create_datePAN = Pre_CenterViewingDatePAN_value[:8]

					Pre_beginViewingDatePAN = scenePAN.getElementsByTagName("beginViewingDate")[0]
					Pre_beginViewingDatePAN_unicode = Pre_beginViewingDatePAN.childNodes[0].data
					Pre_beginViewingDatePAN_value = Pre_beginViewingDatePAN_unicode.strip("\n")
					BeginViewingDatePAN_value = str(Pre_beginViewingDatePAN_value)

					Pre_YearBeginPAN = BeginViewingDatePAN_value [:4]
					YearBeginPAN = str(Pre_YearBeginPAN)

					Pre_MonthBeginPAN = BeginViewingDatePAN_value [4:6]
					MonthBeginPAN = str(Pre_MonthBeginPAN)

					Pre_DateBeginPAN = BeginViewingDatePAN_value [6:8]
					DateBeginPAN = str(Pre_DateBeginPAN)

					Pre_HourBeginPAN = BeginViewingDatePAN_value [8:10]
					HourBeginPAN = str(Pre_HourBeginPAN)

					Pre_MinBeginPAN = BeginViewingDatePAN_value [10:12]
					MinBeginPAN = str(Pre_MinBeginPAN)

					Pre_SecBeginPAN = BeginViewingDatePAN_value [12:14]
					SecBeginPAN = str(Pre_SecBeginPAN)

					Pre_EndViewingDatePAN = scenePAN.getElementsByTagName("endViewingDate")[0]
					Pre_EndViewingDatePAN_unicode = Pre_EndViewingDatePAN.childNodes[0].data
					Pre_EndViewingDatePAN_value = Pre_EndViewingDatePAN_unicode.strip("\n")
					EndViewingDatePAN_value = str(Pre_EndViewingDatePAN_value)

					Pre_YearEndPAN = EndViewingDatePAN_value [:4]
					YearEndPAN = str(Pre_YearEndPAN)

					Pre_MonthEndPAN = EndViewingDatePAN_value [4:6]
					MonthEndPAN = str(Pre_MonthEndPAN)

					Pre_DateEndPAN = EndViewingDatePAN_value [6:8]
					DateEndPAN = str(Pre_DateEndPAN)

					Pre_HourEndPAN = EndViewingDatePAN_value [8:10]
					HourEndPAN = str(Pre_HourEndPAN)

					Pre_MinEndPAN = EndViewingDatePAN_value [10:12]
					MinEndPAN = str(Pre_MinEndPAN)

					Pre_SecEndPAN = EndViewingDatePAN_value [12:14]
					SecEndPAN = str(Pre_SecEndPAN)

					""" Get DSR_begin from Normal scene
					first  : Get beginRangeLine from catalog file
					second  : then get pre dsrbegin """

					# Get beginRangeLine from catalog file
					Pre_BeginRangelinePAN = scenePAN.getElementsByTagName("beginRangeLine")[0]
					Pre_BeginRangelinePAN_unicode = Pre_BeginRangelinePAN.childNodes[0].data
					Pre_BeginRangelinePAN_value = Pre_BeginRangelinePAN_unicode.strip("\n")
					BeginRangeLinePAN_value = 1
					DSR_beginPAN = BeginRangeLinePAN_value

					# Get endRangeLine from catalog file
					Pre_EndRangelinePAN = scenePAN.getElementsByTagName("endRangeLine")[0]
					Per_EndRangeline_unicode = Pre_EndRangelinePAN.childNodes[0].data
					Pre_EndRangelinePAN_value = Per_EndRangeline_unicode.strip("\n")
					EndRangeLinePAN_value = int(Pre_EndRangelinePAN_value)
					DSR_endPAN = EndRangeLinePAN_value

					# { Get KPath and JRow from catalog file and use it to Grid reference
					Pre_KPathPAN = scenePAN.getElementsByTagName("kPath")[0]
					Pre_KPathPAN_unicode = Pre_KPathPAN.childNodes[0].data
					Pre_KPathPAN_value = Pre_KPathPAN_unicode.strip("\n")
					KPathPAN_value = str(Pre_KPathPAN_value)

					Pre_JRowPAN = scenePAN.getElementsByTagName("jRow")[0]
					Pre_JRowPAN_unicode = Pre_JRowPAN.childNodes[0].data
					Pre_JRowPAN_value = Pre_JRowPAN_unicode.strip("\n")
					JRowPAN_value = str(Pre_JRowPAN_value)

					Grid_RefPAN = KPathPAN_value + "-" + JRowPAN_value
					# }

					Pre_PANtechnicalquality = scenePAN.getElementsByTagName("technoQuality")[0]
					Pre_PANtechnicalquality_unicode = Pre_PANtechnicalquality.childNodes[0].data
					Pre_PANtechnicalquality_value = Pre_PANtechnicalquality_unicode.strip("\n")
					PANtechnicalquality_value = str(Pre_PANtechnicalquality_value)

					Pre_PANcloudCover = scenePAN.getElementsByTagName("cloudCover")[0]
					Pre_PANcloudCover_unicode = Pre_PANcloudCover.childNodes[0].data
					Pre_PANcloudCover_value = Pre_PANcloudCover_unicode.strip("\n")
					PANcloudCover_value = str(Pre_PANcloudCover_value)

					Pre_PANsnowcover = scenePAN.getElementsByTagName("snowCover")[0]
					Pre_PANsnowcover_unicode = Pre_PANsnowcover.childNodes[0].data
					Pre_PANsnowcover_value = Pre_PANsnowcover_unicode.strip("\n")
					PANsnowcover_value = str(Pre_PANsnowcover_value)

					Pre_PANcouplingmode = scenePAN.getElementsByTagName("couplingMode")[0]
					Pre_PANcouplingmode_unicode = Pre_PANcouplingmode.childNodes[0].data
					Pre_PANcouplingmode_value = Pre_PANcouplingmode_unicode.strip("\n")
					PANcouplingmode_value = str(Pre_PANcouplingmode_value)

					Pre_PANorientationAngle = scenePAN.getElementsByTagName("orientationAngle")[0]
					Pre_PANorientationAngle_unicode = Pre_PANorientationAngle.childNodes[0].data
					Pre_PANorientationAngle_value = Pre_PANorientationAngle_unicode.strip("\n")
					PANorientationAngle_value = str(Pre_PANorientationAngle_value)

					Pre_PANIncidenceangle = scenePAN.getElementsByTagName("incidenceAngle")[0]
					Pre_PANIncidenceangle_unicoce = Pre_PANIncidenceangle.childNodes[0].data
					Pre_PANIncidenceangle_value = Pre_PANIncidenceangle_unicoce.strip("\n")
					PANIncidenceangle_value = str(Pre_PANIncidenceangle_value)

					Pre_PANLatSceneCenter = scenePAN.getElementsByTagName("latSceneCenter")[0]
					Pre_PANLatSceneCenter_unicode = Pre_PANLatSceneCenter.childNodes[0].data
					Pre_PANLatSceneCenter_value = Pre_PANLatSceneCenter_unicode.strip("\n")
					PANLatSceneCenter_value = str(Pre_PANLatSceneCenter_value)

					Pre_Dec_PANLatSceneCenter_text = PANLatSceneCenter_value[:1]
					Pre_Dec_PANLatSceneCenter_Degrees = PANLatSceneCenter_value[1:-4]
					Dec_PANLatSceneCenter_Degrees = np.float64(Pre_Dec_PANLatSceneCenter_Degrees)
					Pre_Dec_PANLatSceneCenter_minutes = PANLatSceneCenter_value[4:-2]
					Dec_PANLatSceneCenter_minutes = np.float64(Pre_Dec_PANLatSceneCenter_minutes)
					Pre_Dec_PANLatSceneCenter_sec = PANLatSceneCenter_value[6:]
					Dec_PANLatSceneCenter_sec = np.float64(Pre_Dec_PANLatSceneCenter_sec)

					if Pre_Dec_PANLatSceneCenter_text == "N" :
						Dec_PANLatSceneCenter_text = 1.0
					elif Pre_Dec_PANLatSceneCenter_text == "S" :
						Dec_PANLatSceneCenter_text = -1.0
					Use_PANLatSceneCenter_value = np.float64(Dec_PANLatSceneCenter_text * (Dec_PANLatSceneCenter_Degrees + (Dec_PANLatSceneCenter_minutes / 60.0) + (Dec_PANLatSceneCenter_sec / 3600.0)))

 					Pre_PANLongSceneCenter = scenePAN.getElementsByTagName("longSceneCenter")[0]
 					Pre_PANLongSceneCenter_unicode = Pre_PANLongSceneCenter.childNodes[0].data
 					Pre_PANLongSceneCenter_value = Pre_PANLongSceneCenter_unicode.strip("\n")
 					PANLongSceneCenter_value = str(Pre_PANLongSceneCenter_value)

 					Pre_Dec_PANLongSceneCenter_text = PANLongSceneCenter_value[:1]
 					Pre_Dec_PANLongSceneCenter_Degrees = PANLatSceneCenter_value[1:-4]
 					Dec_PANLongSceneCenter_Degrees = np.float64(Pre_Dec_PANLongSceneCenter_Degrees)
 					Pre_Dec_PANLongSceneCenter_minutes = PANLongSceneCenter_value[4:-2]
 					Dec_PANLongSceneCenter_minutes = np.float64(Pre_Dec_PANLongSceneCenter_minutes)
 					Pre_Dec_PANLongSceneCenter_sec = PANLongSceneCenter_value[6:]
 					Dec_PANLongSceneCenter_sec = np.float64(Pre_Dec_PANLongSceneCenter_sec)

 					if Pre_Dec_PANLongSceneCenter_text == "E":
 						Dec_PANLongSceneCenter_text = 1.0
 					elif Pre_Dec_PANLongSceneCenter_text == "W":
 						Dec_PANLongSceneCenter_text = -1.0
 					Use_PANLongSceneCenter_value = np.float64(Dec_PANLongSceneCenter_text * (Dec_PANLongSceneCenter_Degrees + (Dec_PANLongSceneCenter_minutes / 60.0) + (Dec_PANLongSceneCenter_sec / 3600.0)))

 					Pre_PANSunElevation = scenePAN.getElementsByTagName("sunElevation")[0]
 					Pre_PANSunElevation_unicode = Pre_PANSunElevation.childNodes[0].data
 					Pre_PANSunElevation_value = Pre_PANSunElevation_unicode.strip("\n")
 					PANSunElevation_value = str(Pre_PANSunElevation_value)

 					Pre_PANSunAzimuth = scenePAN.getElementsByTagName("sunAzimuth")[0]
 					Pre_PANSunAzimuth_unicode = Pre_PANSunAzimuth.childNodes[0].data
 					Pre_PANSunAzimuth_value = Pre_PANSunAzimuth_unicode.strip("\n")
 					PANSunAzimuth_value = str(Pre_PANSunAzimuth_value)

 					Pre_PANnwLat = scenePAN.getElementsByTagName("nwLat")[0]
 					Pre_PANnwLat_unicode = Pre_PANnwLat.childNodes[0].data
 					Pre_PANnwLat_value = Pre_PANnwLat_unicode.strip("\n")
 					PANnwLat_value = str(Pre_PANnwLat_value)

 					Pre_Dec_PANnwLat_value_text = PANnwLat_value[:1]
 					Pre_Dec_PANnwLat_Degrees = PANnwLat_value[1:-4]
 					Dec_PANnwLat_Degrees = np.float64(Pre_Dec_PANnwLat_Degrees)
 					Pre_Dec_PANnwLat_minutes = PANnwLat_value[4:-2]
 					Dec_PANnwLat_minutes = np.float64(Pre_Dec_PANnwLat_minutes)
 					Pre_Dec_PANnwLat_sec = PANnwLat_value[6:]
 					Dec_PANnwLat_sec = np.float64(Pre_Dec_PANnwLat_sec)

 					if Pre_Dec_PANnwLat_value_text == "N":
 						Dec_PANnwLat_value_text = 1.0

 					elif Pre_Dec_PANnwLat_value_text == "S":
 						Dec_PANnwLat_value_text = -1.0
 					Use_PANnwLat_value = np.float64(Dec_PANnwLat_value_text * (Dec_PANnwLat_Degrees + (Dec_PANnwLat_minutes / 60.0) + (Dec_PANnwLat_sec / 3600.0)))

 					Pre_PANnwLong = scenePAN.getElementsByTagName("nwLong")[0]
 					Pre_PANnwLong_unicode = Pre_PANnwLong.childNodes[0].data
 					Pre_PANnwLong_value = Pre_PANnwLong_unicode.strip("\n")
 					PANnwLong_value = str(Pre_PANnwLong_value)

 					Pre_Dec_PANnwLong_value_text = PANnwLong_value[:1]
 					Pre_Dec_PANnwLong_Degrees = PANnwLong_value[1:-4]
 					Dec_PANnwLong_Degrees = np.float64(Pre_Dec_PANnwLong_Degrees)
 					Pre_Dec_PANnwLong_minutes = PANnwLong_value[4:-2]
 					Dec_PANnwLong_minutes = np.float64(Pre_Dec_PANnwLong_minutes)
 					Pre_Dec_PANnwLong_sec = PANnwLong_value[6:]
 					Dec_PANnwLong_sec = np.float64(Pre_Dec_PANnwLong_sec)

 					if Pre_Dec_PANnwLong_value_text == "W":
 						Dec_PANnwLong_value_text = 1.0

 					elif Pre_Dec_PANnwLong_value_text == "E":
 						Dec_PANnwLong_value_text = -1.0
 					Use_PANnwLong_value = np.float64(Dec_PANnwLong_value_text * (Dec_PANnwLong_Degrees + (Dec_PANnwLong_minutes / 60.0) + (Dec_PANnwLong_sec / 3600.0)))

 					Pre_PANneLat = scenePAN.getElementsByTagName("neLat")[0]
 					Pre_PANneLat_unicode = Pre_PANneLat.childNodes[0].data
 					Pre_PANneLat_value = Pre_PANneLat_unicode.strip("\n")
 					PANneLat_value = str(Pre_PANneLat_value)

 					Pre_Dec_PANneLat_value_text = PANneLat_value[:1]
 					Pre_Dec_PANneLat_Degrees = PANneLat_value[1:-4]
 					Dec_PANneLat_Degrees = np.float64(Pre_Dec_PANneLat_Degrees)
 					Pre_Dec_PANneLat_minutes = PANneLat_value[4:-2]
 					Dec_PANneLat_minutes = np.float64(Pre_Dec_PANneLat_minutes)
 					Pre_Dec_PANneLat_sec = PANneLat_value[6:]
 					Dec_PANneLat_sec = np.float64(Pre_Dec_PANneLat_sec)

 					if Pre_Dec_PANneLat_value_text == "N":
 						Dec_PANneLat_value_text = 1.0

 					elif Pre_Dec_PANneLat_value_text == "S":
 						Dec_PANneLat_value_text = -1.0
 					Use_PANneLat_value = np.float64(Dec_PANneLat_value_text * (Dec_PANneLat_Degrees + (Dec_PANneLat_minutes / 60.0) + (Dec_PANneLat_sec / 3600.0)))

 					Pre_PANneLong = scenePAN.getElementsByTagName("neLong")[0]
 					Pre_PANneLong_unicode = Pre_PANneLong.childNodes[0].data
 					Pre_PANneLong_value = Pre_PANneLong_unicode.strip("\n")
 					PANneLong_value = str(Pre_PANneLong_value)

 					Pre_Dec_PANneLong_value_text = PANneLong_value[:1]
 					Pre_Dec_PANneLong_Degrees = PANneLong_value[1:-4]
 					Dec_PANneLong_Degrees = np.float64(Pre_Dec_PANneLong_Degrees)
 					Pre_Dec_PANneLong_minutes = PANneLong_value[4:-2]
 					Dec_PANneLong_minutes = np.float64(Pre_Dec_PANneLong_minutes)
 					Pre_Dec_PANneLong_sec = PANneLong_value[6:]
 					Dec_PANneLong_sec = np.float64(Pre_Dec_PANneLong_sec)

 					if Pre_Dec_PANneLong_value_text == "W":
 						Dec_PANneLong_value_text = 1.0

 					elif Pre_Dec_PANneLong_value_text == "E":
 						Dec_PANneLong_value_text = -1.0
 					Use_PANneLong_value = np.float64(Dec_PANneLong_value_text * (Dec_PANneLong_Degrees + (Dec_PANneLong_minutes / 60.0) + (Dec_PANneLong_sec / 3600.0)))

 					Pre_PANswLat = scenePAN.getElementsByTagName("swLat")[0]
 					Pre_PANswLat_unicode = Pre_PANswLat.childNodes[0].data
 					Pre_PANswLat_value = Pre_PANswLat_unicode.strip("\n")
 					PANswLat_value = str(Pre_PANswLat_value)

 					Pre_Dec_PANswLat_value_text = PANswLat_value[:1]
 					Pre_Dec_PANswLat_Degrees = PANswLat_value[1:-4]
 					Dec_PANswLat_Degrees = np.float64(Pre_Dec_PANswLat_Degrees)
 					Pre_Dec_PANswLat_minutes = PANswLat_value[4:-2]
 					Dec_PANswLat_minutes = np.float64(Pre_Dec_PANswLat_minutes)
 					Pre_Dec_PANswLat_sec = PANswLat_value[6:]
 					Dec_PANswLat_sec = np.float64(Pre_Dec_PANswLat_sec)

 					if Pre_Dec_PANswLat_value_text == "N":
 						Dec_PANswLat_value_text = 1.0

 					elif Pre_Dec_PANswLat_value_text == "S":
 						Dec_PANswLat_value_text = -1.0
 					Use_PANswLat_value = np.float64(Dec_PANswLat_value_text * (Dec_PANswLat_Degrees + (Dec_PANswLat_minutes / 60.0) + (Dec_PANswLat_sec / 3600.0)))

 					Pre_PANswLong = scenePAN.getElementsByTagName("swLong")[0]
 					Pre_PANswLong_unicode = Pre_PANswLong.childNodes[0].data
 					Pre_PANswLong_value = Pre_PANswLong_unicode.strip("\n")
 					PANswLong_value = str(Pre_PANswLong_value)

 					Pre_Dec_PANswLong_value_text = PANswLong_value[:1]
 					Pre_Dec_PANswLong_Degrees = PANswLong_value[1:-4]
 					Dec_PANswLong_Degrees = np.float64(Pre_Dec_PANswLong_Degrees)
 					Pre_Dec_PANswLong_minutes = PANswLong_value[4:-2]
 					Dec_PANswLong_minutes = np.float64(Pre_Dec_PANswLong_minutes)
 					Pre_Dec_PANswLong_sec = PANswLong_value[6:]
 					Dec_PANswLong_sec = np.float64(Pre_Dec_PANswLong_sec)

 					if Pre_Dec_PANswLong_value_text == "W":
 						Dec_PANswLong_value_text = 1.0

 					elif Pre_Dec_PANswLong_value_text == "E":
 						Dec_PANswLong_value_text = -1.0
 					Use_PANswLong_value = np.float64(Dec_PANswLong_value_text * (Dec_PANswLong_Degrees + (Dec_PANswLong_minutes / 60.0) + (Dec_PANswLong_sec / 3600.0)))

 					Pre_PANseLat = scenePAN.getElementsByTagName("seLat")[0]
 					Pre_PANseLat_unicode = Pre_PANseLat.childNodes[0].data
 					Pre_PANseLat_value = Pre_PANseLat_unicode.strip("\n")
 					PANseLat_value = str(Pre_PANseLat_value)

 					Pre_Dec_PANseLat_value_text = PANseLat_value[:1]
 					Pre_Dec_PANseLat_Degrees = PANseLat_value[1:-4]
 					Dec_PANseLat_Degrees = np.float64(Pre_Dec_PANseLat_Degrees)
 					Pre_Dec_PANseLat_minutes = PANseLat_value[4:-2]
 					Dec_PANseLat_minutes = np.float64(Pre_Dec_PANseLat_minutes)
 					Pre_Dec_PANseLat_sec = PANseLat_value[6:]
 					Dec_PANseLat_sec = np.float64(Pre_Dec_PANseLat_sec)

 					if Pre_Dec_PANseLat_value_text == "N":
 						Dec_PANseLat_value_text = 1.0

 					elif Pre_Dec_PANseLat_value_text == "S":
 						Dec_PANseLat_value_text = -1.0
 					Use_PANseLat_value = np.float64(Dec_PANseLat_value_text * (Dec_PANseLat_Degrees + (Dec_PANseLat_minutes / 60.0) + (Dec_PANseLat_sec / 3600.0)))

 					Pre_PANseLong = scenePAN.getElementsByTagName("seLong")[0]
 					Pre_PANseLong_unicode = Pre_PANseLong.childNodes[0].data
 					Pre_PANseLong_value = Pre_PANseLong_unicode.strip("\n")
 					PANseLong_value = str(Pre_PANseLong_value)

 					Pre_Dec_PANseLong_value_text = PANseLong_value[:1]
 					Pre_Dec_PANseLong_Degrees = PANseLong_value[1:-4]
 					Dec_PANseLong_Degrees = np.float64(Pre_Dec_PANseLong_Degrees)
 					Pre_Dec_PANseLong_minutes = PANseLong_value[4:-2]
 					Dec_PANseLong_minutes = np.float64(Pre_Dec_PANseLong_minutes)
 					Pre_Dec_PANseLong_sec = PANseLong_value[6:]
 					Dec_PANseLong_sec = np.float64(Pre_Dec_PANseLong_sec)

 					if Pre_Dec_PANseLong_value_text == "W":
 						Dec_PANseLong_value_text = 1.0

 					elif Pre_Dec_PANseLong_value_text == "E":
 						Dec_PANseLong_value_text = -1.0
 					Use_PANseLong_value = np.float64(Dec_PANseLong_value_text * (Dec_PANseLong_Degrees + (Dec_PANseLong_minutes / 60.0) + (Dec_PANseLong_sec / 3600.0)))

					# {Get BrowseBeginLine from catalog file}
					BrowseBeginLinePAN_value = 1

					# {Get BrowseEndLine from catalog file}
					BrowseEndLinePAN_value = 499

					# Create catalog file
					Image_FilenamePAN = FIlename_path + "/" + RevolutionNumber_value + "_" + SpectralMode_value + "_Filename%s_SceneRank_%s.cmp"%(FileNamePAN_value , str(ScenePANRank_value))
					Image_FilenamePAN_file = open(Image_FilenamePAN, "w")
					Image_FilenamePAN_file.write(str(BeginReception_year) + str(BeginReception_month) + str(BeginReception_date) + "\n")
					Image_FilenamePAN_file.write(str(BeginReception_hour) + str(BeginReception_min) + str(BeginReception_sec) + "\n")
					Image_FilenamePAN_file.write(str(EndReception_year) + str(EndReception_month) + str(EndReception_date) + "\n")
					Image_FilenamePAN_file.write(str(EndReception_hour) + str(EndReception_min) + str(EndReception_sec) + "\n")
					Image_FilenamePAN_file.write(str(OrbitCycle_value) + "\n")
					Image_FilenamePAN_file.write(str(RevolutionNumber_value) + "\n")
					Image_FilenamePAN_file.write(str(Mission_value) + "\n")
					Image_FilenamePAN_file.write(str(SatelliteIdt_value) + "\n")
					Image_FilenamePAN_file.write(str(PassRank_value) + "\n")
					Image_FilenamePAN_file.write(str(PassId_value) + "\n")
					Image_FilenamePAN_file.write(str(SegmentCount_value) + "\n")
					Image_FilenamePAN_file.write(str("Segment info") + "\n")
					Image_FilenamePAN_file.write(str(FileNamePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(GERALDPAN_name) + "\n")
					Image_FilenamePAN_file.write(str(PANSegmentRank_value) + "\n")
					Image_FilenamePAN_file.write(str(InstrumentTypePAN_value) + str(InstrumentIDPAN_value) + "\n")
					Image_FilenamePAN_file.write(str(TransmissionModePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(PANsegmentquality_value) + "\n")
					Image_FilenamePAN_file.write(str(YearPAN_segment) + str(MonthPAN_segment) + str(DatePAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(HourPAN_segment) + str(MinPAN_segment) + str(SecPAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(EndYearPAN_segment) + str(EndMonthPAN_segment) + str(EndDatePAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(EndHourPAN_segment) + str(EndMinPAN_segment) + str(EndSecPAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(PANCompression_ratio_value) + "\n")
					Image_FilenamePAN_file.write(str(SpectralMode_value) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(PANReferenceBand_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_Alongtrackviewingangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_Acrosstrackviewingangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_ABSGain_value) + "\n")
					Image_FilenamePAN_file.write(str("Scene info") + "\n")
					Image_FilenamePAN_file.write(str(ScenecountPAN_value) + "\n")
					Image_FilenamePAN_file.write(str(ScenePANRank_value) + "\n")
					Image_FilenamePAN_file.write(str(Grid_RefPAN) + "\n")
					Image_FilenamePAN_file.write(str(PANtechnicalquality_value) + "\n")
					Image_FilenamePAN_file.write(str(PANcloudCover_value) + "\n")
					Image_FilenamePAN_file.write(str(PANsnowcover_value) + "\n")
					Image_FilenamePAN_file.write(str(create_datePAN[:4]) + str(create_datePAN[4:6]) + str(create_datePAN[6:]) + "\n")
					Image_FilenamePAN_file.write(str(Use_CenterViewingDatePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(YearBeginPAN) + str(MonthBeginPAN) + str(DateBeginPAN) + "\n")
					Image_FilenamePAN_file.write(str(HourBeginPAN) + str(MinBeginPAN) + str(SecBeginPAN) + "\n")
					Image_FilenamePAN_file.write(str(YearEndPAN) + str(MonthEndPAN) + str(DateEndPAN) + "\n")
					Image_FilenamePAN_file.write(str(HourEndPAN) + str(MinEndPAN) + str(SecEndPAN) + "\n")
					Image_FilenamePAN_file.write(str(PANcouplingmode_value) + "\n")
					Image_FilenamePAN_file.write(str(PANorientationAngle_value) + "\n")
					Image_FilenamePAN_file.write(str(PANIncidenceangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PANSunElevation_value) + "\n")
					Image_FilenamePAN_file.write(str(PANSunAzimuth_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANnwLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANnwLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANneLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANneLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANswLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANswLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANseLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANseLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANLatSceneCenter_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANLongSceneCenter_value) + "\n")
					Image_FilenamePAN_file.write(str(DSR_beginPAN) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0))
					Image_FilenamePAN_file.close()

					# # Create catalog file
					Image_Date_timePAN_filename = Date_time_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Date-%s-%s-%s_Time-%s-%s-%s.cmp"%(str(create_datePAN[:4]),str(create_datePAN[4:6]),str(create_datePAN[6:]),Use_CenterViewingDatePAN_value[:-4], Use_CenterViewingDatePAN_value[2:-2],Use_CenterViewingDatePAN_value[4:])
					Image_ConerPAN_filename = Corner_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Upper_Left(%.4f , %.4f)_Upper_Right(%.4f , %.4f)_Lower_Left(%.4f , %.4f)_Lower_Right(%.4f , %.4f).cmp"%(Use_PANnwLat_value ,Use_PANnwLong_value ,Use_PANneLat_value , Use_PANneLong_value , Use_PANswLat_value , Use_PANswLong_value , Use_PANseLat_value , Use_PANseLong_value)
					Image_CenterPAN_filename = Center_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Center_Lat_long(%.4f , %.4f).cmp"%(Use_PANLatSceneCenter_value , Use_PANLongSceneCenter_value)

					shutil.copy(Image_FilenamePAN , Image_Date_timePAN_filename)
					shutil.copy(Image_FilenamePAN , Image_ConerPAN_filename)
					shutil.copy(Image_FilenamePAN , Image_CenterPAN_filename)


					crop_img_PAN = imgPAN[BrowseBeginLinePAN_value : 499 + BrowseBeginLinePAN_value, 0:ColumnsCountPAN_value]
					cv2.imwrite(Image_FilenamePAN[:-4] + ".JPG", crop_img_PAN)

					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_Date_timePAN_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_ConerPAN_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_CenterPAN_filename[:-4] + ".JPG")

				# Normal scene condition
				elif ScenePANRank_value != ScenecountPAN_value :

					# Get centerViewingDate from catalog file and use it to file name of Image detail file
					Pre_CenterViewingDatePAN = scenePAN.getElementsByTagName("centerViewingDate")[0]
					Pre_CenterViewingDatePAN_unicode = Pre_CenterViewingDatePAN.childNodes[0].data
					Pre_CenterViewingDatePAN_value = Pre_CenterViewingDatePAN_unicode.strip("\n")
					CenterViewingDatePAN_time = Pre_CenterViewingDatePAN_value[8:14]
					CenterViewingDatePAN_value = str(CenterViewingDatePAN_time)
					Use_CenterViewingDatePAN_value = str(CenterViewingDatePAN_time)[:2] + str(CenterViewingDatePAN_time)[2:4] + str(CenterViewingDatePAN_time)[4:]
					create_datePAN = Pre_CenterViewingDatePAN_value[:8]

					Pre_beginViewingDatePAN = scenePAN.getElementsByTagName("beginViewingDate")[0]
					Pre_beginViewingDatePAN_unicode = Pre_beginViewingDatePAN.childNodes[0].data
					Pre_beginViewingDatePAN_value = Pre_beginViewingDatePAN_unicode.strip("\n")
					BeginViewingDatePAN_value = str(Pre_beginViewingDatePAN_value)

					Pre_YearBeginPAN = BeginViewingDatePAN_value [:4]
					YearBeginPAN = str(Pre_YearBeginPAN)

					Pre_MonthBeginPAN = BeginViewingDatePAN_value [4:6]
					MonthBeginPAN = str(Pre_MonthBeginPAN)

					Pre_DateBeginPAN = BeginViewingDatePAN_value [6:8]
					DateBeginPAN = str(Pre_DateBeginPAN)

					Pre_HourBeginPAN = BeginViewingDatePAN_value [8:10]
					HourBeginPAN = str(Pre_HourBeginPAN)

					Pre_MinBeginPAN = BeginViewingDatePAN_value [10:12]
					MinBeginPAN = str(Pre_MinBeginPAN)

					Pre_SecBeginPAN = BeginViewingDatePAN_value [12:14]
					SecBeginPAN = str(Pre_SecBeginPAN)

					Pre_EndViewingDatePAN = scenePAN.getElementsByTagName("endViewingDate")[0]
					Pre_EndViewingDatePAN_unicode = Pre_EndViewingDatePAN.childNodes[0].data
					Pre_EndViewingDatePAN_value = Pre_EndViewingDatePAN_unicode.strip("\n")
					EndViewingDatePAN_value = str(Pre_EndViewingDatePAN_value)

					Pre_YearEndPAN = EndViewingDatePAN_value [:4]
					YearEndPAN = str(Pre_YearEndPAN)

					Pre_MonthEndPAN = EndViewingDatePAN_value [4:6]
					MonthEndPAN = str(Pre_MonthEndPAN)

					Pre_DateEndPAN = EndViewingDatePAN_value [6:8]
					DateEndPAN = str(Pre_DateEndPAN)

					Pre_HourEndPAN = EndViewingDatePAN_value [8:10]
					HourEndPAN = str(Pre_HourEndPAN)

					Pre_MinEndPAN = EndViewingDatePAN_value [10:12]
					MinEndPAN = str(Pre_MinEndPAN)

					Pre_SecEndPAN = EndViewingDatePAN_value [12:14]
					SecEndPAN = str(Pre_SecEndPAN)

					""" Get DSR_begin from Normal scene
					first  : Get beginRangeLine from catalog file
					second  : then get pre dsrbegin """

					# Get beginRangeLine from catalog file
					Pre_BeginRangelinePAN = scenePAN.getElementsByTagName("beginRangeLine")[0]
					Pre_BeginRangelinePAN_unicode = Pre_BeginRangelinePAN.childNodes[0].data
					Pre_BeginRangelinePAN_value = Pre_BeginRangelinePAN_unicode.strip("\n")
					BeginRangeLinePAN_value = int(Pre_BeginRangelinePAN_value)
					DSR_beginPAN = BeginRangeLinePAN_value

					# Get endRangeLine from catalog file
					Pre_EndRangelinePAN = scenePAN.getElementsByTagName("endRangeLine")[0]
					Per_EndRangeline_unicode = Pre_EndRangelinePAN.childNodes[0].data
					Pre_EndRangelinePAN_value = Per_EndRangeline_unicode.strip("\n")
					EndRangeLinePAN_value = int(Pre_EndRangelinePAN_value)
					DSR_endPAN = EndRangeLinePAN_value

					# { Get KPath and JRow from catalog file and use it to Grid reference
					Pre_KPathPAN = scenePAN.getElementsByTagName("kPath")[0]
					Pre_KPathPAN_unicode = Pre_KPathPAN.childNodes[0].data
					Pre_KPathPAN_value = Pre_KPathPAN_unicode.strip("\n")
					KPathPAN_value = str(Pre_KPathPAN_value)

					Pre_JRowPAN = scenePAN.getElementsByTagName("jRow")[0]
					Pre_JRowPAN_unicode = Pre_JRowPAN.childNodes[0].data
					Pre_JRowPAN_value = Pre_JRowPAN_unicode.strip("\n")
					JRowPAN_value = str(Pre_JRowPAN_value)

					Grid_RefPAN = KPathPAN_value + "-" + JRowPAN_value
					# }

					Pre_PANtechnicalquality = scenePAN.getElementsByTagName("technoQuality")[0]
					Pre_PANtechnicalquality_unicode = Pre_PANtechnicalquality.childNodes[0].data
					Pre_PANtechnicalquality_value = Pre_PANtechnicalquality_unicode.strip("\n")
					PANtechnicalquality_value = str(Pre_PANtechnicalquality_value)

					Pre_PANcloudCover = scenePAN.getElementsByTagName("cloudCover")[0]
					Pre_PANcloudCover_unicode = Pre_PANcloudCover.childNodes[0].data
					Pre_PANcloudCover_value = Pre_PANcloudCover_unicode.strip("\n")
					PANcloudCover_value = str(Pre_PANcloudCover_value)

					Pre_PANsnowcover = scenePAN.getElementsByTagName("snowCover")[0]
					Pre_PANsnowcover_unicode = Pre_PANsnowcover.childNodes[0].data
					Pre_PANsnowcover_value = Pre_PANsnowcover_unicode.strip("\n")
					PANsnowcover_value = str(Pre_PANsnowcover_value)

					Pre_PANcouplingmode = scenePAN.getElementsByTagName("couplingMode")[0]
					Pre_PANcouplingmode_unicode = Pre_PANcouplingmode.childNodes[0].data
					Pre_PANcouplingmode_value = Pre_PANcouplingmode_unicode.strip("\n")
					PANcouplingmode_value = str(Pre_PANcouplingmode_value)

					Pre_PANorientationAngle = scenePAN.getElementsByTagName("orientationAngle")[0]
					Pre_PANorientationAngle_unicode = Pre_PANorientationAngle.childNodes[0].data
					Pre_PANorientationAngle_value = Pre_PANorientationAngle_unicode.strip("\n")
					PANorientationAngle_value = np.float64(Pre_PANorientationAngle_value)

					Pre_PANIncidenceangle = scenePAN.getElementsByTagName("incidenceAngle")[0]
					Pre_PANIncidenceangle_unicoce = Pre_PANIncidenceangle.childNodes[0].data
					Pre_PANIncidenceangle_value = Pre_PANIncidenceangle_unicoce.strip("\n")
					PANIncidenceangle_value = np.float64(Pre_PANIncidenceangle_value)

					Pre_PANLatSceneCenter = scenePAN.getElementsByTagName("latSceneCenter")[0]
					Pre_PANLatSceneCenter_unicode = Pre_PANLatSceneCenter.childNodes[0].data
					Pre_PANLatSceneCenter_value = Pre_PANLatSceneCenter_unicode.strip("\n")
					PANLatSceneCenter_value = str(Pre_PANLatSceneCenter_value)

					Pre_Dec_PANLatSceneCenter_text = PANLatSceneCenter_value[:1]
					Pre_Dec_PANLatSceneCenter_Degrees = PANLatSceneCenter_value[1:-4]
					Dec_PANLatSceneCenter_Degrees = np.float64(Pre_Dec_PANLatSceneCenter_Degrees)
					Pre_Dec_PANLatSceneCenter_minutes = PANLatSceneCenter_value[4:-2]
					Dec_PANLatSceneCenter_minutes = np.float64(Pre_Dec_PANLatSceneCenter_minutes)
					Pre_Dec_PANLatSceneCenter_sec = PANLatSceneCenter_value[6:]
					Dec_PANLatSceneCenter_sec = np.float64(Pre_Dec_PANLatSceneCenter_sec)

					if Pre_Dec_PANLatSceneCenter_text == "N" :
						Dec_PANLatSceneCenter_text = 1.0
					elif Pre_Dec_PANLatSceneCenter_text == "S" :
						Dec_PANLatSceneCenter_text = -1.0
					Use_PANLatSceneCenter_value = np.float64(Dec_PANLatSceneCenter_text * (Dec_PANLatSceneCenter_Degrees + (Dec_PANLatSceneCenter_minutes / 60.0) + (Dec_PANLatSceneCenter_sec / 3600.0)))

 					Pre_PANLongSceneCenter = scenePAN.getElementsByTagName("longSceneCenter")[0]
 					Pre_PANLongSceneCenter_unicode = Pre_PANLongSceneCenter.childNodes[0].data
 					Pre_PANLongSceneCenter_value = Pre_PANLongSceneCenter_unicode.strip("\n")
 					PANLongSceneCenter_value = str(Pre_PANLongSceneCenter_value)

 					Pre_Dec_PANLongSceneCenter_text = PANLongSceneCenter_value[:1]
 					Pre_Dec_PANLongSceneCenter_Degrees = PANLatSceneCenter_value[1:-4]
 					Dec_PANLongSceneCenter_Degrees = np.float64(Pre_Dec_PANLongSceneCenter_Degrees)
 					Pre_Dec_PANLongSceneCenter_minutes = PANLongSceneCenter_value[4:-2]
 					Dec_PANLongSceneCenter_minutes = np.float64(Pre_Dec_PANLongSceneCenter_minutes)
 					Pre_Dec_PANLongSceneCenter_sec = PANLongSceneCenter_value[6:]
 					Dec_PANLongSceneCenter_sec = np.float64(Pre_Dec_PANLongSceneCenter_sec)

 					if Pre_Dec_PANLongSceneCenter_text == "E":
 						Dec_PANLongSceneCenter_text = 1.0
 					elif Pre_Dec_PANLongSceneCenter_text == "W":
 						Dec_PANLongSceneCenter_text = -1.0
 					Use_PANLongSceneCenter_value = np.float64(Dec_PANLongSceneCenter_text * (Dec_PANLongSceneCenter_Degrees + (Dec_PANLongSceneCenter_minutes / 60.0) + (Dec_PANLongSceneCenter_sec / 3600.0)))

 					Pre_PANSunElevation = scenePAN.getElementsByTagName("sunElevation")[0]
 					Pre_PANSunElevation_unicode = Pre_PANSunElevation.childNodes[0].data
 					Pre_PANSunElevation_value = Pre_PANSunElevation_unicode.strip("\n")
 					PANSunElevation_value = str(Pre_PANSunElevation_value)

 					Pre_PANSunAzimuth = scenePAN.getElementsByTagName("sunAzimuth")[0]
 					Pre_PANSunAzimuth_unicode = Pre_PANSunAzimuth.childNodes[0].data
 					Pre_PANSunAzimuth_value = Pre_PANSunAzimuth_unicode.strip("\n")
 					PANSunAzimuth_value = str(Pre_PANSunAzimuth_value)

 					Pre_PANnwLat = scenePAN.getElementsByTagName("nwLat")[0]
 					Pre_PANnwLat_unicode = Pre_PANnwLat.childNodes[0].data
 					Pre_PANnwLat_value = Pre_PANnwLat_unicode.strip("\n")
 					PANnwLat_value = str(Pre_PANnwLat_value)

 					Pre_Dec_PANnwLat_value_text = PANnwLat_value[:1]
 					Pre_Dec_PANnwLat_Degrees = PANnwLat_value[1:-4]
 					Dec_PANnwLat_Degrees = np.float64(Pre_Dec_PANnwLat_Degrees)
 					Pre_Dec_PANnwLat_minutes = PANnwLat_value[4:-2]
 					Dec_PANnwLat_minutes = np.float64(Pre_Dec_PANnwLat_minutes)
 					Pre_Dec_PANnwLat_sec = PANnwLat_value[6:]
 					Dec_PANnwLat_sec = np.float64(Pre_Dec_PANnwLat_sec)

 					if Pre_Dec_PANnwLat_value_text == "N":
 						Dec_PANnwLat_value_text = 1.0

 					elif Pre_Dec_PANnwLat_value_text == "S":
 						Dec_PANnwLat_value_text = -1.0
 					Use_PANnwLat_value = np.float64(Dec_PANnwLat_value_text * (Dec_PANnwLat_Degrees + (Dec_PANnwLat_minutes / 60.0) + (Dec_PANnwLat_sec / 3600.0)))

 					Pre_PANnwLong = scenePAN.getElementsByTagName("nwLong")[0]
 					Pre_PANnwLong_unicode = Pre_PANnwLong.childNodes[0].data
 					Pre_PANnwLong_value = Pre_PANnwLong_unicode.strip("\n")
 					PANnwLong_value = str(Pre_PANnwLong_value)

 					Pre_Dec_PANnwLong_value_text = PANnwLong_value[:1]
 					Pre_Dec_PANnwLong_Degrees = PANnwLong_value[1:-4]
 					Dec_PANnwLong_Degrees = np.float64(Pre_Dec_PANnwLong_Degrees)
 					Pre_Dec_PANnwLong_minutes = PANnwLong_value[4:-2]
 					Dec_PANnwLong_minutes = np.float64(Pre_Dec_PANnwLong_minutes)
 					Pre_Dec_PANnwLong_sec = PANnwLong_value[6:]
 					Dec_PANnwLong_sec = np.float64(Pre_Dec_PANnwLong_sec)

 					if Pre_Dec_PANnwLong_value_text == "W":
 						Dec_PANnwLong_value_text = 1.0

 					elif Pre_Dec_PANnwLong_value_text == "E":
 						Dec_PANnwLong_value_text = -1.0
 					Use_PANnwLong_value = np.float64(Dec_PANnwLong_value_text * (Dec_PANnwLong_Degrees + (Dec_PANnwLong_minutes / 60.0) + (Dec_PANnwLong_sec / 3600.0)))

 					Pre_PANneLat = scenePAN.getElementsByTagName("neLat")[0]
 					Pre_PANneLat_unicode = Pre_PANneLat.childNodes[0].data
 					Pre_PANneLat_value = Pre_PANneLat_unicode.strip("\n")
 					PANneLat_value = str(Pre_PANneLat_value)

 					Pre_Dec_PANneLat_value_text = PANneLat_value[:1]
 					Pre_Dec_PANneLat_Degrees = PANneLat_value[1:-4]
 					Dec_PANneLat_Degrees = np.float64(Pre_Dec_PANneLat_Degrees)
 					Pre_Dec_PANneLat_minutes = PANneLat_value[4:-2]
 					Dec_PANneLat_minutes = np.float64(Pre_Dec_PANneLat_minutes)
 					Pre_Dec_PANneLat_sec = PANneLat_value[6:]
 					Dec_PANneLat_sec = np.float64(Pre_Dec_PANneLat_sec)

 					if Pre_Dec_PANneLat_value_text == "N":
 						Dec_PANneLat_value_text = 1.0

 					elif Pre_Dec_PANneLat_value_text == "S":
 						Dec_PANneLat_value_text = -1.0
 					Use_PANneLat_value = np.float64(Dec_PANneLat_value_text * (Dec_PANneLat_Degrees + (Dec_PANneLat_minutes / 60.0) + (Dec_PANneLat_sec / 3600.0)))

 					Pre_PANneLong = scenePAN.getElementsByTagName("neLong")[0]
 					Pre_PANneLong_unicode = Pre_PANneLong.childNodes[0].data
 					Pre_PANneLong_value = Pre_PANneLong_unicode.strip("\n")
 					PANneLong_value = str(Pre_PANneLong_value)

 					Pre_Dec_PANneLong_value_text = PANneLong_value[:1]
 					Pre_Dec_PANneLong_Degrees = PANneLong_value[1:-4]
 					Dec_PANneLong_Degrees = np.float64(Pre_Dec_PANneLong_Degrees)
 					Pre_Dec_PANneLong_minutes = PANneLong_value[4:-2]
 					Dec_PANneLong_minutes = np.float64(Pre_Dec_PANneLong_minutes)
 					Pre_Dec_PANneLong_sec = PANneLong_value[6:]
 					Dec_PANneLong_sec = np.float64(Pre_Dec_PANneLong_sec)

 					if Pre_Dec_PANneLong_value_text == "W":
 						Dec_PANneLong_value_text = 1.0

 					elif Pre_Dec_PANneLong_value_text == "E":
 						Dec_PANneLong_value_text = -1.0
 					Use_PANneLong_value = np.float64(Dec_PANneLong_value_text * (Dec_PANneLong_Degrees + (Dec_PANneLong_minutes / 60.0) + (Dec_PANneLong_sec / 3600.0)))

 					Pre_PANswLat = scenePAN.getElementsByTagName("swLat")[0]
 					Pre_PANswLat_unicode = Pre_PANswLat.childNodes[0].data
 					Pre_PANswLat_value = Pre_PANswLat_unicode.strip("\n")
 					PANswLat_value = str(Pre_PANswLat_value)

 					Pre_Dec_PANswLat_value_text = PANswLat_value[:1]
 					Pre_Dec_PANswLat_Degrees = PANswLat_value[1:-4]
 					Dec_PANswLat_Degrees = np.float64(Pre_Dec_PANswLat_Degrees)
 					Pre_Dec_PANswLat_minutes = PANswLat_value[4:-2]
 					Dec_PANswLat_minutes = np.float64(Pre_Dec_PANswLat_minutes)
 					Pre_Dec_PANswLat_sec = PANswLat_value[6:]
 					Dec_PANswLat_sec = np.float64(Pre_Dec_PANswLat_sec)

 					if Pre_Dec_PANswLat_value_text == "N":
 						Dec_PANswLat_value_text = 1.0

 					elif Pre_Dec_PANswLat_value_text == "S":
 						Dec_PANswLat_value_text = -1.0
 					Use_PANswLat_value = np.float64(Dec_PANswLat_value_text * (Dec_PANswLat_Degrees + (Dec_PANswLat_minutes / 60.0) + (Dec_PANswLat_sec / 3600.0)))

 					Pre_PANswLong = scenePAN.getElementsByTagName("swLong")[0]
 					Pre_PANswLong_unicode = Pre_PANswLong.childNodes[0].data
 					Pre_PANswLong_value = Pre_PANswLong_unicode.strip("\n")
 					PANswLong_value = str(Pre_PANswLong_value)

 					Pre_Dec_PANswLong_value_text = PANswLong_value[:1]
 					Pre_Dec_PANswLong_Degrees = PANswLong_value[1:-4]
 					Dec_PANswLong_Degrees = np.float64(Pre_Dec_PANswLong_Degrees)
 					Pre_Dec_PANswLong_minutes = PANswLong_value[4:-2]
 					Dec_PANswLong_minutes = np.float64(Pre_Dec_PANswLong_minutes)
 					Pre_Dec_PANswLong_sec = PANswLong_value[6:]
 					Dec_PANswLong_sec = np.float64(Pre_Dec_PANswLong_sec)

 					if Pre_Dec_PANswLong_value_text == "W":
 						Dec_PANswLong_value_text = 1.0

 					elif Pre_Dec_PANswLong_value_text == "E":
 						Dec_PANswLong_value_text = -1.0
 					Use_PANswLong_value = np.float64(Dec_PANswLong_value_text * (Dec_PANswLong_Degrees + (Dec_PANswLong_minutes / 60.0) + (Dec_PANswLong_sec / 3600.0)))

 					Pre_PANseLat = scenePAN.getElementsByTagName("seLat")[0]
 					Pre_PANseLat_unicode = Pre_PANseLat.childNodes[0].data
 					Pre_PANseLat_value = Pre_PANseLat_unicode.strip("\n")
 					PANseLat_value = str(Pre_PANseLat_value)

 					Pre_Dec_PANseLat_value_text = PANseLat_value[:1]
 					Pre_Dec_PANseLat_Degrees = PANseLat_value[1:-4]
 					Dec_PANseLat_Degrees = np.float64(Pre_Dec_PANseLat_Degrees)
 					Pre_Dec_PANseLat_minutes = PANseLat_value[4:-2]
 					Dec_PANseLat_minutes = np.float64(Pre_Dec_PANseLat_minutes)
 					Pre_Dec_PANseLat_sec = PANseLat_value[6:]
 					Dec_PANseLat_sec = np.float64(Pre_Dec_PANseLat_sec)

 					if Pre_Dec_PANseLat_value_text == "N":
 						Dec_PANseLat_value_text = 1.0

 					elif Pre_Dec_PANseLat_value_text == "S":
 						Dec_PANseLat_value_text = -1.0
 					Use_PANseLat_value = np.float64(Dec_PANseLat_value_text * (Dec_PANseLat_Degrees + (Dec_PANseLat_minutes / 60.0) + (Dec_PANseLat_sec / 3600.0)))

 					Pre_PANseLong = scenePAN.getElementsByTagName("seLong")[0]
 					Pre_PANseLong_unicode = Pre_PANseLong.childNodes[0].data
 					Pre_PANseLong_value = Pre_PANseLong_unicode.strip("\n")
 					PANseLong_value = str(Pre_PANseLong_value)

 					Pre_Dec_PANseLong_value_text = PANseLong_value[:1]
 					Pre_Dec_PANseLong_Degrees = PANseLong_value[1:-4]
 					Dec_PANseLong_Degrees = np.float64(Pre_Dec_PANseLong_Degrees)
 					Pre_Dec_PANseLong_minutes = PANseLong_value[4:-2]
 					Dec_PANseLong_minutes = np.float64(Pre_Dec_PANseLong_minutes)
 					Pre_Dec_PANseLong_sec = PANseLong_value[6:]
 					Dec_PANseLong_sec = np.float64(Pre_Dec_PANseLong_sec)

 					if Pre_Dec_PANseLong_value_text == "W":
 						Dec_PANseLong_value_text = 1.0

 					elif Pre_Dec_PANseLong_value_text == "E":
 						Dec_PANseLong_value_text = -1.0
 					Use_PANseLong_value = np.float64(Dec_PANseLong_value_text * (Dec_PANseLong_Degrees + (Dec_PANseLong_minutes / 60.0) + (Dec_PANseLong_sec / 3600.0)))

					# {Get BrowseBeginLine from catalog file}
					Pre_BrowseBeginLinePAN = scenePAN.getElementsByTagName("browseBeginLine")[0]
					Pre_BrowseBeginLinePAN_unicode = Pre_BrowseBeginLinePAN.childNodes[0].data
					Pre_BrowseBeginLinePAN_value = Pre_BrowseBeginLinePAN_unicode.strip("\n")
					BrowseBeginLinePAN_value = int(Pre_BrowseBeginLinePAN_value)

					# {Get BrowseEndLine from catalog file}
					Pre_BrowseEndLinePAN = scenePAN.getElementsByTagName("browseEndLine")[0]
					Pre_BrowseEndLinePAN_unicode = Pre_BrowseEndLinePAN.childNodes[0].data
					Pre_BrowseEndLinePAN_value = Pre_BrowseEndLinePAN_unicode.strip("\n")
					BrowseEndLinePAN_value = int(Pre_BrowseEndLinePAN_value)

					# Create catalog file
					Image_FilenamePAN = FIlename_path + "/" + RevolutionNumber_value + "_" + SpectralMode_value + "_Filename%s_SceneRank_%s.cmp"%(FileNamePAN_value , str(ScenePANRank_value))
					Image_FilenamePAN_file = open(Image_FilenamePAN, "w")
					Image_FilenamePAN_file.write(str(BeginReception_year) + str(BeginReception_month) + str(BeginReception_date) + "\n")
					Image_FilenamePAN_file.write(str(BeginReception_hour) + str(BeginReception_min) + str(BeginReception_sec) + "\n")
					Image_FilenamePAN_file.write(str(EndReception_year) + str(EndReception_month) + str(EndReception_date) + "\n")
					Image_FilenamePAN_file.write(str(EndReception_hour) + str(EndReception_min) + str(EndReception_sec) + "\n")
					Image_FilenamePAN_file.write(str(OrbitCycle_value) + "\n")
					Image_FilenamePAN_file.write(str(RevolutionNumber_value) + "\n")
					Image_FilenamePAN_file.write(str(Mission_value) + "\n")
					Image_FilenamePAN_file.write(str(SatelliteIdt_value) + "\n")
					Image_FilenamePAN_file.write(str(PassRank_value) + "\n")
					Image_FilenamePAN_file.write(str(PassId_value) + "\n")
					Image_FilenamePAN_file.write(str(SegmentCount_value) + "\n")
					Image_FilenamePAN_file.write(str("Segment info") + "\n")
					Image_FilenamePAN_file.write(str(FileNamePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(GERALDPAN_name) + "\n")
					Image_FilenamePAN_file.write(str(PANSegmentRank_value) + "\n")
					Image_FilenamePAN_file.write(str(InstrumentTypePAN_value) + str(InstrumentIDPAN_value) + "\n")
					Image_FilenamePAN_file.write(str(TransmissionModePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(PANsegmentquality_value) + "\n")
					Image_FilenamePAN_file.write(str(YearPAN_segment) + str(MonthPAN_segment) + str(DatePAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(HourPAN_segment) + str(MinPAN_segment) + str(SecPAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(EndYearPAN_segment) + str(EndMonthPAN_segment) + str(EndDatePAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(EndHourPAN_segment) + str(EndMinPAN_segment) + str(EndSecPAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(PANCompression_ratio_value) + "\n")
					Image_FilenamePAN_file.write(str(SpectralMode_value) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(PANReferenceBand_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_Alongtrackviewingangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_Acrosstrackviewingangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_ABSGain_value) + "\n")
					Image_FilenamePAN_file.write(str("Scene info") + "\n")
					Image_FilenamePAN_file.write(str(ScenecountPAN_value) + "\n")
					Image_FilenamePAN_file.write(str(ScenePANRank_value) + "\n")
					Image_FilenamePAN_file.write(str(Grid_RefPAN) + "\n")
					Image_FilenamePAN_file.write(str(PANtechnicalquality_value) + "\n")
					Image_FilenamePAN_file.write(str(PANcloudCover_value) + "\n")
					Image_FilenamePAN_file.write(str(PANsnowcover_value) + "\n")
					Image_FilenamePAN_file.write(str(create_datePAN[:4]) + str(create_datePAN[4:6]) + str(create_datePAN[6:]) + "\n")
					Image_FilenamePAN_file.write(str(Use_CenterViewingDatePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(YearBeginPAN) + str(MonthBeginPAN) + str(DateBeginPAN) + "\n")
					Image_FilenamePAN_file.write(str(HourBeginPAN) + str(MinBeginPAN) + str(SecBeginPAN) + "\n")
					Image_FilenamePAN_file.write(str(YearEndPAN) + str(MonthEndPAN) + str(DateEndPAN) + "\n")
					Image_FilenamePAN_file.write(str(HourEndPAN) + str(MinEndPAN) + str(SecEndPAN) + "\n")
					Image_FilenamePAN_file.write(str(PANcouplingmode_value) + "\n")
					Image_FilenamePAN_file.write(str(PANorientationAngle_value) + "\n")
					Image_FilenamePAN_file.write(str(PANIncidenceangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PANSunElevation_value) + "\n")
					Image_FilenamePAN_file.write(str(PANSunAzimuth_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANnwLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANnwLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANneLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANneLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANswLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANswLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANseLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANseLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANLatSceneCenter_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANLongSceneCenter_value) + "\n")
					Image_FilenamePAN_file.write(str(DSR_beginPAN) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0))
					Image_FilenamePAN_file.close()

					# # Create catalog file
					Image_Date_timePAN_filename = Date_time_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Date-%s-%s-%s_Time-%s-%s-%s.cmp"%(str(create_datePAN[:4]),str(create_datePAN[4:6]),str(create_datePAN[6:]),Use_CenterViewingDatePAN_value[:-4], Use_CenterViewingDatePAN_value[2:-2],Use_CenterViewingDatePAN_value[4:])
					Image_ConerPAN_filename = Corner_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Upper_Left(%.4f , %.4f)_Upper_Right(%.4f , %.4f)_Lower_Left(%.4f , %.4f)_Lower_Right(%.4f , %.4f).cmp"%(Use_PANnwLat_value ,Use_PANnwLong_value ,Use_PANneLat_value , Use_PANneLong_value , Use_PANswLat_value , Use_PANswLong_value , Use_PANseLat_value , Use_PANseLong_value)
					Image_CenterPAN_filename = Center_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Center_Lat_long(%.4f , %.4f).cmp"%(Use_PANLatSceneCenter_value , Use_PANLongSceneCenter_value)

					shutil.copy(Image_FilenamePAN , Image_Date_timePAN_filename)
					shutil.copy(Image_FilenamePAN , Image_ConerPAN_filename)
					shutil.copy(Image_FilenamePAN , Image_CenterPAN_filename)


					crop_img_PAN = imgPAN[BrowseBeginLinePAN_value : 499 + BrowseBeginLinePAN_value, 0:ColumnsCountPAN_value]
					cv2.imwrite(Image_FilenamePAN[:-4] + ".JPG", crop_img_PAN)

					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_Date_timePAN_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_ConerPAN_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_CenterPAN_filename[:-4] + ".JPG")

				# Last scene condition
				elif ScenePANRank_value == ScenecountPAN_value :

					# Get centerViewingDate from catalog file and use it to file name of Image detail file
					Pre_CenterViewingDatePAN = scenePAN.getElementsByTagName("centerViewingDate")[0]
					Pre_CenterViewingDatePAN_unicode = Pre_CenterViewingDatePAN.childNodes[0].data
					Pre_CenterViewingDatePAN_value = Pre_CenterViewingDatePAN_unicode.strip("\n")
					CenterViewingDatePAN_time = Pre_CenterViewingDatePAN_value[8:14]
					CenterViewingDatePAN_value = str(CenterViewingDatePAN_time)
					Use_CenterViewingDatePAN_value = str(CenterViewingDatePAN_time)[:2] + str(CenterViewingDatePAN_time)[2:4] + str(CenterViewingDatePAN_time)[4:]
					create_datePAN = Pre_CenterViewingDatePAN_value[:8]

					Pre_beginViewingDatePAN = scenePAN.getElementsByTagName("beginViewingDate")[0]
					Pre_beginViewingDatePAN_unicode = Pre_beginViewingDatePAN.childNodes[0].data
					Pre_beginViewingDatePAN_value = Pre_beginViewingDatePAN_unicode.strip("\n")
					BeginViewingDatePAN_value = str(Pre_beginViewingDatePAN_value)

					Pre_YearBeginPAN = BeginViewingDatePAN_value [:4]
					YearBeginPAN = str(Pre_YearBeginPAN)

					Pre_MonthBeginPAN = BeginViewingDatePAN_value [4:6]
					MonthBeginPAN = str(Pre_MonthBeginPAN)

					Pre_DateBeginPAN = BeginViewingDatePAN_value [6:8]
					DateBeginPAN = str(Pre_DateBeginPAN)

					Pre_HourBeginPAN = BeginViewingDatePAN_value [8:10]
					HourBeginPAN = str(Pre_HourBeginPAN)

					Pre_MinBeginPAN = BeginViewingDatePAN_value [10:12]
					MinBeginPAN = str(Pre_MinBeginPAN)

					Pre_SecBeginPAN = BeginViewingDatePAN_value [12:14]
					SecBeginPAN = str(Pre_SecBeginPAN)

					# print "Begin viewing date : %s/%s/%s %s:%s:%s"%(YearBeginPAN , MonthBeginPAN , DateBeginPAN , HourBeginPAN , MinBeginPAN , SecBeginPAN)

					Pre_EndViewingDatePAN = scenePAN.getElementsByTagName("endViewingDate")[0]
					Pre_EndViewingDatePAN_unicode = Pre_EndViewingDatePAN.childNodes[0].data
					Pre_EndViewingDatePAN_value = Pre_EndViewingDatePAN_unicode.strip("\n")
					EndViewingDatePAN_value = str(Pre_EndViewingDatePAN_value)

					Pre_YearEndPAN = EndViewingDatePAN_value [:4]
					YearEndPAN = str(Pre_YearEndPAN)

					Pre_MonthEndPAN = EndViewingDatePAN_value [4:6]
					MonthEndPAN = str(Pre_MonthEndPAN)

					Pre_DateEndPAN = EndViewingDatePAN_value [6:8]
					DateEndPAN = str(Pre_DateEndPAN)

					Pre_HourEndPAN = EndViewingDatePAN_value [8:10]
					HourEndPAN = str(Pre_HourEndPAN)

					Pre_MinEndPAN = EndViewingDatePAN_value [10:12]
					MinEndPAN = str(Pre_MinEndPAN)

					Pre_SecEndPAN = EndViewingDatePAN_value [12:14]
					SecEndPAN = str(Pre_SecEndPAN)

					""" Get DSR_begin from Normal scene
					first  : Get beginRangeLine from catalog file
					second  : then get pre dsrbegin - 4800 (40% of product line) """

					# Get beginRangeLine from catalog file
					Pre_BeginRangelinePAN = scenePAN.getElementsByTagName("beginRangeLine")[0]
					Pre_BeginRangelinePAN_unicode = Pre_BeginRangelinePAN.childNodes[0].data
					Pre_BeginRangelinePAN_value = Pre_BeginRangelinePAN_unicode.strip("\n")
					BeginRangeLinePAN_value = int(Pre_BeginRangelinePAN_value)
					DSR_beginPAN = BeginRangeLinePAN_value

					# Get endRangeLine from catalog file
					Pre_EndRangelinePAN = scenePAN.getElementsByTagName("endRangeLine")[0]
					Per_EndRangeline_unicode = Pre_EndRangelinePAN.childNodes[0].data
					Pre_EndRangelinePAN_value = Per_EndRangeline_unicode.strip("\n")
					EndRangeLinePAN_value = int(Pre_EndRangelinePAN_value)
					DSR_endPAN = EndRangeLinePAN_value

					# { Get KPath and JRow from catalog file and use it to Grid reference
					Pre_KPathPAN = scenePAN.getElementsByTagName("kPath")[0]
					Pre_KPathPAN_unicode = Pre_KPathPAN.childNodes[0].data
					Pre_KPathPAN_value = Pre_KPathPAN_unicode.strip("\n")
					KPathPAN_value = str(Pre_KPathPAN_value)

					Pre_JRowPAN = scenePAN.getElementsByTagName("jRow")[0]
					Pre_JRowPAN_unicode = Pre_JRowPAN.childNodes[0].data
					Pre_JRowPAN_value = Pre_JRowPAN_unicode.strip("\n")
					JRowPAN_value = str(Pre_JRowPAN_value)

					Grid_RefPAN = KPathPAN_value + "-" + JRowPAN_value
					# }

					Pre_PANtechnicalquality = scenePAN.getElementsByTagName("technoQuality")[0]
					Pre_PANtechnicalquality_unicode = Pre_PANtechnicalquality.childNodes[0].data
					Pre_PANtechnicalquality_value = Pre_PANtechnicalquality_unicode.strip("\n")
					PANtechnicalquality_value = str(Pre_PANtechnicalquality_value)

					Pre_PANcloudCover = scenePAN.getElementsByTagName("cloudCover")[0]
					Pre_PANcloudCover_unicode = Pre_PANcloudCover.childNodes[0].data
					Pre_PANcloudCover_value = Pre_PANcloudCover_unicode.strip("\n")
					PANcloudCover_value = str(Pre_PANcloudCover_value)

					Pre_PANsnowcover = scenePAN.getElementsByTagName("snowCover")[0]
					Pre_PANsnowcover_unicode = Pre_PANsnowcover.childNodes[0].data
					Pre_PANsnowcover_value = Pre_PANsnowcover_unicode.strip("\n")
					PANsnowcover_value = str(Pre_PANsnowcover_value)

					Pre_PANcouplingmode = scenePAN.getElementsByTagName("couplingMode")[0]
					Pre_PANcouplingmode_unicode = Pre_PANcouplingmode.childNodes[0].data
					Pre_PANcouplingmode_value = Pre_PANcouplingmode_unicode.strip("\n")
					PANcouplingmode_value = str(Pre_PANcouplingmode_value)

					Pre_PANorientationAngle = scenePAN.getElementsByTagName("orientationAngle")[0]
					Pre_PANorientationAngle_unicode = Pre_PANorientationAngle.childNodes[0].data
					Pre_PANorientationAngle_value = Pre_PANorientationAngle_unicode.strip("\n")
					PANorientationAngle_value = str(Pre_PANorientationAngle_value)

					Pre_PANIncidenceangle = scenePAN.getElementsByTagName("incidenceAngle")[0]
					Pre_PANIncidenceangle_unicoce = Pre_PANIncidenceangle.childNodes[0].data
					Pre_PANIncidenceangle_value = Pre_PANIncidenceangle_unicoce.strip("\n")
					PANIncidenceangle_value = str(Pre_PANIncidenceangle_value)

					Pre_PANLatSceneCenter = scenePAN.getElementsByTagName("latSceneCenter")[0]
					Pre_PANLatSceneCenter_unicode = Pre_PANLatSceneCenter.childNodes[0].data
					Pre_PANLatSceneCenter_value = Pre_PANLatSceneCenter_unicode.strip("\n")
					PANLatSceneCenter_value = str(Pre_PANLatSceneCenter_value)

					Pre_Dec_PANLatSceneCenter_text = PANLatSceneCenter_value[:1]
					Pre_Dec_PANLatSceneCenter_Degrees = PANLatSceneCenter_value[1:-4]
					Dec_PANLatSceneCenter_Degrees = np.float64(Pre_Dec_PANLatSceneCenter_Degrees)
					Pre_Dec_PANLatSceneCenter_minutes = PANLatSceneCenter_value[4:-2]
					Dec_PANLatSceneCenter_minutes = np.float64(Pre_Dec_PANLatSceneCenter_minutes)
					Pre_Dec_PANLatSceneCenter_sec = PANLatSceneCenter_value[6:]
					Dec_PANLatSceneCenter_sec = np.float64(Pre_Dec_PANLatSceneCenter_sec)

					if Pre_Dec_PANLatSceneCenter_text == "N" :
						Dec_PANLatSceneCenter_text = 1.0
					elif Pre_Dec_PANLatSceneCenter_text == "S" :
						Dec_PANLatSceneCenter_text = -1.0
					Use_PANLatSceneCenter_value = np.float64(Dec_PANLatSceneCenter_text * (Dec_PANLatSceneCenter_Degrees + (Dec_PANLatSceneCenter_minutes / 60.0) + (Dec_PANLatSceneCenter_sec / 3600.0)))

 					Pre_PANLongSceneCenter = scenePAN.getElementsByTagName("longSceneCenter")[0]
 					Pre_PANLongSceneCenter_unicode = Pre_PANLongSceneCenter.childNodes[0].data
 					Pre_PANLongSceneCenter_value = Pre_PANLongSceneCenter_unicode.strip("\n")
 					PANLongSceneCenter_value = str(Pre_PANLongSceneCenter_value)

 					Pre_Dec_PANLongSceneCenter_text = PANLongSceneCenter_value[:1]
 					Pre_Dec_PANLongSceneCenter_Degrees = PANLatSceneCenter_value[1:-4]
 					Dec_PANLongSceneCenter_Degrees = np.float64(Pre_Dec_PANLongSceneCenter_Degrees)
 					Pre_Dec_PANLongSceneCenter_minutes = PANLongSceneCenter_value[4:-2]
 					Dec_PANLongSceneCenter_minutes = np.float64(Pre_Dec_PANLongSceneCenter_minutes)
 					Pre_Dec_PANLongSceneCenter_sec = PANLongSceneCenter_value[6:]
 					Dec_PANLongSceneCenter_sec = np.float64(Pre_Dec_PANLongSceneCenter_sec)

 					if Pre_Dec_PANLongSceneCenter_text == "E":
 						Dec_PANLongSceneCenter_text = 1.0
 					elif Pre_Dec_PANLongSceneCenter_text == "W":
 						Dec_PANLongSceneCenter_text = -1.0
 					Use_PANLongSceneCenter_value = np.float64(Dec_PANLongSceneCenter_text * (Dec_PANLongSceneCenter_Degrees + (Dec_PANLongSceneCenter_minutes / 60.0) + (Dec_PANLongSceneCenter_sec / 3600.0)))

 					Pre_PANSunElevation = scenePAN.getElementsByTagName("sunElevation")[0]
 					Pre_PANSunElevation_unicode = Pre_PANSunElevation.childNodes[0].data
 					Pre_PANSunElevation_value = Pre_PANSunElevation_unicode.strip("\n")
 					PANSunElevation_value = str(Pre_PANSunElevation_value)

 					Pre_PANSunAzimuth = scenePAN.getElementsByTagName("sunAzimuth")[0]
 					Pre_PANSunAzimuth_unicode = Pre_PANSunAzimuth.childNodes[0].data
 					Pre_PANSunAzimuth_value = Pre_PANSunAzimuth_unicode.strip("\n")
 					PANSunAzimuth_value = str(Pre_PANSunAzimuth_value)

 					Pre_PANnwLat = scenePAN.getElementsByTagName("nwLat")[0]
 					Pre_PANnwLat_unicode = Pre_PANnwLat.childNodes[0].data
 					Pre_PANnwLat_value = Pre_PANnwLat_unicode.strip("\n")
 					PANnwLat_value = str(Pre_PANnwLat_value)

 					Pre_Dec_PANnwLat_value_text = PANnwLat_value[:1]
 					Pre_Dec_PANnwLat_Degrees = PANnwLat_value[1:-4]
 					Dec_PANnwLat_Degrees = np.float64(Pre_Dec_PANnwLat_Degrees)
 					Pre_Dec_PANnwLat_minutes = PANnwLat_value[4:-2]
 					Dec_PANnwLat_minutes = np.float64(Pre_Dec_PANnwLat_minutes)
 					Pre_Dec_PANnwLat_sec = PANnwLat_value[6:]
 					Dec_PANnwLat_sec = np.float64(Pre_Dec_PANnwLat_sec)

 					if Pre_Dec_PANnwLat_value_text == "N":
 						Dec_PANnwLat_value_text = 1.0

 					elif Pre_Dec_PANnwLat_value_text == "S":
 						Dec_PANnwLat_value_text = -1.0
 					Use_PANnwLat_value = np.float64(Dec_PANnwLat_value_text * (Dec_PANnwLat_Degrees + (Dec_PANnwLat_minutes / 60.0) + (Dec_PANnwLat_sec / 3600.0)))

 					Pre_PANnwLong = scenePAN.getElementsByTagName("nwLong")[0]
 					Pre_PANnwLong_unicode = Pre_PANnwLong.childNodes[0].data
 					Pre_PANnwLong_value = Pre_PANnwLong_unicode.strip("\n")
 					PANnwLong_value = str(Pre_PANnwLong_value)

 					Pre_Dec_PANnwLong_value_text = PANnwLong_value[:1]
 					Pre_Dec_PANnwLong_Degrees = PANnwLong_value[1:-4]
 					Dec_PANnwLong_Degrees = np.float64(Pre_Dec_PANnwLong_Degrees)
 					Pre_Dec_PANnwLong_minutes = PANnwLong_value[4:-2]
 					Dec_PANnwLong_minutes = np.float64(Pre_Dec_PANnwLong_minutes)
 					Pre_Dec_PANnwLong_sec = PANnwLong_value[6:]
 					Dec_PANnwLong_sec = np.float64(Pre_Dec_PANnwLong_sec)

 					if Pre_Dec_PANnwLong_value_text == "W":
 						Dec_PANnwLong_value_text = 1.0

 					elif Pre_Dec_PANnwLong_value_text == "E":
 						Dec_PANnwLong_value_text = -1.0
 					Use_PANnwLong_value = np.float64(Dec_PANnwLong_value_text * (Dec_PANnwLong_Degrees + (Dec_PANnwLong_minutes / 60.0) + (Dec_PANnwLong_sec / 3600.0)))

 					Pre_PANneLat = scenePAN.getElementsByTagName("neLat")[0]
 					Pre_PANneLat_unicode = Pre_PANneLat.childNodes[0].data
 					Pre_PANneLat_value = Pre_PANneLat_unicode.strip("\n")
 					PANneLat_value = str(Pre_PANneLat_value)

 					Pre_Dec_PANneLat_value_text = PANneLat_value[:1]
 					Pre_Dec_PANneLat_Degrees = PANneLat_value[1:-4]
 					Dec_PANneLat_Degrees = np.float64(Pre_Dec_PANneLat_Degrees)
 					Pre_Dec_PANneLat_minutes = PANneLat_value[4:-2]
 					Dec_PANneLat_minutes = np.float64(Pre_Dec_PANneLat_minutes)
 					Pre_Dec_PANneLat_sec = PANneLat_value[6:]
 					Dec_PANneLat_sec = np.float64(Pre_Dec_PANneLat_sec)

 					if Pre_Dec_PANneLat_value_text == "N":
 						Dec_PANneLat_value_text = 1.0

 					elif Pre_Dec_PANneLat_value_text == "S":
 						Dec_PANneLat_value_text = -1.0
 					Use_PANneLat_value = np.float64(Dec_PANneLat_value_text * (Dec_PANneLat_Degrees + (Dec_PANneLat_minutes / 60.0) + (Dec_PANneLat_sec / 3600.0)))

 					Pre_PANneLong = scenePAN.getElementsByTagName("neLong")[0]
 					Pre_PANneLong_unicode = Pre_PANneLong.childNodes[0].data
 					Pre_PANneLong_value = Pre_PANneLong_unicode.strip("\n")
 					PANneLong_value = str(Pre_PANneLong_value)

 					Pre_Dec_PANneLong_value_text = PANneLong_value[:1]
 					Pre_Dec_PANneLong_Degrees = PANneLong_value[1:-4]
 					Dec_PANneLong_Degrees = np.float64(Pre_Dec_PANneLong_Degrees)
 					Pre_Dec_PANneLong_minutes = PANneLong_value[4:-2]
 					Dec_PANneLong_minutes = np.float64(Pre_Dec_PANneLong_minutes)
 					Pre_Dec_PANneLong_sec = PANneLong_value[6:]
 					Dec_PANneLong_sec = np.float64(Pre_Dec_PANneLong_sec)

 					if Pre_Dec_PANneLong_value_text == "W":
 						Dec_PANneLong_value_text = 1.0

 					elif Pre_Dec_PANneLong_value_text == "E":
 						Dec_PANneLong_value_text = -1.0
 					Use_PANneLong_value = np.float64(Dec_PANneLong_value_text * (Dec_PANneLong_Degrees + (Dec_PANneLong_minutes / 60.0) + (Dec_PANneLong_sec / 3600.0)))

 					Pre_PANswLat = scenePAN.getElementsByTagName("swLat")[0]
 					Pre_PANswLat_unicode = Pre_PANswLat.childNodes[0].data
 					Pre_PANswLat_value = Pre_PANswLat_unicode.strip("\n")
 					PANswLat_value = str(Pre_PANswLat_value)

 					Pre_Dec_PANswLat_value_text = PANswLat_value[:1]
 					Pre_Dec_PANswLat_Degrees = PANswLat_value[1:-4]
 					Dec_PANswLat_Degrees = np.float64(Pre_Dec_PANswLat_Degrees)
 					Pre_Dec_PANswLat_minutes = PANswLat_value[4:-2]
 					Dec_PANswLat_minutes = np.float64(Pre_Dec_PANswLat_minutes)
 					Pre_Dec_PANswLat_sec = PANswLat_value[6:]
 					Dec_PANswLat_sec = np.float64(Pre_Dec_PANswLat_sec)

 					if Pre_Dec_PANswLat_value_text == "N":
 						Dec_PANswLat_value_text = 1.0

 					elif Pre_Dec_PANswLat_value_text == "S":
 						Dec_PANswLat_value_text = -1.0
 					Use_PANswLat_value = np.float64(Dec_PANswLat_value_text * (Dec_PANswLat_Degrees + (Dec_PANswLat_minutes / 60.0) + (Dec_PANswLat_sec / 3600.0)))

 					Pre_PANswLong = scenePAN.getElementsByTagName("swLong")[0]
 					Pre_PANswLong_unicode = Pre_PANswLong.childNodes[0].data
 					Pre_PANswLong_value = Pre_PANswLong_unicode.strip("\n")
 					PANswLong_value = str(Pre_PANswLong_value)

 					Pre_Dec_PANswLong_value_text = PANswLong_value[:1]
 					Pre_Dec_PANswLong_Degrees = PANswLong_value[1:-4]
 					Dec_PANswLong_Degrees = np.float64(Pre_Dec_PANswLong_Degrees)
 					Pre_Dec_PANswLong_minutes = PANswLong_value[4:-2]
 					Dec_PANswLong_minutes = np.float64(Pre_Dec_PANswLong_minutes)
 					Pre_Dec_PANswLong_sec = PANswLong_value[6:]
 					Dec_PANswLong_sec = np.float64(Pre_Dec_PANswLong_sec)

 					if Pre_Dec_PANswLong_value_text == "W":
 						Dec_PANswLong_value_text = 1.0

 					elif Pre_Dec_PANswLong_value_text == "E":
 						Dec_PANswLong_value_text = -1.0
 					Use_PANswLong_value = np.float64(Dec_PANswLong_value_text * (Dec_PANswLong_Degrees + (Dec_PANswLong_minutes / 60.0) + (Dec_PANswLong_sec / 3600.0)))

 					Pre_PANseLat = scenePAN.getElementsByTagName("seLat")[0]
 					Pre_PANseLat_unicode = Pre_PANseLat.childNodes[0].data
 					Pre_PANseLat_value = Pre_PANseLat_unicode.strip("\n")
 					PANseLat_value = str(Pre_PANseLat_value)

 					Pre_Dec_PANseLat_value_text = PANseLat_value[:1]
 					Pre_Dec_PANseLat_Degrees = PANseLat_value[1:-4]
 					Dec_PANseLat_Degrees = np.float64(Pre_Dec_PANseLat_Degrees)
 					Pre_Dec_PANseLat_minutes = PANseLat_value[4:-2]
 					Dec_PANseLat_minutes = np.float64(Pre_Dec_PANseLat_minutes)
 					Pre_Dec_PANseLat_sec = PANseLat_value[6:]
 					Dec_PANseLat_sec = np.float64(Pre_Dec_PANseLat_sec)

 					if Pre_Dec_PANseLat_value_text == "N":
 						Dec_PANseLat_value_text = 1.0

 					elif Pre_Dec_PANseLat_value_text == "S":
 						Dec_PANseLat_value_text = -1.0
 					Use_PANseLat_value = np.float64(Dec_PANseLat_value_text * (Dec_PANseLat_Degrees + (Dec_PANseLat_minutes / 60.0) + (Dec_PANseLat_sec / 3600.0)))

 					Pre_PANseLong = scenePAN.getElementsByTagName("seLong")[0]
 					Pre_PANseLong_unicode = Pre_PANseLong.childNodes[0].data
 					Pre_PANseLong_value = Pre_PANseLong_unicode.strip("\n")
 					PANseLong_value = str(Pre_PANseLong_value)

 					Pre_Dec_PANseLong_value_text = PANseLong_value[:1]
 					Pre_Dec_PANseLong_Degrees = PANseLong_value[1:-4]
 					Dec_PANseLong_Degrees = np.float64(Pre_Dec_PANseLong_Degrees)
 					Pre_Dec_PANseLong_minutes = PANseLong_value[4:-2]
 					Dec_PANseLong_minutes = np.float64(Pre_Dec_PANseLong_minutes)
 					Pre_Dec_PANseLong_sec = PANseLong_value[6:]
 					Dec_PANseLong_sec = np.float64(Pre_Dec_PANseLong_sec)

 					if Pre_Dec_PANseLong_value_text == "W":
 						Dec_PANseLong_value_text = 1.0

 					elif Pre_Dec_PANseLong_value_text == "E":
 						Dec_PANseLong_value_text = -1.0
 					Use_PANseLong_value = np.float64(Dec_PANseLong_value_text * (Dec_PANseLong_Degrees + (Dec_PANseLong_minutes / 60.0) + (Dec_PANseLong_sec / 3600.0)))

					# {Get BrowseBeginLine from catalog file}
					Pre_BrowseBeginPAN = int(Hight_PAN)
					BrowseBeginLinePAN_value = Pre_BrowseBeginPAN - 499

					# {Get BrowseEndLine from catalog file}
					Pre_BrowseEndLinePAN = scenePAN.getElementsByTagName("browseEndLine")[0]
					Pre_BrowseEndLinePAN_unicode = Pre_BrowseEndLinePAN.childNodes[0].data
					Pre_BrowseEndLinePAN_value = Pre_BrowseEndLinePAN_unicode.strip("\n")
					BrowseEndLinePAN_value = int(Pre_BrowseEndLinePAN_value)

					# Create catalog file
					Image_FilenamePAN = FIlename_path + "/" + RevolutionNumber_value + "_" + SpectralMode_value + "_Filename%s_SceneRank_%s.cmp"%(FileNamePAN_value , str(ScenePANRank_value))
					Image_FilenamePAN_file = open(Image_FilenamePAN, "w")
					Image_FilenamePAN_file.write(str(BeginReception_year) + str(BeginReception_month) + str(BeginReception_date) + "\n")
					Image_FilenamePAN_file.write(str(BeginReception_hour) + str(BeginReception_min) + str(BeginReception_sec) + "\n")
					Image_FilenamePAN_file.write(str(EndReception_year) + str(EndReception_month) + str(EndReception_date) + "\n")
					Image_FilenamePAN_file.write(str(EndReception_hour) + str(EndReception_min) + str(EndReception_sec) + "\n")
					Image_FilenamePAN_file.write(str(OrbitCycle_value) + "\n")
					Image_FilenamePAN_file.write(str(RevolutionNumber_value) + "\n")
					Image_FilenamePAN_file.write(str(Mission_value) + "\n")
					Image_FilenamePAN_file.write(str(SatelliteIdt_value) + "\n")
					Image_FilenamePAN_file.write(str(PassRank_value) + "\n")
					Image_FilenamePAN_file.write(str(PassId_value) + "\n")
					Image_FilenamePAN_file.write(str(SegmentCount_value) + "\n")
					Image_FilenamePAN_file.write(str("Segment info") + "\n")
					Image_FilenamePAN_file.write(str(FileNamePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(GERALDPAN_name) + "\n")
					Image_FilenamePAN_file.write(str(PANSegmentRank_value) + "\n")
					Image_FilenamePAN_file.write(str(InstrumentTypePAN_value) + str(InstrumentIDPAN_value) + "\n")
					Image_FilenamePAN_file.write(str(TransmissionModePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(PANsegmentquality_value) + "\n")
					Image_FilenamePAN_file.write(str(YearPAN_segment) + str(MonthPAN_segment) + str(DatePAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(HourPAN_segment) + str(MinPAN_segment) + str(SecPAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(EndYearPAN_segment) + str(EndMonthPAN_segment) + str(EndDatePAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(EndHourPAN_segment) + str(EndMinPAN_segment) + str(EndSecPAN_segment) + "\n")
					Image_FilenamePAN_file.write(str(PANCompression_ratio_value) + "\n")
					Image_FilenamePAN_file.write(str(SpectralMode_value) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(PANReferenceBand_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_Alongtrackviewingangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_Acrosstrackviewingangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PAN_ABSGain_value) + "\n")
					Image_FilenamePAN_file.write(str("Scene info") + "\n")
					Image_FilenamePAN_file.write(str(ScenecountPAN_value) + "\n")
					Image_FilenamePAN_file.write(str(ScenePANRank_value) + "\n")
					Image_FilenamePAN_file.write(str(Grid_RefPAN) + "\n")
					Image_FilenamePAN_file.write(str(PANtechnicalquality_value) + "\n")
					Image_FilenamePAN_file.write(str(PANcloudCover_value) + "\n")
					Image_FilenamePAN_file.write(str(PANsnowcover_value) + "\n")
					Image_FilenamePAN_file.write(str(create_datePAN[:4]) + str(create_datePAN[4:6]) + str(create_datePAN[6:]) + "\n")
					Image_FilenamePAN_file.write(str(Use_CenterViewingDatePAN_value) + "\n")
					Image_FilenamePAN_file.write(str(YearBeginPAN) + str(MonthBeginPAN) + str(DateBeginPAN) + "\n")
					Image_FilenamePAN_file.write(str(HourBeginPAN) + str(MinBeginPAN) + str(SecBeginPAN) + "\n")
					Image_FilenamePAN_file.write(str(YearEndPAN) + str(MonthEndPAN) + str(DateEndPAN) + "\n")
					Image_FilenamePAN_file.write(str(HourEndPAN) + str(MinEndPAN) + str(SecEndPAN) + "\n")
					Image_FilenamePAN_file.write(str(PANcouplingmode_value) + "\n")
					Image_FilenamePAN_file.write(str(PANorientationAngle_value) + "\n")
					Image_FilenamePAN_file.write(str(PANIncidenceangle_value) + "\n")
					Image_FilenamePAN_file.write(str(PANSunElevation_value) + "\n")
					Image_FilenamePAN_file.write(str(PANSunAzimuth_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANnwLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANnwLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANneLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANneLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANswLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANswLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANseLat_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANseLong_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANLatSceneCenter_value) + "\n")
					Image_FilenamePAN_file.write(str(Use_PANLongSceneCenter_value) + "\n")
					Image_FilenamePAN_file.write(str(DSR_beginPAN) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0) + "\n")
					Image_FilenamePAN_file.write(str(0))
					Image_FilenamePAN_file.close()

					# # Create catalog file
					Image_Date_timePAN_filename = Date_time_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Date-%s-%s-%s_Time-%s-%s-%s.cmp"%(str(create_datePAN[:4]),str(create_datePAN[4:6]),str(create_datePAN[6:]),Use_CenterViewingDatePAN_value[:-4], Use_CenterViewingDatePAN_value[2:-2],Use_CenterViewingDatePAN_value[4:])
					Image_ConerPAN_filename = Corner_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Upper_Left(%.4f , %.4f)_Upper_Right(%.4f , %.4f)_Lower_Left(%.4f , %.4f)_Lower_Right(%.4f , %.4f).cmp"%(Use_PANnwLat_value ,Use_PANnwLong_value ,Use_PANneLat_value , Use_PANneLong_value , Use_PANswLat_value , Use_PANswLong_value , Use_PANseLat_value , Use_PANseLong_value)
					Image_CenterPAN_filename = Center_path + "/" + RevolutionNumber_value + "-" + SpectralMode_value + "_Center_Lat_long(%.4f , %.4f).cmp"%(Use_PANLatSceneCenter_value , Use_PANLongSceneCenter_value)

					shutil.copy(Image_FilenamePAN , Image_Date_timePAN_filename)
					shutil.copy(Image_FilenamePAN , Image_ConerPAN_filename)
					shutil.copy(Image_FilenamePAN , Image_CenterPAN_filename)


					crop_img_PAN = imgPAN[BrowseBeginLinePAN_value : 499 + BrowseBeginLinePAN_value, 0:ColumnsCountPAN_value]
					cv2.imwrite(Image_FilenamePAN[:-4] + ".JPG", crop_img_PAN)

					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_Date_timePAN_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_ConerPAN_filename[:-4] + ".JPG")
					shutil.copy(Image_FilenamePAN[:-4] + ".JPG" , Image_CenterPAN_filename[:-4] + ".JPG")

	total_sceneCount = str(sum(SceneCount_list))
	shutil.rmtree(cufdir)
	print "Finishing create command files and cut browse image from strip to scene.\n"

	# Return Revolution number , Segment count , scene count , list of gerald name for use in another function in another script
	return  SegmentCount_value , total_sceneCount
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
	app = QApplication(sys.argv)

	try :
		CUF_path = "C:/Worker/Support-Worker/Sipros_system/CUF_PROCESSING"
		# CUF_path = "/home/sipros/Application_1A_2A/Sipros_System/CUF_PROCESSING"
		CUF_zip = QFileDialog.getOpenFileName(None , "Open CUF zip File" , CUF_path , "*.zip")
		cufzip_file_path = str(CUF_zip)
		Product_detail = "C:/Worker/Support-Worker/Sipros_system/COMMAND_FILES"
		# Product_detail = "/home/sipros/Application_1A_2A/Sipros_System/COMMAND_FILES"
		ReadData(cufzip_file_path, Product_detail)

	except IOError :
		QMessageBox.warning(None , "Warning !" , "Create catalog file is about by user.")
		print traceback.format_exc()

	except :
		 QMessageBox.critical(None , "Critical" , "Cann't open cuf file.")
		 print traceback.format_exc()

	sys.exit()
