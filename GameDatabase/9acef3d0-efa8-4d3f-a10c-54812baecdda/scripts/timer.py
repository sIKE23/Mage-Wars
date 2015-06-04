import time

"""
Long term, this code should be moved to the main file. I am writing it in a separate
file so that it is easy to handle when merging the different branches.
"""

#This function lets the player set a timer
def setTimer(group,x,y):
        startTime = time.time()
        minutes = askInteger("Set timer for how many minutes?",3)
        notify("{} sets a timer for {} minutes.".format(me,minutes))
        seconds = 60*minutes
        endTime = startTime + seconds
        notifications = [endTime-x*60 for x in range(int(minutes))]
        updateTimer(endTime,notifications)

#This function checks the timer, and then remotecalls itself if the timer has not finished
#As it turns out, this works even with 1 player so...basically, it is the perfect timer!
def updateTimer(endTime,notifications):
        mute()
        currentTime = time.time()
        if currentTime>notifications[-1]:
                notify("{} minutes left!".format(int((endTime-notifications[-1])/60)))
                notifications.remove(notifications[-1])
        if notifications: remoteCall(me,"updateTimer",[endTime,notifications])
        else: notify("Time's up!")
