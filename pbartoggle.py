import re
import subprocess as sp

pgrep = sp.run(['pgrep', '-a', 'polybar'], stdout=sp.PIPE) #grep polybar pids
processes = pgrep.stdout.decode('utf-8') # get output
barpid = processes.split(' ')[0] #bar pid

if barpid:
	widcmd = ['xdotool', 'search', '--pid', str(barpid), '--onlyvisible']
	xdowid = sp.run(widcmd, stdout=sp.PIPE)
	wid = xdowid.stdout.decode('utf-8') #get wid
	if wid:
		sp.run(['xdotool', 'windowunmap', str(wid)], stdout=sp.DEVNULL, stderr = sp.DEVNULL)
		sp.run(['bspc', 'config', 'top_padding', '20'])
	else:
		sp.run(['bspc', 'config', 'top_padding', '70'])
		xdowid = sp.run(widcmd[:4], stdout=sp.PIPE) #get wid without visible flag
		wid = xdowid.stdout.decode('utf-8')
		sp.run(['xdotool', 'windowmap', str(wid)], stdout=sp.DEVNULL, stderr = sp.DEVNULL)
else:
	sp.run(['bspc', 'config', 'top_padding', '70'])
	sp.run(['polybar', 'barski'], stdout=sp.DEVNULL, stderr = sp.DEVNULL)
