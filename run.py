import config
import re

# open input file
fin = open(config.DATA.INPUT_FILE, 'r')
datain = fin.read()
fin.close()

# Remove '\n'
while datain.find('\n') > 0:
    i = datain.find('\n')
    for pincat in config.PINFORMAT_CONFIG.PIN_CAT:
        t = len(pincat)
        tc = datain[i+1:i+1+t]
        tcpg = datain[i+1:i+1+config.PINFORMAT_CONFIG.PIN_GLEN]
        # print(pincat, t)
        # print(tc)
        if datain[i-1] == '/':
            # means AA/\nBB
            datain = datain[:i] + datain[i + 1:]
            break
        if pincat == tc \
                or tcpg in config.PINFORMAT_CONFIG.PIN_GRP \
                or datain[i+1] == '-':
            #
            # means PXx
            # means XX\n-
            datain = datain.replace('\n', ' ', 1)
            print(tc)
            break
    if datain[i] == '\n':
        if i >= len(datain) - 1:
            datain = datain[:i]
        else:
            datain = datain[:i] + datain[i+1:]

# convert input to a list
datalist = datain.split()

# Making pinmap
i = 0
pinmap = []
while i * (config.PINFORMAT_CONFIG.AF_NUM + 2) < (len(datalist) - (config.PINFORMAT_CONFIG.AF_NUM + 1)):
    pinmap.append(datalist[i * (config.PINFORMAT_CONFIG.AF_NUM + 2):(i+1) * (config.PINFORMAT_CONFIG.AF_NUM + 2)])
    print(pinmap[i])
    i = i + 1

# Add NUCLEO pin map
# Read input file
fin = open(config.NUCLEO.INPUT_FILE, 'r')
datain = fin.read()
fin.close()

# make pin list
datalist = datain.split('\n')
for i in range(0, len(datalist)):
    datalist[i] = datalist[i].split('\t')
    datalist[i] = datalist[i][2:6]

# merge to pinmap
for i in range(0, len(datalist)):
    if datalist[i] == []:
        break
    # find arduino signal Pin
    ard = re.findall('[A,D]\d+', datalist[i][0])
    if ard != []:
        # find PXx
        pxx = re.findall('P[A-Z]\d+', datalist[i][2])
        if pxx != []:
            # Search to PXx
            for j in range(0, len(pxx)):
                for k in range(0, len(pinmap)):
                    # found PXx
                    if pxx[j] == pinmap[k][0]:
                        # Merge to pinmap
                        pinmap[k].append(ard[0])
                        pinmap[k].append(datalist[i][1])
                        break

# Output CSV format
fout = open(config.DATA.OUTPUT_FILE, 'w')
fout.write('PIN')
for i in range(0, (config.PINFORMAT_CONFIG.AF_NUM + 1)):
    fout.write(',AF{:d}'.format(i))
# Arduino map
fout.write(',ArdPIN,ArdTAG')
fout.write('\n')

for i in range(0, len(pinmap)):
    print(pinmap[i])
    fout.write(','.join(pinmap[i]) + '\n')
fout.close()
