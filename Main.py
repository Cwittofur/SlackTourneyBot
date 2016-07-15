import os
import time
from slackclient import SlackClient
from UserList import *
from Ships import getShip
import re

BOT_ID = "U1N6SRX3K"

AT_BOT = "<@" + BOT_ID + ">:"

messageQueue = []
players = []
botChannel = ""
shipType = []

#  slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def sendMessage(message, channel="C1N5RB2RE"):
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=message, as_user=True)


def getUserName(userID):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # find our user name based on its ID
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('id') == userID:
                return user['name']
    else:
        return None


def getShipTypeID(m):
    if "frigate" in m:
        return 1
    elif "destroyer" in m:
        return 2
    elif "cruiser" in m:
        return 3
    else:
        return 0


def getFactionID(f):
    if "amarr" in f:
        return 1
    elif "caldari" in f:
        return 2
    elif "gallente" in f:
        return 3
    elif "minmatar" in f:
        return 4
    else:
        return 0


def processMessageQueue():
    for item in messageQueue:
        sendMessage(item)
        # time.sleep(0.125)  # Queue messages instead of blasting the server.
    messageQueue.clear()


def printUserList():
    userlist = getUserList()
    message = "{}".format(userCount()) + " users have entered:\n"
    for user in userlist:
        message += "{} ".format(getUserName(user))

    sendMessage(message)


def getRandomType():
    return random.randrange(1, 3)


def getWinners(numWinners):
    winnerList = []
    for x in range(0, numWinners):
        winner = getWinner()
        deleteUser(winner)
        winnerList.append(winner)
    return winnerList


def matchup(shiptype, factionid, teamsize):
    global players
    players = getWinners(teamsize * 2)
    global shipType
    shipType = shiptype
    for user in players:
        userShip = getShip(shiptype, factionid)
        message = "@{}".format(getUserName(user)) + " you fly a {}".format(userShip)
        dmChannel = slack_client.api_call("im.open", user=user)
        slack_client.api_call("chat.postMessage", channel=dmChannel["channel"]["id"], text=message, as_user=True)

    if teamsize == 1:
        messageQueue.append("{}".format(getUserName(players[0])) + " will battle against {}".format(getUserName(players[1])))
    else:
        messageQueue.append("The teams are as follows: ")
        teamMessage = ""
        for player in range(0, teamsize):
            teamMessage += getUserName(players[player]) + " "
        teamMessage += "VS. "
        for player in range(teamsize, teamsize * 2):
            teamMessage += getUserName(players[player]) + " "

        messageQueue.append(teamMessage)

    processMessageQueue()


def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = ""
    if command.startswith("!enter"):
        uName = getUserName(user)
        if addUser(user):
            sendMessage("@{} entered".format(uName))
    elif command.startswith("!reset"):
        resetUsers()
        sendMessage("User List reset, please type `!enter` if you'd like to participate")

    elif command.startswith("!forfeit"):
        deleteUser(user)
        sendMessage("{}".format(getUserName(user)) + " has decided to forfeit!")

    elif command.startswith("!matchup"):
        if userCount() < 2:
            sendMessage("Not enough users for 1v1.")
            printUserList()
        else:
            shipTypeID = getShipTypeID(command)
            shipFactionID = getFactionID(command)
            if shipTypeID == 0:
                shipTypeID = getRandomType()
            matchup(shipTypeID, shipFactionID, 1)

    elif command.startswith("!team"):
        size = int(re.search(r"\d", command).group(0))
        if userCount() < size * 2:
            sendMessage("Not enough users for {}".format(size) + "v{}".format(size))
            printUserList()
        else:
            shipTypeID = getShipTypeID(command)
            shipFactionID = getFactionID(command)
            if shipTypeID == 0:
                shipTypeID = getRandomType()
            matchup(shipTypeID, shipFactionID, size)

    elif command.startswith("!mulligan"):
        if user in players:
            message = "@{}".format(getUserName(user)) + " you fly a {}".format(getShip(shipType, getFactionID(command)))
            dmChannel = slack_client.api_call("im.open", user=user)
            slack_client.api_call("chat.postMessage", channel=dmChannel["channel"]["id"], text=message, as_user=True)
            sendMessage("{}".format(getUserName(user)) + " chose to mulligan!")
            players.remove(user)

    elif command.startswith("!list"):
        printUserList()

    elif command.startswith("!help"):
        helpMessage = "Welcome to the tourney bot! To enter into the drawing please type `!enter`\n" \
                      "To get a 1v1 match type `!matchup` or `!team 1`\n" \
                      "`!team x` where x is the team size.\n" \
                      "`!team 3` will create a 3v3 match\n" \
                      "You may also specify Faction and/or Ship Type.\n" \
                      "For example: `!matchup amarr cruiser` will do a 1v1 with Amarr Cruisers\n" \
                      "You can also have it random the faction or the ship type.\n" \
                      "Current supported ship types are: frigate, destroyer, cruiser" \
                      "You can `!mulligan` ONCE to re-randomize your ship."
        sendMessage(helpMessage)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message
        begins with !
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and "!" in output['text']:  # and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'], \
                       output['channel'], output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = .001  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("TourneyBot connected and running!")
        while True:
            command, botChannel, user = parse_slack_output(slack_client.rtm_read())
            if command and botChannel:
                handle_command(command, botChannel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

