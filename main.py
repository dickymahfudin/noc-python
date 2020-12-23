from getData import runSingle, runAll
from checkProgram import runAllCheck, runSingleChech
import sys


def helpCommand():
    print('main.py getdata:all \t\t program mengambil data semua site')
    print('main.py getdata:single nojs \t program mengambil data satu site')
    print('main.py checkP:all nojs \t mengecek status program semua site')
    print('main.py checkP:single nojs \t mengecek status program satu site')


try:
    param = sys.argv[1]
    if param == 'help':
        helpCommand()
    elif param == 'getdata:all':
        runAll()
    elif param == 'getdata:single':
        try:
            runSingle(sys.argv[2])
        except:
            print('sertakan paramater Nojs dengan benar')
    elif param == 'checkP:all':
        runAllCheck()
    elif param == 'checkP:single':
        try:
            runSingleChech(sys.argv[2])
        except:
            print('sertakan paramater Nojs dengan benar')

except:
    helpCommand()
