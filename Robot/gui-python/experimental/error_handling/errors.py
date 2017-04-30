from time import gmtime, strftime
# Import library used for managing .log files
import logging
# Import library used to extract, format and print stack traces
import traceback

global Log_File
Log_File = "telebot_error.log"

def ErrorLog(message):
	logging.basicConfig(filename = Log_File, level = logging.DEBUG)
	logging.warning(strftime(" %d-%m-%Y %H:%M:%S -> ", gmtime()) + 
					str(message))
	return None

def DebugLog(message):
	logging.basicConfig(filename= Log_File, level = logging.DEBUG)
	logging.debug(strftime(" %d-%m-%Y %H:%M:%S -> ", gmtime()) + 
				  str(message))
	return None
	
def InfoLog(message):
	logging.basicConfig(filename = Log_File, level = logging.DEBUG)
	logging.info(strftime(" %d-%m-%Y %H:%M:%S -> ", gmtime()) + 
				 str(message))
	return None

if __name__ == '__main__':
	try:
		print("Holaaaa")
		raise NameError
	except Exception as e:
		ErrorLog(traceback.format_exc())
	finally:
		InfoLog("Tschüssy")