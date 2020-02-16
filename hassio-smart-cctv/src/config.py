import yaml

class Config:
    class _SMTP:
        Host = None
        Port = None
        Username = None
        Password = None
        UseTLS = False

    class _Email:
        To = None
        Subject = None

    class _Camera:
        Host = None
        Port = None
        Username = None
        Password = None

    # Declare class member
    smtp : _SMTP = _SMTP()
    email : _Email = _Email()
    cameras = dict()

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
            self.email.Subject = config['Email']['Subject']

            # Init Cameras
            for camera_name, camera_info in config['Camera'].items():
                camera = Config._Camera()
                camera.Host = camera_info['Host']
                camera.Port = camera_info['Port']
                camera.Username = camera_info['User']
                camera.Password = camera_info['Pass']
                self.cameras[camera_name] = camera
