#NATE DEVINE
import math, random

#weight should be some float such that 0 < weight < 1
def coinflip(weight):
    mycoin = random.random()
    if mycoin < weight:
        return True
    else:
        return False

#subroutine to evaluate fitness of every chromosome in a population
def fitness(Population):
    scores = []
    for chrom in Population:
        Fitness = 0
        total = 0
        #for each bit in the chromosome
        for i in chrom[0]:
            if i == 1:
                total += 1

        Fitness = total/64
        chrom[1] = Fitness
        scores.append(Fitness)

    return scores

#option to initialize a random pop
def initialize_population(size, chrom_len):

    new_population = []
    
    for i in range(size):

        new_chrom =  []
        for x in range(chrom_len):
            new_chrom.append(random.randint(0,1))

        new_population.append([new_chrom, -1])

    return new_population

def top_individuals(Population, Scores):

    #new array to operate on population passed in
    individuals = []
    individuals = Population

    #new array to operate on fitness scores passed in
    scores = []
    scores = Scores

    test_bin = []
    
    #roulette selection implemented here
    for i in range(len(individuals)):
        for x in range(int(round(scores[i]*100,0))):
            test_bin.append(i)
            
    choice1 = random.choice(test_bin)
    test_bin.remove(choice1)
    choice2 = random.choice(test_bin)
    
    #avoid dupes
    while choice2 == choice1:
        test_bin.remove(choice2)
        choice2 = random.choice(test_bin)

    parent1 = individuals[choice1]
    parent2 = individuals[choice2]

    output = [parent1, parent2]

    return output
                           
def crossover(Parents):
    #crossover happens 70% of the time
    gamble = coinflip(.7)
    chiasma = random.randint(0, 63)
    
    #access the first value (0th index) in the tuple
    parent0 = Parents[0][0]
    parent1 = Parents[1][0]

    if gamble:
        a = parent0[chiasma:]
        b = parent0[:chiasma]

        c = parent1[chiasma:]
        d = parent1[:chiasma]
        
        new1 = a + d
        new2 = b + c
    else:
        new1 = parent0
        new2 = parent1

    #mutation happens here
    for bit in new1:
        if coinflip(.08):
            if bit == 0:
                bit = 1
            else:
                bit = 0
    for bit in new2:
        if coinflip(.08):
            if bit == 0:
                bit = 1
            else:
                bit = 0
    
    output = [[new1,-1], [new2,-1]]
    myfitness = fitness(output)

    guy1 = [new1,myfitness[0]]
    guy2 = [new2,myfitness[1]]

    output = [guy1, guy2]
    return output

#scores should be a list
def mean_fitness(Scores):
    total = 0
    mean = 0

    for i in Scores:
        total += Scores[int(i)]
        
    mean = total/len(Scores)

    return mean

def main():

    generation = 0
    current_fitness = 0.0
    crossover_prob = .7
    mutation_prob = .001

    population_size = 100
    chromosome_length = 64

    population = []
    new_population = []
    fitness_scores = []

    best_individual = []
    best_fitness = 0
    avg_fitness = 0

    newfile = open("GA_output.txt","w+")

    #option to use custom initial pop
    myinput = input("Use custom initial pop? Answer yes or no. ")
    while myinput.lower() != "yes" and myinput.lower() != "no":
        myinput = input("Use custom initial pop? Answer yes or no.")
    if myinput.lower() == "yes":
        infilename = input("What is the name of the population file? ")
        infile = open(infilename,"r", encoding = "utf-8")
        infileread = infile.read()
        population = infileread
    else:
        population = initialize_population(population_size, chromosome_length)

    #save initial pop here
    initialpopfile = open("initialpopfile","w+")

    for i in population:
        initialpopfile.write(str(i))
        initialpopfile.write("\n")
    initialpopfile.close()

    
    #loops until 5000 gens or an individual learns all 1's
    while(generation < 5000 and float(current_fitness) != 1.0):
        
        fitness_scores = fitness(population)

        chromosome_pair = top_individuals(population, fitness_scores)
        new_population = []
        new_population += crossover(chromosome_pair)

        #fills the population until desired size is reached
        while(len(new_population) < population_size):
            new_population += crossover(chromosome_pair)

        population = []
        population = new_population

        fitness_scores = fitness(population)
        
        current_fitness = max(fitness_scores)
        best_individual_index = fitness_scores.index(current_fitness)
        best_individual = population[best_individual_index][0]
        
        generation += 1

        #writes relevant info to file every 10 gens
        if generation%10 == 0:
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
            newfile.write("Average fitness: ")
            newfile.write("\n")
            newfile.write(str(mean_fitness(fitness_scores)))
            newfile.write("\n")
            #newfile.close()

    ###

    #writes to file important info about final gen
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
    newfile.write("Average fitness: ")
    newfile.write("\n")
    newfile.write(str(mean_fitness(fitness_scores)))
    newfile.write("\n")
    newfile.close()

    ###

    #writes to file each individual from the final pop
    popfile = open("GA_final_population.txt","w+")
    for i in population:
        popfile.write(str(i))
        popfile.write("\n")
    #popfile.write(str(population))
    popfile.close()
    
    ###
    print("Generation: ", generation)
    print("Current fitness: ",  current_fitness)
    print()
    print()
    
if __name__ == '__main__':    
    main()
    




    
