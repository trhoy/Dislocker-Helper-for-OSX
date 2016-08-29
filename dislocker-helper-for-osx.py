import sys
import os
import errno
import traceback
import subprocess
import re
import getpass

#NOTE: Made with Python 2.7.10 in mind
#NOTE: Dislocker is a prerequisite to running this program (https://github.com/Aorimn/dislocker)
#NOTE: Also, this program only supports Bitlocker drives that are only encrypted with a password but NOT a key
def main():
	try:
		if os.getuid() == 0:
		
			# Get the bitlocker disk name
			disk_name = getDiskName();
			print "Possible bitlocker drive found: /dev/" + disk_name
			
			# Create a new, mountable dislocker drive
			password = getEscapedPassword()
			dislockerSetup(disk_name, password)
			mountable_drive = createBlockDevice()
			print "Drive now mountable on " + mountable_drive + "."
			
			print "Mounting drive..."
			if mountDrive(mountable_drive):
				print "Drive mounted successfully!"
			
		else:
			raise Exception(errno.EPERM)
	except Exception as error:
		if (error[0] == errno.EPERM):
			print "You must have root permissions to run this script. Try using \"sudo\"."
			sys.exit(1)
		else:
			traceback.print_exc(file=sys.stdout)
	
def getDiskName():
	current_command = "diskutil list"
	output = subprocess.check_output(current_command.split())
	regex = ".+(Microsoft Basic Data)\s\s.+"
	bitlocker_line_regex_match = re.search(regex, output)
		
	if not bitlocker_line_regex_match:
		raise Exception("No possible bitlocker drives were found...")
		
	bitlocker_line = bitlocker_line_regex_match.group(0)
	disk_string =  bitlocker_line.split()[-1]
	return disk_string
	
def getEscapedPassword():
	password = getpass.getpass(prompt="Please enter your bitlocker drive's password: ")
	password = re.escape(password)
	return password
	
def dislockerSetup(disk_name, password):
	if not disk_name or not password:
		raise Exception("No disk name and/or password was given. Abort.")

	if not os.path.isdir("/tmp/bitlocker"):
		current_command = "mkdir /tmp/bitlocker"
		subprocess.check_output(current_command.split())
	
	current_command = "dislocker -v -V /dev/" + disk_name + " -u" + password + " -- /tmp/bitlocker"
	output = subprocess.Popen(current_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = output.communicate()
	
	# Check to make sure the bitlocker-file file was created as expected
	if not os.path.isfile("/tmp/bitlocker/dislocker-file"):
		raise Exception("There was an error when trying to access the drive. Check your password and try again.")
		
# http://linux.die.net/man/1/dislocker
def createBlockDevice():
	current_command = "sudo hdiutil attach -imagekey diskimage-class=CRawDiskImage -nomount /tmp/bitlocker/dislocker-file"
	output = subprocess.Popen(current_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = output.communicate()
	return output.strip("\n").strip()
	
def mountDrive(mountable_drive):
	# Create destination for mount
	if not os.path.isdir("/Volumes/bitlocker"):
		current_command = "mkdir /Volumes/bitlocker"
		subprocess.check_output(current_command.split())
		
	# Mount the new drive
	current_command = "mount -t ntfs " + mountable_drive + " /Volumes/bitlocker"
	subprocess.Popen(current_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return True
	
if __name__ == "__main__":
	main()