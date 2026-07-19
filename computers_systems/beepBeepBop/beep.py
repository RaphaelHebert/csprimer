import sys
import termios
import tty
import re
import time

# get the file descriptor for stdin (stdin is a file object), usually 0 for stdin
fd = sys.stdin.fileno()

# Get the tty attributes for file descriptor fd.
old = termios.tcgetattr(fd)

try:
    # set terminal to read one char at the time 
    # this disable line editing from terminal and disable wait until Enter is pressed to process inputs
    # disable canonical mode, makes sys.stdin.read(1) block until exactly one character arrives, does not disable the ISIG flag (exp ctrl+ c).
    tty.setcbreak(fd)
    while True:
        # read one character
        x = sys.stdin.read(1)
        if re.match('[0-9]', x) != None:
            for i in range(int(x)):
                # make the terminal beep (check 'man ascii' to find the bel byte)
                sys.stdout.buffer.write(b'\x07')
                # if no timer the stoud ends up loosing track of the bel after 5 bips
                time.sleep(1)
                print(i)
            sys.stdin.buffer.flush()
                
        if x == 'q':
            break
    
finally:
    # restore terminal old settings
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
