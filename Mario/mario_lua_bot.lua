-- A Lua program which automates Mario's movement in Super Mario Bros. for the NES.
-- Occasionally, the user has to jump over an enemy, but Mario can survive for a decent time interval.
-- assembly code allowing for Lua scripting found here: https://gist.github.com/1wErt3r/4048722

-- instantiate Lua inputs to be read by FCEUX, the NES emulator
local tableGame = {}
JoypadA = {A=true}
JoypadLeft = {left=true}
JoypadRight = {right=true}
JoypadStart = {start=true}

-- set up functions to automate Mario's movement

function PressStart()
  joypad.set(1, JoypadStart)
end

function PressA()
  joypad.set(1, JoypadA)
end

function JumpObstacle()
  --if Mario runs into an obstacle, the algorithm can detect it if his speed is close to zero, since speed during movement = 24
  -- at full speed, the apex yPos of the jump is 105
  --yPos is 176 when Mario is on the ground and decreases to 105 at its apex
  joypad.set(1, JoypadA)
end

function AvoidEnemy()
  --if Mario is closer than 32 pixels to an enemy, jump
  joypad.set(1, JoypadA)
end

function AvoidPit()
  joypad.set(1, JoypadA)
end

function Motion(mario_x_spd, mario_y_pos, delta_pos, groundPos, airPos, jumpCheck)
  joypad.set(1, JoypadRight)
  
  --Mario yPos > 106 because he must be lower than a certain jump height and have no horizontal speed in order to stop movement, jump, and proceed
  
  --airDiff indicates how high up Mario is, which is used to see if he should jump again or not
  airDiff = groundPos - airPos
  
  if mario_x_spd < 1 and mario_y_pos > 106 then
    JumpObstacle()
  elseif delta_pos <= 32 then
    AvoidEnemy()
  --the below if statement checks if Mario is on the ground, is not jumping, and has the sufficient speed to jump over the pipe
  elseif airDiff == 176 and jumpCheck == 0 and mario_x_spd > 18 then
    AvoidPit()
  --if Mario has no need to jump, then he should keep moving right to progress
  else
    joypad.set(1, JoypadRight)
  end
end

-- set up the main loop to iterate Mario's frame-by-frame movement
while (true) do
  tableGame = joypad.get(1)
  
  if tableGame.start then
    PressStart()
  end
  
  if tableGame.A then
    PressA()
  end
  
  --xPos is an integer from [0, 256) which increases and then wraps back to zero as Mario moves forward
  --xSpd is an integer that returns 24 when Mario is moving at max acceleration to the right and a number in [0, 24) when Mario is experiencing acceleration towards the right (he is always moving right, so d/dx > 0)
  xPos = memory.readbyte(0x86)
  enemyXPos = memory.readbyte(0x87)
  
  xSpd = memory.readbyte(0x57)
  enemyXSpd = memory.readbyte(0x58)
  
  --if player X position - enemy X position = 0 or is close to zero, then Mario is dead
  --to avoid collision, we want Mario to jump at a suitable length away from the enemy, say 64 bytes
  relXPos = memory.readbyte(0x03ad)
  enemyRelXPos = memory.readbyte(0x03ae)
  deltaXPos = math.abs(relXPos - enemyRelXPos)
  
  --yPos is an integer that returns 176 when Mario is solidly on the ground and [0, 176) when Mario is in the air
  --ySpd is an integer that returns 255 when Mario is at the apex of his jump and 0 when he is on the ground; values are in (0, 255) between the ground and apex of jump
  yPos = memory.readbyte(0xce)
  enemyYPos = memory.readbyte(0xcf)
  
  ySpd = memory.readbyte(0x9f)
  enemyYSpd = memory.readbyte(0xa0)
  
  relYPos = memory.readbyte(0x03b8)
  enemyRelYPos = memory.readbyte(0x03b9)
  deltaYPos = math.abs(relYPos - enemyRelYPos)
  
  --take the hypotenuse of delta x and delta y so that we can project more accurately how close enemies are to Mario
  deltaSumSquared = deltaXPos^2 + deltaYPos^2
  pythag = math.floor(math.sqrt(deltaSumSquared))
  
  --playerYMoveForce checks the force of gravity pulling down on Mario after he reaches the apex of the jump
  --ScreenRightX is an indication of whether Mario is jumping, running, or dying
  --JumpOriginY is 176 at y = 0 and is used for calculations to see how high up in the air Mario is
  
  playerYMoveForce = memory.readbyte(0x0433)
  ScreenRightX = memory.readbyte(0x1d)
  JumpOriginY = memory.readbyte(0x0708)
  
  gui.text(140, 80, xPos)
  gui.text(140, 90, xSpd)
  gui.text(140, 100, yPos)
  gui.text(140, 110, ySpd)
  gui.text(180, 80, enemyXPos)
  gui.text(180, 90, relXPos)
  gui.text(180, 100, enemyRelXPos)
  gui.text(180, 110, deltaXPos)
  
  gui.text(170, 120, playerYMoveForce)
  gui.text(170, 130, ScreenRightX)
  gui.text(170, 140, JumpOriginY)
  
  Motion(xSpd, yPos, pythag, JumpOriginY, playerYMoveForce, ScreenRightX)
  
  emu.frameadvance() --move by one frame
  
  joypad.set(1, JoypadA)
end
