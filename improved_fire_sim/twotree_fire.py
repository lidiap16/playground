import sys, random, os, time
import pygame
import matplotlib.pyplot as plt

SC_WIDTH, SC_HEIGHT = 820, 820
MAP_WIDTH, MAP_HEIGHT = 19, 19
TILE_SIZE = 55
INITIAL_TREE_DENSITY = 0.99
GROW_CHANCE = 0.0
FIRE_CHANCE = 0.0
FIRE_SPREAD_CHANCE = 0.8
PAUSE_LENGTH = 0.6
SIM_LENGTH = 25


pygame.init()
screen = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

# Load images
TREE_IMG = pygame.image.load(os.path.join("skins", "tree.png")).convert_alpha()
TREE1_IMG = pygame.image.load(os.path.join("skins", "tree1.png")).convert_alpha()
FIRE_IMG = pygame.image.load(os.path.join("skins", "fire.png")).convert_alpha()

trees = []
fires = []

def main():
    forest = createNewForest()

    for _ in range(SIM_LENGTH):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Count trees
        tree_count = sum(row.count("T") for row in forest)
        tree1_count = sum(row.count("T1") for row in forest)
        tree_land_percentage = ((tree_count + tree1_count) / (MAP_HEIGHT * MAP_WIDTH)) * 100
        trees.append(tree_land_percentage)

        # Count fire
        fire_count = sum(row.count("F") for row in forest)
        fire_land_percentage = (fire_count / (MAP_HEIGHT * MAP_WIDTH)) * 100
        fires.append(fire_land_percentage)

        # Prepare next forest state
        next_forest = [["Empty" for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

        screen.fill((137, 234, 123))  # light green background
        displayForest(forest)

        # Build next forest
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if next_forest[y][x] != "Empty":
                    continue

                if (forest[y][x] == " ") and (random.random() <= GROW_CHANCE):
                    # New tree growth - chance of being normal or special
                    if random.random() < 0.7:
                        next_forest[y][x] = "T"
                    else:
                        next_forest[y][x] = "T1"
# 
#                 elif (forest[y][x] == "T") and (random.random() <= FIRE_CHANCE):
#                   
#                     next_forest[y][x] = "F"
# 
#                 elif (forest[y][x] == "T1") and (random.random() <= FIRE_CHANCE * 0.5):
#                  #harder to ignite tree
#                     next_forest[y][x] = "F"

                elif forest[y][x] == "F":
                    # Spread fire to neighbours
                    for ix in range(-1, 2):
                        for iy in range(-1, 2):
                            if (x + ix) >= 0 and (y + iy) >= 0:
                                if (x + ix) <= (MAP_WIDTH - 1) and (y + iy) <= (MAP_HEIGHT - 1):
                                    if forest[y + iy][x + ix] == "T":
                                        if random.random() <= FIRE_SPREAD_CHANCE:
                                            next_forest[y + iy][x + ix] = "F"
                                    elif forest[y + iy][x + ix] == "T1":
                                        if random.random() <= FIRE_SPREAD_CHANCE * 0.3:  # harder to spread to better trees
                                            next_forest[y + iy][x + ix] = "F"
                    # Fire burns out
                    next_forest[y][x] = " "

                else:
                    next_forest[y][x] = forest[y][x]

        forest = next_forest

        time.sleep(PAUSE_LENGTH) #pause for set time
        pygame.display.update()

    # Plot results on graph
    fig, ax = plt.subplots()
    ax.plot(trees, color='green', label='Trees (T+T1)')
    ax.plot(fires, color='red', label='Fire')
    ax.legend(loc='upper right')
    ax.set_xlabel("Time")
    ax.set_ylabel("Land Occupied (%)")
    plt.show()


# create a Random Map of Trees
def createNewForest():
    map = []
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            if random.random() <= INITIAL_TREE_DENSITY:
                row.append("T1" if random.random() < 0.5 else "T")
            else:
                row.append('F')
            
        map.append(row)
    return map

#sub in img, the forest
def displayForest(forest):
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if forest[y][x] == "T":
                screen.blit(TREE_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif forest[y][x] == "T1":
                screen.blit(TREE1_IMG, (x * TILE_SIZE, y * TILE_SIZE))
            elif forest[y][x] == "F":
                screen.blit(FIRE_IMG, (x * TILE_SIZE, y * TILE_SIZE))


if __name__ == '__main__':
    main()


# if __name__ == '__main__':

#     main(fire_spread_chance=0.3, grow_chance=0.9, fire_chance=0.02)
