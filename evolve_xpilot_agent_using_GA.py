#NATE DEVINE

import libpyAI as ai
import math, random
from genetic_algorithm import *
from utils import *


def AI_loop():
    global frames, frameHistory, generation, current_chrom, population, scores, current_score
    print("frame", frames)
  
  #rules

    chrom = population[current_chrom][0]
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

    #Shooting rules
    if ai.aimdir(0) >= 0 and -angle_diff_shoot <= ai.angleDiff(heading, ai.aimdir(0)) <= angle_diff_shoot and ai.screenEnemyX(0) >= 0 and ai.screenEnemyY(0) >= 0 and ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) == -1:
        ai.fireShot()

    #Turn rules
    if ai.aimdir(0) >= 0 and ai.angleDiff(heading, ai.aimdir(0)) > 0 and ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) == -1:
        ai.turnLeft(1)
        #print("aim turn left")
    elif ai.aimdir(0) >= 0 and ai.angleDiff(heading, ai.aimdir(0)) < 0 and ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) == -1:
        ai.turnRight(1)
        #print("aim turn right")
    elif left90Wall < right90Wall and minmax(10,(rate*ai.selfSpeed()),100):
        ai.turnRight(1)
        #print("left90wall")
    elif right90Wall < left90Wall and minmax(10,(rate*ai.selfSpeed()),100):
        ai.turnLeft(1)
        #print("right90wall")
    elif leftbackWall < minmax(5,(rate1*ai.selfSpeed()),50):
        ai.turnRight(1)
        #print("leftbackwall")
    elif rightbackWall < minmax(5,(rate1*ai.selfSpeed()),50):
        ai.turnLeft(1)
        #print("rightbackwall")
    #base case turn rules
    elif leftWall < rightWall:
        ai.turnRight(1)
    else:
        ai.turnLeft(1)

    #Thrust rules
    if ai.selfSpeed() <= when_to_thrust_speed and frontWall >= front_wall_distance_thrust:
        ai.thrust(1)
        #print("thrust 1")

    #dynamic thrust away from walls
    elif trackWall < track_wall_distance_thrust:
        ai.thrust(1)
        #print("thrust 2")

    #thrust away from back wall
    elif backWall < back_wall_distance_thrust:
        ai.thrust(1)
        #print("thrust 3")

    #Shot avoidance
    elif ai.shotAlert(0) >= 0 and ai.shotAlert(0) <= shot_alert_distance and ai.shotVelDir(0) != -1 and ai.angleDiff(heading, ai.shotVelDir(0)) > 0:
        #print("shotveldir turn left")
        ai.turnLeft(1)
        ai.thrust(1)

    elif ai.shotAlert(0) >= 0 and ai.shotAlert(0) <= shot_alert_distance and ai.shotVelDir(0) != -1 and ai.angleDiff(heading, ai.shotVelDir(0)) < 0:
        #print("shotveldir turn right")
        ai.turnRight(1)
        ai.thrust(1)

    #tracks frames alive
    if ai.selfAlive() == 1:
        frames += 1

    elif ai.selfAlive() == 0 and frames == 0:
        pass

    else:
    #adds every fitness to a list to avoid the issue of xpilot score never resetting
        scores.append(ai.selfScore())
        #base case
        if len(scores) < 2:
            current_score = scores[-1]
        else:
            current_score = scores[-1] - scores[-2]
        if current_score <= 0:
            current_score = 2
        
        population[current_chrom][1] = (frames**2)*current_score
    
        print("fitness: ", population[current_chrom][1])
    
        current_chrom += 1
        print("current_chrom is: ", current_chrom)
        
        if current_chrom >= len(population):
            current_chrom = 0
            print("current_chrom is: ", current_chrom)
        
            generation += 1
        
            fitness_scores = fitness(population)
        
            #writes highest fitness agent to file
            if generation%5 == 0:
                print("first write")
                
                current_fitness = max(fitness_scores)
                best_individual_index = fitness_scores.index(current_fitness)
                best_individual = population[best_individual_index][0]

                newfile = open("GA_output.txt","a+")
                newfile.write("Generation: ")
                newfile.write("\n")
                newfile.write(str(generation))
                newfile.write("\n")
                newfile.write("Best individual: ")
                newfile.write("\n")
                newfile.write(str(best_individual))
                newfile.write("\n")
                newfile.write("Best fitness: ")
                newfile.write("\n")
                newfile.write(str(current_fitness))
                newfile.write("\n")
                newfile.close()
            
            chrom_pair = top_individuals(population, fitness_scores)
            new_pop = []
            new_pop += crossover(chrom_pair)
            
            while (len(new_pop) < population_size):
                new_pop += crossover(chrom_pair)
            
            population = []
            population = new_pop
            
            #writes population to file
            if generation%10 == 0:
                print("second write")
                
                popfile = open("GA_pop.txt","a+")
                popfile.write("Generation: ")
                popfile.write("\n")
                popfile.write(str(generation))
                popfile.write("\n")
                
                for i in population:
                    popfile.write(str(i))
                    popfile.write("\n")
                    popfile.write("\n")

                popfile.close()
            
        frames = 0

def main():

    frames = 0
    generation = 0
    current_fitness = 0.0
    crossover_prob = .7
    mutation_prob = .001
    population_size = 25
    chromosome_length = 64
    current_chrom = 0
    current_score = 0
    best_fitness = 0
    avg_fitness = 0
    frameHistory = []
    new_population = []
    fitness_scores = []
    scores = []
    best_individual = []
    population = []
    population = initialize_population(population_size, chromosome_length)

    ai.start(AI_loop,["-name","dumbo_in_progress","-join","localhost"])
    
if __name__ == '__main__':    
    main()
