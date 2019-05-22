import matplotlib.pyplot as plt

# RGB to CIE XYZ
var_R = ( 137 / 255 )
var_G = ( 56 / 255 )
var_B = ( 146 / 255 )


if (var_R > 0.04045):
    var_R = ((var_R + 0.055 )/1.055)**2.4
else:
    var_R = var_R / 12.92

if (var_G>0.04045):
    var_G = ((var_G +0.055 )/1.055)**2.4
else:
    var_G = var_G / 12.92

if (var_B>0.04045):
    var_B = ((var_B+0.055 )/1.055)**2.4
else:
    var_B = var_B / 12.92

var_R = var_R * 100
var_G = var_G * 100
var_B = var_B * 100

X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
print("Here are corresponding color values in CIE XYZ: X = %.4f, Y = %.4f, Z = %.4f " % (X, Y, Z))

x = X/(X+Y+Z)
y = Y/(X+Y+Z)
print("Here are corresponding color values in CIE xyY: x = %.4f, y = %.4f, Y = %.4f " % (x, y, Y))

var_R = ( 137 / 255 )
var_G = ( 56 / 255 )
var_B = ( 146 / 255 )

var_K = 1-(max(var_R, var_G, var_B))

var_C = (1-var_R-var_K)/(1-var_K)
var_M = (1-var_G-var_K)/(1-var_K)
var_Y = (1-var_B-var_K)/(1-var_K)
print("Here are corresponding color values in CMYK: C = %.4f, M = %.4f, Y = %.4f, K = %.4f " % (var_C, var_M, var_Y, var_K))


var_Min = min( var_R, var_G, var_B )
var_Max = max( var_R, var_G, var_B )
del_Max = var_Max - var_Min

V = var_Max

if (del_Max == 0):
    H = 0
    S = 0
else:
   S = del_Max / var_Max

   del_R = ( ( ( var_Max - var_R ) / 6 ) + ( del_Max / 2 ) ) / del_Max
   del_G = ( ( ( var_Max - var_G ) / 6 ) + ( del_Max / 2 ) ) / del_Max
   del_B = ( ( ( var_Max - var_B ) / 6 ) + ( del_Max / 2 ) ) / del_Max

   if (var_R == var_Max):
       H = del_B - del_G
   elif(var_G == var_Max):
       H = ( 1 / 3 ) + del_R - del_B
   elif(var_B == var_Max):
       H = ( 2 / 3 ) + del_G - del_R

if ( H < 0 ):
    H += 1
if ( H > 1 ):
    H -= 1
print("Here are corresponding color values in HSV: H = %.4f, S = %.4f, V = %.4f " % (H, S, V))


HSL_L = ( var_Max + var_Min )/ 2

if (del_Max == 0):
    HSL_H = 0
    HSL_S = 0
else:
    if(HSL_L<0.5):
        HSL_S = del_Max/ (var_Max+var_Min)
    HSL_S = del_Max/ (2-var_Max-var_Min)

    del_R = ( ( ( var_Max - var_R ) / 6 ) + ( del_Max / 2 ) ) / del_Max
    del_G = ( ( ( var_Max - var_G ) / 6 ) + ( del_Max / 2 ) ) / del_Max
    del_B = ( ( ( var_Max - var_B ) / 6 ) + ( del_Max / 2 ) ) / del_Max

    if (var_R == var_Max):
        HSL_H = del_B - del_G
    elif(var_G == var_Max):
        HSL_H = ( 1 / 3 ) + del_R - del_B
    elif(var_B == var_Max):
        HSL_H = ( 2 / 3 ) + del_G - del_R

if ( HSL_H < 0 ):
    HSL_H += 1
if ( HSL_H > 1 ):
    HSL_H -= 1
print("Here are corresponding color values in HSL: H = %.4f, S = %.4f, V = %.4f " % (HSL_H, HSL_S, HSL_L))

plt.imshow([[(var_R, var_G, var_B)]])
plt.savefig('Color.png')
plt.show()
