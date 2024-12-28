A = 1
beta = 0.35
Tp = 0.1 
Qd = 0.05
h = [0.0, ]
t = [0.0, ]
t_sin = 3600.0 
N = int(t_sin/Tp) + 1 
h_min = 0.0
h_max = 5.0
q_min, U_min = 1,1
q_max, u_max = 10,10


for i in range(1, N):
    x = (((Qd  - beta * pow((h[i-1]),1/2))  * Tp)/A +h[i-1])
    h.append(min(h_max, max(h_min, x)))
    
print(h[-10:])

def line(x1,y1,x2,y2):
    a = ((y2-y1)/(x2-x1))
    b = a*x1 + y1

# WYKRESY:
# WARTOSC ZADANA
# DOPLYW I ODPLYW
# UPI/U
# modele matemtyczne proste, sprawdzic czy wszystko jest
# na za dwa tygodnie: ROWNANIA ROZNICZKOWE OPISUJACE PROCES z propozycja projektu
# Tematy:
# ogrzewanie temperatury poweitrza w pomieszceniu
# ogrzewanie wody
# zbiornik/ mieszanie/ przygotowywanie shotow
# tempomat?
# przemysł 4.0 lub 5.0?!