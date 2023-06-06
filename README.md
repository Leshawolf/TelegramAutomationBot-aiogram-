# **TelegramAutomationBot**
### Bot for automating work with the tweeter audience
---
## User Profile:
#### Each user can add multiple accounts to their profile. For each account, the user can set the status as active or inactive. The user can also add a specific number of keys required for the bot's proper functioning.

## Bot Initialization:
#### Once the bot is added and all the necessary data is filled in, it can be launched.

## Bot's Twitter Actions:
#### After the bot is launched, it will authenticate itself on Twitter using the account specified in the user's profile. The bot will enter a keyword in the search field, which was previously set in the account settings. The bot will subscribe to (follow) the users that appear in the search results. Additionally, the bot will like the three most recent posts of the subscribed users. These actions will be repeated several times during a single bot run.

## User Interaction Check:
#### After three hours of subscribing to a user, the bot will check if the user has reciprocated the subscription. If the user has not subscribed back, the bot will unsubscribe from the user and remove the likes.

## Logical structure of use
![AutomationBot_Logic_Shema](https://github.com/Leshawolf/TelegramAutomationBot/assets/74571120/29e6c389-9cea-400a-8098-965b3890fc99)

## Database Structure
1. Table "tweeter_subscriptions":
>- id (int) / Null - no / auto_increment
>- tgID_user (text) / Null - no
>- id_acc_sub (text) / Null - no
>- username_suv (text) / Null - no
>- id_sub (text) / Null - no
>- date (datetime) / Null - no
>- status (tinyint(1)) / Null - no

2. Table "twitter_key":
>- id (int) / Null - no / auto_increment
>- tgID_user (text) / Null - no
>- name_account (text) / Null - no
>- api_key (text) / Null - yes
>- api_secret (text) / Null - yes
>- bearer_key (text) / Null - yes
>- access_token (text) / Null - yes
>- access_secret (text) / Null - yes
>- keyword (text) / Null - yes
>- status (tinyint(1)/ Null - no

3. Table "tweeter_subscriptions":
>- id (int) / Null - no / auto_increment
>- telegramID (text) / Null - no
>- username (text) / Null - no
>- language (text) / Null - yes

## Disadvantages/bugs
#### - Works exclusively with V2 keys
#### - If a user replaces the keys in an account that has already subscribed to someone but has not received a reciprocal subscription yet, the bot may malfunction or stop working. This is because the bot will continue using the old keys for checking the reciprocal subscription, while the account will be using the new keys. As a result, authentication and interaction with the Twitter API can be disrupted. To avoid such situations, it is recommended to check and update the keys in the bot's accounts only after completing the reciprocal subscription check or block the ability to change keys if the bot has not been run for the past 3 hours.

### All the necessary libraries for the correct operation of the bot are in the file "requarments.txt"
