from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time,sys,os
from math import cos,sin,pi

try:
   import cPickle as pickle
except:
   import pickle

def isinteger(x):
    try:
        test = np.equal(np.mod(x, 1), 0)
    except:
        try:
            test = np.equal(np.mod(int(x), 1), 0)
        except:
            return False
    return test

def isfloat(x):
  try:
    float(x)
    return True
  except ValueError:
    return False

def firstTimeRun(fa,la,errorMessage=False):
    print "----------------------------------------------------"
    portfolioData = loadMasterList()
    pause()
    if not fa or not la:
        print "----------------------------------------------------"
        if not errorMessage: print "It seems this is the first time you run this program."
        print "You need to open this script in an editor and search"
        print "for 'firstAsset' and 'lastAsset' and replace them with"
        print "the names of your first and last fund/asset, then re-run"
        print "this program. Example:"
        print '    Change this: firstAsset = ""'
        print '     ...to this: firstAsset = "Skagen Kon-Tiki" '
        print 'if "Skagen Kon-Tiki" is your first asset'
        if len(portfolioData) > 0:
            print "----------------------------------------------------"
            print "NB: There already exist some historic portfolio data."
            print "To avoid corruption, you might need to delete the file:"
            print '"portfolioData.p"'
        sys.exit(0)
    return portfolioData

def readNewDataFromNordnet(filename="dagensData.txt"):
    with open(filename, 'r') as f:
        allLines  = f.read().splitlines()    # Read all lines into a list and rm newline-chars
        while True:                          # Delete empty lines at end or start
            if allLines[-1].strip() in ["","\n"]:
                del allLines[-1]
                continue
            elif allLines[0].strip() in ["","\n"]:
                del allLines[0]
                continue
            else:
                break
        allLines   = [line.strip().replace(",",".") for line in allLines] # Change comma to dot
        nmbr_of_lines = 0 # Of funds
        for line in allLines:
            if line == "_-_-_FUNDS_-_-_":
                continue
            if line in ["", "_-_-_STOCKS_-_-_"]:
                break
            nmbr_of_lines += 1
        nmbr_of_funds = nmbr_of_lines/3
        for i in range(nmbr_of_funds-1): # Dont add line after last fund
            index = (i+1)*3 + i+1
            allLines.insert(index, "")
        partFunds  = [None,None]
        partStocks = [None,len(allLines)]
        for i,line in enumerate(allLines):
            if line == "_-_-_FUNDS_-_-_":
                partFunds[0]  = i+1
            if line == "_-_-_STOCKS_-_-_":
                partFunds[1]  = i-1
                partStocks[0] = i+1
        partFunds  = allLines[partFunds[0]:partFunds[1]]
        partStocks = allLines[partStocks[0]:partStocks[1]]
        allLines   = partFunds # This is because first version of code only used funds
        nmbrFunds  = (1+len(partFunds ))/4
        nmbrStocks = (1+len(partStocks))/4
        fundDict   = {}
        for i in np.arange(nmbrFunds)*4: # This takes care of all funds
            fundDict[allLines[i]] = []
            j = 1
            splittedLines = allLines[i+j].split()
            for splitLine in splittedLines[0:2]:
                fundDict[allLines[i]].append(splitLine)
            if len(splittedLines) > 2:
                fundDict[allLines[i]].append( "".join(splittedLines[2:]) )
            j = 2; notDone = True; k = 0
            splittedLines = allLines[i+j].split()
            while notDone:
                if isinteger(splittedLines[k]) and isinteger(splittedLines[k+1]):
                    splittedLines[k] = "".join(splittedLines[k:k+2])
                    del splittedLines[k+1]
                    try:
                        splittedLines[k+1] # Fondsavkastning > 999 kr
                        continue
                    except:
                        break
                k += 1
                try:
                    splittedLines[k+1]
                except:
                    break
            indices = []
            for k in range(len(splittedLines)): #Find indices of floats
                if isfloat(splittedLines[k]) and not isinteger(splittedLines[k]):
                    indices.append(k)
            low = indices[0]+1; high = indices[1]+1
            splittedLines[low] = "".join(splittedLines[low:high])
            for del_i in range(low+1,high):
                del splittedLines[del_i]
            for toAppend in splittedLines:
                fundDict[allLines[i]].append( toAppend )
        allLines = partStocks # Change it back again.. bad practise.. :)
        for i in np.arange(nmbrStocks)*4:
            fundDict[allLines[i]] = []
            splittedLines = allLines[i+1].split() # First line after name
            for splitLine in splittedLines[0:2]:
                fundDict[allLines[i]].append(splitLine)
            if len(splittedLines) > 2:
                fundDict[allLines[i]].append( "".join(splittedLines[2:]) )
            splittedLines = allLines[i+2].split() # Second line after name
            fundDict[allLines[i]].append(splittedLines[0])
            fundDict[allLines[i]].append(splittedLines[1])
            joinedNumbers = "".join(splittedLines[2:3+1])
            fundDict[allLines[i]].append(joinedNumbers)
            joinedNumbers = "".join(splittedLines[4:5+1])
            fundDict[allLines[i]].append(joinedNumbers)
            fundDict[allLines[i]].append(splittedLines[6])
            joinedNumbers = "".join(splittedLines[7:])
            fundDict[allLines[i]].append(joinedNumbers)
    return fundDict

def todaysDatestamp():
    return datetime.datetime.now().strftime("%d.%m.%y")

def giveDictA_Timestamp(fundDict):
    try:
        datestamp = fundDict["date"]
    except KeyError as e:
        datestamp = None
    if datestamp is None:
        datestamp = todaysDatestamp()
        fundDict["date"] = [time.time(), datestamp]
    else:
        print "Date already set: %s. Give new timestamp for time = now?" %datestamp[1]
        yesOrNo = raw_input("In that case, write YES and hit enter: ")
        if yesOrNo in ["YES", "yes", "y", "Y"]:
            del fundDict["date"]
            giveDictA_Timestamp(fundDict) # Use recursiveness of this function

def loadMasterList(doBackup=False):
    try:
        portfolioData = pickle.load( open("portfolioData.p", "rb") )
    except IOError:
        print "No portfolio data found. Making a brand new file..."
        portfolioData = []
        pickle.dump( portfolioData, open("portfolioData.p", "wb" ) )
    if doBackup:
        saveMasterList(portfolioData,filename="backup") # Backup before continue
    if len(portfolioData) > 0:
        lastUpdate = portfolioData[-1]["date"][1]
        print "Last update in portfolio was %s" %lastUpdate
    return portfolioData

def saveMasterList(portfolioData,delete=False,filename="portfolioData.p"):
    if filename == "portfolioData.p":
        pickle.dump(portfolioData, open(filename, "wb" ) )
        if not delete:
            print "Successfully updated portfolio data with newest data"
    elif filename == "backup":
        dateLastEntry = (portfolioData[-1]["date"][1]).replace(".", "-")
        filename  = "backup/pDataBack%s.p" %(dateLastEntry)
        if os.path.isfile(filename):
            print "Backup already exist, continuing..."
        else:
            pickle.dump(portfolioData, open(filename, "wb" ) )
            print 'Data safely backed up to "%s"' %filename

def updatePortfolio(portfolioData,fundDict):
    """
    Handles assets/funds added/removed from portfolio
    """
    if not portfolioData: # First added data
        portfolioData.append(fundDict)
        saveMasterList(portfolioData)
    else:
        # Check if new data is different from previous:
        prevDict   = portfolioData[-1]
        notUpdated = []
        assetNames = [i for i in fundDict.keys() if (i != "date" and i != "yield")]
        prevANames = [i for i in prevDict.keys() if (i != "date" and i != "yield")]
        allANames  = set(assetNames+prevANames) # Pick out unique list
        for key in allANames:
            if key in assetNames and key in prevANames:
                if prevDict[key] == fundDict[key]: # Exact match of all info of that asset, i.e. bad for stocks that continously update through the day...
                    notUpdated.append(key)
        notUpdated.sort() # No real point in doing this
        if len(notUpdated) > 0: # There are not updated entries
            pause()
            print "These funds (%d/%d) have not been updated yet:" %(len(notUpdated),len(assetNames))
            for asset,i in zip(notUpdated,range(len(notUpdated))):
                print "  - %d/%d: %s" %(i+1,len(notUpdated), asset)
            pause()
            print "Wait some hours and try again. New data will NOT be stored. Exiting."
            sys.exit(0)
        else:
            # All data are new, but datestamp says "same day":
            if prevDict["date"][1] == todaysDatestamp():
                if fundDict["date"][1] == todaysDatestamp():
                    t_diff = fundDict["date"][0] - portfolioData[-1]["date"][0]
                    pause()
                    print "New data has already been added for today." \
                          + "\nTime since the previous update: %d sec / %d min / %d hours ago" \
                           %(t_diff, int(round(t_diff/(60.))), int(round(t_diff/(60.*60))))
                    pause()
                    yesOrNo = raw_input("Ignoring new data, unless override? (y/yes) ")
                    if yesOrNo in ["YES", "yes", "y", "Y"]:
                        portfolioData.append(fundDict)
                        saveMasterList(portfolioData)
                    else:
                        pause()
                        print "No new data added to portfolio!"
            else:
                portfolioData.append(fundDict)
                saveMasterList(portfolioData)

def plot_PortfolioTimeEvo(portfolioData, start=0):
    """
    Currently: Funds can be added or removed in time
    x-axis: epoch-time converted to date
    y-axis: net value, percent change etc.
    """
    assetsNames = []
    if start != 0:
        # portfolioData = portfolioData[start:] # OBS THIS MAY GIVE ERRORS
        print "Plot will use datapoints from entry number %d to present" %start
    for curDict in portfolioData[start:]:
        assetsNames += [i for i in curDict.keys() if (i != "date" and i != "yield")]
    assetsNames      = list(set(assetsNames)) # "set" picks out one of each unique
    datapointsInTime = len(portfolioData)
    nmbrOfAssets     = len(assetsNames)
    x_datestamp      = []
    x_timestamp      = np.zeros(datapointsInTime)
    netWorth         = np.zeros(datapointsInTime)
    assetYield       = np.zeros(nmbrOfAssets)     # Cumulative sum
    assetValue       = np.zeros((nmbrOfAssets,datapointsInTime))
    assetValChange   = 0.0
    assetValReturn   = np.zeros((nmbrOfAssets,datapointsInTime))
    assetPstOfTotal  = np.zeros((nmbrOfAssets,datapointsInTime))
    assetValChgYield = np.zeros((nmbrOfAssets,datapointsInTime)) # Inclusive yield
    assetsNames.sort() # Sort assets in alphabetical order
    for i,dataDict in enumerate(portfolioData):
        x_timestamp[i]   = dataDict["date"][0]
        x_datestamp.append(dataDict["date"][1])
        for j in range(nmbrOfAssets):
            if "yield" in dataDict.keys():
                if assetsNames[j] in dataDict["yield"].keys():
                    assetYield[j] += dataDict["yield"][assetsNames[j]]
                    # print j, assetYield[j],assetsNames[j]
            if assetsNames[j] not in dataDict.keys():
                # Set fund to zero if it no longer exist in portfolio
                dataDict[assetsNames[j]] = [0.0, 0.0, 0.0]
            assetValue[j,i]      = float(dataDict[assetsNames[j]][-3])
            assetValChange       = float(dataDict[assetsNames[j]][-2])
            assetValReturn[j,i]  = assetYield[j] + float(dataDict[assetsNames[j]][-1])
            # Fix the effect of yield on the future percentage increase
            if assetValue[j,i] and assetYield[j]: # Both NOT zero (avoid RuntimeWarning divide by zero)
                assetValChgYield[j,i] = (assetValue[j,i]+assetYield[j])*((1+assetValChange)/assetValue[j,i]) # (m+u)*(p/m)
            else:
                assetValChgYield[j,i] = assetValChange
            assetPstOfTotal[j,i] = assetValue[j,i] # First step of computation
            netWorth[i]         += assetValue[j,i]
        assetPstOfTotal[:,i] = np.round(assetPstOfTotal[:,i]/netWorth[i] * 100., decimals=2) # Second step of computation

        # Make a nice print out:
        pause( 0.01*np.random.uniform(0,12)*25.0/datapointsInTime )
        percent = i/float(datapointsInTime-1)*100.0 if i<datapointsInTime else 100
        sys.stdout.write("\rCrunching the numbers... %d%% " % percent) # Print out a simple "progress bar" showing percent
        sys.stdout.flush()
    sys.stdout.write("\nOpening the plot. Please watch in FULLSCREEN!\n"); sys.stdout.flush() # Fix newline problem

    # # Make 3x2 subplots, fill at least some of them
    fig      = plt.figure()
    colormap = plt.cm.nipy_spectral #Other possible colormaps: Set1, Accent, nipy_spectral, Paired
    colors   = [colormap(i) for i in np.linspace(0, 0.985, nmbrOfAssets)]
    fig.suptitle('Time-evolution of funds in portfolio', fontsize=18) # Central title for all subplots
    x_timestamp /= 24.*3600.      # Convert to days
    x_timestamp -= x_timestamp[0] # Day 0 = first day

    subFig = fig.add_subplot(3,2,1)

    for i in range(nmbrOfAssets):
        xi,yi = splineInterp(x_timestamp[start:],assetValue[i,start:])
        # x,y   = dontPlotSeriesOfZeros(xi,yi)
        plt.plot(xi,yi)
        subFig.lines[i].set_color(colors[i])
    # subFig.set_title('Time-evo of portfolio') # this is a subtitle for this subplot
    subFig.set_ylabel('Asset value [NOK]')

    subFig = fig.add_subplot(3,2,2)
    # These numbers spell out "FOND" when plotted, just for fun
    xDatNoUse = np.array([[0,0,1,0,0,1],[2.5,3.5,2.5,1.5,2.5,2.5],[4,4,6,6,6,6],[7,7,8.5,7,7,7]])
    yDatNoUse = np.array([[0,2,2,2,1,1],[0  ,1  ,2  ,1  ,0  ,0]  ,[0,2,0,2,2,2],[0,2,1  ,0,0,0]])
    for i in range(nmbrOfAssets):
        if i <= 3 and nmbrOfAssets > 3:
            plt.plot(-yDatNoUse[i],xDatNoUse[i]) # Rotate -90 degrees
            subFig.lines[i].set_color(colors[i])
        else:
            plt.plot([0],[0])
            subFig.lines[i].set_color(colors[i])
    plt.legend([asset for asset in assetsNames],loc="center right",fancybox=True)
    subFig.axis([-3,10,-1,9])
    subFig.set_ylabel('ONLY LEGEND NAMES')

    subFig = fig.add_subplot(3,2,3)
    for i in range(nmbrOfAssets):
        xi,yi = splineInterp(x_timestamp[start:],assetValChgYield[i,start:])
        # xi,yi = splineInterp(x_timestamp, test[i,:])
        # x,y = dontPlotSeriesOfZeros(xi,yi)
        plt.plot(xi,yi)
        subFig.lines[i].set_color(colors[i])
    subFig.set_ylabel('Asset value change, yield inclusive [%]')

    subFig = fig.add_subplot(3,2,4)
    for i in range(nmbrOfAssets):
        xi,yi = splineInterp(x_timestamp[start:],assetValReturn[i,start:])
        # x,y = dontPlotSeriesOfZeros(xi,yi)
        plt.plot(xi,yi)
        subFig.lines[i].set_color(colors[i])
    subFig.set_ylabel('Asset return [NOK]')

    """subFig = fig.add_subplot(3,2,5)
    for i in range(nmbrOfAssets):
        x,y = splineInterp(x_timestamp,assetPstOfTotal[i,:])
        plt.plot(x,y)#,"-",xp,yp,"o")
        subFig.lines[i].set_color(colors[i])
    subFig.set_ylabel('Asset % of portfolio')
    subFig.set_xlabel('Days since start %s' %x_datestamp[0])
    #subFig.annotate(x_datestamp[0], xy=(0, 0),xycoords='axes fraction',xytext=(10, 20),textcoords='offset pixels',horizontalalignment='left',verticalalignment='bottom')
    subFig.annotate("Last data: %s" %(x_datestamp[-1]), xy=(1, 0),xycoords='axes fraction',xytext=(-10, 20),textcoords='offset pixels',horizontalalignment='right',verticalalignment='bottom')"""

    subFig = fig.add_subplot(3,2,5)
    xi,yi  = x_timestamp[start:], np.sum(assetValReturn, axis=0)[start:]
    x, y   = splineInterp(xi, yi, linPointsBetween=1, clip=False) # Dont care too much about precision here
    profit_high, p_high_index = np.max(y), np.argmax(y) # Should use yi, but hey, dream about potential higher profits!
    plt.plot(x,y)#,"-",xi,yi,"-")
    plt.plot(x[p_high_index],profit_high,"ro",linewidth=4)
    subFig.lines[0].set_color("black")
    # subFig.lines[1].set_color("blue")
    plt.legend(["Portfolio total return / loss"], loc="best")
    subFig.set_ylabel('Portfolio net profit')
    subFig.set_xlabel('Days since start %s' %x_datestamp[0])
    #subFig.annotate(x_datestamp[0], xy=(0, 0),xycoords='axes fraction',xytext=(10, 20),textcoords='offset pixels',horizontalalignment='left',verticalalignment='bottom')
    subFig.text(x[p_high_index], profit_high*1.035, "Profit max: %g NOK" %(round(profit_high,2)), horizontalalignment='center')

    subFig = fig.add_subplot(3,2,6)
    xi,yi = splineInterp(x_timestamp[start:],netWorth[start:],clip=False)
    plt.plot(xi,yi, "-", x_timestamp[start:],netWorth[start:],"o")
    subFig.lines[0].set_color("black") # Set color to black
    subFig.lines[1].set_color("black") # Set color to black
    plt.legend(["Total value of assets"], loc="best")
    subFig.set_xlabel('Days since start %s' %x_datestamp[0])

    subFig.annotate("Last data: %s" %(x_datestamp[-1]), xy=(1, 0),xycoords='axes fraction',xytext=(-10, 20),textcoords='offset pixels',horizontalalignment='right',verticalalignment='bottom')

    plt.show()

def linearInterp(x,y,points=2):
    """
    Recommended number of linearly interpolated points: 2 (or 3).
    Setting points to 0 is bad, 1 is okeeey..
    (May cause non-existing oscillations, when used in spline interp. later)
    """
    list_x = []; list_y = []
    if points == 0: # I.e. do nothing
        return x,y
    if points in [1,3]: #  One points in between (start of algo for 3 as well)
        for i in range(0,len(x)-1):
            list_x.append( x[i] )
            list_y.append( y[i] )
            list_x.append( (x[i] + x[i+1])/2.0 )
            list_y.append( (y[i] + y[i+1])/2.0 )
        list_x.append(x[-1]); list_y.append(y[-1]) # Append last points

    if points == 2: # Chosen number of points between: 2
        for i in range(0,len(x)-1):
            list_x.append( x[i] )
            list_y.append( y[i] )
            list_x.append( 2./3.*x[i] + 1./3.*x[i+1] )
            list_y.append( 2./3.*y[i] + 1./3.*y[i+1] )
            list_x.append( 1./3.*x[i] + 2./3.*x[i+1] )
            list_y.append( 1./3.*y[i] + 2./3.*y[i+1] )
        list_x.append(x[-1]); list_y.append(y[-1]) # Append last points

    if points == 3:# Three points in between, continues from earlier
        list2_x = []; list2_y = []
        for i in range(0,len(list_x)-1):
            list2_x.append( list_x[i] )
            list2_y.append( list_y[i] )
            list2_x.append( (list_x[i] + list_x[i+1])/2.0 )
            list2_y.append( (list_y[i] + list_y[i+1])/2.0 )
        list2_x.append(list_x[-1]); list2_y.append(list_y[-1]) # Append last points
        list_x, list_y = list2_x, list2_y # pointer swap for simple return statement
    return list_x, list_y

def splineInterp(x,y,linPointsBetween=2,clip=True):
    """
    Spline interpolation over-/undershoots and this causes weird effects like assets having
    negative worth instead of zero... Changing algo to first insert X linearly interpolated points
    between existing points, to reduce this effect somewhat and clipping at low / high.
    X can be [0,1,2,3]
    """
    x,y = removeZerosAtBegAndEnd(x,y)
    Ymax = np.max(y) # For correction purpose later
    Ymin = np.min(y)
    list_x, list_y = linearInterp(x,y,points=linPointsBetween)
    N    = len(list_x)

    # Cubic spline needs AT LEAST 4 points:
    if N == 1:
        return x,y # break here and just return the points
    elif N == 2:
        interp_kind = "slinear"   # This is really no point, just a straight line
    elif N == 3:
        interp_kind = "quadratic" # Spline interpolation of second order
    else:
        interp_kind = "cubic"     # Spline interpolation of third order
    fxy = interp1d(list_x, list_y, kind=interp_kind)
    xN  = np.linspace(x[0], x[-1], len(x)*10+3)
    if clip:
        y_ret = [] # Clip negative values and values > Ymax
        for yi in fxy(xN):
            if yi <= Ymin:
                y_ret.append(Ymin)
                continue
            if yi > Ymax:
                y_ret.append(Ymax)
                continue
            y_ret.append(yi)
    else:
        y_ret = np.array([yi for yi in fxy(xN)])
    return xN,y_ret

def removeZerosAtBegAndEnd(x,y):
    # Keeps only one trailing zero and one at beginning
    lx = list(x); ly = list(y)
    if len(lx) < 2:
        return lx,ly
    while True:
        if ly[0] == 0 and ly[1] == 0:
            del ly[0]
            del lx[0]
            continue
        if ly[-1] == 0 and ly[-2] == 0:
            del ly[-1]
            del lx[-1]
            continue
        break
    return lx,ly

def pause(length=0.5):
    """
    Should be pretty obvious what this does, eh?
    """
    time.sleep(length)

def FormatDataFromNordnet(firstAssetName,lastAssetName,filename="dagensData.txt",additionalStocks=[]):
    if not os.path.isfile(filename):
        print "----------------------------------------------------"
        print 'Found no file with the name of "%s".' %filename
        print "Log into Nordnet and open your portfolio page. Ctrl + A, then Ctrl + C"
        print 'and save to a file you name "%s". Exiting...' %filename
        sys.exit(0)
    else:
        with open(filename, 'r') as f:
            allLines  = f.read().splitlines() # Read all lines into a list and rm newline-chars
            someLines = allLines[81:108]      # Predicted lines containing info # TODO: maybe delete this
            dataMustBeSearched = 0            # Check if already formatted
            for line in allLines:
                if line == "_-_-_FUNDS_-_-_":
                    dataMustBeSearched += 1
                if line == "_-_-_STOCKS_-_-_":
                    dataMustBeSearched += 1
            if dataMustBeSearched == 2:
                pause(0.75)
                raw_input("Data is already sorted and nicely formatted. Hit enter to skip to next step!")
                dataMustBeSearched = False
            else:
                dataMustBeSearched = True
            if dataMustBeSearched:
                print "Searching data for info on assets..."
                for i,line in enumerate(allLines):
                    if line in additionalStocks:
                        for j,stock in enumerate(additionalStocks):
                            if line == stock:
                                additionalStocks[j] = (allLines[i],allLines[i+1],allLines[i+2])
                    if line == firstAssetName:
                        startIndex = i
                    if line == lastAssetName:
                        lastIndex  = i+3
                        break # Stocks lists before funds
                try:
                    someLines = allLines[startIndex:lastIndex]
                except UnboundLocalError as e:
                    print "...found none."
                    firstTimeRun(None,None,True)
                    sys.exit(0)
                print " - Found first asset: %s at line %d" %(firstAssetName,startIndex)
                print " - Found last asset:  %s at line %d" %(lastAssetName,lastIndex)
        if dataMustBeSearched:
            with open(filename, 'w') as f: # Write back extracted info
                f.write("_-_-_FUNDS_-_-_" + "\n")
                for line in someLines:
                    f.write(line + "\n")
                f.write("\n_-_-_STOCKS_-_-_" + "\n")
                for lines in additionalStocks:
                    for line in lines:
                        f.write(line + "\n")
                    f.write("\n")
        with open(filename, 'r') as f: # Check file for errors always
            allLines = f.read().splitlines()
            for line in allLines:
                if len(line) == 1:
                    print "### WARNING ###"
                    print "Found a line with only a single character: suspecting error in"
                    print 'file "%s", please inspect before continuing.' %filename
                    cont = raw_input("Enter 'cont' to continue or program will exit.")
                    if not cont == 'cont':
                        sys.exit(0)
            pause()
            if dataMustBeSearched:
                print "The file %s is formatted and ready to go!\n" %filename


def readCommandLineArgs(possibleYieldStocks=[]):
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-delete","--delete"]:
            yes = raw_input("Deleting last entry? (y/yes) ")
            if yes in ["yes","YES","y","Y"]:
                portfolioData = loadMasterList()
                try:
                    del portfolioData[-1]
                except IndexError:
                    print "Portfolio empty, nothing to delete here!"
                    sys.exit(0)
                saveMasterList(portfolioData,delete=True)
                print "Last entry deleted, exiting..."
                sys.exit(0)
            else:
                print "No valid command given, exiting..."
                sys.exit(0)
        if sys.argv[1] in ["-yield","--yield"]:
            print "This will add yield starting from last update!"
            yieldAddToPortfolio(possibleYieldStocks)
            sys.exit(0)
    plotFlag = False; addDataFlag = False
    command_line_args    = []
    command_line_args[:] = sys.argv[1:] # Necessary to make a copy (not just ref)
    startDate = 0 # Plot data from start if not defined from command line
    for i,arg in enumerate(command_line_args):
        if (arg[0] == arg[1]) and (arg[0] == "-"):
            arg = arg[1:] # Example:--update -> -update
        if arg == "-plot":
            try:
                startDate = int(command_line_args[i+1]) # plot from this data point
                del command_line_args[i+1]              # Delete so that number is not printed as "unknown command"
            except:
                startDate = 0
            plotFlag = True
            continue
        if arg == "-update":
            addDataFlag = True
            continue
        if arg in ["-h","-H","-help","-HELP"]:
            plotFlag,addDataFlag = False, False
            break
        print 'Unknown command "%s" was ignored.' %(arg) # This is only printed if none of the if-tests above is met
    if (not plotFlag and not addDataFlag) or (plotFlag and addDataFlag): # If both or none args are given
        print "--------------------------------"
        print "How to use this program:"
        print "Please give ONE command line arg:\n" + \
                "'-update' : Adds current values to portfolio data and saves to file. \n" + \
                "'-plot'   : Plots only existing data \n" + \
                "'-plot 20': Plots data starting from index 20 \n" + \
                "'-delete' : Removes last addition of data to portfolio \n" + \
                "'-yield'  : Lets user specify the yield of LAST updated funds/stocks. \n" + \
              "Example usage:"
        print ">>> python portfolioNordnet.py -update"
        print "Program will now exit..."
        sys.exit(0)
    return addDataFlag,plotFlag,startDate

def yieldAddToPortfolio(possibleYieldStocks):
    try:
        portfolioData[-1]["yield"]
        yieldAdded = True
    except KeyError as e:
        yieldAdded = False
    if yieldAdded:
        print "Yield already added for last portfolio data:"
        print portfolioData[-1]["yield"]
        print "Will now exit."
        sys.exit(0)
    else:
        portfolioData[-1]["yield"] = {}
        for stock in possibleYieldStocks:
            print "--------------------------------------------"
            print "If tax on yield, input value after reduction"
            input_from_user = raw_input("Input yield for stock %s [NOK]: " %stock)
            userAmount = float(eval(input_from_user)) # Must be careful with eval for security purpose...
            portfolioData[-1]["yield"][stock] = userAmount
        print "If you entered something wrong, this is your last chance to exit and try again."
        exitOnError = raw_input("Hit enter to save or anything else to cancel: ")
        if not exitOnError:
            saveMasterList(portfolioData)
            print "Yield added successfully - and saved to file."
        else:
            print "Yield was not added - nothing saved."



if __name__ == '__main__':
    # Must be done manually (at the moment):
    # Log into Nordnet and open your portfolio page. Ctrl + A, then Ctrl + C
    # and save to a file you call: (in the same folder as this script)
    filename   = "dagensData.txt"

    # Replace these names:
    firstAsset = "Alfred Berg Gambak"
    lastAsset  = "SKAGEN Focus A"

    # Additional stocks to add (i.e. ETFs which lists as stocks on Nordnet)
    stockList = ["Global X MSCI SuperDividend EAFE ETF", \
                 "Global X SuperIncome Preferred ETF"]

    # Check if this is the first time program is run
    # and load all portfolio data from file
    portfolioData = firstTimeRun(firstAsset, lastAsset)

    # Give the possibility of deleting data from last update,
    # plot or update the portfolio.
    addDataFlag, plotFlag, startDate = readCommandLineArgs(possibleYieldStocks=stockList)

    if addDataFlag:
        FormatDataFromNordnet(firstAsset,lastAsset,filename,additionalStocks=stockList) # Search ctrl + a from nordnet for right data:
        fundDictNew = readNewDataFromNordnet(filename)
        giveDictA_Timestamp(fundDictNew)
        updatePortfolio(portfolioData,fundDictNew)

    if plotFlag:
        plot_PortfolioTimeEvo(portfolioData, startDate)

"""
#######################
TODO: Make this possible by i.e. a command line arg like "-nameswitch"
#######################
If a fond or asset ever where to change name (yeah fuck you DNB Nordic Technology, 2016/-17)
this is a way to fix that by swapping dictionary key for all previous entries:

filename      = "portfolioData.p"
portfolioData = pickle.load( open(filename, "rb") ) # Load
dat           = portfolioData
dnb           = "DNB Nordic Technology" # I.e. OLD NAME
dnbNY         = "DNB Teknologi"         #      NEW NAME
for dikk in dat:
    if dnb in dikk.keys():
        dikk["dnbNY"] = dikk.pop(dnb) # This is the magic

pickle.dump(portfolioData, open(filename, "wb" ) ) # Save
"""
