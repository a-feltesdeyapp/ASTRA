def copCalc(a,b,F1,F2,F3,F4):
    # calculates center of pressure for pressure sensors in cardinal directions
    # a contains the length from the center of the board to left and right sides
    # b contains the length from the center of the board to forward and backwards sides

    W1 = F1+F3
    W2 = F2+F4
    cop = [a*(F1-F3)/W1,a*(F2-F4)/W2]
    return cop
    
def copCornerCalc(a,b,F1,F2,F3,F4):
    # calculates center of pressure for pressure sensors in corners
    # a contains the length from the center of the board to left and right sides
    # b contains the length from the center of the board to forward and backwards sides

    W = F1+F2+F3+F4
    cop = [a*((F1+F2)-(F3+F4))/W, b*((F1+F4)-(F2+F3))/W]
    return cop