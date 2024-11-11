import euler.py as e
def angleCalc(Lx,Ly,phi_x,theta_x,phi_y,theta_y,r_a1_O,r_a2_O):
    xb = 1/2*Lx[1,0,0]
    yb = 1/2*Ly[0,1,0]
    x = e.euler_321_matrix(0,theta_x,phi_x)@xb
    y = e.euler_321_matrix(0,theta_y,phi_y)@yb
    r_c1_O=x-y
    r_c2_O=x+y
