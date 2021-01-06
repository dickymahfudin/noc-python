from getData import runAllNewSite, runSingleNewSite, runAllV1
from checkProgram import runAllCheckNew, runSingleChechNew
import sys


def helpCommand():
    print()
    print('main.py getdata:all:v1 \t\t mengambil data ehub v1 100 site (all)\n')
    print('main.py getdata:all:v3 \t\t mengambil data ehub v3 site baru (all)')
    print('main.py getdata:single:v3 nojs \t mengambil data ehub v3 site baru (single)')
    print('main.py checkP:all \t mengecek status program semua site')
    print('main.py checkP:single nojs \t mengecek status program satu site')
    print()


try:
    param = sys.argv[1]
    if param == 'help':
        helpCommand()
    elif param == 'getdata:all:v1':
        runAllV1()
    elif param == 'getdata:all:v3':
        runAllNewSite()
    elif param == 'getdata:single:v3':
        try:
            runSingleNewSite(sys.argv[2])
        except:
            print('sertakan paramater Nojs dengan benar')

    elif param == 'checkP:all':
        runAllCheckNew()
    elif param == 'checkP:single':
        try:
            runSingleChechNew(sys.argv[2])
        except:
            print('sertakan paramater Nojs dengan benar')

except:
    helpCommand()
    pass
