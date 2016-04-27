import numpy as np
import matplotlib.pyplot as plt

dt = 0.001
v  = 1
N  = int(round(1/dt))
a = 1; b = 1/np.sqrt(2) # Values for exact solution

r1 = np.zeros((N,2))
r2 = np.zeros((N,2))
r3 = np.zeros((N,2))
r4 = np.zeros((N,2))
t  = np.linspace(0,dt*N-dt,N)

"""# Exact solution for r1 NOT FINISHED
rex = a*np.exp(-b*t)*np.cos(t)
rey = a*np.exp(-b*t)*np.sin(t)

plt.plot(rex,rey)
plt.show()
"""

# At t = 0
r1[0] = np.array((0,0))
r2[0] = np.array([1,0])
r3[0] = np.array([1,1])
r4[0] = np.array([0,1])

for i in range(N-1):
    """ # Forward Euler, first order
    r1r2 = (r2[i]-r1[i])/(np.linalg.norm(r2[i]-r1[i]))
    r2r3 = (r3[i]-r2[i])/(np.linalg.norm(r3[i]-r2[i]))
    r3r4 = (r4[i]-r3[i])/(np.linalg.norm(r4[i]-r3[i]))
    r4r1 = (r1[i]-r4[i])/(np.linalg.norm(r1[i]-r4[i]))

    r1[i+1] = r1[i] + r1r2*v*dt
    r2[i+1] = r2[i] + r2r3*v*dt
    r3[i+1] = r3[i] + r3r4*v*dt
    r4[i+1] = r4[i] + r4r1*v*dt

    """

    # Runge Kutta of seconds order aka midpoint method
    r1r2 = (r2[i]-r1[i])/(np.linalg.norm(r2[i]-r1[i])) # Direction, unit vector
    r2r3 = (r3[i]-r2[i])/(np.linalg.norm(r3[i]-r2[i]))
    r3r4 = (r4[i]-r3[i])/(np.linalg.norm(r4[i]-r3[i]))
    r4r1 = (r1[i]-r4[i])/(np.linalg.norm(r1[i]-r4[i]))

    k1r1 = r1[i] + r1r2*v*dt    # New position
    k1r2 = r2[i] + r2r3*v*dt
    k1r3 = r3[i] + r3r4*v*dt
    k1r4 = r4[i] + r4r1*v*dt

    k2r1r2 = (k1r2-k1r1)/(np.linalg.norm(k1r2-k1r1)) # New direction at new position
    k2r2r3 = (k1r3-k1r2)/(np.linalg.norm(k1r3-k1r2))
    k2r3r4 = (k1r4-k1r3)/(np.linalg.norm(k1r4-k1r3))
    k2r4r1 = (k1r1-k1r4)/(np.linalg.norm(k1r1-k1r4))

    r1[i+1] = r1[i] + 0.5*dt*(r1r2 + k2r1r2)*v # Use direction at mid-interval
    r2[i+1] = r2[i] + 0.5*dt*(r2r3 + k2r2r3)*v
    r3[i+1] = r3[i] + 0.5*dt*(r3r4 + k2r3r4)*v
    r4[i+1] = r4[i] + 0.5*dt*(r4r1 + k2r4r1)*v


if raw_input("Hit 'enter' to skip plot") != '':
    plt.plot(r1[:,0], r1[:,1],'o-')
    plt.plot(r2[:,0], r2[:,1],'o-')
    plt.plot(r3[:,0], r3[:,1],'o-')
    plt.plot(r4[:,0], r4[:,1],'o-')
    plt.legend(["r1","r2","r3","r4"])
    plt.show()

def integratooor(r):
    dr = 0
    for i in range(N-1):
        dx = (r[i+1]-r[i])[0]
        dy = (r[i+1]-r[i])[1]
        dr += np.sqrt(dx**2 + dy**2)
    return dr

def radial_velocity(r,dt):
    vr = np.zeros(len(r)) # Magnitude of v in direction of middle
    rm = np.array([0.5,0.5])
    for i in range(N-1):
        rmi   = np.linalg.norm(rm - r[i])
        rmi_n = np.linalg.norm(rm - r[i+1])  # n = next
        drm = rmi - rmi_n # Distance travelled towards center

        vr[i] = drm/dt
    return vr


#rtotal = integratooor(r1)
#print "The magical distance is", rtotal

vr = radial_velocity(r1,dt)
plt.plot(t,vr)
plt.show()
#print vr
vr_avgN20pst = sum(vr[0:int(N/5)])/int(N/5) # Average over first 20% of vr values
rmid         = np.sqrt(2*0.5**2)

print "As we ca see, the radial velocity stays constant,"
print "(except for numerical errors near the end), "
print "and the distance to middle, rm = sqrt(2*(0.5)^2), we have"
print "that time = rm / vr = ", rmid/vr_avgN20pst
