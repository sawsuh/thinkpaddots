import re
import subprocess as sp

pidcmd = ['pgrep', '-a', 'polybar']
pgrep = sp.run(pidcmd, stdout=sp.PIPE) #grep polybar pids
processes = pgrep.stdout.decode('utf-8') # get output
barpid = processes.split(' ')[0] #bar pid 

if barpid != "":
	widcmd = ['xdotool', 'search', '--pid', str(barpid), '--onlyvisible']
	xdowid = sp.run(widcmd, stdout=sp.PIPE)
	wid = xdowid.stdout.decode('utf-8') #get wid
	if wid != "":
		sp.call(['xdotool', 'windowunmap', str(wid)])
		sp.call(['bspc', 'config', 'top_padding', '20'])
	else:
		sp.call(['bspc', 'config', 'top_padding', '70'])
		xdowid = sp.run(widcmd[:4], stdout=sp.PIPE) #get wid without visible flag
		wid = xdowid.stdout.decode('utf-8')
		sp.call(['xdotool', 'windowmap', str(wid)])
else:
	sp.call(['bspc', 'config', 'top_padding', '70'])
	sp.call(['polybar', 'barski'])

