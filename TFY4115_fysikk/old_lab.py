import numpy
from matplotlib import pyplot as plt
import os


def gjennomsnitt(liste): #Returnerer gjennomsnittet av et datasett. Inputen må være en liste
    return sum(liste)/len(liste)

def standardavvik(liste): #Returnerer standardavviket til et datasett. Inputen må være en liste
    Sigma = 0
    snitt=gjennomsnitt(liste)
    for x in liste:
        Sigma += (x-snitt)**2
    return((1/(len(liste)-1)*Sigma)**0.5)

def standardfeil(liste): #Returnerer standardfeilen til et gjennomsnitt. Inputen må være en liste
    return(standardavvik(liste)/(len(liste)**0.5))

def vinkelfeil(c,b): #Denne er egentlig bare nyttig til skråplan, men den vil gi standardavviket til vinkelen til et skråplan
    c_snitt=gjennomsnitt(c) #inputen c er en liste over lengden til skråplanet, målt flere ganger for å få flere verdier
    b_snitt=gjennomsnitt(b)#inputen b er en liste over lengden til det horisontale katetet, målt flere ganger for å få flere verdier
    return((((c_snitt*standardavvik(b))**2+(b_snitt*standardavvik(c))**2)/(c_snitt**2-b_snitt**2))/c_snitt)
    
A=[[4,1,0,0,0,0],[1,4,1,0,0,0],[0,1,4,1,0,0],[0,0,1,4,1,0],[0,0,0,1,4,1],[0,0,0,0,1,4]]


y=[0.376, 0.352, 0.327, 0.251, 0.100, 0.244, 0.099, 0.251]
#y=[0.3, 0.26, 0.19, 0.1, 0.07, 0.1, 0.06, 0]


b=[]
h=0.2
x_p=[round(i*h,1) for i in range(8)]

h_0=0.35 #Her kan du endre starthøyden til ballen. Den kan du også endre når du kaller opp relevante funksjoner, men dette er standarden
c=0.4 #Samme c som i fysikktimene - endre hvis du ikke har en kompakt kule


for j in range(1,len(y)-1):
    b.append(6/(h**2)*(y[j+1]-2*y[j]+y[j-1]))


d2y = list(numpy.linalg.solve(A,b))
d2y.append(0)
d2y.insert(0,0)

try:
    os.makedirs('Figurer av kulebanen/N med diverse h0') #Lager noen mapper som snart får noen fine figurer i
except:
    0

def S(x): #En funkson av hele banen. Returnerer y-verdien i punktet x. Definisjonsmengden er [0,1.4]
    j=min(int(5*x),6)
    #if x>1.4 or x<0:
     #   raise IndexError('Value out of range')
    return float(d2y[j]/(6*h)*(x_p[j+1]-x)**3+(d2y[j+1]/(6*h))*(x-x_p[j])**3+(y[j+1]/h-d2y[j+1]*h/6)*(x-x_p[j])+(y[j]/h-d2y[j]*h/6)*(x_p[j+1]-x))
 
    
def dS(x): #En tilnærming for den deriverte av S
    return float((S(x+0.01)-S(x))/0.01)

def d2S(x): #En tilnærming for den dobbeltderiverte av S
    return float((dS(x+0.01)-dS(x))/0.01)

def a(x): #Aksellerasjonen til ballen i et punkt x
    return(-9.81*numpy.sin(numpy.arctan(dS(x)))/(1+c))

def v_and_x(t, x0, x=1.4, dt=0.0001, v0=0):
    t=numpy.arange(0, t, dt)
    V=numpy.zeros(len(t))
    X=numpy.zeros(len(t))
    x_old=x0
    v_old=v0
    V[0]=v_old
    X[0]=x_old
    for j in range(1,len(t)):
        X[j]=X[j-1]+dt*V[j-1]
        V[j]=V[j-1]+dt*(-9.81*numpy.sin(numpy.arctan(dS(X[j-1])))/(1+c)*(1-c))
        print((-9.81*numpy.sin(numpy.arctan(dS(X[j-1])))/(1+c)*(1-c)))
    plt.plot(t,X,color='r')
    plt.plot(t,V,color='b')
    plt.show()
    
    

def new_N(x,h=h_0): #Returnerer normalkraften til kula i punktet x. Positiv retning er nedover
    global h_0
    h_0=h
    G=numpy.cos(numpy.arctan(dS(x)))
    s=(((h_0-S(x)))/(1+c)*d2S(x))/(1+(dS(x))**2)**1.5
    return(9.81*(G+s))

def fikspunkt(f,x0, iterasjoner):
    print(x0)
    if iterasjoner<1:
        return f(x0)-x0
    return fikspunkt(f,f(x0)-x0,iterasjoner-1)

    
def draw_full_func(): #Tegner kulebanen 
    fig = plt.figure()
    t1 = numpy.arange(0.2, 1.4,0.001)
    plt.plot(t1,[S(x) for x in t1])
    plt.title('Kulebanen')
    plt.ylabel('y (meter)')
    plt.xlabel('x (meter)')
    fig.set_size_inches(20, 2.25*4)
    fig.savefig('Figurer av kulebanen/Kulebane_kort.png')

def draw_derivert(): #Tegner den deriverte av kulebanen
    fig = plt.figure()
    t1 = numpy.arange(0,1.4,0.001)
    plt.plot(t1,[dS(x) for x in t1])
    plt.title('Derivert')
    plt.ylabel('y (meter)')
    plt.xlabel('x (meter)')
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('Figurer av kulebanen/Kulebane_derivert.png')
    
def draw_dobbeltderivert(): #Tegner den dobbeltderiverte
    fig = plt.figure()
    t1 = numpy.arange(0,1.4,0.01)
    plt.plot(t1,[d2S(x) for x in t1])
    plt.title('Dobbeltderivert')
    plt.ylabel('y (meter)')
    plt.xlabel('x (meter)')
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('Figurer av kulebanen/Kulebane_dobbeltderivert.png')

def draw_kombo(): #Tegner den deriverte og den dobbeltderiverte i samme plot. Må kalles manuelt om den ønskes. derivert er rød og dobbel er blå
    fig = plt.figure()
    t1 = numpy.arange(0,1.4,0.01)
    plt.plot(t1,[dS(x) for x in t1], color='r')
    plt.plot(t1,[d2S(x) for x in t1], color='b')
    plt.plot(t1,[0 for x in t1])
    plt.title('Derivert (rød) og dobbeltderivert (blå)')
    plt.ylabel('y (meter)')
    plt.xlabel('x (meter)')
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('Figurer av kulebanen/Kulebane_kombo.png')


def draw_new_N(a=0,b=1.4,h0=h_0): #Tegner normalkraften til kula gjennom hele banen. Normalkraften er rød, x=0 er grønn.
    # a og b er start og slutt for tegningen, så hvis du ser et område med et nullpunkt kan du tegne det alene.
    # h0 trenger du ikke å ha med når du kaller opp funksjonen, men hvis du gjør det endrer du til info h_0 globalt også.
    # Det vil altså si at hvis du kaller opp denne med h0=10000 for gøy, så endrer du h_0 til 10000 i hele filen, helt fram til
    # du kaller opp denne på nytt med en ny h0, eller starter programmet på nytt. Sistnevnte tilbakestiller h_0 til standard
    global h_0
    h_0=h0
    fig = plt.figure()
    t1 = numpy.arange(a,b,.0001)
    plt.title('Normalkraft/masse')
    plt.subplot(2, 1, 1)
    plt.plot(t1,[new_N(x) for x in t1], color='r')
    plt.plot(t1,[0 for x in t1], color='g')
    plt.ylabel('y (N/kg)')
    plt.xlabel('x (meter)')


    plt.subplot(2,1,2)
    plt.plot(t1, [S(x) for x in t1], color='c')
    plt.plot(t1, [h0 for x in t1], color='b')
    plt.ylabel('y (meter)')
    plt.xlabel('x (meter)')

    

    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f'Figurer av kulebanen/N med diverse h0/N_med_h0_lik_{h0}.png')

def ballbane(område,start_x):
    global h_0
    L=0
    x0=0
    v0=0
    fin=[]
    for x in område:
        if new_N(x)>=0 and not L:
            fin.append(S(x))
            L=0
        else:
            if L!=1:
                L=1
                x0=x
                v0=((9.81*(h_0-S(x)))*10/7)**0.5
                print(x0,v0)
            print(ball_i_lufta(x,x0,v0))
            fin.append(ball_i_lufta(x,x0,v0))
            if new_N(x)>=0 and ball_i_lufta(x,x0,v0)-S(x)<=0:
                L=0
    return numpy.array(fin)

def ball_i_lufta(x, x0, v0):
    return dS(x0)*(x-x0)-9.81/2*((x-x0)**2/(v0*numpy.cos(numpy.arctan(dS(x0)))))**2+S(x0)

def draw_ballbane(a,b, x0):
    global h_0
    h_0=S(x0)
    fig = plt.figure()
    t1 = numpy.arange(a,b,0.001)
    plt.plot(t1,ballbane(t1,x0), color='r')
    plt.plot(t1,[S(x)-0.01 for x in t1], color='b')
    plt.title('Ballens bane')
    plt.ylabel('y (meter)')
    plt.xlabel('x (meter)')
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(f'Figurer av kulebanen/Ballbaner/Ballbane_h0={S(x0)}.png')
    
def draw_N_3D(a=0.95, b=1.05):
    global h_0
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111, projection='3d')
    X = numpy.arange(a, b, 0.001)
    Y=numpy.flip(numpy.arange(a-0.65, b-0.65, 0.001))
    Z = numpy.array([[new_N(x,y) for x in X] for y in Y])
    null=[]
    for x in Y:
        temp=[]
        for y in X:
            if new_N(y,x)<=0:
                temp.append(0)
            else:
                temp.append(numpy.NAN)
        null.append(temp)
    null=numpy.array(null)
    X,Y=numpy.meshgrid(X,Y)
    plt.title('Normalkraft/masse')
    ax.set_ylim(0.4,0.3)
    plt.xlabel('x (meter)')
    plt.ylabel('Starthøyde (meter)')
    ax.set_zlabel('Normalkraft (N/kg)')
    ax.set_zlim(-10,10)
    ax.plot_surface(X,Y,Z, color='r',alpha = 1, rstride=4, cstride=4, linewidth=0.5, antialiased=True) 
    ax.plot_surface(X,Y,null,alpha = 1, rstride=1, cstride=1, color='g', linewidth=0.2, antialiased=True)
    ax.scatter(0.99, 0.32, 0, s=100)
    fig.savefig('fig1.png',dpi=300)

def fart(h, x):
    return (9.81*(h-S(x))/(1+c))**0.5

lette_x_for_h319=0.9898
lette_x_for_h3465=0.9685
#print('hei')

t_ex=[x*0.007+0.15 for x in range(13, 93)]
y_exp=[0.074462, 0.074152, 0.07328, 0.07308, 0.07216, 0.07119, 0.07035, 0.06989, 0.06893, 0.06796, 0.06697, 0.06592, 0.06486, 0.06381, 0.06269, 0.06152, 0.05975, 0.05849, 0.05661, 0.0552, 0.05327, 0.05111, 0.04896, 0.04623, 0.04381, 0.04072, 0.03754, 0.03353, 0.02954, 0.02497, 0.02005, 0.01479, 0.00935, 0.00405, -0.00584, -0.01395, -0.02354, -0.03354, -0.04354, -0.05454, -0.06554, -0.07754, -0.08954, -0.10054, -0.11154, -0.12154, -0.12954, -0.13454, -0.13654, -0.13154, -0.12954, -0.12154, -0.11154, -0.10054, -0.08954, -0.07954, -0.06854, -0.05754, -0.04754, -0.03954, -0.03154, -0.02454, -0.01754, -0.01214, -0.00737, -0.00326, 0, 0.00216, 0.0324, 0.00928, 0.00929, 0.0024, 0.00025, -0.00245, -0.00615, -0.01057, -0.01575, -0.02154, -0.02954, -0.03754, ]
x_exp=[x+0.42 for x in [0.035043573, 0.03707998, 0.042020881, 0.04452191, 0.049584093, 0.054122423, 0.058817662, 0.06188555, 0.0669361, 0.072002349, 0.076667724, 0.081620955, 0.086616592, 0.091516128, 0.096379113, 0.101482533, 0.107701305, 0.112935551, 0.119254274, 0.124532713, 0.130868697, 0.137046662, 0.143364312, 0.15046132, 0.156869125, 0.163853898, 0.170752283, 0.178430744, 0.185998598, 0.193510627, 0.201405117, 0.209174453, 0.217312763, 0.227234887, 0.233246332, 0.241245041, 0.249345179, 0.257263154, 0.265360036, 0.273725519, 0.282245033, 0.291568715, 0.301328199, 0.312423903, 0.324812789, 0.338593258, 0.354073968, 0.370585028, 0.387957655, 0.405265928, 0.421943374, 0.436694276, 0.44945966, 0.460738556, 0.470388629, 0.479566587, 0.488416009, 0.496617783, 0.504691189, 0.512265641, 0.520500759, 0.528812884, 0.5371219, 0.54511384, 0.553891557, 0.562233046, 0.570576692, 0.578904869, 0.586535802, 0.596577434, 0.601372514, 0.611630018, 0.61990079, 0.628471823, 0.637861791, 0.646961331, 0.656374872, 0.665875531, 0.675651293, 0.685515154 ]]
v_ex=[x*0.8+0.3 for x in [0.315839473, 0.353857081, 0.375928175, 0.382230156, 0.489270387, 0.470549273, 0.393529468, 0.412037947, 0.514989392, 0.49632738, 0.491624249, 0.508557021, 0.505897257, 0.500075292, 0.511286908, 0.584844609, 0.592356776, 0.598579905, 0.602768937, 0.604209031, 0.658272181, 0.660967999, 0.713592695, 0.72275349, 0.724151742, 0.761681777, 0.812615572, 0.860864267, 0.867205826, 0.904713545, 0.933956697, 0.958595956, 1.050601462, 1.100434412, 1.140348727, 1.178205471, 1.257224736, 1.303938369, 1.341607943, 1.396573475, 1.455881142, 1.513638112, 1.559215621, 1.61987856, 1.663060155, 1.709481179, 1.736148417, 1.733078604, 1.740875339, 1.733682417, 1.655103701, 1.652578902, 1.580541731, 1.504379036, 1.433785849, 1.412146572, 1.371211874, 1.295315261, 1.194609553, 1.148455796, 1.134175744, 1.074743531, 1.010015783, 0.984649717, 0.964087446, 0.911961687, 0.876538, 0.8142443, 0.952754213, 0.801046138, 0.827636629, 1.030618031, 0.87620478, 0.953398159, 1.009774271, 1.042713539, 1.10149762, 1.173937123, 1.245510461, ]]

t=0.7
x0=0.45
x=1.4
dt=0.0001
v0=0
t=numpy.arange(0, t, dt)
V=numpy.zeros(len(t))
X=numpy.zeros(len(t))
x_old=x0
v_old=v0
V[0]=v_old
X[0]=x_old
cond=0
for j in range(1,len(t)):
    X[j]=X[j-1]+dt*V[j-1]
    if X[j-1]<1.4:
        V[j]=V[j-1]-dt*9.81*numpy.sin(numpy.arctan(dS(X[j-1])))/(1+c)

    else:
        V[j]=V[j-1]+(dt*9.81)
        cond=1
#fig=plt.figure()
#fig.set_size_inches(10*0.7, 7*0.7)
##plt.subplot(2, 1, 1)
##plt.xlabel('tid (s)')
##plt.ylabel('x(t) (meter)')
##plt.plot(t,X,'r')
##plt.plot(t_ex,x_exp,':b')
##plt.subplot(2, 1, 2)
##plt.ylabel('y(t) (meter)' )
##plt.xlabel('tid (s)')
##plt.plot(t,[S(x) for x in X],'r')
##plt.plot(t_ex,[S(x) for x in x_exp],':b')
##fig.tight_layout()
##plt.savefig('x_og_y.png')
#
#new_v=numpy.zeros(len(X)-1)
#for x in range(len(X)-1):
#    new_v[x]=(numpy.sqrt(X[x+1]**2+S(X[x+1])**2)-numpy.sqrt(X[x]**2+S(X[x])**2))/dt
#
#extra_new_v=new_v=numpy.zeros(len(X))
#extra_new_v[0]=0
#new_cond=0
#for j in range(1,len(t)):
#    if new_N(X[j-1])>0 and new_cond==0:
#        extra_new_v[j]=extra_new_v[j-1]+9.81*dt-new_N(X[j-1])*dt*numpy.cos(numpy.arctan(dS(X[j-1])))
#    else:
#        extra_new_v[j]=extra_new_v[j-1]+9.81*dt
#        new_cond=1
#
#
#plt.xlabel('tid (s)')
#plt.ylabel('v(t) (m/s)')
#plt.plot(t,V,'r')
##plt.plot(t,new_v,'b')
##plt.plot(t, extra_new_v, 'g')
#plt.plot(t_ex[:-1],v_ex,':b')
#plt.savefig('fart.png')

f=numpy.zeros(len(t))
n=f.copy()
for j in range(len(f)):
    f[j]=9.81*numpy.sin(numpy.arctan(dS(X[j])))/(1+c)-9.81*numpy.cos(numpy.arctan(dS(X[j])))/(1+c)
    n[j]=new_N(X[j])
plt.xlabel('tid (s)')
plt.ylabel('kraft/masse (N/kg)')
plt.plot(t,f,'r')
plt.plot(t,n,'b')
plt.title('Friksjonskraft og normalkraft')
plt.savefig('f.png')

#draw_full_func()
#draw_derivert()
#draw_dobbeltderivert()
#draw_new_N()
#for x in range(10):
#    draw_new_N(h0=round(0.27+x*0.01.2))
#draw_ballbane(0,1.4, 0.2)
#print('Nå har du fått en ny mappe med masse figurer av kulebanen. Hver gang du\ntegner normalkraften med en ny h0 vil en ny figur dukke opp i undermappen\n"N med diverse h0"')