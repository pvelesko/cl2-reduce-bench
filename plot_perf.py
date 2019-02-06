#!/usr/bin/env python
import subprocess
import sys
import os
import re
#import matplotlib.pyplot as plt
#import pandas as pd
"""
Plot performance for each reduction type
"""

#if len(sys.argv) < 2:
#  print("Usage: ./plot_perf.py 1")


#platform_id = int(sys.argv[1])

def process_run(output):
  idxs = [l for l in range(len(output)) if re.match("\d. ", output[l]) != None ]

  t = []
  # Time: 1.86694 msecs
  #process 1. Shared memory only kernel
  for idx in idxs:
    if "not supported" not in output[idx+1]:
      t.append(float(output[idx+2].split("Time: ")[1].split(" msecs")[0]))
    else:
      t.append(-1)
  return t

cmd = 'printf \"32\\n1\" | ./cl2-reduce-bench'
[out, err] = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
out = str(out)
num_platforms = int(out.split("Total platforms: ")[1].split("\\n")[0])

times = dict()
wg_sizes = [32, 64]
for plat in range(1, num_platforms+1):
  for wg_size in wg_sizes:
    cmd = 'printf \"%d\\n%d\" | ./cl2-reduce-bench' % (wg_size, plat)
    print(cmd)
    [out, err] = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    tokenized_out = str(out).split("\\n")
    [print(l) for l in tokenized_out]
    times[wg_size] = process_run(tokenized_out)
    print("\n\n")
print(times)

#times_df = pd.DataFrame(times)
#times_df.plot(kind='bar')
#plt.savefig("perf.png")
