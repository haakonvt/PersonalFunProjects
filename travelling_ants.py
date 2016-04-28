import numpy as np
import matplotlib.pyplot as plt

dt = 0.05
v  = 1
N  = int(round(1/dt))
t  = np.linspace(0,dt*N-dt,N)

# At t = 0
r1 = np.zeros((N,2))
r2 = np.zeros((N,2))
r3 = np.zeros((N,2))
r4 = np.zeros((N,2))
r1[0] = np.array((0,0))
r2[0] = np.array([1,0])
r3[0] = np.array([1,1])
r4[0] = np.array([0,1])

# Create separate solution with Runge Kutta 4
R1 = np.zeros((N,2))
R2 = np.zeros((N,2))
R3 = np.zeros((N,2))
R4 = np.zeros((N,2))
R1[0] = np.array((0,0))
R2[0] = np.array([1,0])
R3[0] = np.array([1,1])
R4[0] = np.array([0,1])

# Create separate solution with Forward Euler
r1fe = np.zeros((N,2))
r2fe = np.zeros((N,2))
r3fe = np.zeros((N,2))
r4fe = np.zeros((N,2))
r1fe[0] = np.array((0,0))
r2fe[0] = np.array([1,0])
r3fe[0] = np.array([1,1])
r4fe[0] = np.array([0,1])

for i in range(N-1):
    # -----------------------------
    # Forward Euler, first order
    r1r2 = (r2fe[i]-r1fe[i])/(np.linalg.norm(r2fe[i]-r1fe[i]))
    r2r3 = (r3fe[i]-r2fe[i])/(np.linalg.norm(r3fe[i]-r2fe[i]))
    r3r4 = (r4fe[i]-r3fe[i])/(np.linalg.norm(r4fe[i]-r3fe[i]))
    r4r1 = (r1fe[i]-r4fe[i])/(np.linalg.norm(r1fe[i]-r4fe[i]))

    r1fe[i+1] = r1fe[i] + r1r2*v*dt
    r2fe[i+1] = r2fe[i] + r2r3*v*dt
    r3fe[i+1] = r3fe[i] + r3r4*v*dt
    r4fe[i+1] = r4fe[i] + r4r1*v*dt
    # -----------------------------

    # ----------------------------------------
    # Runge Kutta of second order
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
    # ----------------------------------------

    # ----------------------------------------
    # Runge Kutta of fourth order
    k1R1 = (R2[i]-R1[i])/(np.linalg.norm(R2[i]-R1[i]))
    k1R2 = (R3[i]-R2[i])/(np.linalg.norm(R3[i]-R2[i]))
    k1R3 = (R4[i]-R3[i])/(np.linalg.norm(R4[i]-R3[i]))
    k1R4 = (R1[i]-R4[i])/(np.linalg.norm(R1[i]-R4[i]))

    R1k2 = R1[i] + k1R1*v*dt/2.0 # Use k1 direction and walk half the interval
    R2k2 = R2[i] + k1R2*v*dt/2.0
    R3k2 = R3[i] + k1R3*v*dt/2.0
    R4k2 = R4[i] + k1R4*v*dt/2.0

    k2R1 = (R2k2-R1k2)/(np.linalg.norm(R2k2-R1k2)) # New direction half interval
    k2R2 = (R3k2-R2k2)/(np.linalg.norm(R3k2-R2k2))
    k2R3 = (R4k2-R3k2)/(np.linalg.norm(R4k2-R3k2))
    k2R4 = (R1k2-R4k2)/(np.linalg.norm(R1k2-R4k2))

    R1k3 = R1[i] + k2R1*v*dt/2.0 # Use k2 direction and walk half the interval from beginning
    R2k3 = R2[i] + k2R2*v*dt/2.0
    R3k3 = R3[i] + k2R3*v*dt/2.0
    R4k3 = R4[i] + k2R4*v*dt/2.0

    k3R1 = (R2k3-R1k3)/(np.linalg.norm(R2k3-R1k3)) # New even better direction at half interval
    k3R2 = (R3k3-R2k3)/(np.linalg.norm(R3k3-R2k3))
    k3R3 = (R4k3-R3k3)/(np.linalg.norm(R4k3-R3k3))
    k3R4 = (R1k3-R4k3)/(np.linalg.norm(R1k3-R4k3))

    R1k4 = R1[i] + k3R1*v*dt # Use k3 direction and walk the whole interval from beginning
    R2k4 = R2[i] + k3R2*v*dt
    R3k4 = R3[i] + k3R3*v*dt
    R4k4 = R4[i] + k3R4*v*dt

    k4R1 = (R2k4-R1k4)/(np.linalg.norm(R2k4-R1k4)) # Direction at end of interval after "iterative process"
    k4R2 = (R3k4-R2k4)/(np.linalg.norm(R3k4-R2k4))
    k4R3 = (R4k4-R3k4)/(np.linalg.norm(R4k4-R3k4))
    k4R4 = (R1k4-R4k4)/(np.linalg.norm(R1k4-R4k4))

    R1[i+1] = R1[i] + dt*v*(k1R1 + k2R1*2. + k3R1*2. + k4R1)/6.0
    R2[i+1] = R2[i] + dt*v*(k1R2 + k2R2*2. + k3R2*2. + k4R2)/6.0
    R3[i+1] = R3[i] + dt*v*(k1R3 + k2R3*2. + k3R3*2. + k4R3)/6.0
    R4[i+1] = R4[i] + dt*v*(k1R4 + k2R4*2. + k3R4*2. + k4R4)/6.0


def radial_velocity(r,dt):
    vr = np.zeros(len(r)) # Magnitude of v in direction of middle
    rm = np.array([0.5,0.5])
    for i in range(N-1):
        rmi   = np.linalg.norm(rm - r[i])
        rmi_n = np.linalg.norm(rm - r[i+1])  # n = next
        drm = rmi - rmi_n # Distance travelled towards center

        vr[i] = drm/dt
    return vr

# Compute the radial velocity (towards the center)
vr = radial_velocity(R1,dt)

if raw_input("Hit 'enter' to skip plot (or 'anything' then 'enter' to see plots)") != '':
    plt.plot(r1[:,0], r1[:,1],'o-')
    plt.plot(r1fe[:,0], r1fe[:,1],'o-')
    plt.plot(R1[:,0], R1[:,1],'o-')
    plt.plot(r2[:,0], r2[:,1],'o-')
    plt.plot(r2fe[:,0], r2fe[:,1],'o-')
    plt.plot(R2[:,0], R2[:,1],'o-')
    plt.plot(r3[:,0], r3[:,1],'o-')
    plt.plot(r3fe[:,0], r3fe[:,1],'o-')
    plt.plot(R3[:,0], R3[:,1],'o-')
    plt.plot(r4[:,0], r4[:,1],'o-')
    plt.plot(r4fe[:,0], r4fe[:,1],'o-')
    plt.plot(R4[:,0], R4[:,1],'o-')
    plt.legend(["r1 RK2","r1 FE","r1 RK4","r2 RK2","r2 FE","r2 RK4","r3 RK2","r3 FE","r3 RK4","r4 RK2","r4 FE","r4 RK4"])
    plt.axis('equal')
    plt.show()

    plt.plot(t,vr,'o-')
    plt.title("Magnitude of radial velocity (i.e. towards center)")
    plt.xlabel("Time")
    plt.ylabel("Velocity")
    plt.show()

vr_avgN20pst = sum(vr[0:int(N/5)])/int(N/5) # Average over first 20% of vr values
rmid         = np.sqrt(2*0.5**2)

print "-------------------------"
print "As we ca see, the radial velocity stays constant,"
print "(except for numerical errors near the end), "
print "and the distance to middle, rm = sqrt(2*(0.5)^2), we have"
print "that time = rm / vr = ", rmid/vr_avgN20pst
