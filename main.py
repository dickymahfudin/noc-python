from getData import runAllNewSite, runSingleNewSite, runAllV1, runOtherSite
from checkProgram import runAllCheckNew, runSingleChechNew
from capacity import runAllCapacity, runSingleCapacity
from ssh import webAppAll, webAppSingle
import sys
from variable import PORT_APT1, PORT_APT2


def helpCommand():
    print()
    print('main.py getdata:all:v1 \t\t\t mengambil data ehub v1 100 site (all)')

    print('\nmain.py getdata:all:apt1 \t\t mengambil data ehub v3 APT1 (all)')
    print('main.py getdata:single:apt1 nojs \t mengambil data ehub v3 APT1 (single)')
    print('main.py program:all:apt1 \t\t cek status program APT1 (all)')
    print('main.py program:single:apt1 nojs \t cek status program APT1 (single)')
    print('main.py capacity:all:apt1 \t\t cek status ram, disk APT1 (all)')
    print('main.py capacity:single:apt1 nojs \t cek status ram, disk APT1 (single)')
    print('main.py webapp:all:apt1 \t\t update program webapp APT1 (all)')
    print('main.py webapp:single:apt1 nojs \t update program webapp APT1 (single)')

    print('\nmain.py getdata:all:apt2 \t\t mengambil data ehub v3 APT2 (all)')
    print('main.py getdata:single:apt2 nojs \t mengambil data ehub v3 APT2 (single)')
    print('main.py program:all:apt2 \t\t cek status program APT2 (all)')
    print('main.py program:single:apt2 nojs \t cek status program APT2 (single)')
    print('main.py capacity:all:apt2 \t\t cek status ram, disk APT2 (all)')
    print('main.py capacity:single:apt2 nojs \t cek status ram, disk APT2 (single)')
    print('main.py webapp:all:apt2 \t\t update program webapp APT2 (all)')
    print('main.py webapp:single:apt2 nojs \t update program webapp APT2 (single)\n')
    print('main.py other \t\t\t\t mengambil data ehub v3 Non Bakti')
    print()


try:
    param = sys.argv[1]
    if param == 'help':
        helpCommand()
    # ---------------v1---------------
    elif param == 'getdata:all:v1':
        runAllV1()

    # ---------------APT1---------------
    elif param == 'getdata:all:apt1':
        runAllNewSite(PORT_APT1, "APT1")
    elif param == 'getdata:single:apt1':
        try:
            runSingleNewSite(sys.argv[2], PORT_APT1, "APT1")
        except:
            print('sertakan paramater Nojs dengan benar')
    elif param == 'program:all:apt1':
        runAllCheckNew(PORT_APT1, "APT1")
    elif param == 'program:single:apt1':
        try:
            runSingleChechNew(sys.argv[2], PORT_APT1, "APT1")
        except:
            print('sertakan paramater Nojs dengan benar')
    elif param == 'capacity:all:apt1':
        runAllCapacity(PORT_APT1, "APT1")
    elif param == 'capacity:single:apt1':
        try:
            runSingleCapacity(sys.argv[2], PORT_APT1, "APT1")
        except:
            print('sertakan paramater Nojs dengan benar')
    elif param == 'webapp:all:apt1':
        webAppAll(PORT_APT1, 'APT1')
    elif param == 'webapp:single:apt1':
        try:
            webAppSingle(sys.argv[2], PORT_APT1, "APT1")
        except:
            print('sertakan paramater Nojs dengan benar')

    # ---------------APT2---------------
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
    elif param == 'capacity:single:apt2':
        try:
            runSingleCapacity(sys.argv[2], PORT_APT2, "APT2")
        except:
            print('sertakan paramater Nojs dengan benar')
    elif param == 'webapp:all:apt2':
        webAppAll(PORT_APT2, 'APT2')
    elif param == 'webapp:single:apt2':
        try:
            webAppSingle(sys.argv[2], PORT_APT2, "APT2")
        except:
            print('sertakan paramater Nojs dengan benar')

    # ---------------else---------------
    elif param == 'other':
        print("masuk")
        runOtherSite()
        # try:
        # except:
        #     print('sertakan paramater Nojs dengan benar')

    else:
        helpCommand()

except:
    helpCommand()
