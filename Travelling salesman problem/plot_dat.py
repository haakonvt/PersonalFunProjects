import matplotlib.pyplot as plt
import numpy as np

def LoadData(file):
    arrayfile = np.loadtxt(file)
    return arrayfile[:,1]

if __name__ == '__main__':
    data1 = LoadData('dataP20.dat')
    data2 = LoadData('dataP20_2.dat')
    data3 = LoadData('dataP20_3.dat')
    #print np.sort(data),np.mean(data)

    f, axarr = plt.subplots(3, sharex=True)
    axarr[0].hist(data1)
    axarr[1].hist(data2)
    axarr[2].hist(data3,20)
    plt.show()
