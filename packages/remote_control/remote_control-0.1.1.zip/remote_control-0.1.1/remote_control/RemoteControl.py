import serial
import serial.tools.list_ports
from threading import Thread
import logging as log

from pydispatch import dispatcher


class RemoteControlWrapper:
    def __init__(self, verbose=False):
        """
        Tries to connect to comport, otherwise connects to first comport available
        """
        if verbose:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
            log.info("Verbose output.")
        else:
            log.basicConfig(format="%(levelname)s: %(message)s")
            
        self.holdCodes = {}
        self.pressCodes = {}
        self.historyCodes = []

    def connect(self, comport):
        try:
            self.arduinoSerialData = serial.Serial(comport, 9600)
            self.comport = comport
            log.info("Connected to port: " + comport)
        except serial.SerialException:
            raise serial.SerialException("Specified comport is not available")
        self._connectSuccess()

    def connectToFirstComportAvailable(self):
        log.info("Finding all comports available...")

        comportList = list(serial.tools.list_ports.comports())

        if comportList:
            log.info ("Found Ports: " + " ".join([comport.device for comport in comportList]))
            log.info ("Connecting to first comport: " + comportList[0].device)
            try:
                self.arduinoSerialData = serial.Serial(comportList[0].device, 9600)
            except serial.SerialException:
                raise serial.SerialException("Cannot connect to comport: " + comportList[0].device)
            self.comport = comportList[0]
            log.info ("Connected")
        else:
            raise serial.SerialException("There is no comports available!")
        self._connectSuccess()

    def _connectSuccess(self):
        self.listenForEvents()

    def listAvailableComPorts(self):
        comportList = []
        for comport in serial.tools.list_ports.comports():
                comportList.append(comport)
        log.info ("List of comports available: " + ",".join([comport.device for comport in comportList]))

    def onButtonPress(self, hexCode, func):
        dispatcher.connect(func, signal=hexCode, sender=dispatcher.Any)
        if hexCode not in self.pressCodes:
            self.pressCodes[hexCode] = [func]
        else:
            self.pressCodes[hexCode].append(func)

    def onButtonHold(self, hexCode, func):
        dispatcher.connect(func, signal=hexCode, sender=dispatcher.Any)
        if hexCode not in self.holdCodes:
            self.holdCodes[hexCode] = [func]
        else:
            self.holdCodes[hexCode].append(func)

    def listenForEvents(self):
        """
        Starts an infinite loop listening for events from serial
        """
        worker = Thread(target=self._listener)
        worker.start()

    def _listener(self):
        lastData = ""
        log.info("Listening for commands...")
        while(1):
            if(self.arduinoSerialData.in_waiting > 0):
                myData = self.arduinoSerialData.readline()

                dataForSignal = str(myData, "utf-8").strip()
                log.info ("Code received: " + dataForSignal)

                if ("FFFFFFFF" in str(myData)) and (str(lastData, "utf-8").strip() in self.holdCodes):
                    myData = lastData

                self.historyCodes.append(dataForSignal)

                dispatcher.send(signal=dataForSignal, sender=self.comport)

                lastData = myData

    def listHistory(self):
        print(self.historyCodes)

    def _listCommands(self):
        print ("Codes for presses:\n%s" % self.pressCodes)
        print ("Codes for holds:\n%s" % self.holdCodes)

