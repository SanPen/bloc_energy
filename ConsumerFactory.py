import pandas as pd
import datetime
import matplotlib.pyplot as plt




class ConsumerFactory:

    # Mandatorty
    # Optional
    # Flexible

   def __init__(self, scale_factor, reparto=None , fpath=None, maximum_price=0.08):
        """

        :param scale_factor:
        :param reparto:
        :param fpath:
        :param maximum_price:
        """
        self.scalefactor = 0

        if fpath is None:
            self.fpath = "consumer1"
        else:
            self.fpath = fpath

        if reparto is None:
            self.reparto = {'Electricity:Facility [kW](Hourly)': (100, 0, 0),
                            'Heating:Electricity [kW](Hourly)': (40, 30, 30),
                            'Cooling:Electricity [kW](Hourly)': (20, 50, 30),
                            'HVACFan:Fans:Electricity [kW](Hourly)': (10, 10, 100),
                            'Electricity:HVAC [kW](Hourly)': (10, 10, 80),
                            'Fans:Electricity [kW](Hourly)': (60, 30, 20),
                            'General:InteriorLights:Electricity [kW](Hourly)': (100, 0, 0),
                            'General:ExteriorLights:Electricity [kW](Hourly)': (20, 70, 10),
                            'Appl:InteriorEquipment:Electricity [kW](Hourly)': (0, 50, 50),
                            'Misc:InteriorEquipment:Electricity [kW](Hourly)': (0, 100, 0)}

        self.bidprices = [maximum_price, maximum_price*0.5, maximum_price*0.2]


   def importcsv(self):
        """

        :return:
        """
        dateparse = lambda x: pd.datetime.strptime(x, ' %m/%d %H:%M:%S')
        self.profile = pd.read_csv(self.fpath)
        new_origin= datetime.datetime.now().replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
        new_origin_ts= new_origin.timestamp()
        new_dates = [datetime.datetime.fromtimestamp(new_origin_ts + n*3600) for n in range(self.profile.shape[0])]
        self.profile['Date/Time'][:] = new_dates
        print(self.profile['Date/Time'].dtypes)
        self.profile.set_index(keys = ['Date/Time'], drop = True, inplace = True)
        # print(self.profile.index)
        self.mean = self.profile.groupby(self.profile.index.hour).mean()
        keysnotodrop = []
        keys_drop = []
        for key in self.mean.columns.values:
            if not ('Electricity' in key):
                keys_drop.append(key)
            else:
                keysnotodrop.append(key)
        print('dropped', keys_drop, 'useful', keysnotodrop)
        self.mean.drop(keys_drop, axis=1, inplace=True)
        # self.mean.plot()
       # plt.show()

   def agregate(self):
        mandatory_data = [0]*24
        optional = [0]*24
        flexible = [0]*24
        hours = self.mean.index.values
        for key, value in self.reparto.items():
            if key in self.mean.columns.values:
                mandatory_data += self.mean[key].values*self.profile[key][0]/100
                optional += self.mean[key].values * self.profile[key][1]/100
                flexible += self.mean[key].values * self.profile[key][2]/100
                self.offers = {'mandatory': mandatory_data, 'optional' : optional, 'flexible': flexible}
            pass

   def getbid(self, nhours ):
       # Mandatorty
       # Optional
       # Flexible
        self.importcsv()
        self.agregate()
        mandatory = list()
        optional = list()
        flexible = list()
        current_hour = datetime.datetime.now().hour

        i = current_hour + 1
        for n in range(nhours):

            if i>23:
                i = 0
            else:
                mandatory.append ((i, self.offers['mandatory'][i], self.bidprices[0]))
                optional.append((i, self.offers['optional'][i], self.bidprices[1]))
                flexible.append((i, self.offers['flexible'][i], self.bidprices[2]))
            i+=1
        return [mandatory, optional,  flexible]

class GeneratorFactory:
    def __init__(self, fpath = 'solargen', max_price = 180, scale_factor = 1):
        self.fpath = fpath
        self.importcsv()
        self.maxprice = max_price
        self.scaleFactor = scale_factor
        pass


    def importcsv(self):
        self.profile = pd.read_csv(self.fpath)
        new_origin = datetime.datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        new_origin_ts = new_origin.timestamp()
        new_dates = [datetime.datetime.fromtimestamp(new_origin_ts + n * 3600) for n in range(self.profile.shape[0])]
        self.profile['Date/Time'][:] = new_dates
        self.profile.set_index(keys=['Date/Time'], drop=True, inplace=True)
        self.mean = self.profile.groupby(self.profile.index.hour).mean()
        self.mean = self.profile.groupby(self.profile.index.hour).mean()

    def getbid(self):
        current_hour = datetime.datetime.now().hour

        return (current_hour, self.mean.values[current_hour][0]*self.scaleFactor, self.maxprice)

    def getmax(self):
        pass


if __name__ == "__main__":

    #filetest = "D:\\BlockChain\\RESIDENTIAL_LOAD_DATA_E_PLUS_OUTPUT\\BASE\\USA_MA_Boston-Logan.Intl.AP.725090_TMY3_BASE.csv"
    #a = ConsumerFactory(fpath=filetest, scale_factor=1)
    #a.importcsv()
    #a.agregate()
    #print(a.getbid(5))

    gen = GeneratorFactory('solargen.csv')
    gen.getmax()




    pass