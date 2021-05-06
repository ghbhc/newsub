# newsub

This is a small CLI tool to more quickly create Slurm submission scripts.  Depening on the parameters used & default set, you can have the script write out Slurm headers, module load statements, and any commands to follow.  The default is to only write out a bash shebang and four Slurm headers, but you can change that if you wish with the `--update-defaults` parameter.  Every parameter is optional, so it's totally up to you how you use this tool to create submission scripts. 

## Installation

OS X & Linux:

`pip install newsub`

## Usage examples


default submission script headers:

`newsub`

produces a file called sub.sh in the current dir with this content (or with whatever you've changed the defaults to):

```
#!/bin/bash

#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --mem=10gb
#SBATCH --01:00:00
```

changing some values:

`newsub/main.py -p higmem_p -m 300gb -t 10:00:00 -J myHighMemJob --cpus-per-task 8 --sub-script mysub.sh --ml Python/3.7.4-GCCcore-8.3.0 --cmds 'time python myscript.py'`

produces a file called mysub.sh in the current dir with this content:

```
#!/bin/bash

#SBATCH --partition=higmem_p
#SBATCH --ntasks=1
#SBATCH --mem=300gb
#SBATCH --time=10:00:00
#SBATCH --job-name=myHighMemJob
#SBATCH --cpus-per-task=8

ml Python/3.7.4-GCCcore-8.3.0

time python myscript.py
```



## Updating Script Defaults:


`newsub/main.py --update-defaults`

A prompt is produced giving the user the option to update any default value for the script's parameters.  For example, if you prefer the gpu_p to be your default partition, you could use the `--update-defaults` option as follows:

```
Please enter a new default value for each Slurm header.  Enter to skip, 'clear' to clear a default value

partition: gpu_p
ntasks: 
mem: 
time: 
sub_script: 
job_name: 
cpus_per_task: 
nodes: 
array: 
error: 
output: 
gres: 
ntasks_per_node: 
mem_per_cpu: 
export: 
mail_type: 
mail_user: 
ml: 
cmds: 
```

Please note that this changes the package's main.py script, so any defaults you set will persist.


## CLI Options

```
newsub -h

usage: main.py [-h] [-p] [-n] [-m] [-t] [-s] [-J] [-c] [-N]
               [-a] [-e] [-o] [--gres] [--ntasks-per-node]
               [--mem-per-cpu] [--export] [--mail-type] [--mail-user]
               [--update-defaults] [--ml  ...]] [--cmds  ...]]

Expdite the creation of Slurm submission scripts

optional arguments:
  -h, --help            show this help message and exit
  -p, --partition   (default: batch)
  -n, --ntasks      (default: 1)
  -m, --mem         (default: 10gb)
  -t, --time        (default: 01:00:00)
  -s, --sub-script  (default: sub.sh)
  -J, --job-name 
  -c, --cpus-per-task 
  -N, --nodes 
  -a, --array 
  -e, --error 
  -o, --output 
  --gres 
  --ntasks-per-node 
  --mem-per-cpu 
  --export 
  --mail-type 
  --mail-user 
  --update-defaults     Begins a prompt to change this script's Slurm header
                        default values. Press enter with no value to skip, and
                        type 'clear' to clear a default value. (default:
                        False)
  --ml  ...], --module-load  ...]
                        Enter a space-separated list of any modules you would
                        like loaded in your submission script. (default: None)
  --cmds  ...], --commands  ...]
                        Enter any number of commands to be written to your
                        submission script below module load statements (if
                        any). Please surround each command with quotes
                        (default: None)
```
