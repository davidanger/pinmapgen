import config

# open input file
f = open(config.DATA.INPUT_FILE, 'r')
datain = f.read()

# Remove '\n'
while datain.find('\n') > 0:
    i = datain.find('\n')
    for pincat in config.PINFORMAT_CONFIG.PIN_CAT:
        t = len(pincat)
        tc = datain[i+1:i+1+t]
        tcpg = datain[i+1:i+1+config.PINFORMAT_CONFIG.PIN_GLEN]
        print(pincat, t)
        print(tc)
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
            break
    if datain[i] == '\n':
        datain = datain[:i] + datain[i+1:]

# convert input to a list
datalist = datain.split()

# make a PIN definition class
