#**TelegramAutomationBot**
---
###Bot for automating work with the tweeter audience
---
##User Profile:
Each user can add multiple accounts to their profile.
For each account, the user can set the status as active or inactive.
The user can also add a specific number of keys required for the bot's proper functioning.
---
##Bot Initialization:
Once the bot is added and all the necessary data is filled in, it can be launched.
---
##Bot's Twitter Actions:
After the bot is launched, it will authenticate itself on Twitter using the account specified in the user's profile.
The bot will enter a keyword in the search field, which was previously set in the account settings.
The bot will subscribe to (follow) the users that appear in the search results.
Additionally, the bot will like the three most recent posts of the subscribed users.
These actions will be repeated several times during a single bot run.
---
##User Interaction Check:
After three hours of subscribing to a user, the bot will check if the user has reciprocated the subscription.
If the user has not subscribed back, the bot will unsubscribe from the user and remove the likes.
