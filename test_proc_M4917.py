#!/usr/bin/env python3

##############################################################################
# 
# Module: test_proc_M4917.py
#
# Description:
#     MFG test script for Model 4917
#
# Copyright notice:
#     This file copyright (c) 2022 by
#
#         MCCI Corporation
#         3520 Krums Corners Road
#         Ithaca, NY  14850
#
#     Released under the MIT license.
#
# Author:
#     Dhinesh Kumar Pitchai, MCCI    July 2022
#
##############################################################################

import argparse
import importlib
import os
import re
import subprocess
import sys
import time

import serial
from serial.tools import list_ports

##############################################################################
# Utilities
##############################################################################

def verbose(msg):
    """
    Display verbose message

    Args:
        msg: receives verbose message

    Returns:
        No explicit result        
    """
        
    if(optVerbose):
        print(msg, end='\n')


def debug(msg):
    """
    Display debug message

    Args:
        msg: receives debug messages

    Returns:
        No explicit result
    """

    if (optDebug):
        print (msg, end='\n')


def error(msg):
    """
    Display error message

    Args:
        msg: receives error messages

    Returns:
        No explicit result
    """

    print (msg, end='\n')


def fatal(msg):
    """
    Display error message and exit

    Args:
        msg: receives error messages

    Returns:
        No explicit result        
    """

    error(msg)
    sys.exit(1)


def report():
    pass


def exec_cmd(cmdList, sPath):
    """
    receive cli command to run provisioining

    Args:
        cmdList: command line arguments

    Returns:
        True if success
    """

    try:
        result = subprocess.Popen(
            cmdList, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=sPath)
        op, err = result.communicate()
    except Exception as e:
        print("Error occured: ", e)
        print("Subprocess communication failed")
        sys.exit(1)

    if result.returncode == 1:
        print("Error result in subprocess...")
        print(op.decode())
        print(err.decode())
        return False, op.decode()
    else:
        print(op.decode(), end='\n')
        print(err.decode())

    return True, op.decode()

def availablePort(listPort, portName):
    for p in listPort:
        if p.device == portName \
            or p.device == portName.upper():
            return p.device

def wait_for_device(provScriptPath, provScript, portName):
    """
    wait for com port

    Args:
        provScriptPath: provisioning script directory

    Returns:
        No explicit result
    """

    while True:
        listPort = []
        listPort = list(list_ports.comports())
        portAvail = availablePort(listPort, portName)

        if portAvail:
            infoCmdList = [
                'python',
                provScript,
                '-v',
                '-port',
                portName,
                '-permissive',
                '-info'
            ]
            if exec_cmd(infoCmdList, provScriptPath):
                return 0
                
        print('Waiting for device on port {}...'
                .format(portName), end='\n')
        time.sleep(1)

def add_argument(optparser):
    optparser.add_argument(
        '-D',
        action='store_true',
        default=False,
        dest='debug',
        help='Operate in debug mode. \
        Causes more output to be produced')
    optparser.add_argument(
        '-n',
        action='store',
        nargs='+',
        dest='negate',
        type=str,
        help='Negate the option. E.g. -n D M F v; \
        If -n F, don\'t do final provisioning')
    optparser.add_argument(
        '-M',
        action='store_true',
        default=True,
        dest='mfg',
        help='For perform MFG test')
    optparser.add_argument(
        '-F',
        action='store_true',
        default=True,
        dest='final',
        help='Do final provisioning')
    optparser.add_argument(
        '-v',
        action='store_true',
        default=False,
        dest='verbose',
        help='Operate in verbose mode')
    optparser.add_argument(
        '-s',
        action='store',
        nargs=1,
        dest='userserial',
        type=str,
        required=True,
        help='Specify the low-order digits of the \
        serial number to be used, in hex, without \
        inserted \'-\' or other byte separators.')
    optparser.add_argument(
        '-port',
        action='store',
        nargs=1,
        dest='portname',
        type=str,
        required=True,
        help='Specify the COM port name. This is \
        system specific. E.g. -p COM8')
    return optparser


# main function
def main():

    pName = os.path.basename(__file__)
    pDir = os.path.dirname(os.path.abspath(__file__))

    # Capture arguments
    optparser = argparse.ArgumentParser(description='MCCI MFG Test Script')

    optparser = add_argument(optparser)

    opt = optparser.parse_args()

    optDebug = opt.debug
    optMfg = opt.mfg
    optFinal = opt.final
    optVerbose = opt.verbose
    optUserserial = opt.userserial
    optPortname = opt.portname

    opt = optparser.parse_args()
        
    optDebug = opt.debug
    optMfg = opt.mfg
    optFinal = opt.final
    optVerbose = opt.verbose
    optUserserial = opt.userserial

    if opt.negate:
        negCount = len(opt.negate)
    else:
        negCount = 0

    for i in range(negCount):
        nResult = re.search(r'[D|M|F|v]', opt.negate[i])
                
        if not nResult:
            verbose('Illegal negate option argument: -n {}'
                .format(opt.negate[i]))
            optparser.print_help()
            fatal('ERROR: Illegal argument passed')
        else:
            if opt.negate[i] == 'D':
                optDebug = False
            if opt.negate[i] == 'M':
                optMfg = False
            if opt.negate[i] == 'F':
                optFinal = False
            if opt.negate[i] == 'v':
                optVerbose = False

    # Setup required variables
    stPath = 'c:\\stlink\\bin'
    stFlash = stPath + '\\st-flash.exe'
    imgMfg = 'c:\\tmp\\build-model4917-mfgtest\\model4917-mfgtest.ino.hex'
    imgUser = 'c:\\tmp\\build-Model4917-LoRawan\\Model4917-LoRawan.ino.hex'
    provScriptPath ='E:\\IoT\\Projects\\Windsor\\Model4917-test-procedure-script\\20230127\\test-proc-M4917' #'d:\\MCCI-IoT\\McGraw\\GitLab\\mcci\\test-proc-M4917\\test-proc-M4917'
    provScript = provScriptPath + '\\mcci_catena_provision_ttn.py'
    portName = opt.portname[0]
    mfgPfx = 'mfg-'
    mfgApp = 'cdc-mfg-test-pranau'
    userPfx = 'device-'
    userApp = 'model4917-default'
    snFormat = '0002cc010000xxxx'
    mSerial = snFormat[:-4] + optUserserial[0][-4:]
    mSerialNo = '-'.join(mSerial[i:i+2] for i in range(0, len(mSerial), 2))
    userJoineui = '0000000000000001'
    mfgJoineui = '0000000000000002'
    freqplan = 'US915'
    loraver = '1.0.3'

    # Serial port Settings
    comPort = serial.Serial()
    comPort.port = portName
    comPort.baudrate = 115200
    comPort.bytesize = serial.EIGHTBITS
    comPort.parity = serial.PARITY_NONE
    comPort.stopbits = serial.STOPBITS_ONE

    # Validate user serial
    if (re.match(r'[0-9A-Fa-f]{16}', mSerial)):
        print('serial looks good: SERIAL: {} SN: {}'
                .format(mSerial, mSerialNo), end='\n')
    else:
        fatal('serial looks good: SERIAL: {} SN: {}'
                .format(mSerial, mSerialNo))

    if optMfg:
        # Load the mfg program
        print('Loading the firmware...')
        mCmdList = [stFlash, '--format', 'ihex', 'write', imgMfg]
        exec_cmd(mCmdList, stPath)

        # Provision using the script
        initVarUserSerial = 'INIT_SYSEUI=' + mSerial
        initVarSn = 'INIT_SN=' + mSerialNo

        initCmdList = [
            'python',
            provScript,
            '-v',
            '-port',
            portName,
            '-permissive',
            '-V',
            initVarUserSerial,
            '-V',
            initVarSn,
            '-s',
            'mfgtest-init.cat'
        ]

        provCmdList = [
            'python',
            provScript,
            '-D',
            '-port',
            portName,
            '-V',
            'APPID=' + mfgApp,
            '-V',
            'BASENAME=' + mfgPfx,
            '-V',
            'JOINEUI=' + mfgJoineui,
            '-V',
            'FREQPLAN=' + freqplan,
            '-V',
            'LORAVER=' + loraver,
            '-r',
            '-s',
            'mfgtest-provision.cat'
        ]

        print('provision for mfg SYSEUI={} SN={}'
                .format(mSerial, mSerialNo), end='\n')
        time.sleep(9)
        wait_for_device(provScriptPath,provScript, portName)

        print('Initialize serial number')
        exec_cmd(initCmdList, provScriptPath)

        print('Set up TTN provisioning')
        exec_cmd(provCmdList, provScriptPath)

        # Run the test
        input('run the test on port {}: '.format(portName))

        # Run deep sleep
        print('run deep sleep test and check current')

        # Wait for OK
        input('Press enter when ready')

    if optFinal:
        wait_for_device(provScriptPath, provScript, portName)

        provCmdList = [
                        'python',
                        provScript,
                        '-D',
                        '-port',
                        portName,
                        '-V',
                        'APPID=' + userApp,
                        '-V',
                        'BASENAME=' + userPfx,
                        '-V',
                        'JOINEUI=' + userJoineui,
                        '-V',
                        'FREQPLAN=' + freqplan,
                        '-V',
                        'LORAVER=' + loraver,
                        '-r',
                        '-s',
                        'user-provision.cat'
                        ]
        exec_cmd(provCmdList, provScriptPath)

        # Load the user program
        print('Loading the firmware...')
        mCmdList = [stFlash, '--format', 'ihex', 'write', imgUser]
        exec_cmd(mCmdList, stPath)

        print()
        print('User app provisioned for {} and downloaded'
                .format(userApp), end='\n')
        input('Check signal strenth on user-app join: ')

    while True:
        tResult = input('Enter y for pass, n for fail: ')
        if tResult == 'y' or tResult == 'n':
            status = tResult
            break

    if status != 'y':
        sys.exit(1)
    else:
        sys.exit(0)


#### the standard trailer #####
if __name__ == '__main__':
    main()