# This function is how Alexa can determine what should happen next and what to output for the user in-game.
# As seen it is returning a JSON of information for Alexa to save for the users next command. Along
# with telling Alexa what to say in response.
def speak(string,state,location="Blacksburg",Three_Star=False,Four_Star=False,ending=False):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech":{
                "type": "PlainText",
                "text": string
            },
            "shouldEndSession": ending
        },
        "sessionAttributes": {
            "gameState": state,
            "location": location,
            "3 star recruit": Three_Star,
            "4 star recruit": Four_Star
        }
    }


# This is the introduction function that tells each player how to play the game and sets the state of the game.
# It teaches the user the goal of the game and the general sequence to follow.
def print_introduction(state):
    return speak("""You have just been hired to coach Amazon University football! 
    In order to succeed as head coach you need to get a commitment from a 5 Star recruit. 
    However, this five star recruit needs to be convinced! Along with this 5 Star recruit,
    a 4 Star recruit also needs some more convincing. 
    Go on the recruiting trail and build your roster for next year. You can visit 
    the three star recruit, the four star recruit, and the five star recruit. 
    Once at the recruits home you can either stay there, return home, or visit one of the other recruits.""",state)
    
# This handles the basic logic of the game
# Event contains all the users information about their current state in the game. This is important because everytime a user
# speaks a command they are essentially running another instance of this script, so all their data must be saved and returned to Alexa before
# they give their next command.
def main(event, context):
    # Sets the state for Alexa, this value gets passed in the print_introduction method
    state = "playing"
    # Sets the player at home. Go Hokies!
    location = "Blacksburg"
    Three_Star = False
    Four_Star = False
    # This handles the players state so the script can tell where they are in the game each time they give a command
    if "attributes" in event["session"]:
        state = event["session"]["attributes"]["gameState"]
        location = event["session"]["attributes"]["location"]
        Three_Star = event["session"]["attributes"][ "3 star recruit"]
        Four_Star = event["session"]["attributes"][ "4 star recruit"]
    # If this is a new game, ie the game is being launched, the introduction is printed out and continued
    if event["request"]["type"] == "LaunchRequest":
        return print_introduction(state)
    # If the user has already started a game this is where their voice commands are handled
    elif event["request"]["type"] == "IntentRequest":
        # Get's the users intent
        intent = event["request"]["intent"]["name"]
        # If they quit the game it will exit for them
        if intent == "quitIntent":
            return speak("You have quit",state,location,Three_Star,Four_Star,True)
        # This is the visit intent. 
        if intent == "Visit":
            rating = event["request"]["intent"]["slots"]["RatingSlot"]["value"]
            if rating == str(3):
                if location == "3*":
                    return speak("You cannot do that, you are already at the home of the three star recruit.",state,location,Three_Star,Four_Star)
                if Three_Star == False:
                    Three_Star = True
                    location = "3*"
                    return speak("Congratulations you have gained a three star commitment! You are currently at the home of the three star recruit.",state,location,Three_Star,Four_Star)
                else:
                    location = "3*"
                    return speak("Coach I am glad you came back, but go find more recruits! You are currently at the home of the three star recruit.",state,location,Three_Star,Four_Star)
            if rating == str(4):
                if location == "4*":
                    return speak("You cannot do that, you are already at the home of the four star recruit.",state,location,Three_Star,Four_Star)
                if Three_Star == False:
                    location = "4*"
                    return speak("Coach, you need more recruits before I can commit. You are currently at the home of the four star recruit.",state,location,Three_Star,Four_Star)
                if Three_Star == True:
                    if Four_Star == False:
                        Four_Star = True
                        location = "4*"
                        return speak("Congratulations you have gained a four star commitment! You are currently at the home of the four star recruit.",state,location,Three_Star,Four_Star)
                    else:
                         return speak("Coach I am glad you came back, but go find more recruits! You are currently at the home of the four star recruit.",state,location,Three_Star,Four_Star)
            if rating == str(5):
                if location == "5*":
                    return speak("You cannot do that, you are already at the home of the five star recruit.",state,location,Three_Star,Four_Star)
                if Three_Star == False:
                    location = "5*"
                    return speak("The 5 star recruit is extremely disappointed you have not landed anymore recruits. He tells you he is no longer interested. Fans and administrators alike are so disappointed you are quickly fired...",state,location,Three_Star,Four_Star,True)
                if Three_Star == True:
                    if Four_Star == False:
                        location = "5*"
                        return speak("Coach, you need more recruits before I can commit You are currently at the home of the five star recruit.",state,location,Three_Star,Four_Star)
                    if Four_Star == True:
                        return  speak("Congratulations, you have just received a 5 star commitment! Amazon University fans and administrators are both equally happy! You future is looking very bright!",state,location,Three_Star,Four_Star,True)
                else:    
                    return speak("Coach I am glad you came back, but go find more recruits! You are currently at the home of the four star recruit.",state,location,Three_Star,Four_Star)
        if intent == "ReturnHome":
            if location != "Blacksburg":
                location = "Blacksburg"
                return speak("You are now home in Blacksburg",state,location,Three_Star,Four_Star)
            else:
                return speak("You are already in Blacksburg!",state,location,Three_Star,Four_Star)
        if intent == "Stay":
            if location == "3*":
                return speak("Coach, I am already committed, go find more recruits! You are currently at the home of the three star recruit",state,location,Three_Star,Four_Star)
            if location == "4*":
                if Three_Star == False:
                    return speak("Coach, I told you, you need more recruits before I can join! You are currently at the home of the four star recruit",state,location,Three_Star,Four_Star)
                else:
                    return speak("Coach I am already committed! Go find more recruits! You are currently at the home of the four star recruit",state,location,Three_Star,Four_Star)
            if location == "5*":
                return speak("Coach, I told you, you need more recruits before I can join! You are currently at the home of the five star recruit",state,location,Three_Star,Four_Star)
                
        else:
            # Handles an unknown command
            return speak("please try again",state,location,Three_Star,Four_Star)