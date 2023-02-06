# Model 4917 Test Procedure

## Requirements

- Test fixture (documented at https://gitlab-x.mcci.com/mcci/hardware/catena/mfg/test-fixture-4917)

- Model 4917 board.

- Clone the libraries for mfg test (https://gitlab-x.mcci.com/mcci/hardware/catena/mfg/catena-mfgtest) under 'C:\Users.......\Documents\Arduino\libraries'

- Test sketch [model4917-mfgtest.ino]( https://gitlab-x.mcci.com/mcci/hardware/catena/model4917/model4917-mfgtest)

- Test script

- A copy of `stlink` (latest version from - https://github.com/stlink-org/stlink/releases), unzipped at `c:/stlink` (so that `c:/stlink/bin` has the executables)

- The build file for model4917-mfgtest is added to PDX under SW #23400xxxx. Download the ZIP/RAR file, extract and rename the HEX file (`model4917-mfgtest.ino-vx.y.z-........-mcci_test.hex`) in it as `model4917-mfgtest.ino.hex`.

- The binary images to be programmed at c:\tmp\build-model4917-mfgtest and c:\tmp\build-user-firmware (optional)

- Tera Term

- Make sure that the appropriate key is set in regedit by importing `disable-sn-M4917.reg`.

- MCCI provisioning tools from [mcci-catena-provision](https://github.com/mcci-catena/mcci-catena-provision)

  - Follow README in `mcci-catena-provision` for `mcci_catena_provision_ttn.py` to configure TTN CLI.
  - Copy `mcci_catena_provision_ttn.py` to same directory as test procedure of 4917.

- OTII tester and OTII software from https://www.qoitech.com/.

- Ideally, a 9V power supply for the OTII, but that can be avoided.

- A USB hub to connect all the things to your PC.

- A short USB cable to connect the hub to the UUT.

## Setup

1. Edit the script to change paths to the components as needed.

2. Open the OTII tool, and set the power supply. It can only be 3.75V if you don't have a power supply for the OTII.

3. Copy the build files of MFG tests to the directory `c:\mcci\tmp\`.

4. Make a directory (suggested `c:\mcci\mfg\test-YYYYMMDD`), and save the OTII project there.

5. Copy the spreadsheet from the template to the mfg directory, and set it up with your starting serial number. Leave it open.

6. open a git bash window, and `cd` to this directory.

7. Open Tera Term.

7. Get a tape of serial numbers. Use [`mcci/tools/bin/make-sn-list`](https://gitlab-x.mcci.com/mcci/tools/bin/make-sn-list) to generate if needed.  Note that only about 140 serial numbers will fit on a fresh 7m roll of tape. A commnand like this gets 90 sns.

    ```sh
    bright make-sn-list.bri -n90 01-00-00-xx-nn > /mcci/mfg/20191209/sn-xxxx-to-xxnn-n90.txt
    ```

   Use the dymo label printer to load the file and print labels.

8. Open two firefox windows (or tabs), open to

- https://nam1.cloud.thethings.network/console/applications/mcci-mfg-4917
- https://nam1.cloud.thethings.network/console/applications/model4917-default

## Testing a board

1. Get the serial number of the next board to be tested from the spreadsheet, and open a bash shell.

2. Insert board in tester w/o USB cable

3. Close tester

4. Attach USB cable.

5. Make sure that power light comes on but red LED doesn't light up -- if red LED lights, then you've already tested this board.

6. Start the test. To skip user firmware (download and provisioning), use argument `-n F` while running the script.

    ```console
    $ ./test_proc_4917.py -D -n F -s 0A2F -p COM8
    serial looks good: SERIAL: 0002cc0100000A2F SN: 00-02-cc-01-00-00-0A-2F
    Loading the firmware...
    st-flash 1.5.1
    Flash page at addr: 0x0801da00 erased
    1577/1577 halfpages written

    2023-02-02T16:43:00 INFO common.c: Loading device parameters....
    2023-02-02T16:43:00 INFO common.c: Device connected is: L0x Category 5 device, id 0x20086447
    2023-02-02T16:43:00 INFO common.c: SRAM size: 0x5000 bytes (20 KiB), Flash: 0x30000 bytes (192 KiB) in pages of 128 bytes
    2023-02-02T16:43:00 INFO common.c: Attempting to write 100964 (0x18a64) bytes to stm32 address: 134238208 (0x8005000)
    2023-02-02T16:43:05 INFO common.c: Finished erasing 789 pages of 128 (0x80) bytes
    2023-02-02T16:43:05 INFO common.c: Starting Half page flash write for STM32L core id
    2023-02-02T16:43:05 INFO flash_loader.c: Successfully loaded flash loader in sram
    2023-02-02T16:43:17 INFO common.c: Starting verification of write complete
    2023-02-02T16:43:18 INFO common.c: Flash written and verified! jolly good!

    provision for mfg SYSEUI=0002cc0100000A2F SN=00-02-cc-01-00-00-0A-2F
    Command sent: system echo off

    Command sent: system version

    Board: Model 4917
    Platform-Version: 0.21.2
    Arduino-LoRaWAN-Version: 0.9.1
    Arduino-LMIC-Version: 4.1.1
    MCCIADK-Version: 0.2.2
    MCCI-Arduino-BSP-Version: 3.0.5


    Command sent: system configure syseui


    Catena Type: Model 4917
    Platform Version: 0.21.2
    SysEUI: 0002cc010000090e


    Catena Type: Model 4917
    Platform Version: 0.21.2
    SysEUI: 0002cc010000090e



    Initialize serial number
    Command sent: system echo off

    Command sent: system version

    Board: Model 4917
    Platform-Version: 0.21.2
    Arduino-LoRaWAN-Version: 0.9.1
    Arduino-LMIC-Version: 4.1.1
    MCCIADK-Version: 0.2.2
    MCCI-Arduino-BSP-Version: 3.0.5


    Command sent: system configure syseui


    Catena Type: Model 4917
    Platform Version: 0.21.2
    SysEUI: 0002cc010000090e

    Expansion of system configure syseui ${INIT_SYSEUI}: system configure syseui 0002cc0100000a2f
    Command sent: system configure syseui 0002cc0100000a2f

    Command sent: system configure platformguid 53ca094b-b888-465e-aa0e-e3064ec56d21

    Expansion of sn ${INIT_SN}: sn 00-02-cc-01-00-00-0a-2f
    Command sent: sn 00-02-cc-01-00-00-0a-2f



    Set up TTN provisioning
    Port COM8 opened
    >>> system echo off

    <<< OK

    CheckComms
    >>> system version

    <<< Board: Model 4917
    Platform-Version: 0.21.2
    Arduino-LoRaWAN-Version: 0.9.1
    Arduino-LMIC-Version: 4.1.1
    MCCIADK-Version: 0.2.2
    MCCI-Arduino-BSP-Version: 3.0.5
    OK

    >>> system configure syseui

    <<< 00-02-cc-01-00-00-0a-2f
    OK

    Creating TTN end device...
    TTN COMMAND: D:\MCCI-IoT\McGraw\TTNV3\lorawan-stack-cli_3.14.2_windows_amd64\ttn-lw-cli end-devices create mcci-mfg-4917 mfg-0002cc010000090d --join-eui 0000000000000002 --dev-eui 0002CC0100000A2F --lorawan-version 1.0.3 --lorawan-phy-version PHY_V1_0_3_REV_A --frequency-plan-id US_902_928_FSB_2 --with-root-keys
    {
    "ids": {
        "device_id": "mfg-0002cc010000090d",
        "application_ids": {
        "application_id": "mcci-mfg-4917"
        },
        "dev_eui": "0002CC0100000A2F",
        "join_eui": "0000000000000002"
    },
    "created_at": "2023-02-02T11:13:39.964Z",
    "updated_at": "2023-02-02T11:13:40.545046400Z",
    "attributes": {
    },
    "network_server_address": "nam1.cloud.thethings.network",
    "application_server_address": "nam1.cloud.thethings.network",
    "join_server_address": "nam1.cloud.thethings.network",
    "lorawan_version": "MAC_V1_0_3",
    "lorawan_phy_version": "PHY_V1_0_3_REV_A",
    "frequency_plan_id": "US_902_928_FSB_2",
    "supports_join": true,
    "root_keys": {
        "root_key_id": "ttn-lw-cli-generated",
        "app_key": {
        "key": "730B9832062EDA56CF86CFA71D758B45"
        },
        "nwk_key": {
        "key": "2396C96E633535B6550DF809C4C295B2"
        }
    }
    }


    DoScript: mfgtest-provision.cat
    >>> system configure syseui 0002CC0100000A2F

    <<< OK

    >>> system configure platformguid d9d35ffd-1859-4686-900c-dd7fd5941886

    <<< OK

    >>> lorawan configure deveui 0002CC0100000A2F

    <<< OK

    >>> lorawan configure appeui 0000000000000002

    <<< OK

    >>> lorawan configure appkey 730B9832062EDA56CF86CFA71D758B45

    <<< OK

    >>> lorawan configure devaddr 0

    <<< OK

    >>> lorawan configure fcntup 0

    <<< OK

    >>> lorawan configure fcntdown 0

    <<< OK

    >>> lorawan configure appskey 0

    <<< OK

    >>> lorawan configure nwkskey 0

    <<< OK

    >>> lorawan configure join 1

    <<< OK

    >>> system configure operatingflags 1

    <<< OK

    Port COM8 closed
    No errors detected
    run the test on port com8:
    ```

7. Open Tera Term, and open port **com8** (select COM port number to match COM port on your system).

8. Use the reset button on the 4917 to restart it. This tests the reset button. A paperclip is useful.

9. You should see initial print logs.

10. Enter the command `test start` and press enter.

11. Check the RSSI of the join message in the data page for Things Network Console for [mcci-mfg-4917](https://console.thethingsnetwork.org/applications/mcci-mfg-4917/data). Record it.  Expected values close to a gateway are in -50 to -85 range, if antenna is working.

12. Use the `sn` command to check serial number.

    ```console
    sn
    serial-number: 00-02-cc-01-00-00-0a-2f
    Assembly-number: 234001499
    Model: 4917
    ModNumber: 0
    Rev: A
    Dash: 0

    OK
    ```

13. Alt+tab to switch to OTII window, and switch back, so that alt+tab just moves between Tera Term and OTII.

14. Start a sleep test, using `sleep 15`. Switch to OTII, start a recording. Measure the current with OTII software.  Current should be about 562 uA. It will vary based on STLINK state, apparently.

    Record power.  If grossly wrong, stop -- usually this indicates a failure.

15. Return to git bash window.  Press enter twice. Program will finish provisioning for production (if needed) and will download user software (if needed).

16. Disconnect Tera Term from the port if you're forgotten.

    ```console
    run deep sleep test and check current
    Press enter when ready
    Enter y for pass, n for fail: y
    ```

17. Go to https://nam1.cloud.thethings.network/console/applications/mcci-mfg-4917/devices/mfg-0002cc010000090d/data and confirm the signal strength of the join request for the new device.

18. Update the power consumption, signal strength and test result to the spreadsheet. Also save the serial logs and test-proc logs with name serial-log-xxxx and test-proc-log-xxxx (where xxxx is serial number).

19. Remove device, attach serial number sticker, and put in bag.

20. Take out the new board and repeat the test.