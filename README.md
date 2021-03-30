# screenshot-warning
Automated warning message (via email or Slack) based on color of point on screenshot. Example use-case for equipment errors. Code in Python


At work, we have equipment with different levels of logging and error messaging. For automated overnight processes, it is better to have some kind of email or other automatic communication from the system to let you know when a process has failed instead of needing someone to watch the tool or check on it throughout the night. Some systems don't provide that, or an easy way to connect to the software. I came up with a quick little script to send automated alerts when the process indicator turns red on the sequence screen of one of my tools. This speeds up the evening operator's intervention and makes it so someone doesn't have to watch the process throughout the evening. 

![example screenshot](/ExampleScreenshot.png)


Automated slack message

![example slack message](/slackmessage.PNG)


## Screenshot 
Using the Pillow module in Python you can easily take a screengrab and save the image. If you open the image in Paint or some other photo editor you can get the pixel position you want to check color on and then add that x,y pixel position to your code. If you don't know the RGB color values for the color you are trying to find and compare against, one easy way is to put the image in powerpoint and use the color dropper tool to get the color (many other ways to do this as well). 

## Send an email
For sending either a simple email or an email with the image attached. I followed the instructions [here](https://realpython.com/python-send-email/) to set up a dedicated gmail account and used the code provided. I set up my email addresses and passwords in a separate config.py file that I import. 

## Send Slack message
I followed the instructions from Slack's website to install the Slack SDK. I set up authetication to get an authorization token and set up permissions for my message app (allow to post to a channel that the app was invited to). The basic sending a message code from [here](https://slack.dev/python-slackclient/basic_usage.html) is what I edited and used.

## Automating the code running
I used Windows task scheduler to set the code to run every 5 minutes by setting up a batch file. Unfortunately, whenever the batch file would run, it would open the command window in front of the pixels I was trying to get the color for, so I needed a way to run the script without the command window opening. I was able to do this by putting the batch file inside a VBScript file that does not open the command prompt. In task scheduler, if you select the option to run the file even when not logged in, it won't open the command prompt either, but I had many issues with directory and file access permissions going that route, that was making my batch file fail to run. Examples of both my .bat and .vbs files are in the repository. I put the vbs file into the task scheduler. 
