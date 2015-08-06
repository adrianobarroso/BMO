'''
Processamento dos dados
do PNBOIA baixados pelo
openDAP

B69008 - recife
B69007 - porto seguro
B69009 - baia guanabara
B69150 - santos
B69152 - florianopolis
B69153 - rio grande

site: goosbrasil.saltambiental
'''

import matplotlib.pylab as pl
import os
import netCDF4 as nc

pl.close('all')

pathname = os.environ['HOME'] + '/Dropbox/pnboia/rot/opendap/'

#argosname = 'B69008_argos.nc' #recife
#argosname = 'B69007_argos.nc' #porto seguro
argosname = 'B69150_argos.nc' #santos
#argosname = 'B69152_argos.nc' #florianopolis
#argosname = 'B69153_argos.nc' #rio grande

#opendap
buoy = nc.Dataset(pathname + argosname)

#lista o nome das variaveis
for v in buoy.variables:
	print v

#define variaveis
time = buoy.variables['time'][:]
avg_radiation = buoy.variables['avg_radiation'][:]
rel_humid = buoy.variables['rel_humid'][:]
wave_period = buoy.variables['wave_period'][:]
cm_dir1 = buoy.variables['cm_dir1'][:]
temp_air = buoy.variables['temp_air'][:]
wave_dir = buoy.variables['wave_dir'][:]
battery = buoy.variables['battery'][:]
wind_dir1 = buoy.variables['wind_dir1'][:]
cm_int1 = buoy.variables['cm_int1'][:]
cm_int3 = buoy.variables['cm_int3'][:]
cm_int2 = buoy.variables['cm_int2'][:]
wave_hs = buoy.variables['wave_hs'][:]
sst = buoy.variables['sst'][:]
wind_gust1_f2 = buoy.variables['wind_gust1_f2'][:]
pressure = buoy.variables['pressure'][:]
wave_h_max = buoy.variables['wave_h_max'][:]
wind_dir1_f2 = buoy.variables['wind_dir1_f2'][:]
dew_point = buoy.variables['dew_point'][:]
avg_wind_int1_f2 = buoy.variables['avg_wind_int1_f2'][:]
cm_dir3 = buoy.variables['cm_dir3'][:]
cm_dir2 = buoy.variables['cm_dir2'][:]
longitude = buoy.variables['longitude'][:]
avg_wind_int1 = buoy.variables['avg_wind_int1'][:]
avg_wind_int2 = buoy.variables['avg_wind_int2'][:]
wind_gust2 = buoy.variables['wind_gust2'][:]
avg_dir2 = buoy.variables['avg_dir2'][:]
wind_gust1 = buoy.variables['wind_gust1'][:]

#converte data em juliano (time) para datetime
datat = pl.num2date(time)

#figuras
pl.figure()
pl.subplot(311)
pl.plot(datat,wave_hs,'.')
pl.ylim(0,7)
pl.subplot(312)
pl.plot(datat,wave_period,'.')
pl.ylim(0,25)
pl.subplot(313)
pl.plot(datat,wave_dir,'.')
pl.ylim(0,360)

pl.show()