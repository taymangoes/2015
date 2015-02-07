import wpilib
from wpilib.command import Subsystem
import math

class Drive(Subsystem): 
    '''
        The drive object is used to move our robot with a
        mecanum drive. It uses a gyro to help achieve a more
        precise angle measure
    '''
    
    kP_rotate = .5
    kI_rotate = .01
    kD_rotate = .0
    
    
    def __init__(self, lf_motor, lb_motor, rf_motor, rb_motor, gyro, accel):
        '''
            constructor for the drive object. Should take in
            gyro and a mecanum drive.
        '''
        self.robot_drive = wpilib.RobotDrive(lf_motor, lb_motor, rf_motor, rb_motor)
        
        self.lf_motor = lf_motor
        self.lb_motor = lb_motor
        self.rf_motor = rf_motor
        self.rb_motor = rb_motor
        self.gyro = gyro
        self.accel = accel 
        
        
        self.gyro_pid = wpilib.PIDController(
             Drive.kP_rotate, 
             Drive.kI_rotate, 
             Drive.kD_rotate, 
             self.pid_source, 
             self.pid_output)
        
        
    def pid_source(self):
        return self.get_angle_difference(self.gyro_pid.getSetpoint(), self.gyro.getAngle())
    
    def pid_output(self, output):
        self.robot_move(0, 0, output, 0)
    
    
    def robot_move(self, x, y, z, angle):
        '''
            this function is used to control the
            power/speed/torque of our robot/drive/motors
        '''
        self.robot_drive.mecanumDrive_Cartesian(x, y, z, angle)
        
    def robot_rotate(self, angle):
        '''
            rotate to a certain angle within a specified set
            of parameters
        '''
        
        angle_difference = self.get_angle_difference(angle, self.gyro.getAngle())
        z = 0
        if angle_difference < -5:
            z = -.5
        elif angle_difference > 5:
            z = .5
        
        self.robot_move(0, 0, z, angle)
        
    def get_angle_difference(self, target, source):
        # target> angle you want; source> the gyro angle
        return (target - source + math.pi) % (math.pi * 2) - math.pi
    
    def log(self):
        '''
            log records various things about the robot
        '''
        wpilib.SmartDashboard.putData("angle", self.gyro.getAngle())
        wpilib.SmartDashboard.putData("acceleration_x", self.accel.getX())
        wpilib.SmartDashboard.putData("acceleration_y", self.accel.getY())
        wpilib.SmartDashboard.putData("acceleration_z", self.accel.getZ())
    