#NATE DEVINE
import libpyAI as ai
from utils import *

def AI_loop():
  
  chrom = [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0]
  when_to_thrust_speed = convert(chrom[0:4])
  front_wall_distance_thrust = convert(chrom[4:8])*4
  back_wall_distance_thrust = convert(chrom[8:12])*2
  track_wall_distance_thrust = convert(chrom[12:16])*4
  left_wall_angle = convert(chrom[16:20])*3
  right_wall_angle = convert(chrom[20:24])*3
  back_wall_angle = convert(chrom[24:28])*10
  left_90_wall_angle = convert(chrom[28:32])*6
  right_90_wall_angle = convert(chrom[32:36])*6
  left_back_wall_angle = convert(chrom[36:40])*9
  right_back_wall_angle = convert(chrom[44:48])*9
  fuzzy_rate = convert(chrom[48:52])
  fuzzy_rate_1 = convert(chrom[52:56])
  angle_diff_shoot = convert(chrom[56:60])
  shot_alert_distance = convert(chrom[60:64])*6
  
  rate = fuzzy_rate
  rate1 = fuzzy_rate_1
  
  #Release keys
  ai.thrust(0)
  ai.turnLeft(0)
  ai.turnRight(0)

  #Set variables
  heading = int(ai.selfHeadingDeg())
  tracking = int(ai.selfTrackingDeg())
  frontWall = ai.wallFeeler(500,heading)
  leftWall = ai.wallFeeler(500,heading+left_wall_angle)
  rightWall = ai.wallFeeler(500,heading-right_wall_angle)

  left90Wall = ai.wallFeeler(500,heading+left_90_wall_angle)
  right90Wall = ai.wallFeeler(500,heading-right_90_wall_angle)

  leftbackWall = ai.wallFeeler(500,heading+left_back_wall_angle)
  rightbackWall = ai.wallFeeler(500,heading-right_back_wall_angle)

  trackWall = ai.wallFeeler(500,tracking)
  backWall = ai.wallFeeler(500, heading-back_wall_angle)

  #Shooting rule - checks whether theres an enemy to aim at using aimdir, 
  #and then if we're pointing at them within 10 degrees
  #check whether theres a wall between us and the enemy; if there is not then we shoot
  if ai.aimdir(0) >= 0 and -angle_diff_shoot <= ai.angleDiff(heading, ai.aimdir(0)) <= angle_diff_shoot and ai.screenEnemyX(0) >= 0 and ai.screenEnemyY(0) >= 0 and ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) == -1:
    ai.fireShot()
    
  #Turn rules
  #standard check for enemy proximity and wall between us, 
  #and if we're not aiming at them the angle is corrected
  if ai.aimdir(0) >= 0 and ai.angleDiff(heading, ai.aimdir(0)) > 0 and ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) == -1:
    ai.turnLeft(1)
    print("aim turn left")
  elif ai.aimdir(0) >= 0 and ai.angleDiff(heading, ai.aimdir(0)) < 0 and ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) == -1:
    ai.turnRight(1)
    print("aim turn right")
   
  #misc turn rules with fuzzy logic
  elif left90Wall < right90Wall and minmax(10,(rate*ai.selfSpeed()),100):
    ai.turnRight(1)
    print("left90wall")
  elif right90Wall < left90Wall and minmax(10,(rate*ai.selfSpeed()),100):
    ai.turnLeft(1)
    print("right90wall")
  elif leftbackWall < minmax(5,(rate1*ai.selfSpeed()),50):
    ai.turnRight(1)
    print("leftbackwall")
  elif rightbackWall < minmax(5,(rate1*ai.selfSpeed()),50):
    ai.turnLeft(1)
    print("rightbackwall")
    
  #default/base case turn rules
  elif leftWall < rightWall:
    ai.turnRight(1)
  else:
    ai.turnLeft(1)

#Thrust rules
  #rule for speeding up when no wall in front of us
  if ai.selfSpeed() <= when_to_thrust_speed and frontWall >= front_wall_distance_thrust:
    ai.thrust(1)
    print("thrust 1")
   
  #dynamic thrust away from walls
  elif trackWall < track_wall_distance_thrust:
    ai.thrust(1)
    print("thrust 2")
    
  #thrust away from back wall
  elif backWall < back_wall_distance_thrust: 
    ai.thrust(1)
    print("thrust 3")
    
#this block handles dodging enemy bullets
    
  elif ai.shotAlert(0) >= 0 and ai.shotAlert(0) <= shot_alert_distance and ai.shotVelDir(0) != -1 and ai.angleDiff(heading, ai.shotVelDir(0)) > 0:
    print("shotveldir turn left")
    ai.turnLeft(1)
    ai.thrust(1)
    
  elif ai.shotAlert(0) >= 0 and ai.shotAlert(0) <= shot_alert_distance and ai.shotVelDir(0) != -1 and ai.angleDiff(heading, ai.shotVelDir(0)) < 0:
    print("shotveldir turn right")
    ai.turnRight(1)
    ai.thrust(1)

def main():
    ai.start(AI_loop,["-name","dumbo666","-join","localhost"])

if __name__ == '__main__':    
    main()
