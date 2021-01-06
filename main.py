from getData import runAllNewSite, runSingleNewSite, runAllV1
from checkProgram import runAllCheckNew, runSingleChechNew
from capacity import runAllCapacity
import sys
from variable import PORT_APT1, PORT_APT2


def helpCommand():
    print()
    print('main.py getdata:all:v1 \t\t\t mengambil data ehub v1 100 site (all)\n')
    print('main.py getdata:all:apt2 \t\t mengambil data ehub v3 APT2 (all)')
    print('main.py getdata:single:apt2 nojs \t mengambil data ehub v3 APT2 (single)')
    print('main.py program:all:apt2 \t\t mengecek status program APT2 (all)')
    print('main.py program:single:apt2 nojs \t mengecek status program APT2 (single)')
    print('main.py capacity:all:apt2 \t\t mengecek status ram, disk APT2 (all)')
    print()


try:
    param = sys.argv[1]
    if param == 'help':
        helpCommand()
    elif param == 'getdata:all:v1':
        runAllV1()
    elif param == 'getdata:all:apt2':
        runAllNewSite(PORT_APT2, "APT2")
    elif param == 'getdata:single:apt2':
        try:
            runSingleNewSite(sys.argv[2], PORT_APT2, "APT2")
        except:
            print('sertakan paramater Nojs dengan benar')
    elif param == 'program:all:apt2':
        runAllCheckNew(PORT_APT2, "APT2")
    elif param == 'program:single:apt2':
        try:
            runSingleChechNew(sys.argv[2], PORT_APT2, "APT2")
        except:
            print('sertakan paramater Nojs dengan benar')
    elif param == 'capacity:all:apt2':
        runAllCapacity(PORT_APT2, "APT2")
        pass
    else:
        helpCommand()

except:
    helpCommand()
