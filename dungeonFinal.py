import time
import random

# S = start
# _ = Empty Room
# W = Wind Strike Tome
# T = Treasure
# B = Basic Encounter
# BT = Basic Encounter or Treasure
# MB = Medium Encounter
# MT = Medium Teasure
# MBT = Medium Encounter or Treasure
# LB = Large Encounter
# LT = Large Treasure
# LBT = Large Encounter or Treasure
# FB = Final Encounter

#This is what the game will read to determine what event to trigger.
dungeonMap = [["mb","lt","fb","lt","lbt"],
              ["lt","lb","lb","lbt","t"],
              ["mt","lbt","lt","mb","mt"],
              ["b","mbt","mb","_","lt"],
              ["t","mb","t","mb","t"],
              ["b","mt","b","b","_"],
              ["_","bt","b","bt","_"],
              ["t","_","S","w","t"]]

#This is the player's perspective of the map, which will change throughout the game.
playerMap  = [["_","_","_","_","_"],
              ["_","_","_","_","_"],
              ["_","_","_","_","_"],
              ["_","_","_","_","_"],
              ["_","_","_","_","_"],
              ["_","_","_","_","_"],
              ["_","_","_","_","_"],
              ["_","_","S","_","_"]]

#Displays an aesthetically pleasing map, without commas, quotes, or brackets.
def displayMap(maps):
  print("╔═══╡ᴍᴀᴘ╞═══╗")
  for x in maps:
    print(f"║ {' '.join(x)} ║")
  print("╚═══════════╝")
  
#Allows the player to see a smaller scope around them.
def miniMapScope(y, x, playerMap):
  try: #Player Location used as a basis
    scopeBase = playerMap[y][x]
  except IndexError:
    pass
  #x and y coordinates are altered to fit their scope's base.
  mmLeft = x - 1
  mmTopLeftX = x - 1
  mmTopLeftY = y - 1
  mmTop = y - 1
  mmTopRightX = x + 1
  mmTopRightY = y - 1
  mmRight = x + 1
  mmBottomRightX = x + 1
  mmBottomRightY = y + 1
  mmBottom = y + 1
  mmBottomLeftX = x - 1
  mmBottomLeftY = y + 1
  print("")
  try:
    #Design for when player is against a wall.
    if x == 0 and y != 0:
      print("║ " + playerMap[mmTop][x] + " " + playerMap[mmTopRightY][mmTopRightX])
    elif x == 0 and y == 0:
      print("╔════")
    elif x < 4 and y == 0:
      print("═════")
    elif x == 4 and y == 0:
      print("════╗")
    else:
      print(playerMap[mmTopLeftY][mmTopLeftX] + " " + playerMap[mmTop][x] + " " + playerMap[mmTopRightY][mmTopRightX])
  except IndexError:
    #If the player is on the edge, there are tiles that cannot load due to index error, this will replace them with a wall.
    if x == 0:
      print("║ " + playerMap[mmTop][x] + " " + playerMap[mmTopRightY][mmTopRightX])
    if x == 4:
      print(playerMap[mmTopLeftY][mmTopLeftX] + " " + playerMap[mmTop][x] + " ║")
    pass
  try:
    if x == 0:
      print("║ " + scopeBase + " " + playerMap[y][mmRight])
    elif x == 4:
      print(playerMap[y][mmLeft] + " " + scopeBase + " ║")
    else:
      print(playerMap[y][mmLeft] + " " + scopeBase + " " + playerMap[y][mmRight])
  except IndexError:
    pass
  try:
    if x == 0 and y != 7:
      print("║ " + playerMap[mmBottom][x] + " " + playerMap[mmBottomLeftY][mmBottomLeftX])
    elif x == 4 and y != 7:
      print(playerMap[mmBottomLeftY][mmBottomLeftX] + " " + playerMap[mmBottom][x] + " ║")
    else:
      print(playerMap[mmBottomLeftY][mmBottomLeftX] + " " + playerMap[mmBottom][x] + " " + playerMap[mmBottomRightY][mmBottomRightX])
  except IndexError:
    if x == 0 and y == 7:
      print("╚════")
    elif x == 4 and y == 7:
      print("════╝")
    else:
      print("═════")
    pass
  
#Determines an extra damage modifier based on player's current level.
def levelDamage(level):
  if level <= 2:
    damage = level * random.randint(2,4)
  if level <= 3:
    damage = level * random.randint(3,5)
  if level <= 4:
    damage = level * random.randint(4,6)
  if level <= 5:
    damage = level * random.randint(5,7)
  return damage

#Displays health and moves while in battle.
def battleUI(playerHealth, enemyHealth, playerMoves):
  print(f"\nPlayer HP: {playerHealth}\nEnemy HP: {enemyHealth}")
  print("\nSelect a number to execute an attack:")
  for key in sorted(playerMoves.items()):
    print(f"{key}")

#Main battle loop attack selection
def attackChoice(battle, playerMove, playerMoves, level, skeleAlly, justCast, divine, focused, gold):
  while battle == True:
    playerMove = input(">>> ").lower()
    #Some special moves have a flag that needs to be established if the player does not already have them unlocked.
    if "5. Raise Skeleton" not in playerMoves:
      skeleAlly = False
    if "6. Focused Magic" not in playerMoves:
      focused = False
    if "7. Divine Protection" not in playerMoves:
      divine = False
      justCast = False
    
    if playerMove != "7":
      justCast = False
      
    #Attack information to be passed for damage calculation
    if playerMove == "1":
      playerAttack = random.randint(10,20) + levelDamage(level)
      
      print("You throw a rock.")
      time.sleep(1)
      print(f"Enemy takes {playerAttack} damage.")
      time.sleep(1)
      
    elif playerMove == "2" and "2. Wind Strike" in playerMoves:
      windRoll1 = random.randint(5,15) + levelDamage(level)
      windRoll2 = random.randint(5,15) + levelDamage(level)
      playerAttack = windRoll1 + windRoll2
      
      print("You cast Wind Strike.")
      time.sleep(1)
      print(f"Enemy takes {windRoll1} damage.")
      time.sleep(1)
      print(f"Enemy takes {windRoll2} from the second cast.")
      time.sleep(1)
      
    elif playerMove == "3" and "3. Fire Bolt" in playerMoves:
      fireBoltMain = random.randint(15,35) + levelDamage(level)
      fireBoltDot1 = round(fireBoltMain * 0.1 + level + random.randint(0,2))
      fireBoltDot2 = round(fireBoltMain * 0.1 + level + random.randint(0,2))
      playerAttack = fireBoltMain + fireBoltDot1 + fireBoltDot2
      
      print("You cast Fire Bolt.")
      time.sleep(1)
      print(f"Enemy takes {fireBoltMain} damage from the initial hit.")
      time.sleep(1)
      print(f"Enemy takes {fireBoltDot1} burning damage.")
      time.sleep(1)
      print(f"Enemy takes {fireBoltDot2} burning damage.")
      
    elif playerMove == "4" and "4. Rapid Fire" in playerMoves:
      print("You ready your bow.")
      time.sleep(1)
      
      rapidFire1 = random.randint(1,6) + level
      rapidFire2 = random.randint(1,6) + level
      rapidFire3 = random.randint(1,6) + level
      rapidFire4 = random.randint(1,6) + levelDamage(level)
      rapidFire5 = random.randint(1,6) + levelDamage(level)
      playerAttack = rapidFire1 + rapidFire2 + rapidFire3 + rapidFire4 + rapidFire5
      
      print(f"Enemy takes {rapidFire1} damage.")
      time.sleep(0.5)
      print(f"Enemy takes {rapidFire2} damage.")
      time.sleep(0.5)
      print(f"Enemy takes {rapidFire3} damage.")
      time.sleep(0.5)
      print(f"Enemy takes {rapidFire4} damage.")
      time.sleep(0.5)
      print(f"Enemy takes {rapidFire5} damage.")
      time.sleep(1)
      
    elif playerMove == "5" and "5. Raise Skeleton" in playerMoves:
      print("You summon a skeleton to aid you in battle.")
      time.sleep(1)
      skeleAlly = True
      playerAttack = 0
      
    elif playerMove == "6" and "6. Focused Magic" in playerMoves:
      print("You cast Focused Magic.")
      time.sleep(1)
      playerAttack = random.randint(40,80) + levelDamage(level)
      
      print(f"Enemy takes {playerAttack} damage.")
      time.sleep(1)
      print(f"You suffer {round(playerAttack * 0.5)} damage from the recoil.")
      time.sleep(1)
      focused = True
    
      
    elif playerMove == "7" and "7. Divine Protection" in playerMoves:
      if justCast == True:
        print("You cannot cast Divine Protect right now.")
        time.sleep(1)
        continue
      else:
        print("You cast Divine Protection, granting you immunity to all enemy damage until your next turn.")
        time.sleep(1)
        divine = True
        justCast = True
        playerAttack = 0
    
    elif playerMove == "8" and "8. Greed" in playerMoves:
      print("You cast Greed.")
      time.sleep(1)
      playerAttack = random.randint(1,20) + levelDamage(level)
      goldDmg = round(gold * 0.1)
      
      print(f"Enemy takes {playerAttack} damage and an additional {goldDmg} damage from your held wealth.")
      
      playerAttack += goldDmg
      time.sleep(1)
      
    elif playerMove == "9" and "9. Rampage" in playerMoves:
      print("You swing your ancient warhammer.")
      time.sleep(1)
      critChance = random.randint(1,4)
      playerAttack = random.randint(75,150) + levelDamage(level)
      if critChance == 1:
        playerAttack = playerAttack + round(playerAttack * 0.5)
        print(f"You strike the enemy's weakspot and deal {playerAttack} damage.")
        time.sleep(1)
      else:
        print(f"Enemy takes {playerAttack} damage.")
        time.sleep(1)
        
    else:
      #Fallback for players who fail to type a valid move.
      print("\nThat is not a valid move. Please try again.")
      time.sleep(1)
      continue
    
    #Return any variables that need to be updated
    return playerAttack, skeleAlly, focused, divine, justCast

#Damage calculation, takes a lot of arguments, in the future, I would probably split this into multiple functions to keep it cleaner
def dmgCalc(playerTurn, enemyTurn, skeleAlly, focused, divine,  playerMove, playerAttack, justCast, playerHealth, enemyHealth, battle, enemyMove, level, gold, xp, playerMap, y, x, enemyType, justFought, playerMoves, hiddenMoves):
  if playerTurn and battle == True:
    if skeleAlly:
      skeleDmg = random.randint(1,6) + levelDamage(level)
      print(f"Your skeleton deals {skeleDmg} damage.")
      enemyHealth -= skeleDmg
      enemyHealth -= playerAttack
    if focused:
      enemyHealth -= playerAttack
      playerHealth -= round(playerAttack * 0.5)
    else:
      if divine:
        justCast = True
        divine = False
      enemyHealth -= playerAttack
    playerTurn = False
    enemyTurn = True
    
  #When a player defeats an enemy
  if enemyHealth <= 0:
    #When an enemy defeats a player on the same turn a player defeats them, the player will still lose, this is possible due to some attacks having recoil damage
    if playerHealth <= 0:
      playerHealth = 0
      winner = "Enemy"
      battle = False
      print("You become overpowered by the enemy, forcing you to leave the dungeon.")
      time.sleep(1)
      exit()
    else: 
      enemyHealth = 0
      winner = "Player"
      battle = False
      skeleAlly = False
    
    #Loot and XP Calculation for all battles
    if winner == "Player" and battle == False:
      #Basic enemy
      if enemyType == "b":
        heal = random.randint(10,40)
        goldGain = random.randint(5,25)
        xpGain = random.randint(15,25)
        tomeChance = random.randint(1,20)
        #Spell drop chance
        if tomeChance == 1:
          if "5. Raise Skeleton" in hiddenMoves:
            playerMoves.update({"5. Raise Skeleton": hiddenMoves["5. Raise Skeleton"]})
            del hiddenMoves["5. Raise Skeleton"]
            print("You find an old necromancer's journal.")
            time.sleep(1)
            print("You have learned Raise Skeleton!")
            time.sleep(1)
      
      #Medium enemy
      elif enemyType == "mb":
        rapidChance = random.randint(1,4)
        heal = random.randint(30,70)
        goldGain = random.randint(20,45)
        xpGain = random.randint(20,30)
        if rapidChance == 1:
          if "4. Rapid Fire" in hiddenMoves:
            playerMoves.update({"4. Rapid Fire": hiddenMoves["4. Rapid Fire"]})
            del hiddenMoves["4. Rapid Fire"]
            print("You find a bow.")
            time.sleep(1)
            print("It seems to be eminating power...")
            time.sleep(1)
            print("You have learned Rapid Fire!")
            time.sleep(1)
          elif "3. Fire Bolt" in hiddenMoves:
            playerMoves.update({"3. Fire Bolt": hiddenMoves["3. Fire Bolt"]})
            del hiddenMoves["3. Fire Bolt"]
            print("You find a pyromancer's book.")
            time.sleep(1)
            print("You begin to read...")
            time.sleep(1)
            print("You have learned Fire Bolt!")
            time.sleep(1)
      
      #Large enemy      
      elif enemyType == "lb":
        divChance = random.randint(1,2)
        heal = random.randint(60,100)
        goldGain = random.randint(30,75)
        xpGain = random.randint(40,55)
        if divChance == 1:
          if "7. Divine Protection" in hiddenMoves:
            playerMoves.update({"7. Divine Protection": hiddenMoves["7. Divine Protection"]})
            del hiddenMoves["7. Divine Protection"]
            print("You find an old Paladin's handbook.")
            time.sleep(1)
            print("You have learned Divine Protection!")
            time.sleep(1)
      
      #Final Boss
      elif enemyType == "fb":
        print(f"Congratulations! You have defeated the dungeon in {turnCount} turns!")
        time.sleep(1)
        print("You grab all the loot and head home.")
        time.sleep(4)
        exit()
      
      #Displays to player their gold and xp gained for victory.
      print(f"You find {goldGain} gold.")
      time.sleep(1)
      print(f"You gain {xpGain} XP for defeating the enemy and find some loot")
      time.sleep(1)
      gold += goldGain
      xp += xpGain
      time.sleep(1)
      playerMap[y][x] = "P"
      
      #When an enemy is defeated, depending on the enemy, it will roll a random number and heal according to these statements
      if heal < 20:
        print("You find a stale piece of bread, you're starving so you eat it anyways. (HP +10)")
        time.sleep(1)
        playerHealth += 10
      elif heal < 35:
        print("You find a stash of rations and quickly eat them. (HP +25)")
        time.sleep(1)
        playerHealth += 25
      elif heal < 50:
        print("You find a basic healing potion. (HP +50)")
        time.sleep(1)
        playerHealth += 50
      elif heal < 70:
        print("You find an adept potion. (HP +70)")
        time.sleep(1)
        playerHealth += 70
      elif heal < 90:
        print("You find a strong healing potion. (HP +90)")
        time.sleep(1)
        playerHealth += 90
      elif heal < 95:
        print("You find an elixir of life. (HP +150)")
        time.sleep(1)
        playerHealth += 150
      print("\nYou continue through.\n")
      time.sleep(1)
      justFought = True

  #Enemy Damage Calculation, attack value is passed from when the function is called
  if enemyTurn and battle == True:
    if divine:
      justCast = True
    else:
      playerHealth -= enemyMove
      divine = False
    playerTurn = True
    enemyTurn = False
    if playerHealth <= 0:
      playerHealth = 0
      winner = "Enemy"
      battle = False
      if winner == "Enemy":
        print("You become overpowered by the enemy, forcing you to leave the dungeon.")
        time.sleep(1)
        exit()
  return playerTurn, enemyTurn, skeleAlly, focused, divine, justCast, playerHealth, enemyHealth, battle, justFought, gold, xp, playerMap, y, x

#Initial values to establish in order to start our main function
mapChoice = dungeonMap

position = mapChoice[0][0]

playerMove = None
enemyMove = None
enemyHealth = None
justFought = False

#MAIN PROGRAM LOOP
def main(mapChoice, playerMap, position):

  #Resets any flags that are used during battle
  battle = False
  skeleAlly = False
  focused = False
  divine = False
  justCast = False

  print("You wake up in a dark and damp dungeon.")
  time.sleep(2)
  print("Beside you, you find see a man laying down.")
  time.sleep(2)
  print("You realize the man is no longer alive, clutching a journal.")
  time.sleep(2)
  print("The journal reads 'I have given up on this cruel fate. This dungeon seems to be filled with magic and wealth with no way out.")
  time.sleep(3)
  print("'The enemies within seem to be stronger the further North I go, and the enemies never seem to stop coming.'")
  time.sleep(3)
  print("You trudge onwards, undesiring of a similar fate.")
  time.sleep(2)
  
  #Player Starting Information
  x = 2
  y = 7
  playerHealth = 100
  gold = 0
  level = 1
  xp = 0
  
  #Starting Player Attack
  playerMoves = {"1. Throw Rock": "Basic damage"}
  
  #Unlockable attacks
  hiddenMoves = {"2. Wind Strike": "Basic wind spell, deals basic damage twice.",
                 "3. Fire Bolt": "Deals moderate damage, followed by two smaller hits",
                 "4. Rapid Fire": "Quickly fire your bow to inflict five strikes, becomes stronger with player levels (5d6)",
                 "5. Raise Skeleton": "Summons a skeleton to aid you in battle.",
                 "6. Focused Magic": "A strong attack that damages the user for half of the damage dealt.",
                 "7. Divine Protection": "Grants immunity to all damage for one turn.",
                 "8. Greed": "Deals damage relative to the amount of gold held.",
                 "9. Rampage": "Smashes the enemy for moderate damage using your warhammer, has a chance to deal double damage."}
  
  turnCount = 1
  position = 0
  
  #Things that happen between battles
  while battle == False:
    #Sets a variable for the previous location, allows for player to "bump" into walls without going through them.
    previousX = x
    previousY = y
    
    #Depending on the current XP total of the player, an additional damage and health modifier may be active.
    if level == 1:
      if playerHealth > 100:
        playerHealth = 100
        
      if xp >= 50:
        level = 2
        print("You are now level 2. Your damage and maximum health has increased.")
        time.sleep(1)
        
    elif level == 2:
      if playerHealth > 150:
        playerHealth = 150
      
      if xp >= 120:
        level = 3
        print("You are now level 3. Your damage has increased.")
        time.sleep(1)
        
    elif level == 3:
      if playerHealth > 150:
        playerHealth = 150
        
      if xp >= 210:
        level = 4
        print("You are now level 4. Your damage has increased and maximum health.")
        time.sleep(1)
        
    elif level == 4:
      if playerHealth > 200:
        playerHealth = 200
        
      if xp >= 320:
        level = 5
        print("You are now level 5. Your damage and maximum health have maximized.")
        time.sleep(1) 
        
    elif level == 5:
      if playerHealth > 250:
        playerHealth = 250
    
    #displays map on turn 1
    if turnCount == 1:
      displayMap(playerMap)
      
    miniMapScope(y, x, playerMap)
    print(f"\nHP: {playerHealth}")
    print(f"Gold: {gold}")
    print(f"Turn: {turnCount}")
    print(f"Level: {level}")
    print("\nChoose a Direction (N, E, S, W, MAP):")
    movement = input(">>> ").upper()
    turnCount += 1
    playerMap[previousY][previousX] = "X"
    
    
    
    if movement == "N":
      if y > 0:
      #If the player is not against the northern wall, they can go North. This logic is used for all cardinal directions.
        y -= 1
        position = mapChoice[y][x]
        playerMap[y][x] = "P"
        #Sets flags, if a player checked the map without these flags, the room's event would repeat
        justFought = False
        justLooted = False
      else:
      #If the player is against the northern wall, they cannot go North
        print("You don't see any way through that way.")
        time.sleep(1)
        playerMap[y][x] = "P"
        dungeonMap[y][x] = "_"   
        pass

    if movement == "S":
      if y < 7:
        y += 1
        position = mapChoice[y][x]
        playerMap[y][x] = "P"
        justFought = False
        justLooted = False
      else:
        print("You don't see any way through that way.")
        time.sleep(1)
        playerMap[y][x] = "P"
        dungeonMap[y][x] = "_"   
        pass

    if movement == "E":
      if x < 4:
        x += 1
        position = mapChoice[y][x]
        playerMap[y][x] = "P"
        justFought = False
        justLooted = False
      else:
        print("You don't see any way through that way.")
        time.sleep(1)
        playerMap[y][x] = "P"
        dungeonMap[y][x] = "_"   
        pass

    if movement == "W":
      if x > 0:
        x -= 1
        position = mapChoice[y][x]
        playerMap[y][x] = "P"
        justFought = False
        justLooted = False
      else:
        print("You don't see any way through that way.")
        time.sleep(1)
        playerMap[y][x] = "P"
        dungeonMap[y][x] = "_"   
        pass

    if movement == "MAP":
      if "t" in dungeonMap[y][x]:
        #If the player checks their map in any room that contains a treasure, this will clear the room, not allowing the player to loot the same chest multiple times.
        try:
          dungeonMap[y][x] = "_"   
          print("")
        except TypeError:
          continue
      playerMap[y][x] = "P"
      displayMap(playerMap)
    
    #Multiple positions among the map can be either a battle or a treasure, this will flip a coin to decide which room it will be for this run.
    if position == "bt":
      btCheck = random.randint(1,2)
      if btCheck == 1:
        position = "b"
        justFought = False
      else:
        position = "t"
        
    if position == "mbt":
      btCheck = random.randint(1,2)
      if btCheck == 1:
        position = "mb"
        justFought = False
      else:
        position = "mt"
        
    if position == "lbt":
      btCheck = random.randint(1,2)
      if btCheck == 1:
        position = "lb"
        justFought = False
      else:
        position = "lt"
      
    # BASIC ENEMY ENCOUNTER
    if (position == "b" and justFought == False):
      print("A nearby skeleton comes to life!")
      #Establish enemyType for loot calculation
      enemyType = "b"
      time.sleep(1)
      #Set flags for battle
      battle = True
      playerTurn = True
      enemyTurn = False
      skeleAlly = False
      justCast = False
      divine = False
      focused = False
      #Set enemy HP
      enemyHealth = random.randint(25,40);
      
      #Battle Loop
      while battle == True:
        if playerTurn == True:
          #UI function
          battleUI(playerHealth, enemyHealth, playerMoves)
          
          #Attack selection function, assigned to a variable, so that the returned data can be used
          result = attackChoice(battle, playerMove, playerMoves, level, skeleAlly, justCast, divine, focused, gold)
          playerAttack = result[0]
          skeleAlly = result[1]
          focused = result[2]
          divine = result[3]
          justCast = result[4]
          enemyMove = 0
        if enemyTurn:
          #This result must be passed during an enemy turn for proper calculation, the divine flag indicates player invulnerability for that turn/
          divine = result[3]
          enemyMove = random.randint(10,20)
          print(f"The enemy attacks you, dealing {enemyMove} damage.")
          time.sleep(1)

        #BASIC ENCOUNTER DAMAGE, LOOT, AND XP CALCULATION
        #Same as above, this function is passed to a variable so that we can reuse the data. Personally, this looks very messy but I am afraid to mess with it and break the entire script. I believe I should rewrite this entire thing with classes. In the beginning I wasn't sure about all attributes necessary so the thought of creating classes was intimidating. Now that I have an idea of everything, it may be easier to incorporate classes since many of these enemies, attacks, and rooms share mutual attributes and this would reduce code bloat.
        
        dmgResult = dmgCalc(playerTurn, enemyTurn, skeleAlly, focused, divine, playerMove, playerAttack, justCast, playerHealth, enemyHealth, battle, enemyMove, level, gold, xp, playerMap, y, x, enemyType, justFought, playerMoves, hiddenMoves)
        
        playerTurn = not playerTurn
        enemyTurn = not enemyTurn
        skeleAlly = dmgResult[2]
        focused = dmgResult[3]
        divine = dmgResult[4]
        justCast = dmgResult[5]
        playerHealth = dmgResult[6]
        enemyHealth = dmgResult[7]
        battle = dmgResult[8]
        justFought = dmgResult[9]
        gold = dmgResult[10]
        xp = dmgResult[11]
        playerMap = dmgResult[12]
        y = dmgResult[13]
        x = dmgResult[14]
        if divine:
          print("Your divine protection fades.")
          divine = False
  
    if (position == "mb" and justFought == False):
      #Once the previous section was written, the following loops for the medium, large, and boss enemies are essentially copy pasted. This is something that I should have put in a function, since there are many repeating lines from other sections.
      print("A troll charges at you!")
      time.sleep(1)
      enemyType = "mb"
      battle = True
      playerTurn = True
      enemyTurn = False
      skeleAlly = False
      justCast = False
      divine = False
      focused = False
      enemyHealth = random.randint(80,120);
      while battle == True:
        if playerTurn == True:
          battleUI(playerHealth, enemyHealth, playerMoves)
            
          result = attackChoice(battle, playerMove, playerMoves, level, skeleAlly, justCast, divine, focused, gold)
          playerAttack = result[0]
          skeleAlly = result[1]
          focused = result[2]
          divine = result[3]
          justCast = result[4]
          enemyMove = 0
        else:
          divine = result[3]
          enemyMove = random.randint(25,40)
          print(f"The enemy attacks you, dealing {enemyMove} damage.")
          time.sleep(1)

        #MED ENCOUNTER DAMAGE, LOOT, AND XP CALCULATION
        dmgResult = dmgCalc(playerTurn, enemyTurn, skeleAlly, focused, divine,  playerMove, playerAttack, justCast, playerHealth, enemyHealth, battle, enemyMove, level, gold, xp, playerMap, y, x, enemyType, justFought, playerMoves, hiddenMoves)
        
        playerTurn = not playerTurn
        enemyTurn = not enemyTurn
        skeleAlly = dmgResult[2]
        focused = dmgResult[3]
        divine = dmgResult[4]
        justCast = dmgResult[5]
        playerHealth = dmgResult[6]
        enemyHealth = dmgResult[7]
        battle = dmgResult[8]
        justFought = dmgResult[9]
        gold = dmgResult[10]
        xp = dmgResult[11]
        playerMap = dmgResult[12]
        y = dmgResult[13]
        x = dmgResult[14]
        if divine:
          print("Your divine protection fades.")
          divine = False
        
    #LARGE ENEMY ENCOUNTER
    if (position == "lb" and justFought == False):
      print("A large stone golem emerges out of the ground.")
      time.sleep(1)
      enemyType = "lb"
      battle = True
      playerTurn = True
      enemyTurn = False
      skeleAlly = False
      justCast = False
      divine = False
      focused = False
      specialExecute = False
      normalAttack = False
      specialAttack = False
      enemyHealth = random.randint(200,300);
      while battle == True:
        if playerTurn == True:
          battleUI(playerHealth, enemyHealth, playerMoves)
          
          result = attackChoice(battle, playerMove, playerMoves, level, skeleAlly, justCast, divine, focused, gold)
          playerAttack = result[0]
          skeleAlly = result[1]
          focused = result[2]
          divine = result[3]
          justCast = result[4]
          enemyMove = 0
        else:
        #This enemy has different AI than the basic and medium encounters, this is supposed to work as a weaker preview of the final boss, so that the player may know what to expect if they pay attention to the mechanics. This enemy has a 50% chance to drop Divine Protection, which is almost necessary to beat the game.
          divine = result[3]
          if specialExecute:
            print("The enemy swings a massive blow.")
            time.sleep(1)
            enemyMove = random.randint(120,180)
            specialExecute = False
          else:
            attackChance = random.randint(1,2)
            if attackChance == 1:
              normalAttack = True
            else:
              specialAttack = True
            if normalAttack == True:
              enemyMove = random.randint(40,65)
              print(f"The enemy attacks you, dealing {enemyMove} damage.")
              time.sleep(1)
              normalAttack = False
            elif specialAttack:
              print("The enemy prepares a powerful attack.")
              time.sleep(1)
              enemyMove = 0
              specialExecute = True
              specialAttack = False

        #LARGE ENCOUNTER DAMAGE, LOOT, AND XP CALCULATION
        dmgResult = dmgCalc(playerTurn, enemyTurn, skeleAlly, focused, divine, playerMove, playerAttack, justCast, playerHealth, enemyHealth, battle, enemyMove, level, gold, xp, playerMap, y, x, enemyType, justFought, playerMoves, hiddenMoves)
        
        
        playerTurn = not playerTurn
        enemyTurn = not enemyTurn
        skeleAlly = dmgResult[2]
        focused = dmgResult[3]
        divine = dmgResult[4]
        justCast = dmgResult[5]
        playerHealth = dmgResult[6]
        enemyHealth = dmgResult[7]
        battle = dmgResult[8]
        justFought = dmgResult[9]
        gold = dmgResult[10]
        xp = dmgResult[11]
        playerMap = dmgResult[12]
        y = dmgResult[13]
        x = dmgResult[14]
        if divine:
          print("Your divine protection fades.")
          divine = False
          
    #BOSS ENCOUNTER
    if (position == "fb" and justFought == False):
      print("The room leads to a large cave filled with treasures, you smell fire.")
      time.sleep(1)
      print("You feel the ground beneath you shaking.")
      time.sleep(1)
      print("Suddenly, a cloud of smoke begins to fill the air.")
      time.sleep(1)
      print("A dragon appears!")
      time.sleep(1)
      enemyType = "fb"
      battle = True
      playerTurn = True
      enemyTurn = False
      skeleAlly = False
      justCast = False
      divine = False
      focused = False
      specialExecute = False
      normalAttack = False
      specialAttack = False
      enemyHealth = 500;
      while battle == True:
        if playerTurn == True:
          battleUI(playerHealth, enemyHealth, playerMoves)
          
          result = attackChoice(battle, playerMove, playerMoves, level, skeleAlly, justCast, divine, focused, gold)
          playerAttack = result[0]
          skeleAlly = result[1]
          focused = result[2]
          divine = result[3]
          justCast = result[4]
          enemyMove = 0
        else:
          divine = result[3]
          if specialExecute:
            print("The dragon unleashes a wall of flames.")
            time.sleep(1)
            enemyMove = random.randint(200,250)
            specialExecute = False
          else:
            attackChance = random.randint(1,2)
            if attackChance == 1:
              normalAttack = True
            else:
              specialAttack = True
            if normalAttack == True:
              enemyMove = random.randint(60,95)
              print(f"The dragon bites you, dealing {enemyMove} damage.")
              time.sleep(1)
              normalAttack = False
            elif specialAttack:
              print("The dragon takes a deep breath.")
              time.sleep(1)
              enemyMove = 0
              specialExecute = True
              specialAttack = False

        #LARGE ENCOUNTER DAMAGE, LOOT, AND XP CALCULATION
        dmgResult = dmgCalc(playerTurn, enemyTurn, skeleAlly, focused, divine, playerMove, playerAttack, justCast, playerHealth, enemyHealth, battle, enemyMove, level, gold, xp, playerMap, y, x, enemyType, justFought, playerMoves, hiddenMoves)
        
        
        playerTurn = not playerTurn
        enemyTurn = not enemyTurn
        skeleAlly = dmgResult[2]
        focused = dmgResult[3]
        divine = dmgResult[4]
        justCast = dmgResult[5]
        playerHealth = dmgResult[6]
        enemyHealth = dmgResult[7]
        battle = dmgResult[8]
        justFought = dmgResult[9]
        gold = dmgResult[10]
        xp = dmgResult[11]
        playerMap = dmgResult[12]
        y = dmgResult[13]
        x = dmgResult[14]
        if divine:
          print("Your divine protection fades.")
          divine = False
    
    
    #TREASURE CHEST ROOMS
    
    #Wind Strike
    #Placed a basic spell near the starting area
    if position == "w":
      print("You find a treasure chest.")
      time.sleep(1)
      if "2. Wind Strike" in hiddenMoves:
        playerMoves.update({"2. Wind Strike": hiddenMoves["2. Wind Strike"]})
        del hiddenMoves["2. Wind Strike"]
        print("You find a dusty tome. You have learned Wind Strike!")
        time.sleep(1)
      else:
        print("It's empty...")
    
    #Basic Treasure chest, uses basic random integer if statements to determine what the player receives
    if position == "t" and justLooted == False:
      print("You find a treasure chest.")
      time.sleep(1)
      lootRoll = random.randint(1,10)
      if lootRoll <= 4:
        print("You find some gold and food.")
        time.sleep(1)
        goldRoll = random.randint(5,15)
        foodRoll = random.randint(8,18)
        print(f"You gain {goldRoll} gold and {foodRoll} health.")
        gold += goldRoll
        playerHealth += foodRoll
        time.sleep(1)
      elif lootRoll <= 6:
        print("You find a lot of gold.")
        time.sleep(1)
        goldRoll = random.randint(30,50)
        print(f"You manage to fill your pockets with {goldRoll} gold.")
        gold += goldRoll
        time.sleep(1)
      elif lootRoll <= 8:
        if "3. Fire Bolt" in hiddenMoves:
          playerMoves.update({"3. Fire Bolt": hiddenMoves["3. Fire Bolt"]})
          del hiddenMoves["3. Fire Bolt"]
          print("You find an old book.")
          time.sleep(1)
          print("You have learned Fire Bolt!")
          time.sleep(1)
        else:
          print("You find a partially finished health potion.")
          time.sleep(1)
          foodRoll = random.randint(10,20)
          print(f"You heal for {foodRoll} health.")
          playerHealth += foodRoll
          time.sleep(1)
      else:
        if "4. Rapid Fire" in hiddenMoves:
          playerMoves.update({"4. Rapid Fire": hiddenMoves["4. Rapid Fire"]})
          del hiddenMoves["4. Rapid Fire"]
          print("You find a shortbow, it seems to be emanating power.")
          time.sleep(1)
          print("You have learned Rapid Fire!")
          time.sleep(1)
        else:
          print("You find some gold.")
          goldRoll = random.randint(8,24)
          gold += goldRoll
          time.sleep(1)
      dungeonMap[y][x] = "_"                              
      justLooted = True
    
    #MEDIUM TREASURE
    if position == "mt" and justLooted == False:
      print("You find a treasure chest.")
      time.sleep(1)
      lootRoll = random.randint(1,10)
      if lootRoll <= 2:
        print("You find some gold and food.")
        time.sleep(1)
        goldRoll = random.randint(10,30)
        foodRoll = random.randint(14,26)
        print(f"You gain {goldRoll} gold and {foodRoll} health.")
        gold += goldRoll
        playerHealth += foodRoll
        time.sleep(1)
      elif lootRoll <= 4:
        print("You find a lot of gold.")
        time.sleep(1)
        goldRoll = random.randint(50,70)
        print(f"You manage to fill your pockets with {goldRoll} gold.")
        gold += goldRoll
        time.sleep(1)
      elif lootRoll <= 5:
        print("You find a freshly baked pie, you try not to think about why and just eat it.")
        time.sleep(1)
        print("You feel much better (HP + 40)")
        time.sleep(1)
        playerHealth += 40
      else:
        if "5. Raise Skeleton" in hiddenMoves:
          playerMoves.update({"5. Raise Skeleton": hiddenMoves["5. Raise Skeleton"]})
          del hiddenMoves["5. Raise Skeleton"]
          print("You find an old necromancer's journal.")
          time.sleep(1)
          print("You have learned Raise Skeleton!")
          time.sleep(1)
        else:
          print("You find some gold.")
          goldRoll = random.randint(15,30)
          gold += goldRoll
          time.sleep(1)
      dungeonMap[y][x] = "_"                              
      justLooted = True
    
    #LARGE TREASURE
    if position == "lt" and justLooted == False:
      print("You find a treasure chest.")
      time.sleep(1)
      lootRoll = random.randint(1,10)
      if lootRoll <= 1:
        print("You find some loot.")
        time.sleep(1)
        goldRoll = random.randint(50,90)
        foodRoll = random.randint(44,86)
        print(f"You gain {goldRoll} gold and {foodRoll} health.")
        gold += goldRoll
        playerHealth += foodRoll
        time.sleep(1)
      elif lootRoll <= 8:
        #There is a 70% chance to find this spell to compensate if the player does not receive it from defeating a golem.
        if "7. Divine Protection" in hiddenMoves:
          playerMoves.update({"7. Divine Protection": hiddenMoves["7. Divine Protection"]})
          del hiddenMoves["7. Divine Protection"]
          print("You find a Paladin's handbook.")
          time.sleep(1)
          print("You have learned Divine Protection!")
          time.sleep(1)
        else:
          print("You find a lot of food.")
          foodRoll = random.randint(150,300)
          playerHealth += foodRoll
          time.sleep(1)
      else:
        if "8. Greed" in hiddenMoves:
          playerMoves.update({"8. Greed": hiddenMoves["8. Greed"]})
          del hiddenMoves["8. Greed"]
          print("You find a journal of a king.")
          time.sleep(1)
          print("You have learned Greed!")
          time.sleep(1)
        else:
          print("You find a lot of gold.")
          goldRoll = random.randint(150,300)
          gold += goldRoll
          time.sleep(1)
      dungeonMap[y][x] = "_"                            
      #Set flag to True so the player cannot loot the chest multiple times.  
      justLooted = True

main(mapChoice,playerMap,position)

#All in all, this was incredibly fun to write. I imagine from an experienced coder's point of view that this is incredibly messy on the backend. It's evident that I was working with what I am more familiar with. I've learned that I should be reaching out into fields where I am not as familiar. It's easy to get carried away with a fun idea. You want it to work so bad that you would only use what you know already, rather than risk it with something you are more likely to be frustrated with. I look forward to working with this script again and possibly refactoring this into something that uses classes, has sounds, and uses an actual GUI rather than just being text based. I've spent quite a few hours debugging this, but I am sure someone or myself will still end up finding ways to break this script. One other thing that I would change is the order of functions, or possibly storing them in their own module.
