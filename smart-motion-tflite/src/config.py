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
        SnapshotUri = None
        SnapshotUsr = None
        SnapshotPwd = None
        DetectList = None

    class _TFLite:
        Instances = int(math.ceil(multiprocessing.cpu_count() / 2))
        Model = "model.tflite"
        Label = "coco_labels.txt"
        Threshold = 0.4
        JpegQuality = 95

    # Declare class member
    smtp : _SMTP = _SMTP()
    email : _Email = _Email()
    cameras = dict()
    tflite = _TFLite()

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

            # Init TFLite
            if ('TFLite' in config) and (config['TFLite'] is not None):
                if "Instances" in config['TFLite']:
                    self.tflite.Instances = int(config['TFLite']['Instances'])
                if "Model" in config['TFLite']:
                    self.tflite.Model = config['TFLite']['Model']
                if "Label" in config['TFLite']:
                    self.tflite.Label = config['TFLite']['Label']
                if "Threshold" in config['TFLite']:
                    self.tflite.Threshold = config['TFLite']['Threshold']
                if "JpegQuality" in config['TFLite']:
                    self.tflite.JpegQuality = int(config['TFLite']['JpegQuality'])

            # Init Cameras
            for camera_name, camera_info in config['Camera'].items():
                camera = Config._Camera()
                camera.Host = camera_info['Host']
                camera.Port = camera_info['Port']
                camera.Username = camera_info['User']
                camera.Password = camera_info['Pass']
                camera.DetectList = camera_info['Detect']
                if camera_info['Snap'] is not None:
                    camera.SnapshotUri = camera_info['Snap']['Uri']
                    if 'User' in camera_info['Snap']:
                        camera.SnapshotUsr = camera_info['Snap']['User']
                    if 'Pass' in camera_info['Snap']:
                        camera.SnapshotPwd = camera_info['Snap']['Pass']
                self.cameras[camera_name] = camera
