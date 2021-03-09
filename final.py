from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#karakteristike projektila:
#m-masa, diam-poluprecnik, rho-gustina atmosfere, D-faktor za racunanje otpora vazduha za sferu 
m = 0.2
diam = 0.025
rho = 1.293
D = 3.0 * rho * diam ** 2
Dm = D / m
#gravitacija
g = array([0.0, 0.0, 9.8])
#pocetni uslovi:
#u0-maksimalna brzina tornada kategorije F1, rast-poluprecnik tornada, r0-pocetna pozicija, alpha-ugao pri bacanju 
u0 = 50.0
rast = 5.0
r0 = array([-100.0, 0.0, 0.0])
alpha = 45.0 * pi / 180.0
#predstavljamo putanje vise projektila lansiranih razlicitim uglovima u stranu
teta = deg2rad(arange(-30, 31, 10))
fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection = '3d')
for teta1 in teta:
	#pocetna brzina
	v0 = 100.0 * array([cos(alpha)*cos(teta1), cos(alpha)*sin(teta1), sin(alpha)])
	#maksimalno dozvoljeno vreme izvrsavanja u sekundama
	time = 10.0
	#vremenski korak
	dt = 0.001
	#maksimalni dozvoljen broj koraka petlje
	n = int(round(time / dt))
	#inicijalizacija nizova koji cuvaju polozaj, brzinu, ubrzanje i vreme
	r = zeros((n, 3), float)
	v = zeros((n, 3), float)
	a = zeros((n, 3), float)
	t = zeros(n, float)
	r[0] = r0
	v[0] = v0
	i = 0#u knjizi stoji 1 i ne radi program!
	#uslovi izlaska su ili da telo udari u podlogu ili da se dostigne maksimalan broj koraka
	while (r[i,2] >= 0.0) and (i < n):
		#racunanje brzine u tornadu(u) koriscenjem modela cilindra u fluidu
		rr = norm(r[i])
		if (rr > rast):
			U = u0 * (rast / rr)
		else:
			U = u0 * (rr / rast)
		#mnozimo intenzitet brzine(U) sa jedinicnim vektorom normalnim na pravac brzine
		u = U * array([-r[i, 1] / rr, r[i, 0] / rr, 0.0])
		vrel = v[i] - u
		#ovde se faktorise sila otpora sredine i uz pomoc drugog Njutnovog zakona dolazimo do ubrazanja
		aa = -g - Dm * norm(vrel) * vrel
		a[i] = aa
		#Ojler-Kromerova metoda
		v[i+1] = v[i] + dt*aa
		r[i+1] = r[i] + dt*v[i+1]
		t[i+1] = t[i] + dt
		i = i + 1
	#nakon izlaska iz petlje pamtimo broj koraka koji su izvrseni i pozicije tela
	imax = i
	ii = r[1:imax]
	#plotujemo putanju za dato teta
	ax.plot([i[0] for i in ii], [i[1] for i in ii], [i[2] for i in ii], color = 'b')


#ovaj deo je posvecen plotovanju polja sile unutar tornada
#koristi se formula vec vidjena u prethodnom delu programa, a zatim se plotuju strelice koje prikazuju vektore sile u polju
i = 0
j = 0
xovi = arange(-75, 75,7)
yoni = arange(-75, 75,7)
while i < 21:
	while j < 21:
		pp = norm([xovi[i], yoni[j], 0])
		if(pp > rast):
			G = u0 * (rast / pp)
		else:
			G = u0 * (pp / rast)
		u = G * ((-yoni[j])/pp)
		v = G * (xovi[i]/pp)
		ax.quiver(xovi[i], yoni[j], 0, u, v, 0, length = 5-pp/21, normalize = True, color = 'g')
		j += 1
	i += 1
	j = 0

ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_zlabel("z [m]")

show()
