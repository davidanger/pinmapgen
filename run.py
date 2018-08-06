import config

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

# Output CSV format
fout = open(config.DATA.OUTPUT_FILE, 'w')
fout.write('PIN')
for i in range(0, (config.PINFORMAT_CONFIG.AF_NUM + 1)):
    fout.write(',AF{:d}'.format(i))
fout.write('\n')

i = 0
while i * (config.PINFORMAT_CONFIG.AF_NUM + 2) < (len(datalist) - (config.PINFORMAT_CONFIG.AF_NUM + 1)):
    tempout = datalist[i * (config.PINFORMAT_CONFIG.AF_NUM + 2):(i+1) * (config.PINFORMAT_CONFIG.AF_NUM + 2)]
    print(tempout)
    fout.write(','.join(tempout) + '\n')
    i = i + 1
fout.close()

