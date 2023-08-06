#!python
import ThetaOSC
import time


def TakeSeries(interval=10,  numshot=3):
    dev=ThetaOSC.ThetaS()
    dev.connect()
    try:
        dev.StopCapture()
    except:
        pass
    dev.SetStillMode()
    dev.SetTimelapseInterval(interval)
    dev.SetTimelapseNumber(numshot)
    dev.StartCapture()
    time.sleep(interval*numshot+5)
    try:
        dev.StopCapture()
    except:
        pass

def main():
    
    if len(sys.argv) != 2:
        #print >>sys.stderr, "Syntax: TimelapseCapture <interval in seconds>"
        sys.exit(1)
    interval = int(sys.argv[1])

