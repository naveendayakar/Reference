import pip
import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize

pip.main(["install","yelp3"])
from yelp3.client import Client

apikey='HsoG8rJLtpsvMaQ5_fjUvTSKuFg20fMAzKWWD-4NPSthNeTP3p2yNGSviZ9bmZ0z17vOW1k0Kzpx_FW8qAgSLrHLOYv1kT6Zx9qJUN3jshfcBWy2hcfpQmhk2l-oWnYx'

api = Client(apikey)

params={'term':'Indian','limit':50,'offset':0}
val = api.business_search(location='New Jersey',**params)
df = json_normalize(val,'businesses')
df2 = json_normalize(val)

pip.main(['install','uszipcode'])
from uszipcode import ZipcodeSearchEngine

search = ZipcodeSearchEngine()
res = search.by_state(state='New Jersey',returns=0)
resdf = json_normalize(res)

zcode = resdf[0]
za = zcode.values
zc=za[-10:].tolist()
zc
mdf = pd.DataFrame()
for i in zc:
    params={'term':'Indian','limit':50,'offset':0}
    val = api.business_search(location=i,**params)##what does params do
    df = json_normalize(val)
    df2 = json_normalize(val,'businesses')
    t = df.loc[0,'total']
    mdf = mdf.append(df2,ignore_index=True)
    cnt=50
    while t>0:
        params={'term':'Indian','limit':50,'offset':cnt}
        val = api.business_search(location=i,**params)
        df2 = json_normalize(val,'businesses')
        mdf = mdf.append(df2,ignore_index=True)
        t = t-50
        cnt=cnt+50

mdf.shape

mdf.columns

pip.main(['install','textblob'])
from textblob import TextBlob

idlist = mdf.id
idlist

idlist = mdf['id'].tolist()
idlist2 = idlist[307:767]
len(idlist2)
ps = []
for i in idlist2:
    rev = api.review(i)
    dfrev = json_normalize(rev,'reviews')
    textlist = dfrev['text'].tolist()
    polarity = []
    for t in textlist:
        tx = TextBlob(t)
        polarity.append(tx.sentiment.polarity)
    pol = np.array(polarity)
    ps.append(pol.mean())  
    
ps2[306]
idlist[306]

psc = ps2+ ps
        
mdf['pol']=pd.Series(psc)
mdf['location']
mdf.columns
mdf['rating']
mdf.head()


gdf2 = gdf.reset_index(True)

mdf2 = mdf.location.apply(pd.Series)
mdf2.head()

mdf[['address1','city','state','zip_code']]=mdf2[['address1','city','state','zip_code']]

mdf3 = mdf.coordinates.apply(pd.Series)
mdf3.head()

mdf[['latitude','longitude']]=mdf3[['latitude','longitude']]


mdf2['id']=mdf['id']
mdf2['pol']=mdf['pol']
gdf = mdf2.groupby(['id','zip_code'])['pol'].mean()
gdf2 = gdf.reset_index()
mdf2.shape
gdf2.shape

gdf2.columns
mdf2.columns


dictyelp = dict(zip(mdf2.id,mdf2.zip_code))

gdf2['zip_code']=gdf3['id'].map(dictyelp)    
gdf2.shape

gdf4 = gdf2.groupby('zip_code')['pol'].mean()
gd5 = gdf4.reset_index()
gd5.sort_values('pol',ascending=False)


resdf[resdf[0]=='07866']
resdf


##########################################  TensorFlow intro ####################
mdf.head()
pip.main(['install','quandl'])
import quandl

qdl='sY4DyVQWmYyv3CbpeSEM'

quandl.ApiConfig.api_key=qdl

mydata = quandl.get('ZILLOW/Z08854_TURNAH')

mydata.head()

mydata2 = quandl.get('ZILLOW/Z07029_TURNAH')

mydata.Value.tail(1).tolist()[0]
mydata2.tail()

mdf['zip_code']
mdf['zid']='ZILLOW/Z'+mdf['zip_code']+'_TURNAH'
mdf['zid']

zzid = mdf['zid'].tolist()
zzid

turnah=[]
for i in zzid:
    try:
        mydata = quandl.get(i)
        v=mydata.Value.tail(1).tolist()[0]
        turnah.append(v)
    except:
        turnah.append(0)

zz = mdf['zip_code'].unique()

bb = []
zz2 = 'ZILLOW/Z'+zz.tolist()+'_TURNAH'
zz3 = zz2.tolist()
zz3

del zz3[26]

for i in zz3:
    mydata = quandl.get(i)
    v=mydata.Value.tail(1).tolist()[0]
    bb.append(i)

len(bb)

mdf[mdf['zip_code']=='08818']

turnah[turnah==0]

aturnah = np.array(turnah)
aturnah[aturnah==0]

azzid = np.array(zzid)

azzid[aturnah==0]

mdf['Score']=turnah

mdf.columns

mdf.info()

mdf['rating'].value_counts()

mdf.describe()

mdf.hist(bins=50,figsize=(20,15))

r,c = mdf.shape
test_ratio = .3

si = np.random.permutation(r)
test_set_size = int(r*test_ratio)
test_set_size



test_indices = si[:test_set_size]
train_indices = si[test_set_size:]

train_indices

train_set = mdf.iloc[train_indices]
test_set = mdf.iloc[test_indices]

train_set.shape
test_set.shape

pip.main(['install','sklearn'])
pip.main(['install','scipy'])
from sklearn.model_selection import train_test_split

train_set2, test_set2 = train_test_split(mdf, test_size=.2, random_state=42)

train_set2.shape
test_set2.shape

from sklearn.model_selection import StratifiedShuffleSplit
mdf.rating.value_counts()

split = StratifiedShuffleSplit(n_splits=1, test_size=.3, random_state=42)

for train_indices, test_indices in split.split(mdf, mdf['rating']):
    strat_train_set = mdf.loc[train_indices]
    strat_test_set = mdf.loc[test_indices]
