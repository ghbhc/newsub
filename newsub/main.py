#!/usr/bin/env python

# expdite the creation of Slurm submission scripts

import argparse
import re
import os

parser = argparse.ArgumentParser(
	description = 'Expdite the creation of Slurm submission scripts',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)

# required by Slurm
parser.add_argument('-p', '--partition', metavar='\b', type=str, nargs=1,default='batch', help=' ')
parser.add_argument('-n', '--ntasks', metavar='\b', type=str, nargs=1,default='1', help=' ')
parser.add_argument('-m', '--mem', metavar='\b', type=str, nargs=1,default='10gb', help=' ')
parser.add_argument('-t', '--time', metavar='\b', type=str, nargs=1,default='01:00:00', help=' ')

# not required by Slurm
parser.add_argument('-s', '--sub-script', metavar='\b', type=str, nargs=1,default='sub.sh', help=' ')
parser.add_argument('-J', '--job-name', metavar='\b', type=str, nargs=1,)
parser.add_argument('-c', '--cpus-per-task', metavar='\b', type=str, nargs=1,)
parser.add_argument('-N', '--nodes', metavar='\b', type=str, nargs=1,)
parser.add_argument('-a', '--array', metavar='\b', type=str, nargs=1,)
parser.add_argument('-e', '--error', metavar='\b', type=str, nargs=1,)
parser.add_argument('-o', '--output', metavar='\b', type=str, nargs=1,)
parser.add_argument('--gres', metavar='\b', type=str, nargs=1,)
parser.add_argument('--ntasks-per-node', metavar='\b', type=str, nargs=1,)
parser.add_argument('--mem-per-cpu', metavar='\b', type=str, nargs=1,)
parser.add_argument('--export', metavar='\b', type=str, nargs=1,)
parser.add_argument('--mail-type', metavar='\b', type=str, nargs=1,)
parser.add_argument('--mail-user', metavar='\b', type=str, nargs=1,)

# update default params
parser.add_argument('--update-defaults', 
help='''Begins a prompt to change this script's Slurm header default values.  
Press enter with no value to skip, and type \'clear\' to clear a 
default value.''',
action='store_true')

# ml load
parser.add_argument('--ml', '--module-load', metavar='\b', type=str, nargs='+', 
help='''Enter a space-separated list of any modules you would 
like loaded in your submission script.''')

# commands 
parser.add_argument('--cmds', '--commands', metavar='\b', type=str, nargs='+',
help='''Enter any number of commands to be written to your submission script
below module load statements (if any).  Please surround each 
command with quotes''')

args = parser.parse_args()

# main submission script class
class SubScript:
	
	def __init__(self, args):
		self.partition = args.partition
		self.ntasks = args.ntasks
		self.mem = args.mem
		self.time = args.time
		self.sub_script = args.sub_script
		self.job_name = args.job_name
		self.cpus_per_task = args.cpus_per_task
		self.nodes = args.nodes
		self.array = args.array
		self.error = args.error
		self.output = args.output
		self.gres = args.gres
		self.ntasks_per_node = args.ntasks_per_node
		self.mem_per_cpu = args.mem_per_cpu
		self.export = args.export
		self.mail_type = args.mail_type
		self.mail_user = args.mail_user		
		self.ml = args.ml
		self.cmds = args.cmds
		
	# method to write any Slurm headers from SubScript object (self.__dict__)
	def writeHeaders(self):

		# define the class attributes you DON'T want to be treated as Slurm headers
		notslurmheaders = ['sub_script', 'ml', 'cmds']

		# define submission script name will be a list if defined with param, string using default value	
		if type(self.sub_script) == list:
			subscript = self.sub_script[0]
		else:
			subscript = self.sub_script
	
		# create the submission script in the current dir	
		with open(subscript, 'w') as f:
			print(f'Creating new submission script ({subscript})...')
			
			# write shebang first
			f.write('#!/bin/bash\n\n')

			# iterate through headers/values
			for header, value in self.__dict__.items():
				# if not using default, headers.items() value is a list, needs to change to str
				if type(value) == list: 
					value = value[0]	
				
				# pass if attribute is not a Slurm header
				if header in notslurmheaders:
					pass	
				# if they didn't just press enter to the prompt, write Slurm header to file
				elif value != None:
					f.write(f"#SBATCH --{header.replace('_', '-')}={value}\n")

	# method to write any modules to be loaded from SubScript object
	def writeModules(self):
		
		with open(subscript, 'a') as f:
			f.write('\n')
			for module in self.ml:
				f.write(f'ml {module}\n')	

	def writeCommands(self):
		
		with open(subscript, 'a') as f:
			f.write('\n')
			for cmd in self.cmds:
				f.write(f'{cmd}\n')

# uses re library to allow user to change argparse default values of this script
def updateDefaults(args):

	# path to this script
	mainpy = os.path.abspath(__file__)
	# make argparse obj a dict
	argdict = vars(args)	

	# get rid of 'update_defaults' param from dict
	del argdict['update_defaults']
	
	print('\nPlease enter a new default value for each Slurm header.  Enter to skip, \'clear\' to clear a default value\n')
	
	# get main.py readlines
	with open(mainpy, 'r') as f:
		mainpylines = f.readlines()
	
	# get header/newvalue pairs into a dictionary	
	newdefaults = {}	
	for header, value in argdict.items():
		newval = input(f'{header}: ')
		if newval != '':
			newdefaults[header] = newval
	
	# update mainpylines var 
	for header, newvalue in newdefaults.items():
		for index, line in enumerate(mainpylines):
			# if user is trying to clear default value
			if f"--{header.replace('_', '-')}'" in line and newvalue == 'clear':
				mainpylines[index] = re.sub('\s?default=\'.*', ')', line)	
			# if user is changing a default value
			elif f"--{header.replace('_', '-')}'" in line and 'default' in line:
				mainpylines[index] = re.sub('default=\'.*?\'', f'default=\'{newvalue}\'', line)
			# if user is adding a default value
			elif f"--{header.replace('_', '-')}'" in line and 'default' not in line:
				mainpylines[index] = re.sub('\)', f'default=\'{newvalue}\', help=\' \')', line)

	# update main.py
	with open(mainpy, 'w') as f:
		for line in mainpylines:
			f.write(line)	
				
			
def main():
	
	# update default arg values	
	if args.update_defaults == True:
		updateDefaults(args)
	# or create a new submission script in current dir
	else:
		script = SubScript(args)	
		script.writeHeaders()
		# write ml statements if there were any args passed to --ml
		if args.ml != None:
			script.writeModules()
		# write any commands to script if there were any args passed to --cmds
		if args.cmds !=None:
			script.writeCommands()

if __name__ == '__main__':
	main()
