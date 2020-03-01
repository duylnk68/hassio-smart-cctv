import yaml
import math
import multiprocessing

class Config:
    class _SMTP:
        Host = None
        Port = None
        Username = None
        Password = None
        UseTLS = False

    class _Email:
        To = None
        Subject = "[None]"
        Body = "(null)"

    class _Camera:
        Host = None
        Port = None
        Username = None
        Password = None
        DetectList = None

    class _OpenCV:
        Instances = int(math.ceil(multiprocessing.cpu_count() / 2))
        PB = "frozen_inference_graph.pb"
        PBTXT = "frozen_inference_graph.pbtxt"
        Label = "coco_labels.txt"
        Threshold = 0.5
        JpegQuality = 95

    # Declare class member
    smtp : _SMTP = _SMTP()
    email : _Email = _Email()
    cameras = dict()
    opencv = _OpenCV()

    # Constructor
    def __init__(self, config_path):
        with open(config_path, 'r') as stream:
            # Load yaml config file
            config = yaml.safe_load(stream)

            # Init SMTP instance!
            smtp_config = config['Email']['SMTP']
            self.smtp.Host = smtp_config['Host']
            self.smtp.Port = smtp_config['Port']
            self.smtp.Username = smtp_config['User']
            self.smtp.Password = smtp_config['Pass']
            self.smtp.UseTLS = smtp_config['TLS']

            # Init Email instance!
            self.email.To = config['Email']['To']
            if 'Subject' in config['Email']:
                self.email.Subject = config['Email']['Subject']
            if 'Body' in config['Email']:
                self.email.Body = config['Email']['Body']

            # Init OpenCV
            if ('OpenCV' in config) and (config['OpenCV'] is not None):
                if "Instances" in config['OpenCV']:
                    self.opencv.Instances = int(config['OpenCV']['Instances'])
                if "PB" in config['OpenCV']:
                    self.opencv.PB = config['OpenCV']['PB']
                if "PBTXT" in config['OpenCV']:
                    self.opencv.PBTXT = config['OpenCV']['PBTXT']
                if "Label" in config['OpenCV']:
                    self.opencv.Label = config['OpenCV']['Label']
                if "Threshold" in config['OpenCV']:
                    self.opencv.Threshold = config['OpenCV']['Threshold']
                if "JpegQuality" in config['OpenCV']:
                    self.opencv.JpegQuality = int(config['OpenCV']['JpegQuality'])

            # Init Cameras
            for camera_name, camera_info in config['Camera'].items():
                camera = Config._Camera()
                camera.Host = camera_info['Host']
                camera.Port = camera_info['Port']
                camera.Username = camera_info['User']
                camera.Password = camera_info['Pass']
                camera.DetectList = camera_info['Detect']
                self.cameras[camera_name] = camera
