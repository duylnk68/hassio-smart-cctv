import multiprocessing
import math
import os.path
from datetime import timedelta, datetime
import time
from zeep_patch import ZeepPatch
from camera import Camera
from sendmail import Email
from config import Config
from obj_detect_pool import ObjDetectPool

def main():
    # Patch Zeep
    ZeepPatch().Patch()

    # Load configuration
    config = None
    if os.path.isfile('config.yaml'):
        config = Config('config.yaml')
    else:
        config = Config('/share/hassio-smart-cctv/config.yaml')

    # Create SMTP instance!
    email = Email(config.smtp.Host, config.smtp.Port, config.smtp.UseTLS, config.smtp.Username, config.smtp.Password)
    email.start()

    # Create a list of Camera
    cameras = dict()
    for name, camera in config.cameras.items():
        if camera.DetectList is None:
            continue
        cameras[name] = Camera(camera.Host, camera.Port, camera.Username, camera.Password, camera.DetectList)

    # Start all camera
    for camera in cameras.values():
        camera.start()

    # Load Object detect!
    objDetectPool = ObjDetectPool(int(math.ceil(multiprocessing.cpu_count() / 2)), 
                    "frozen_inference_graph.pb",
                    "frozen_inference_graph.pbtxt")

    # Wait a little bit!
    time.sleep(10)

    # Email start status
    attachments = []
    for name, camera in cameras.items():
        # Wait for ready!
        while not camera.IsReady:
            time.sleep(0.01)

        # Take a image!
        image = camera.CaptureImage()

        # Check if succeed!
        if image is None:
            continue

        # Add to attachment!
        attachments.append(Email.Attachment("%s.jpg" % name, image))

    # Mail
    subject = config.email.Subject
    subject = subject.replace("{CAMERA_NAME}", "ALL")
    subject = subject.replace("{CAMERA_HOST}", "NONE")
    subject = subject.replace("{EVENT_TYPE}", "System Start")
    email.SendMail(config.email.To, subject, config.email.Body, attachments)
    
    # Delete some variables for safety!
    del attachments
    del subject

    # Run detector
    counter = 0
    while True:
        time.sleep(1)
        for name, camera in cameras.items():
            if camera.IsMotion is True:
                # Take a image!
                image = camera.CaptureImage()

                # Detect object in this image!
                if image is not None:
                    objDetectPool.Detect(name, image, camera.Tag)

        # Check result each 5s
        if counter >= 5:
            for cam_name, cam_imgs in objDetectPool.GetResults().items():
                attachments = []
                for cam_img in cam_imgs:
                    attachments.append(Email.Attachment("%s_%d.jpg" % (cam_name, len(attachments)), cam_img))
                if len(attachments) > 0:
                    subject = config.email.Subject
                    subject = subject.replace("{CAMERA_NAME}", cam_name)
                    if cam_name in cameras:
                        subject = subject.replace("{CAMERA_HOST}", cameras[cam_name].Hostname)
                    subject = subject.replace("{EVENT_TYPE}", "Motion Detected")
                    email.SendMail(config.email.To, subject, config.email.Body, attachments)
                    print(subject)
        else:
            counter = counter + 1

if __name__ == "__main__":
    main()

input("Press Enter to exit...")