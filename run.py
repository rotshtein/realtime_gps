import sys
import time
import wget
import os.path
import gzip
import argparse
import zlib
import subprocess
import py_compile


def get_ephemeris(ephemeris_directory):
    global GZIP_DIR
    year = time.localtime().tm_year
    yearExtension = year-2000
    yday = time.localtime().tm_yday
    filename = 'brdc' + str(yday).zfill(3) + '0.' + str(yearExtension) + 'n'
    print '***********' + filename
    eFile = ephemeris_directory + '/' + filename
    if is_windows():
        eFile = ephemeris_directory + '\\' + filename

    if not os.path.isfile(eFile):
        if not os.path.isfile(eFile + '.Z'):
            print 'get the ephemeris file ' + filename + '\n\r'
            source = 'http://ftp.pecny.cz/ftp/LDC/orbits/' + filename +'.Z'
            print 'File location=' + eFile
            dFile = wget.download(source, ephemeris_directory)
            print '\n\r' + dFile+ ' Downloaded\n\r'
        else:
            dFile = eFile + '.Z'
        print 'Uncompress...\n\r'
	if is_windows():
            subprocess.call(GZIP_DIR + '\\7z e '+ dFile + ' -o' + ephemeris_directory, shell=True)
        else:
            subprocess.call('gunzip -k -d '+ dFile, shell=True)
        print 'Finish to Uncompress\n\r'
    return eFile

def buildIQ(eFile, duration, csv_file, location, binfilename):
    print eFile
    if csv_file is None:
        print '\nBuilding static location\n'
        if is_windows():
            print 'gps-sdr-sim -v -T now -e ' + eFile + ' -l ' + location + ' -b 8 -d '+ duration + ' -s 4000000' + ' -o ' + binfilename
            subprocess.call('gps-sdr-sim -v -T now -e ' + eFile + ' -l ' + location + ' -b 8 -d '+ duration + ' -s 4000000' + ' -o ' + binfilename, shell=True)
        else:
            subprocess.call('./gps-sdr-sim -v -T now -e ' + eFile + ' -l ' + location + ' -b 8 -d '+ duration + ' -s 4000000' + ' -o ' + binfilename, shell=True)			
        #subprocess.call('gps-sdr-sim -v -e ' + eFile + ' -l 32.1464833,34.933,30 -b 8 -d '+ duration + ' -s 4000000', shell=True)
    else:
        print '\nBuilding dynamic location according ' + csv_file + '\n'
        if is_windows():
            subprocess.call('gps-sdr-sim -v -T now -e ' + eFile + ' -u ' + csv_file + ' -b 8 -d '+ duration + ' -s 4000000' + ' -o ' + binfilename, shell=True)
        else:
            subprocess.call('./gps-sdr-sim -v -T now -e ' + eFile + ' -u ' + csv_file + ' -b 8 -d '+ duration + ' -s 4000000' + ' -o ' + binfilename, shell=True)
    return binfilename

def RunRealtime(eFile, location, binfilename):
    if is_windows():
        print ('gps-sdr-sim -b 8 -e ' + eFile + '-l ' + location)
        subprocess.call('.gps-sdr-sim -b 8 -e ' + eFile + ' -l ' + location, shell=True)
    else:
        subprocess.call('nc -l 0.0.0.0 22500 | ./rt_gpssim  -b 8 -e ' + eFile + ' -l  ' + location, shell=True)			
    return binfilename    
    
def start_broadcast(binFile, additional_param):
    global HACKRF_DIR 
    print 'HACKRF_DIR = ' + HACKRF_DIR
    print 'hackrf_transfer from ' + binFile + '\n\r'
    #subprocess.call([HACKRF_DIR + '\\hackrf_transfer', '-t',  binFile,'-f', '1575420000', '-s', '4000000', '-a', '1', '-x', '1', '-R'],shell=True)
    command = HACKRF_DIR + '\\hackrf_transfer -t ' + binFile + ' -f 1575420000 -s 4000000 -a 1 -x 1 ' + additional_param
    subprocess.call(command,shell=True)

def help():
	s = 'Environment settings\n'
	s += '\tEphemeris directory stored by default at ./Files. Can by set by EPHEREMIS_DIR\n'
	if is_windows():
	    s += '\thackrf_transfer.exe location is set by default to "C:/Program Files/GNURadio-3.7/bin/". Can by set by HACKRF_DIR\n'
	    s += '\t7z.exe location is set by default to "c:\\Program Files (x86)\\7-Zip\\7z". Can by set by GZIP_DIR\n'
        else:
	    s += '\thackrf_transfer.exe location is set at installation to by default to "/usr/bin". Can by set by HACKRF_DIR\n'

	return s
	
def update_dirs():
    global FILES_DIR
    global HACKRF_DIR 
    global GZIP_DIR
    FILES_DIR = os.environ.get('FILES_DIR')
    HACKRF_DIR = os.environ.get('HACKRF_DIR')
    GZIP_DIR = os.environ.get('GZIP_DIR')

    if is_windows():
        if FILES_DIR is None:
            FILES_DIR = '.\Files'

        if HACKRF_DIR is None:
            HACKRF_DIR = '"C:\\Program Files\\GNURadio-3.7\\bin"'

        if GZIP_DIR is None:
            GZIP_DIR = '"c:\\Program Files (x86)\\7-Zip"'
    else:
        if FILES_DIR is None:
            FILES_DIR = './Files'

def is_windows():
	if os.name == 'nt':
		return True
	return False

def main():
    global FILES_DIR
    global HACKRF_DIR

    update_dirs()
    csv_file = None

    parser = argparse.ArgumentParser(description='Run.py - GPS spoofing tool')
    parser._optionals.title = help()
    parser.add_argument('-d', action="store", dest='duration', type=str, help='Running suration in seconds', default='300')
    parser.add_argument('-u', action="store", dest='csv_file', type=str, help='Set route csv file')
    parser.add_argument('-o', action="store", dest='sim_filename', type=str, help='save the gpsbin file at specify filename', default='gpssim.bin')
    parser.add_argument('-l', action="store", dest='location', type=str, help='Use specific lat/long. use -l lat,long,hight', default='32.162,34.9337,157.0')
    parser.add_argument('-f', action="store", dest='input_sim_filename', type=str, help='Skip the generation of gps file and transmit the given file')
    parser.add_argument('-R', action="store_true", dest='repeat', help='Repeat transmiting in loop', default = False)
    parser.add_argument('-r', action="store_true", dest='realtime', help='Realtime mode coordinate from goole map', default = False)
    parser.add_argument('-N', action="store_true", dest='do_not_transmit', help='Do not transmit', default = False)
    results = parser.parse_args()
    #start_broadcast(results.input_sim_filename, '')
    
	
    
    if results.input_sim_filename is None:
        ephemerisFile = get_ephemeris(FILES_DIR)
        print 'ephemerisFile = ' + ephemerisFile
        if results.realtime is False:
            results.input_sim_filename = buildIQ(ephemerisFile, results.duration, results.csv_file, results.location, results.sim_filename)
    if results.realtime is True:
        RunRealtime (ephemerisFile, results.location, results.sim_filename)
        
    else:
        if results.do_not_transmit is not True:
            R = '-R' if results.repeat is True else ''
            start_broadcast(results.input_sim_filename, R)
    
if __name__ == '__main__':
	#py_compile.compile('run.py')
	main()

