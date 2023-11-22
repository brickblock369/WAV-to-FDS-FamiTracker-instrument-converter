import sys, os

#Can only detect mono wav files!
directory = os.path.dirname(sys.argv[0])
list = os.listdir(directory)

def sampleData(offset, bit):
    unsignedData = int((bytearray.fromhex(data[offset*4:(offset*4)+4])[::-1]).hex(), 16)
    if unsignedData >= ((2 ** bit) / 2):
        return unsignedData - 65336
    else:
        return unsignedData

for singleFile in list:
    with open(os.path.join(directory, singleFile), 'rb') as f:
        file = f.read()
        filehex = file.hex()
        if (filehex[0:8] == "52494646" and
            filehex[16:32] == "57415645666d7420" and
            filehex[32:34] == "10" and
            filehex[44:46] == "01" and #makes sure that it's mono
            filehex[40:42] == "01" and
            filehex[72:80] == "64617461"): #WAV file header checker
            o = open(directory+'\\'+str(singleFile)+'.fti', 'wb')
            dataStart = 88
            data = filehex[dataStart:]
            looper = 0

            bit = int(filehex[68:70], 16)
            FDSbit = 6
            bitDividerToFDS = 2 ** (bit - FDSbit)
            #filehex[80:88] is the the amount of samples * (bits / 8).
            samples = int((bytearray.fromhex(filehex[80:88])[::-1]).hex(), 16) / (bit / 8)
            SixbitSampleSet = []
            fdsSampleSet = []
            Sample64Divider = samples / 64
            
            
            while looper < samples:
                SixbitSampleSet.append(int(sampleData(looper, bit) / bitDividerToFDS) + 32)
                looper += 1
            looper = 0
            while looper < samples:
                fdsSampleSet.append(SixbitSampleSet[int(looper)])
                looper += Sample64Divider
            o.write(bytes("FTI2.4", 'ASCII'))
            FTIbytes = bytes.fromhex("0400000000")
            o.write(FTIbytes)
            for i in fdsSampleSet:
                o.write(i.to_bytes(1, 'big'))
            looper = 0
            o.write(bytes.fromhex("04 07 07 07 07 07 07 00 00 00 01 01 01 01 01 01 04 01 01 01 01 01 01 00 00 00 07 07 07 07 07 07"))
            while looper < 16:
                o.write(bytes.fromhex("00"))
                looper += 1
            looper = 0
            while looper < 2:
                looper2 = 0
                while looper2 < 8:
                    o.write(bytes("ÿ", 'cp1252'))
                    looper2 += 1
                looper2 = 0
                while looper2 < 8:
                    o.write(bytes.fromhex("00"))
                    looper2 += 1
                looper += 1
            looper2 = 0
            while looper2 < 8:
                o.write(bytes("ÿ", 'cp1252'))
                looper2 += 1
            looper2 = 0
            while looper2 < 4:
                o.write(bytes.fromhex("00"))
                looper2 += 1
                
            o.close()
        f.close()



