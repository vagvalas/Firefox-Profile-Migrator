# Firefox Profile Migrator
Backup Copy and Restore Firefox's profile data


# Purpose

Always wanted to automate a way of copying Firefox (my main browser) profiles aroung my PCs, or even when i format a pc to restore the backup of a profile.
All those years i thought (as searched everywhere) that just copy-pasting the whole Profile folder will be okay.
It is, BUT:

have some inconsistencies,
1. Version missmatches of profile copied and actual firefox binary installed version, (if you have a newer for some reason profile and not updated firefox, the Firefox refuses to load the Profile)
2. The UserAgent always stays the same. :P So if you had copied from a Windows 10, to Windows 11, or vice-versa the UA String will always point to the original profile UA, not able to update the string. (ALSO, the version never changes automatically, so it stays Always (Firefox;111) as of original
   profile version and not updated by app.


# Usage

Backup - Restore or just copy.

For backup navigate to your %APPDATA% folder and backup it to a safe destination

1. Just select the Source and it will automatically search which files are there and can be copied. Have some sub-files for categories that has more than one, but i think we need all..
2. Choose the dest folder.
3. Hit GO
4. Proof!



For Restoring backup, as it's not straightforward with the buttons.

1. You can choose the exported folder as Source
2. And choose the Destination for %APPDATA%, so to overwrite the data and (restore your old one)

# Thoughts
MANY!
Needed it a long time.
I think it can work right away also on macos.
I didnt test to overwrite to %APPDATA% (restore functionality) , (maybe it need to be run as administrator)
For that reason also wrote to python for cross-platform. My original though was to be written in my fav C#.


# Things to do
## Sure: Check all toggle to toggle all files
## Auto-Detect intalled profiles (maybe only for windows) , and choosing which to backup
## An option for zipping. ( i don't know for un-zipping), do it yourself :P

Feel free to help me out with pull requests.
I think that software in final form, with all platforms support, backing up, restoring , zipping , unzipping, auto-detecting, safe-backuping, and list of versions.
Will BE a must tool for all Firefox's users.
