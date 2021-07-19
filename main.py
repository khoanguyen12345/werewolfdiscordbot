#last working save: 1:51PM July 5th
import discord
import os
import random
import keep_alive
client = discord.Client()

global dead #array of dead people throughout the entire match (global alive in determineDeadAlive())
dead=[]

global alive
alive=[]

global rolesAllocated #array of "player_name: role"
rolesAllocated = []
players = []
playersAddedString = ""

global currentNight
currentNight=1

global wolfKillsAvailable #wolfKills update to False when wolf kills, and true when night ends
wolfKillsAvailable = True

global witchKillAvailable #witchKill does not update because witch only kills once
witchKillAvailable = True

global witchSaveAvailable
witchSaveAvailable = True

global messagedVotingDone
messagedVotingDone = False

global tiedVoting
tiedVoting = False

global night
night = False

global playerSaved
playerSaved = ""

global seerAvailable #seerAvailable update to False when seer seers, and true when night ends
seerAvailable = True

global saveAvailable #saveAvailable update to False when bodyguard saves, and true when night ends
saveAvailable = True

global hookupAvailable
hookupAvailable = True

global cupidPairedPlayers #save paired players as an array
cupidPairedPlayers = []

global savedPlayers #array of saved players (does not carry over to next night)
savedPlayers = []

global killedPlayers #array of killed players (does not carry over to next night)
killedPlayers = []

global votersArray #array of players to track who already voted
votersArray = []

global votedArray #dict of players getting voted
votedArray = {}

global votingFinished #communicates that voting is finished
votingFinished = False

global gameEnd
gameEnd = False

global winner
winner = ""

global witchNoAction
witchNoAction = False

global cupidNoAction
cupidNoAction = False

global hunterNoAction
hunterNoAction = False

global hunterKillAvailable
hunterKillAvailable = True

rolePowers = ["kill","save","seer","hookup","N/A","choose Wolf or Villager after night 3"]


def resetGlobals ():
    global currentNight
    global wolfKillsAvailable
    global witchKillAvailable
    global messagedVotingDone
    global night
    global playerSaved
    global saveAvailable
    global seerAvailable
    global hookupAvailable
    global votingFinished
    global gameEnd
    global winner
    global witchSaveAvailable
    global hunterKillAvailable
    global witchNoAction
    global cupidNoAction
    global hunterNoAction
    global tiedVoting
    global rolesAllocated
    global alive
    global dead
    currentNight = 1
    wolfKillsAvailable = True
    witchSaveAvailable = True
    witchKillAvailable = True
    messagedVotingDone = False
    hunterKillAvailable = True
    night = False
    playerSaved = ""
    saveAvailable = True
    seerAvailable = True
    hookupAvailable = True
    votingFinished = False
    gameEnd = False
    winner = ""
    witchNoAction = False
    cupidNoAction = False
    hunterNoAction = False
    tiedVoting = False
    rolesAllocated.clear()
    alive.clear()
    dead.clear()

def checkFinishedActions():
    global wolfKillsAvailable
    global witchKillAvailable
    global saveAvailable
    global seerAvailable
    global hookupAvailable
    global witchSaveAvailable
    global hunterKillAvailable
    global witchNoAction
    global cupidNoAction
    global hunterNoAction
    witchActionDone = False
    hunterActionDone = False
    cupidActionDone = False
    if witchKillAvailable == False or witchNoAction == True:
      witchActionDone = True
    if len(cupidPairedPlayers)>0 or cupidNoAction == True:
      cupidActionDone = True
    if hunterKillAvailable == False or hunterNoAction == True:
      hunterActionDone = True
    if wolfKillsAvailable == False and saveAvailable == False and seerAvailable == False and hunterActionDone == True and cupidActionDone == True and witchActionDone == True:
      return True
    else:
      return False

def advanceNight (): #to reset everything when morning comes
  global currentNight
  currentNight = currentNight+1
  global wolfKillsAvailable
  wolfKillsAvailable = True
  global seerAvailable
  seerAvailable = True
  global saveAvailable
  global tiedVoting
  saveAvailable = True
  killedPlayers.clear()
  savedPlayers.clear()
  votersArray.clear()
  votedArray.clear()
  global votingFinished
  votingFinished = False
  global messagedVotingDone
  messagedVotingDone = True
  global witchNoAction
  global cupidNoAction
  global hunterNoAction
  witchNoAction = False
  cupidNoAction = False
  hunterNoAction = False
  tiedVoting = False
  return

def assignRoles (playerList): #assign roles to added players at the beginning of game
  rolesList = []
  
  while rolesList.count("werewolf") < werewolf.count:
      rolesList.append("werewolf")

  while rolesList.count("orphan") < orphan.count:
      rolesList.append("orphan")

  while rolesList.count("cupid") < cupid.count:
      rolesList.append("cupid")
  
  while rolesList.count("seer") < seer.count:
      rolesList.append("seer")
  
  while rolesList.count("witch") < witch.count:
      rolesList.append("witch")

  while rolesList.count("bodyguard")<bodyguard.count:
      rolesList.append("bodyguard")

  while rolesList.count("hunter")<hunter.count:
      rolesList.append("hunter")

  while len(rolesList)<len(playerList):
    rolesList.append("villager")

  rolesAllocationList = []

  for x in range(len(rolesList)):
    rolesAllocationList.append(playerList[x] + ": " + rolesList[x])

  return rolesAllocationList

def determineDeadAlive (): #determine dead and alive players after every night (taking into consideration kills from witch, cupid, werewolves/saves from bodyguard)
  finalKillArray = [item for item in killedPlayers if item not in savedPlayers]
  if cupidPairedPlayers:
    if cupidPairedPlayers[1] in finalKillArray or cupidPairedPlayers[0] in finalKillArray:
      anotherTemp = [thing for thing in cupidPairedPlayers if thing not in finalKillArray]
    else:
      anotherTemp = finalKillArray
  else:
    anotherTemp = finalKillArray
  savedPlayers.append(" ")
  if anotherTemp:
    if len(savedPlayers) == 3:
      for x in range(len(anotherTemp)):
        if anotherTemp[x]!=savedPlayers[0] and anotherTemp[x]!=savedPlayers[1]:
          finalKillArray.append(anotherTemp[x])
    else:
      for x in range(len(anotherTemp)):
        if anotherTemp[x]!=savedPlayers[0]:
          finalKillArray.append(anotherTemp[x])
  tempCount = 0
  global rolesAllocated
  global alive
  tempAliveArray = alive.copy();
  finalKillArray = list(dict.fromkeys(finalKillArray))
  for o in range(len(finalKillArray)):
    tempCount = 0
    for player in rolesAllocated:
      tempCount = tempCount+1
      if str(player).split(": ")[0] == finalKillArray[o]:
        dead.append(rolesAllocated[tempCount-1])
        tempAliveArray[tempCount-1] = " "
        alive = tempAliveArray
  return

def kill (playerName): #add who the werewolf wants to kill to an array (does not guarantee kill)
    killedPlayers.append(playerName)
    return

def save (playerName): #add who the bodyguard wants to save to an array (does not guarantee save)
    savedPlayers.append(playerName)
    return

def hookup (playerNames):
    for i in range(len(playerNames)):
      cupidPairedPlayers.append(playerNames[i])
    return

def vote (playerName):
  global votedArray
  global alive
  playersAlive = 0
  if (sum(votedArray.values()) < len(alive)):
    if playerName in votedArray.keys():
        votedArray.update({playerName:votedArray[playerName]+1})
    else:
        votedArray.update({playerName:1})
  for x in range(len(alive)):
        if (alive[x]== " "):
          continue
        else:
          playersAlive +=1
  if (sum(votedArray.values()) == playersAlive):
    global votingFinished
    votingFinished = True
    highest = max(votedArray.values())
    playerVotedOut = [k for k, v in votedArray.items() if v == highest]
    if len(playerVotedOut) == 1:
      for x in range(len(alive)):
        if alive[x].split(":")[0] == playerVotedOut[0]:
          dead.append(alive[x])
          alive[x] = " "
        else:
          continue
    else:
      global tiedVoting
      tiedVoting = True
  return

def checkGameEnd ():
  global gameEnd
  global winner
  wolfSideCurrent = 0
  villagerSideCurrent = 0
  for x in range(len(alive)):
    if alive[x]== " ":
      continue
    else:
      if getattr(eval(alive[x].split(": ")[1]),'wolfSide') == True:
        wolfSideCurrent +=1
      else:
        villagerSideCurrent += 1

  if wolfSideCurrent >= villagerSideCurrent:
    gameEnd = True
    winner = "Werewolves"
    return True
  
  if wolfSideCurrent == 0:
    gameEnd = True
    winner = "Villagers"
    return False

def checkNight():
  global night
  if night:
    return True
  else:
    return False

def seerPlayer (playerName): #seer
  tempCount = 0;
  onWolfsSide = False
  global rolesAllocated
  sub = playerName + ":";
  for player in rolesAllocated:
    tempCount = tempCount+1
    if str(player).find(sub) != -1:
      if getattr(eval(rolesAllocated[tempCount-1].split(": ")[1]),'wolfSide') == False:
        onWolfsSide = False
      else:
        onWolfsSide = True
    else:
      continue
  return onWolfsSide

def checkEnoughPlayers (requiredPlayers):
  global rolesAllocated
  if len(rolesAllocated)<requiredPlayers:
      return False
  else:
      return True

class playerRole: #class playerRole
    serverRole = "player"
    def __init__(self, name,count,specialFunction,wolfSide):
        self.name = name
        self.count = count
        self.specialFunction = specialFunction
        self.wolfSide = wolfSide

werewolf = playerRole("werewolf",2,rolePowers[0],True) #done
villager = playerRole("villager",len(players)-werewolf.count-5,rolePowers[4],False)
orphan = playerRole("orphan",0,rolePowers[4],False)
cupid = playerRole("cupid",1,rolePowers[5],False) #done
seer = playerRole("seer",1,rolePowers[3],False) #done
witch = playerRole("witch",1,rolePowers[0],True) #done
bodyguard = playerRole("bodyguard",1,rolePowers[1],False)#done
hunter = playerRole("hunter",1,rolePowers[0],False)

keep_alive.keep_alive()

@client.event #discord bot stuff
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event #this is basically main()
async def on_message(message):
  global messagedVotingDone
  global winner
  admins = client.get_channel(860106935336828958)
  if message.author == client.user:
      return
  
  if message.content.startswith('$addplayers') and message.channel.name == "admins": #admins add player
      global alive
      resetGlobals()
      playerRepeated = False
      playersAddedString = message.content[11:]
      players = playersAddedString.split( )
      seen = []
      for name in players:
        if name in seen:
          playerRepeated = True
        else:
          seen.append(name)
      if playerRepeated == False:
        randomizedList = players.copy()
        random.shuffle(randomizedList)
        global rolesAllocated
        rolesAllocated = assignRoles(randomizedList)
        alive = rolesAllocated
        for x in range(len(players)):
          await message.channel.send(rolesAllocated[x])
        await message.channel.send("------------------------")
      else:
        await message.channel.send("player names repeated")

  if gameEnd == False:
    if message.content.startswith('$nightstart') and message.channel.name == "admins": #admins start night
      requiredPlayers = werewolf.count+orphan.count+cupid.count+seer.count+witch.count+bodyguard.count+hunter.count+2
      if (checkEnoughPlayers(requiredPlayers) == False):
        await message.channel.send("not enough players. " + str(requiredPlayers) + " required. $addplayers to add players.")
      else:
        await message.channel.send("Night "+ str(currentNight) + " has started")
        global night
        night = True

    if message.content.startswith('$kill'): #werewolves kill
      players = []
      if message.channel.name == "werewolves":
        global wolfKillsAvailable
        if night == True:
          if wolfKillsAvailable == True:
            for ppl in range(len(alive)):
              if(alive[ppl].find(": werewolf") == -1):
                players.append(alive[ppl].split(": ")[0])
              else:
                continue
            playerKilled = message.content[6:]
            if " " not in playerKilled:
              if playerKilled in players: 
                kill(playerKilled) 
                await message.channel.send("ok")
                wolfKillsAvailable = False
                actionsFinished = checkFinishedActions()
                if actionsFinished == True:
                  await admins.send("all actions are complete. $nightend to end the night.")
              else:
                await message.channel.send("player does not exist/dead/is a werewolf")
            else:
              await message.channel.send("include 1 person after $kill")
              playerKilled = ""
          else: 
            await message.channel.send("you already killed tonight")
        else:
            await message.channel.send("you can't kill in the morning")
      else:
        if message.channel.name == "witch":
          global witchKillAvailable
          if night == True:
            if witchKillAvailable == True:
              for ppl in range(len(alive)):
                if(alive[ppl].find(": witch") == -1):
                  players.append(alive[ppl].split(": ")[0])
                else:
                  continue
              playerKilled = message.content[6:]
              if " " not in playerKilled:
                if playerKilled in players:
                  kill(playerKilled) 
                  await message.channel.send("ok")
                  witchKillAvailable = False
                  actionsFinished = checkFinishedActions()
                  if actionsFinished == True:
                    await admins.send("all actions are complete. $nightend to end the night.")
                else:
                  await message.channel.send("player does not exist/dea/is a witch")
              else:
                await message.channel.send("include 1 person after $kill")
                playerKilled = ""
            else: 
              await message.channel.send("you already killed as a witch")
          else:
            await message.channel.send("you can't kill in the morning")
        else:
          if message.channel.name == "hunter":
            global hunterKillAvailable
            if night == True:
              if hunterKillAvailable == True:
                for ppl in range(len(alive)):
                  if(alive[ppl].find(": hunter") == -1):
                    players.append(alive[ppl].split(": ")[0])
                  else:
                    continue
                playerKilled = message.content[6:]
                if " " not in playerKilled:
                  if playerKilled in players:
                    kill(playerKilled) 
                    await message.channel.send("ok")
                    hunterKillAvailable = False
                    actionsFinished = checkFinishedActions()
                    if actionsFinished == True:
                      await admins.send("all actions are complete. $nightend to end the night.")
                  else:
                    await message.channel.send("player does not exist/dead/is a hunter")
                else:
                    await message.channel.send("include 1 person after $kill")
                    playerKilled = ""
              else: 
                  await message.channel.send("you already killed as a hunter")
            else:
                await message.channel.send("you can't kill in the morning")
          else:
            if message.channel.name != "witch" and message.channel.name != "werewolves" and message.channel.name != "hunter":
              await message.channel.send("you can't kill dumbass")

    if message.content.startswith('$vote'): #vote
      players = []
      if message.channel.name == "voting":
        if night == False:
          #if message.author.id not in votersArray:
            if votingFinished == False:
              for ppl in range(len(alive)):
                players.append(alive[ppl].split(": ")[0])
              playerVotedFor = message.content[6:]
              if " " not in playerVotedFor:
                if playerVotedFor in players:
                  votersArray.append(message.author.id)
                  vote(playerVotedFor)
                  await message.channel.send(playerVotedFor + " now has " + str(votedArray[playerVotedFor])+ " votes")
                else:
                  await message.channel.send("player does not exist/dead")
              else:
                await message.channel.send("include 1 person after $vote")
            else:
              await message.channel.send("Voting Finished. $currentinfo to see status of game")
          #else:
            #await message.channel.send("you already voted")
        else:
            await message.channel.send("you can't vote at night")
      else:
        await message.channel.send("you can't vote in this channel")

    if message.content.startswith('$seer'): #seer seers
      players = []
      if message.channel.name == "seer":
        global seerAvailable
        if night == True:
          if seerAvailable == True:
            for ppl in range(len(alive)):
              if(alive[ppl].find(": seer") == -1):
                players.append(alive[ppl].split(": ")[0])
              else:
                continue
            playerSeered = message.content[6:]
            if " " not in playerSeered:
              if playerSeered in players:
                seerAvailable = False
                actionsFinished = checkFinishedActions()
                if actionsFinished == True:
                  await admins.send("all actions are complete. $nightend to end the night.")
                if seerPlayer(playerSeered) == True:
                  await message.channel.send("on wolf's side")               
                else:
                  await message.channel.send("not on wolf's side")
              else:
                await message.channel.send("player does not exist/dead/is a seer")
            else:
              await message.channel.send("include 1 person after $seer")
              playerSeered = ""
          else: 
            await message.channel.send("you already seered tonight")
        else:
            await message.channel.send("you can't seer in the morning")
      else:
        await message.channel.send("you can't seer dumbass")

    if message.content.startswith('$save'): #bodyguard saves
      players = []
      if message.channel.name == "bodyguard":
        global saveAvailable
        if night == True:
          if saveAvailable == True:
            for ppl in range(len(alive)):
                players.append(alive[ppl].split(": ")[0])
            playerSaved = message.content[6:]
            if " " not in playerSaved:
              if playerSaved in players:
                save(playerSaved)
                await message.channel.send("ok")
                saveAvailable = False
                actionsFinished = checkFinishedActions()
                if actionsFinished == True:
                  await admins.send("all actions are complete. $nightend to end the night.")
              else:
                await message.channel.send("player does not exist/dead")
            else:
              await message.channel.send("include 1 person after $save")
              playerSaved = ""
          else: 
            await message.channel.send("you already saved someone tonight")
        else:
            await message.channel.send("you can't be a bodyguard in the morning")
      else:
        if message.channel.name == "witch":
          global witchSaveAvailable
          if night == True:
            if witchSaveAvailable == True:
              for ppl in range(len(alive)):
                players.append(alive[ppl].split(": ")[0])
              playerSaved = message.content[6:]
              if " " not in playerSaved:
                if playerSaved in players:
                  save(playerSaved)
                  await message.channel.send("ok")
                  witchSaveAvailable = False
                  actionsFinished = checkFinishedActions()
                  if actionsFinished == True:
                    await admins.send("all actions are complete. $nightend to end the night.")
                else:
                  await message.channel.send("player does not exist/dead")
              else:
                await message.channel.send("include 1 person after $save")
                playerSaved = ""
            else: 
                await message.channel.send("you already saved this game")
          else:
              await message.channel.send("you can't save in the morning")
        else:
          if message.channel.name != "witch" and message.channel.name != "bodyguard":
            await message.channel.send("you can't save people dumbass")

    if message.content.startswith('$pair'): #cupid hooksup
      players = []
      if message.channel.name == "cupid":
        global hookupAvailable
        if night == True:
          if hookupAvailable == True:
            for ppl in range(len(alive)):
                players.append(alive[ppl].split(": ")[0])
            playersPaired = message.content[5:].split( )
            check =  all(item in players for item in playersPaired)
            if len(playersPaired) == 2 and playersPaired[0] != playersPaired[1]:
              if check == True:
                hookup(playersPaired)
                await message.channel.send(playersPaired[0].split(": ")[0]+  " and " +playersPaired[1].split(": ")[0] + " are now paired")
                hookupAvailable = False
                actionsFinished = checkFinishedActions()
                if actionsFinished == True:
                  await admins.send("all actions are complete. $nightend to end the night.")
              else:
                await message.channel.send("players do not exist/dead")
            else:
              await message.channel.send("include 2 people after $hookup")
          else: 
            await message.channel.send("you already paired people tonight")
        else:
            await message.channel.send("you can't be a cupid in the morning")
      else:
        await message.channel.send("you can't pair people up dumbass")

    if message.content.startswith('$noaction'):
      if message.channel.name == "witch":
        await message.channel.send("ok")
        global witchNoAction
        witchNoAction = True
        actionsFinished = checkFinishedActions()
        if actionsFinished == True:
          await admins.send("all actions are complete. $nightend to end the night.")
      if message.channel.name == "hunter":
        await message.channel.send("ok")
        global hunterNoAction
        hunterNoAction = True
        actionsFinished = checkFinishedActions()
        if actionsFinished == True:
          await admins.send("all actions are complete. $nightend to end the night.")
      if message.channel.name == "cupid":
        await message.channel.send("ok")
        global cupidNoAction
        cupidNoAction = True
        actionsFinished = checkFinishedActions()
        if actionsFinished == True:
          await admins.send("all actions are complete. $nightend to end the night.")

    if message.content.startswith('$nightend') and message.channel.name == "admins": #admins end night (shows who is alive and not alive)
      if checkNight() == True:
        determineDeadAlive();
        await message.channel.send("DEAD: ")
        for x in range(len(dead)):
          await message.channel.send(dead[x])
        await message.channel.send("ALIVE: ")
        for x in range(len(alive)):
          if (alive[x]== " "):
            continue
          else:
            await message.channel.send(alive[x])
        await message.channel.send("------------------------")
        advanceNight();
        night = False
        gameEnded = checkGameEnd();
        global winner
        if gameEnded == True:
          await message.channel.send("Game Over")
          await message.channel.send(winner + " wins")
          if message.channel.name != "admins":
            await message.channel.send("Game ended. Winner is " + winner + ". waiting for admins to start new game.")
          else:
            await admins.send("Start new game with $startgame")

      else:
        await message.channel.send("you haven't started the night yet")

    if message.content.startswith('$currentinfo') and message.channel.name != "admins": #for everyone to see current status of the game
      printedArrayAlive = []
      printedArrayDead = []
      for x in range(len(dead)):
        printedArrayDead.append(dead[x].split(": ")[0])
      await message.channel.send("DEAD: " + str(printedArrayDead)[1:-1].replace("'", ""))
      for x in range(len(alive)):
        if (alive[x]== " "):
          continue
        else:
          printedArrayAlive.append(alive[x].split(": ")[0])
      random.shuffle(printedArrayAlive)
      await message.channel.send("ALIVE: " + str(printedArrayAlive)[1:-1].replace("'", ""))
    
    if votingFinished == True:
      global tiedVoting
      if messagedVotingDone == False:
        await message.channel.send("Voting Done.")
      if tiedVoting == True:
        await message.channel.send("Voting tied. Noone died.")
      gameEnded = checkGameEnd();
      messagedVotingDone = True
      tiedVoting = False
      if gameEnded == True:
        await message.channel.send("Game Over")
        await message.channel.send(winner + " wins")
        await admins.send("Game Over. Werewolves win. $startgame to start new game.")

  else:
    if gameEnd == True:
      if message.content.startswith('$startgame') and message.channel.name == "admins":
        await message.channel.send("restart in progress...")
        alive.clear()
        dead.clear()
        rolesAllocated.clear()
        cupidPairedPlayers.clear()
        savedPlayers.clear() 
        killedPlayers.clear() 
        votersArray.clear() 
        votedArray.clear()
        resetGlobals()
        await message.channel.send("restart finished. you can now add new players")
      else:
        if message.content.startswith('$')and message.channel.name != "admins":
          await message.channel.send("Game ended. Winner is " + winner + ". Waiting for admins to start new game.")


  #game cycle: $addplayers, $nightstart, $kill/$save/$seer, $nightend, $vote
  
  

client.run(os.environ['TOKEN'])
