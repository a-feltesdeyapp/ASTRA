def copCalc(a,F1,F2,F3,F4):
    # calculates center of pressure
    # a contains the length from the center of the board to each pressure 
    W=F1+F2
    cop = [a*(F1-F3)/W,a*(F2-F4)/W]
    