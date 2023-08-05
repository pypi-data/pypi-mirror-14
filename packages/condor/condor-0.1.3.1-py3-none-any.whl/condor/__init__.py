'''
Test definition
'''

import sys, os

sys.path.append(os.getcwd()) 


if __name__ == 'condor':
    try:
        import condorscript
    except ImportError:
        print("No condorscript.py file was detected in directory")
        exit(0)
