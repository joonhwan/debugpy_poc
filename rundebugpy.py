import sys
import debugpy
debugpy.log_to(sys.stderr)
debugpy.listen(54321)
sys.stdin.readline()