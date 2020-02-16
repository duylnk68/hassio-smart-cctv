from datetime import timedelta, datetime
import time
from camera import Camera
from sendmail import Email
from config import Config
from obj_detect import ObjDetect

def main():
    # Load configuration
    config = Config("config.yaml")

    # Create SMTP instance!
    email = Email(config.smtp.Host, config.smtp.Port, config.smtp.UseTLS, config.smtp.Username, config.smtp.Password)
    email.start()

    # Create a list of Camera
    cameras = dict()
    for name, camera in config.cameras.items():
        cameras[name] = Camera(camera.Host, camera.Port, camera.Username, camera.Password)

    # Start all camera
    for camera in cameras.values():
        camera.start()

    # Load Object detect!
    objDetect = ObjDetect("frozen_inference_graph.pb", "frozen_inference_graph.pbtxt")

    # Run detector
    time.sleep(2)
    while True:
        time.sleep(0.1)
        for name, camera in cameras.items():
            if camera.IsMotion is True:
                # Take a image!
                image = camera.CaptureImage()

                # Detect object in this image!
                if image is not None:
                    image = objDetect.Detect(image)

                # Send email!
                if image is not None:
                    subject = config.email.Subject
                    subject = subject.replace("{CAMERA_NAME}", name)
                    subject = subject.replace("{CAMERA_HOST}", camera.Hostname)
                    subject = subject.replace("{EVENT_TYPE}", "Motion Detected")
                    attachments = [ Email.Attachment("capture.jpg", image) ]
                    email.SendMail(config.email.To, subject, "", attachments)
                    print(subject)

if __name__ == "__main__":
    main()

input("Press Enter to exit...")