#!/usr/bin/env python3

import traceback
import struct

import src.comp_run as cr
import src.pi_run as pi
import src.helpers as h

def runComputer(writeImagePath=None, rot=False):
    known = cr.getKnownFaces()
    while True:
        conn, _ = cr.getConnection()

        while True:
            send = recv = None
            try:
                send, recv = cr.getWriteSocs(conn)
                h.closeSocket(conn, recv, send)

                images = cr.getImages(connect=recv)

                # For our orientation during testing, images need to be corrected
                # The face_recognition library can't see faces that aren't upright
                if rot:
                    images = cr.rotList(images)

                if not writeImagePath is None:
                    cr.writeImages(images, writeImagePath)
                
                if len(images):
                    res = cr.getResults(images, known)

                    cr.sendResults(res, connect=send)
            except Exception:
                traceback.print_exc()
                print("Breaking")
                break
            
            if not send is None or not recv is None:
                cr.closeWriteFiles(send, recv)
        
        cr.closeConnection(conn)
    
def runPi(ipaddress='10.3.141.198', port=8000):
    print("Pi Pie Phi guy running")

    command = ''
    while True:
        conn = pi.getConnection()
        while command != 'quit':
            send = recv = None
            try:
                send, recv = pi.getWriteSocs(conn)
                pi.sendFrames(connect=send)

                pi.readResults(connect=recv)
            except Exception:
                traceback.print_exc()
                print("Breaking")
                break
            
            if not send is None or not recv is None:
                cr.closeWriteFiles(send, recv)
        pi.closeConnection(conn)

if __name__ == "__main__":
    OnPi = compsystem.nodename == 'raspberrypi'
    if OnPi:
        #runPi(ipaddress='10.3.141.198')
        runPi(ipaddress='10.186.129.210')
    else:
        runComputer(rot=True)
