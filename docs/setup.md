# Installation Guide

1- Open the terminal and clone the repository:
```bash
git clone <repository_url>
cd <repository_directory>
```
2- Install dependencies:

```bash
pip install -r requirements.txt
```

3- Go to the [Discord Developer Portal](https://discord.com/developers/home) and sign into your Discord account

4- Go to the "Applications" section and create a "New Application"

5- Select the newly created app and under overview menu, go to the "Bot" section

6- Check "Public Bot" if it is not checked.

7- Click on the "Reset Token" and copy it.

8- Create a file called ==.env== in the root directory of the project

9- Edit the ==.env== file to have your bot key as variable named ==TOKEN==

10- Paste your previously copied token
	Example: ==TOKEN=LZeB8R5S0QCGbWqkazf2iGtPR8eXKB==
	Note: *Never share your token with anyone for the safety of your bot*

11- Go back to previous **Bot** section and under **Privileged Gateway Intents** and check **Server Members Intent** and **Message Content Intent**

12- Go to **OAuth2** section under overview menu just above **Bot**

13- Under **Scopes** check the box that says ==bot==

14- Under **Bot Permissions** check these boxes:
	14.1- General Permissions:
		- Manage Roles
		- View Messages
	14.2-Text Permissions:
		- Send Messages
		- Create Public Threads
		- Send Messages in Threads
		- Manage Threads
		- Embed Links
		- Attach Files
		- Use External Emojis
		- Add Reactions
		- Create Polls

15-  Copy the generated URL at the bottom of the page and use it to invite the bot into your Discord guild.

16- Run bot.py
