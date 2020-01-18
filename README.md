# FundsFeesTracker
A tracker app to follow the fees required by the funds you own. No more surprises or "under the radar" increse in fees.
Once deployed, the app will check the "nihol" and "nemanut" fees for all fund numbers provided to it and will inform you about any changes in the fees.  
***Note: the app uses www.funder.co.il/ to acquire information regarding the fees and thus bound to the update routine of this website.***

The app supports two types of notifications: **pushbullet** and **output to textfile**.

## Deployment stages: ##
  1. Create a csv file with all the funds numbers and the current fees. An example for the correct csv structure is attached.
  2. Choose which type of notifications you prefer. 
For pushbullet usage you will need to provide a pushbullet key. More details on the pushbullet app and key here: https://www.pushbullet.com. 
For output to file you need to provide a full path to the file. The notifictions will be appended and not over-written.
  3. Make sure you have all the python required packages installed. Check the "requirments.txt for the list of required packages. I highly recommend using Conda for enviroment and library managment: https://www.anaconda.com/ 
  4. Run the python script with the required **arguments**:

      -h, --help            show this help message and exit

      --mode {file,push}    Choose your output form, "file" (default) to write to
                            file or "push" for pushbullet

      --test {on,off}       Run in test mode to check that it works

      --p_key PUSHBULLET_KEY
                            Your pushbullet key (optional). Only if mode is push

      --funds FUNDS_INFO_FILE
                            Full path to funds csv file. default: funds_fees.csv
                            (searches in current directory)

      --o OUTPUT_FILE       Full path to output file (optional). Only if mode is
                            "file"
                        
  ## Usage examples ## 
  ***Run test mode and output to my_outfile.txt:*** 
  
  python funds_tracker.py --mode file --test on --o FULL/PATH/TO/FILE/my_outfile.txt
  
  
  ***Run ,read the csv from a different dir and get notification by pushbullet:***
  
  python funds_tracker.py --mode push --p_key MYPUSHBULLETKEY --funds FULL/PATH/TO/FILE/funds_fees.txt
  
  ## Additional options ##
  It is very convinient and recommended to use scheduled deployment of the script to "run and forget".
  The basic steps for windows:
  1. Wrap the execution line with a .dat file.
  2. Use the windows task scheduler to schedule and deploy the script.
  Read more about task scheduler: https://www.windowscentral.com/how-create-task-using-task-scheduler-command-prompt
  
  The basic steps for Linux:
  1. Wrap the execution line with a .sh file.
  2. Use crontab to schedule the script.
  Read more about crontab usage: https://www.computerhope.com/unix/ucrontab.htm
