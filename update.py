import subprocess 
process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE) 
output = process.communicate()[0] 