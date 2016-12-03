#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arfedora-nvidiab.py
#
#  Copyright 2016 youcef sourani <youcef.m.sourani@gmail.com>
#
#  www.arfedora.blogspot.com
#
#  www.arfedora.com
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import subprocess
import platform
import sys
import time
from talwin import talwin

arch=platform.machine()
home=os.path.join("/home",os.getenv("LOGNAME"))
dirname=os.path.abspath(os.path.dirname(__file__))
fedora_versions=["25"]#,"24","23"]

def init_check():
	
	if os.getuid()==0:
		sys.exit("Run Script Without Root Permissions.")
		
	if platform.linux_distribution()[0]!="Fedora":
		sys.exit("Fedora Not Found.")
		
	if not sys.version.startswith("3"):
		sys.exit("Use Python 3 Try run python3 arfedora-nvidiab.py")
		
	if  platform.linux_distribution()[1] not in fedora_versions:
		sys.exit("Fedora Version Not Suppoerted.")
		







def check_vga_supported():
	count1=0
	count2=0
	sto1= subprocess.Popen("lspci |grep  VGA;lspci |grep 3D",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].decode('utf-8').strip().split()
	for word in sto1:
		if word=="VGA" or word=="3D":
			count1+=1
		if word=="Intel" or word=="NVIDIA":
			count2+=1

	if count1!=2 and count2!=2:
		sys.exit("VGA NOT SUPPORTED.")



init_check()
check_vga_supported()


def welcome():
	subprocess.call("clear")
	welcom="""
*******************************************************************
*[[[[[[[[[[[[[[[[[[[[[[[[          ~~~~~~~~~~~~~~~~~~~~~~~~~      *
*[[[[[[[[[[[[[[[[[[[[[[[[          ~~~~~~~~~~~~~~~~~~~~~~~~~      *
*{{{{{{{{{{{,{{{{{{{{{{{{          [{{{{{{{{{{{{{{{{{{{{{{{{      *
*{{{{{{{{{{,,,{{{{{{{{{{{          [[{{{{{{{{{{{{{{{{{{{{{{{      *
*{{{{{{{{{,,,,,{{{{{{{{{{          [[[{{{{{{{{{{{{{{{{{{{{{{      *
*{{{{{{{{,,,,,,,{{{{{{{{{          [[{{{{{{{{{{{{{{{{{{{{{{{      *
*{{{{{{{{{{,,,{{{{{{{{{{{          [{{{{{{{{{{{{{{{{{{{{{{{{      *
*[[[[[[[[[[[[[[[[[[[[[[[[          ,,,,,,,,,,,,,,,,,,,,,,,,,      *
*[[[[[[[[[[[[[[[[[[[[[[[[          ,,,,,,,,,,,,,,,,,,,,,,,,,      *
*                                                                 *
*Welcome to arfedora-nvidiab Copyright 2016 version 1.0           *
*youssef sourani <youssef.m.sourani@gmail.com>                    *
*www.arfedora.blogspot.com                                        *
*This is python script to install Bumblebee + Nvidia Driver       *
*fedora    link:http://spins.fedoraproject.org/                   *
*favorite  link:http://www.linuxac.org/forum/forum.php            *
*******************************************************************\n\n"""              

	for i in welcom:
		if i=="*":
			talwin(i,"blue",end='')
		elif i=="["  :
			talwin(i,"red",bg="red",end='')
		elif i=="~"  :
			talwin(i,"black",bg="black",end='')
		elif i=="{"  :
			talwin(i,"white",bg="white",end='')
		elif i==",":
			talwin(i,"green",bg="green",end='')
		else :
			talwin(i,"yellow",end='')


def __get_kernel_name():
	kernel=platform.release()
	if arch=="i686":
		if kernel.endswith("E"):
			return kernel[0:-4]
		return kernel
	else:
		return kernel

def install_kernel_devel():
	kernel=__get_kernel_name()
	subprocess.call("sudo dnf group mark remove c-development",shell=True)
	subprocess.call("sudo dnf group mark remove development-tools",shell=True)

	if arch=="x86_64":
		check=subprocess.call("sudo dnf -y --best install kernel-devel-%s  kernel-headers-%s \
		@c-development @development-tools"%(kernel,kernel),shell=True)
		if check!=0:
			return main("Error Check Your Connection || Check dnf || Update And Reboot System And Try Again.")
	else:
		check=subprocess.call("	sudo dnf -y --best install kernel-PAE-devel-%s kernel-devel-%s kernel-headers-%s \
		@c-development @development-tools"%(kernel,kernel,kernel),shell=True)
		if check!=0:
			return main("Error Check Your Connection || Check dnf || Update And Reboot System And Try Again.")



		

def install_rpmfusionrepos():
	check=subprocess.call("sudo dnf install  --best -y --nogpgcheck  http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm",shell=True)
	if check!=0:
		return main("Error Check Your Connection.")
		

def get_all_extensions():
	result=[]
	if os.path.isdir("%s/.local/share/gnome-shell/extensions"%home):
		for filee in os.listdir("%s/.local/share/gnome-shell/extensions"%home):
			if filee not in result:
				result.append(filee)

	if os.path.isdir("/usr/local/share/gnome-shell/extensions"):
		for filee in os.listdir("/usr/local/share/gnome-shell/extensions"):
			if filee not in result:
				result.append(filee)

	for filee in os.listdir("/usr/share/gnome-shell/extensions"):
		if filee not in result:
			result.append(filee)

	return result


def gnome_extensions():
	if os.getenv("XDG_CURRENT_DESKTOP")=="GNOME" :
		old_extension=get_all_extensions()
		os.makedirs("%s/.local/share/gnome-shell/extensions"%home,exist_ok=True)
		for f in os.listdir("%s/extensions"%dirname):
			if f not in old_extension:
				subprocess.call("cp -r %s/extensions/%s %s/.local/share/gnome-shell/extensions"%(dirname,f,home),shell=True)
			subprocess.call("gnome-shell-extension-tool -e  %s"%f,shell=True)
			time.sleep(1)
			
		check=subprocess.call("sudo dnf install  --best -y lm_sensors hddtemp",shell=True)
		if check!=0:
			return main("Error Check Your Connection.")
		subprocess.call("sudo sensors-detect --auto",shell=True)
	
		subprocess.call("dconf reset -f /org/gnome/shell/extensions/freon/",shell=True)
		time.sleep(1)
		subprocess.call("dconf write /org/gnome/shell/extensions/freon/gpu-utility \"\'bumblebee-nvidia-smi\'\"",shell=True)
	else:
		return main("Gnome Shell Desktop Not Found.")

	



def nvidia():
	install_kernel_devel()
	install_rpmfusionrepos()
	fedora_version=platform.linux_distribution()[1]
	arch=os.uname().machine
	remove_nouveau()
	
	check=subprocess.call("sudo dnf -y  --best install http://install.linux.ncsu.edu/pub/yum/itecs/public/bumblebee/fedora%s/noarch/bumblebee-release-1.2-1.noarch.rpm"%fedora_version,shell=True)
	if check!=0:
		return main("Error Check Your Connection.")

	check=subprocess.call("sudo dnf  -y  --best install http://install.linux.ncsu.edu/pub/yum/itecs/public/bumblebee-nonfree/fedora%s/noarch/bumblebee-nonfree-release-1.2-1.noarch.rpm"%fedora_version,shell=True)
	if check!=0:
		return main("Error Check Your Connection.")

	if arch!="x86_64":
		check=subprocess.call("sudo dnf -y  --best install bumblebee-nvidia bbswitch-dkms primus",shell=True)
		if check!=0:
			return main("Error Check Your Connection.")
	else:
		check=subprocess.call("sudo dnf -y  --best install bumblebee-nvidia bbswitch-dkms VirtualGL.x86_64 VirtualGL.i686 primus.x86_64 primus.i686",shell=True)
		if check!=0:
			return main("Error Check Your Connection.")

	subprocess.call("sudo touch /etc/sysconfig/nvidia/compile-nvidia-driver",shell=True)
	subprocess.call("sudo systemctl enable bumblebee-nvidia.service",shell=True)
	subprocess.call("sudo systemctl start bumblebee-nvidia.service",shell=True)
	subprocess.call("sudo systemctl enable dkms.service",shell=True)
	subprocess.call("sudo usermod -a -G bumblebee $USER",shell=True)
	
	

def remove_nvidia():
	subprocess.call("sudo dnf -y remove bumblebee-nvidia bbswitch-dkms  bumblebee primus --setopt clean_requirements_on_remove=false",shell=True)

def remove_nouveau():
	subprocess.call("sudo dnf -y remove bumblebee-nouveau bbswitch-dkms bumblebee  --setopt clean_requirements_on_remove=false",shell=True)


		
def troubleshoot_nvidia_1():
	fedora_version=platform.linux_distribution()[1]
	arch=os.uname().machine


	check=subprocess.call("sudo dnf -y  --best reinstall http://install.linux.ncsu.edu/pub/yum/itecs/public/bumblebee/fedora%s/noarch/bumblebee-release-1.2-1.noarch.rpm"%fedora_version,shell=True)
	if check!=0:
		return main("Error Check Your Connection.")

	check=subprocess.call("sudo dnf  -y  --best reinstall http://install.linux.ncsu.edu/pub/yum/itecs/public/bumblebee-nonfree/fedora%s/noarch/bumblebee-nonfree-release-1.2-1.noarch.rpm"%fedora_version,shell=True)
	if check!=0:
		return main("Error Check Your Connection.")

	if os.path.isdir("/etc/sysconfig/nvidia/"):
			subprocess.call("sudo rm -r  /etc/sysconfig/nvidia/* ",shell=True)

	nvidia()
	subprocess.call("sudo bumblebee-nvidia --debug --force",shell=True)
	
	
def troubleshoot_nvidia_2():
	subprocess.call("echo \"options bbswitch load_state=-1 unload_state=1\" |sudo tee /etc/modprobe.d/50-bbswitch.conf",shell=True)
	talwin("Please do not power off or unplug your machine.\n","red")
	subprocess.call(" sudo dracut -f",shell=True)
	
def undo_troubleshoot_nvidia_2():
	if os.path.isfile("/etc/modprobe.d/50-bbswitch.conf"):
		subprocess.call("sudo rm /etc/modprobe.d/50-bbswitch.conf",shell=True)
		talwin ("Please do not power off or unplug your machine.\n","red")
		subprocess.call(" sudo dracut -f",shell=True)
	else:
		return main("Nothing To Do.")
	

	
	
def msg(m):
	while True:
		subprocess.call("clear")
		print()
		talwin (m,"red")
		talwin("\nY To Continue || N To Back || Q To Quit : \n-","blue",end="")
		y_n=input().strip()
		if y_n=="Y" or y_n=="y":
			break
		elif y_n=="N" or y_n=="n":
			return main()
		elif y_n=="q" or y_n=="Q":
			sys.exit("\nBye...\n")
			
def main(ms=""):
	if len(ms)!=0:
		ms="((((%s))))"%ms
	while True:
		welcome()
		talwin("Do You Want Install Nvidia Closed Source Driver?\n","blue")
		print("1-Install Nvidia Closed Source Driver.\t\t\t\t\t2-Level 1 Troubleshoot Nvidia Closed Source Driver\n\n\n3-Level 2 Troubleshoot Nvidia Closed Source Driver\t\t\t4-Undo Level 2 Troubleshoot Nvidia Closed Source Driver.\n\n\n5-Remove Nvidia CLosed Source Driver.\t\t\t\t\t6-Install Gnome Shell Extentios.")
		talwin("\n%s\n"%ms,"red")
		talwin("Choice Number || q to Exit.\n-","blue",end="")
		answer=input().strip()
		ms=""
		if answer=="1":
			msg("Install Nvidia Closed Source Driver.")
			nvidia()
			return main("Finish Reboot Your Machine.")
			
			
		elif answer=="2":
			msg("Reinstall Nvidia Closed Source Driver.")
			troubleshoot_nvidia_1()
			return main("Finish Reboot Your Machine.")

		elif answer=="3":
			msg("Add Option \"options bbswitch load_state=-1 unload_state=1\" To /etc/modprobe.d/50-bbswitch.conf And Rebuild initramfs.")
			troubleshoot_nvidia_2()
			return main("Finish Reboot Your Machine.")

		elif answer=="4":
			msg("Remove File /etc/modprobe.d/50-bbswitch.conf And Rebuild initramfs.")
			undo_troubleshoot_nvidia_2()
			return main("Finish Reboot Your Machine.")

			

		elif answer=="5":
			msg("Remove Nvidia Closed Source Driver.")
			remove_nvidia()
			return main("Finish Reboot Your Machine.")

			
		elif answer=="6":
			msg("Install Gnome Shell Extentions.")
			gnome_extensions()
			return main("Finish Reboot Your Machine.")
			
		elif answer=="q" or answer=="Q":
			sys.exit("\nBye...\n")
		
	

if __name__=="__main__":
	main()
	
