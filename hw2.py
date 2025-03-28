import netCDF4 as nc 
import numpy as np
import matplotlib.pyplot as plt

dataset = nc.Dataset("EngFlx_zm_CESM2_piControl_r1i1p1f1_gn_090001-099912.nc" ,'r')

# print(dataset)

# print(dataset.variables.keys())

lat = dataset.variables['lat'][:]

rsdt = dataset.variables['rsdt'][:] #TOA SW
rsut = dataset.variables['rsut'][:] #TOA ILR
rlut = dataset.variables['rlut'][:] #TOA OLR

rss = dataset.variables['rss'][:] #surface net SW
rls = dataset.variables['rls'][:] #surface net LW
hfls = dataset.variables['hfls'][:] #latent heat
hfss = dataset.variables['hfss'][:] #sensible heat

rtoa = np.zeros_like(lat)
rsur = np.zeros_like(lat)
ra = np.zeros_like(lat)
divFa = np.zeros_like(lat)
divF = np.zeros_like(lat)

rtoa = rsdt - rsut - rlut
rsur = rss - rls
ra = rtoa - rsur
# ra = rsdt -rss + rls -rsut - rlut
divFa = ra + hfls + hfss
divF = rsdt - rsut - rlut

plt.figure()
plt.plot(lat, divFa, label='ΔFa')
plt.plot(lat, ra, label='Ra')
plt.plot(lat, hfls, label='LE')
plt.plot(lat, hfss, label='SH')
plt.xlim(-90,90)
plt.xlabel('Latitude')
plt.ylabel('Energy Flux [W' f'$m^{-2}$]')
plt.legend()
plt.grid()
plt.savefig('hw2.png')
plt.show()

a = 6.371e6 
dlat = np.deg2rad(np.gradient(lat)) 

F_atm = np.cumsum(2 * np.pi * a * np.cos(np.deg2rad(lat)) * divFa * dlat * a) / 1e15  # Petawatts
F_total = np.cumsum(2 * np.pi * a * np.cos(np.deg2rad(lat)) * divF * dlat * a) / 1e15
F_ocean = F_total - F_atm

plt.plot(lat, F_total, 'k-', label="Total")
plt.plot(lat, F_atm, 'r--', label="Atmosphere")
plt.plot(lat, F_ocean, 'b:', label="Ocean")
plt.xlim(-90,90)
plt.xlabel("Latitude")
plt.ylabel("Northward Flux (PW)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig('hw2_1.png')
plt.show()
