#Adapted from a script by www.stuffaboutcode.com
#Raspberry Pi, Minecraft - hide and seek

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import sleep from the time library
from time import sleep
#import random module to create random number
import random
#import math module to use square root function
import math
#import the GPIO Zero library, specifically LED for the light
from gpiozero import LED

led = LED(17)

#function to round players float position to integer position
def roundVec3(vec3):
    return minecraft.Vec3(int(vec3.x), int(vec3.y), int(vec3.z))

def distanceBetweenPoints(point1, point2):
    xd = point2.x - point1.x
    yd = point2.y - point1.y
    zd = point2.z - point1.z
    return math.sqrt((xd*xd) + (yd*yd) + (zd*zd))
  
if __name__ == "__main__":

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()

    #Post a message to the minecraft chat window
    mc.postToChat("Welcome to Minecraft Hide & Seek")

    sleep(2)
  
    #Find the players position
    playerPos = mc.player.getPos()
  
    #Create random position within 50 blocks from the player, our hidden block will go there
    randomBlockPos = roundVec3(playerPos)
    randomBlockPos.x = random.randrange(randomBlockPos.x - 50, randomBlockPos.x + 50)
    randomBlockPos.y = random.randrange(randomBlockPos.y - 5, randomBlockPos.y + 5)
    randomBlockPos.z = random.randrange(randomBlockPos.z - 50, randomBlockPos.z + 50)
    print randomBlockPos
  
    #Create hidden diamond block
    mc.setBlock(randomBlockPos.x, randomBlockPos.y, randomBlockPos.z, block.LAPIS_LAZULI_BLOCK.id)
    mc.postToChat("Find the hidden block!")
  
    #Start hide and seek
    seeking = True
    lastPlayerPos = playerPos
    lastDistanceFromBlock = distanceBetweenPoints(randomBlockPos, lastPlayerPos)
    position = 5
    while (seeking == True):
        #Get players position
        playerPos = mc.player.getPos()
        #Has the player moved
        if lastPlayerPos != playerPos:
            distanceFromBlock = distanceBetweenPoints(randomBlockPos, playerPos)
            
            if distanceFromBlock < 2:
                #found it!
                seeking = False
            else:
                if distanceFromBlock < 5 and position != 4:
                    led.on()
                    position = 4
                if 4 < distanceFromBlock < 11 and position != 3:
                    led.blink(0.3,0.3)
                    position = 3
                if 10 < distanceFromBlock < 26 and position != 2:
                    led.blink(0.6,0.5)
                    position = 2
                if 25 < distanceFromBlock < 41 and position != 1:
                    led.blink(1,0.5)
                    position = 1
                if distanceFromBlock > 40 and distanceFromBlock < lastDistanceFromBlock:
                    led.blink()
                if distanceFromBlock > 40 and distanceFromBlock > lastDistanceFromBlock:
                    led.off()
          
            lastDistanceFromBlock = distanceFromBlock
          
        sleep(2)
    mc.postToChat("You found the block!")
