from picameracv.cameramodule import camera

modes = ['single_camera_process', 'multi']
object_types = ['face', 'eye', 'sign']
camera_types = ['camera', 'web_camera', 'pi_camera']

class MainLoopClass:
    @staticmethod
    def dummyProc():
        import time
        time.sleep(2)
        print 'Dummy proc worked'
        exit(0)

    def startMultipleProcs(self, procList):
        for i in range(len(procList)):
            currentProc = procList[i]
            if currentProc is 'dummy':
                self.dummyProc()
            print str(currentProc)

    def __init__(self, mode=modes[0], cam_type=camera_types[0], object_type='face',
                 procs=['dummy']):
        if (mode not in modes) | (object_type not in object_types):
            raise Exception("Hey, human, no such animal found")

        if mode is modes[0]:
            camClass = camera.CameraClass(cam_type, object_type, 20)
            camClass.launchCameraDetection()
            exit(0)
        elif mode is modes[1]:
            self.startMultipleProcs(procList=procs)


    # import time
    # from multiprocessing import Process
    # from client import client
    # clientProcess = client.Client.createAndStartClient()
    # # execfile("..\server\server.py")
    # if client is None:
    #     print "client fucked up"
    # print 'OK, man'
    # if clientProcess.is_alive():
    #     print 'alive'
    # else:
    #     print 'dead'
    #
    #
    # cameraProcess = Process(target=camera.CameraClass.launchCameraDetection(), )
    # cameraProcess.start()
    # while True:
    #     time.sleep(1)
    #     if clientProcess.is_alive() & cameraProcess.is_alive():
    #         print 'OK'
    #     else:
    #         exit(0)
