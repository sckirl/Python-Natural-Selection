from random import randint, randrange, choice
import pygame
import sys
import matplotlib.pyplot as plt
pygame.init()

WIN = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Natural Selection")

CLOCK = pygame.time.Clock()

class Individual:
    # individual class, with fithess and position
    def __init__(self, 
                speed=randrange(5, 20), 
                stamina=randrange(100, 1000), 
                senseArea=randrange(20, 50)):

        self.fitness = {"speed" : speed,
                        "stamina" : stamina,
                        "senseArea" : senseArea,
                        }

        self.stamina = stamina
        self.age = 1

        self.sprite = pygame.sprite.Sprite()
        self.sprite.rect = pygame.Rect(randrange(0, 500), randrange(0, 500), 
                                        self.fitness["senseArea"], self.fitness["senseArea"])

    def move(self):
        # move the character to random places at its speed
        SPEED = self.fitness["speed"]
        # change the position with speed, at random direction
        temp = [self.sprite.rect.left, self.sprite.rect.top]
        temp[randint(0, 1)] += SPEED * randint(-1, 1)

        if self.stamina > SPEED/10:
            if (-SPEED < temp[0] and temp[0] < 500 + SPEED) and \
                (-SPEED < temp[1] and temp[1] < 500 + SPEED):
                    # make sure the movement isn't outside of the screen
                    self.sprite.rect.left, self.sprite.rect.top = temp
                    self.stamina -= SPEED/10

            else: 
                try: self.move()
                except: pass

class Simulation:
    def __init__(self, populationLimit=1000):
        self.POPULATIONLIMIT = populationLimit
        self.population = set()
        self.survivors = set()
        self.populationSprites = []

        self.food = pygame.sprite.Group()
        self.lastWeek = -1

    def addPopulation(self, individual: Individual):
        self.population.add(individual)

    def spawnFood(self):
        self.food = pygame.sprite.Group()
        
        for _ in range(len(self.population)):
            foodSprite = pygame.sprite.Sprite()
            foodSprite.rect = pygame.Rect(randrange(100, 400), randrange(100, 400), 0, 0)

            self.food.add(foodSprite)
    
    def getFood(self): # credit: https://stackoverflow.com/a/65064907
        # get collision of food from sense Area
        for indv in self.population:
            collide = pygame.sprite.spritecollide(indv.sprite, self.food, 
                                                  True, pygame.sprite.collide_circle)
            if collide: 
                # eat the food, survive for another week
                self.survivors.add(indv)
    
    def breed(self, indv, chance=70):
        # search other individual to breed, with the same 
        # senseArea for finding food, for simplicity. 
        collide = pygame.sprite.spritecollide(indv.sprite, list(self.populationSprites.keys()), 
                                              False, pygame.sprite.collide_circle)

        for pair in collide:
            firstParent = indv
            secondParent = self.populationSprites[pair]

            # when finding other individual in senseArea, they might
            # breed on chance %/chance percent.
            # make sure the individual doesn't breed with itself
            if randrange(0, 100) <= chance and firstParent != secondParent \
               and len(self.population) < self.POPULATIONLIMIT:

                offspring = Individual()
                for point in offspring.fitness.keys():
                    # on each point of fitness (speed, stamina, etc), the offspring will 
                    # develop its points from its parents. Offspring can get either of its parents' fitness
                    offspring.fitness[point] = choice([firstParent, secondParent]).fitness[point]

                    # random occurances happen so the offspring can be better, the same, or worse
                    # than its parents
                    offspring.fitness[point] += randrange(0, 10) * randint(-1, 1)
                    offspring.fitness[point] = offspring.fitness[point] if offspring.fitness[point] > 0 else 0 
                
                # the position will be the average/in the middle of its parents' position
                position = [(firstParent.sprite.rect.left + secondParent.sprite.rect.left) // 2,
                            (firstParent.sprite.rect.top + secondParent.sprite.rect.top) // 2]
            
                offspring.sprite.rect = pygame.Rect(position[0], position[1],
                                        offspring.fitness["senseArea"], offspring.fitness["senseArea"])
                
                self.addPopulation(offspring)

    def checkWeek(self, period=5):
        # end the week after a period of time
        ticks = pygame.time.get_ticks() // 1000
        if ticks % period == 0 and ticks != self.lastWeek:
            self.lastWeek = ticks

            # only survivors remain on the field for the next week
            self.population = self.survivors.copy()
            self.survivors.clear()

            self.populationSprites = {indv.sprite : indv for indv in self.population}
            # breed and reset population's stamina
            for indv in self.population.copy():
                self.breed(indv, chance=100)
                indv.stamina = indv.fitness["stamina"]
                indv.age += 1
            
            self.getGraph(yValue="population", period=period)
            self.spawnFood()
        
    def getGraph(self, yValue="population", xValue="period", period=5):
        data = {"population" : len(self.population),
                "period" : self.lastWeek}

        for indv in self.population:
            for point in indv.fitness:
                data.setdefault(point, indv.fitness[point])
                data.update({point : data[point] + indv.fitness[point]})
            data.setdefault("age", indv.age)
            data.update({"age" : data["age"] + indv.age})

        for point in data:
            if point not in list(self.population)[0].fitness.keys() and point != "age": continue
            data.update({point : data[point] / len(self.population)})
        
        plt.title("{} to {}".format(yValue, xValue))
        plt.scatter(data[xValue], data[yValue])
        
        plt.xlabel(xValue, fontsize=16)
        plt.ylabel(yValue, fontsize=16)

        plt.pause(0.05)

    def draw(self):
        # redraw each object into display 
        WIN.fill((0, 0, 0))

        for food in self.food:
            pygame.draw.circle(WIN, [255, 0, 0], (food.rect.left, food.rect.top), 2)

        for indv in self.population:
            pygame.draw.circle(WIN, [255, 255, 255], (indv.sprite.rect.left, indv.sprite.rect.top), 5)
            pygame.draw.circle(WIN, [100, 100, 100], (indv.sprite.rect.left, indv.sprite.rect.top), 
                                                indv.fitness["senseArea"], 2)

        pygame.display.update()

def main():
    NaturalSelection = Simulation(populationLimit=3000)
    for _ in range(100):
        indv = Individual()
        NaturalSelection.addPopulation(indv)
    NaturalSelection.survivors = set(NaturalSelection.population)

    while True:
        CLOCK.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        for indv in NaturalSelection.population:
            indv.move()
        
        NaturalSelection.checkWeek(period=1)
        NaturalSelection.getFood()
        NaturalSelection.draw()

if __name__ == "__main__":
    main()