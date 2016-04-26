import matplotlib
import csv
import matplotlib.pyplot as plt
import scipy
from scipy import stats
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import interp1d
from sklearn.metrics import r2_score
import numpy as np
import sys
from sklearn import linear_model
import math
from collections import OrderedDict
from operator import itemgetter
from sklearn.linear_model import LinearRegression
import pandas as pd
import statsmodels.api as sm 
import itertools
from scipy.optimize import curve_fit

def rmse(p,x,y):
    yfit = np.polyval(p,x)
    return np.sqrt(np.mean((y-yfit)**2))
def flatten(lst):
    return sum( ([x] if not isinstance(x, list) else flatten(x)
             for x in lst), [] )
def plot_learning_curve(d,x,xleft,y,yleft):
    sizes = np.linspace(2,15,50).astype(int)
    train_err = np.zeros(sizes.shape)
    crossval_err = np.zeros(sizes.shape)
    for i,size in enumerate(sizes):
        p = np.polyfit(x[:size],y[:size],d)
        crossval_err[i] = rmse(p,xleft,yleft)
        train_err[i] = rmse(p,x[:size],y[:size])
    fig,ax = plt.subplots()
    ax.plot(sizes,crossval_err,lw=2,label='validation error')
    ax.plot(sizes,train_err,lw=2,label='training error')
    ax.plot([0,15],[1.,1.],'-',lw=3,label='intrinsic error')
    ax.set_xlabel('training set size')
    ax.set_ylabel('rms error')
    ax.legend(loc=0)
    ax.set_xlim(0,15)
    ax.set_title('d = %i'%d)
    plt.show()

class Interpolation:
    def __init__(self, statecc,stategdp,statepop):
        self.complaint_allstate = {}
        self.gdp = {}
        self.pop = {}
        for value,key in zip(statecc.values(),statecc.keys()):
            tem = []
            ctr = 1
            for v in value:
                if int(ctr) != 16:
                     tem.append((ctr,int(v)))
                else:
                    break
                ctr = ctr + 1
            self.complaint_allstate.update({key: dict(tem)})
        for value,key in zip(stategdp.values(),stategdp.keys()):
            tem = []
            ctr = 1
            for v in value:
                tem.append((ctr,int(v)))
                ctr = ctr + 1
            self.gdp.update({key: dict(tem)})
        self.ax = []
        self.ay = []

    def lagrange(self):
        '''Lagrange Interpolation. Unsuccessful because it's a linear equation, so doesn't
        get the target result that I want. The result is -3565+2421.41*(x)'''

        orig_stdout = sys.stdout
        f = file('lagrangeout.txt', 'w')
        sys.stdout = f

        tmp = scipy.poly1d([0])
        result=scipy.poly1d([0])
        for value,key in zip(self.complaint_allstate.values(),self.complaint_allstate.keys()):
            for i in value.keys():
                numerator=scipy.poly1d([1])
                denom = 1.0
                for j in value.keys():
                    if (i != j):
                        tmp = scipy.poly1d([1,-j])
                        numerator = numerator * tmp
                        denom = denom * (i - j)
                tmp = (numerator/denom) * value.get(i)
                result = result + tmp
            print key + " : "
            print result
            print '\n'
        sys.stdout = orig_stdout
        f.close()
    def interpolation1d(self):
        #basic data
        new_length = 25
        legend_array = []
        highest_value = []
        for value,key in zip(self.complaint_allstate.values(),self.complaint_allstate.keys()):
            k = np.array(value.keys())
            v = np.array(value.values())
            #interpolation
            new_x = np.linspace(k.min(),k.max(), new_length)
            new_y = interp1d(k,v, kind='cubic')(new_x)
            poly = np.polyfit(k, v, deg=4)
            y_int  = np.polyval(poly, new_x)
            #extrapolate interpolation
            plt.plot(new_x,y_int)
            #legend_array.append(key)
            tck = scipy.interpolate.splrep(k,v,k=3,s=0)
            #another extrapolate interpolation using polyfit

            print y_int
            '''print key 
            print " : "
            print scipy.interpolate.splev(15,tck)
            print "\n"'''
            if k[14] >= 2000:
                legend_array.append(key)
        print legend_array
        plt.title("Consumer Complaints 15 Querter Interpolation")
        plt.ylabel("Consumer Compalaints Amount")
        plt.xlabel("Quarters(Q1 2012 to Q# 2015)")
        plt.show()

    def correlation(self):
        keys_a = set(self.gdp.keys())
        keys_b = set(self.complaint_allstate.keys())
        intersection = keys_a & keys_b
        corr_dict = {}
        ax = []
        ay = []
        for v in intersection:
            y = np.array(self.gdp[v].values())
            x = np.array(self.complaint_allstate[v].values())
            if(len(x) != len(y)):
                continue
            else:
                ax.append(self.complaint_allstate[v].values())
                ay.append(self.gdp[v].values())
                corr_dict.update({v:np.corrcoef(x,y)[0,1]})
        self.ax = flatten(ax)
        self.ay = flatten(ay)
        print "Nation Wide: %f"%np.corrcoef(flatten(ax),flatten(ay))[0,1]
        corrdict = OrderedDict(sorted(corr_dict.items(), key=itemgetter(1)))
        print corrdict

        '''
    def simplePredict(self):
        keys_a = set(self.gdp.keys())
        keys_b = set(self.complaint_allstate.keys())
        intersection = keys_a & keys_b
        for v in intersection:
            y = np.array(self.gdp[v].values())
            #yleft = np.array(self.gdp[v].values())[12:]
            x = np.array(self.complaint_allstate[v].values()).T
            coefficient'''
    def linearRegression(self):
        regr = linear_model.LinearRegression()
        keys_a = set(self.gdp.keys())
        keys_b = set(self.complaint_allstate.keys())
        intersection = keys_a & keys_b
        #intersection = ['FL','TX','NY','PA','CA','GA']
        for v in intersection:
            y = np.array(self.gdp[v].values())[:12]
            yleft = np.array(self.gdp[v].values())[12:]
            x = np.array(self.complaint_allstate[v].values())[:12]
            xleft = np.array(self.complaint_allstate[v].values())[12:]
            if(len(x) != len(y)):
                continue
            else:
                regr.fit(x.reshape(12,1),y.reshape(12,1))
                print 'Coefficients of %s & %F'%(v,regr.coef_)
                print np.mean((regr.predict(xleft.reshape(3,1))-yleft.reshape(3,1))**2)
                print regr.score(xleft.reshape(3,1),yleft.reshape(3,1))
                plt.scatter(xleft.reshape(3,1),yleft.reshape(3,1),color='black')
                plt.plot(xleft.reshape(3,1),regr.predict(xleft.reshape(3,1)),color='blue')
                plt.show()
    def extrapolator(self):
        keys_a = set(self.gdp.keys())
        keys_b = set(self.complaint_allstate.keys())
        intersection = keys_a & keys_b
        #intersection = ['FL','TX','NY','PA','CA','GA']
        a = np.array([])
        aleft = np.array([])
        b = np.array([])
        bleft = np.array([])
        intersection = ['US']
        for v in intersection:
            '''
            y = np.array(self.gdp[v].values())[:12]
            yleft = np.array(self.gdp[v].values())[12:]
            x = np.array(self.complaint_allstate[v].values())[:12]
            xleft = np.array(self.complaint_allstate[v].values())[12:]
            '''
            y = np.array(self.ay)[:600]
            yleft = np.array(self.ay)[600:]
            x = np.array(self.ax)[:600]
            xleft = np.array(self.ax)[600:]
            if(len(x) != len(y)):
                continue
            else:
            #wanted = np.array([ i for i in range(0,1000)])
                ds = np.arange(41)
                train_err = np.zeros(len(ds))
                test_err = np.zeros(len(ds))
                for i,d in enumerate(ds):
                    p = np.polyfit(x,y,d)
                    train_err[i] = rmse(p,x,y)
                    test_err[i] = rmse(p,xleft,yleft)
                print "RMSE: lowest: %f ;highest: %f; proportion: %f"%(test_err.min(),test_err.max(),test_err.min()/test_err.max())
                degree = np.argmin(test_err)
                print degree
                plt.title( "(  %s  )in %d th order regression"%(v,3))
                xp = np.linspace(x.min()-1000, x.max()+1000,10000)
                coeff = np.polyfit(x,y,degree)

                f = np.polyval(coeff,xp)
                temp= []
                occurance = []
                for index,element in enumerate(xp):
                    i = round(element,0)
                    if i in xleft and i not in occurance:
                        occurance.append(i)
                        temp.append(index)

                temp = np.unique(temp)
                a = [ f[i]for i in temp]
                print len(a),len(yleft)
                e = yleft[:127]
                if not a or len(a)!=len(e):
                    print 0
                else:
                    slope, intercept, r_value, p_value, std_err =stats.linregress(a,e)
                    print r_value**2
                plt.scatter(x,y,c="green")
                plt.xlabel("Complaints Amount")
                plt.ylabel("State GDP")
                plt.scatter(xleft,yleft,c="red")
                plt.axis([x.min()+10,xleft.max()+10,y.min()+10,yleft.max()+100])
                plt.plot(xp,f,'blue')
                plt.savefig("(  %s  )Extrapolation with %d th Order Regression Model"%(v,degree)+".jpg")
                plt.show()

                '''
                fig,ax = plt.subplots()
                ax.plot(ds,test_err,lw=2,label='test error')
                ax.plot(ds,train_err,lw=2,label='training error')
                ax.legend(loc=0)
                ax.set_xlabel('degree of fit')
                ax.set_ylabel('rms error')
                plt.title( "(  %s  )RMSE vs Degree of Fit"%v )
                plt.savefig("(  %s  )RMS Error vs Degree of Curve Fit"%v+".jpg")'''
                
                #plot_learning_curve(d=3,x=x,xleft=xleft,y=y,yleft=yleft)


                '''
                temp = []
                for index,element in enumerate(xp):
                    if round(element,0) in xleft:
                        temp.append(index)
                mean = []
                for i in temp:
                    mean.append(f[i])
                print mean
                print scipy.stats.pearsonr(xleft, mean)
                '''
                '''
                xp = sm.add_constant(x)
                model = sm.OLS(y,xp)
                result = model.fit()

                print result.summary()
                print stats.linregress(xleft,yleft)
                print "std is %f"%result.rsquared '''
                #plt.savefig("(  %s  )Extrapolation with scipy.interpolate.UnivariateSpline"%v+".jpg")
                #plt.show()
def getStatePop():
    statedict = {}
    csvfile = open("AnnualPopulation.csv","r+")
    spamreader = csv.reader(csvfile,delimiter=',')
    for row in spamreader:
        state = [(i,[]) for i in row]
        statedict = dict(state)
        break
    for row in spamreader:
        for x,y in zip(row[1:len(row)],sorted(statedict.keys())):
            statedict[y].append(float(x))
    csvfile.close()
    for key in statedict.keys():
        statedict[key] = np.diff(statedict[key]) / statedict[key][:4]
    print statedict
    return statedict
def getStateCC():
    statearray = {}
    csvfile = open("Consumer_Complaints_1215_PY.csv","r+")
    spamreader = csv.reader(csvfile,delimiter=',')
    for row in spamreader:
        state = [(i,[]) for i in row]
        statedict = dict(state)
        break
    del statedict['Row Labels']
    del statedict['US']
    for row in spamreader:
        for x,y in zip(row[1:len(row)],sorted(statedict.keys())):
            statedict[y].append(x)
    csvfile.close()
    return statedict

def getStategdp():
    statearray = {}
    csvfile = open("StateGDP_1215.csv","r+")
    spamreader = csv.reader(csvfile,delimiter=',')
    for row in spamreader:
        state = [(i,[]) for i in row]
        statedict = dict(state)
        break
    for row in spamreader:
        for x,y in zip(row[1:len(row)],sorted(statedict.keys())):
            statedict[y].append(x)
    csvfile.close()
    return statedict


def main():
    cc = getStateCC()
    gdp = getStategdp()
    pop = getStatePop()
    state = Interpolation(cc,gdp,pop)
    #state.linearRegression()
    #state.correlation()
    #state.extrapolator()



if __name__ == "__main__":
    main()
