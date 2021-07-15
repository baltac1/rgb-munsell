import pandas as pd 

# dönüşümler hakkında ayrıntılı bilgi edinmek için http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
# sitesini okuyabilirsiniz. 

def xyY_to_XYZ(xyY):
	X = xyY_df['x'] * (xyY_df['Y'] / xyY_df['y'])
	Y = xyY_df['Y']
	Z = (1 - xyY_df['x'] - xyY_df['y']) * (xyY_df['Y']/xyY_df['y'])

	XYZ_df = pd.DataFrame()
	XYZ_df['H'] = xyY_df['H']
	XYZ_df['V'] = xyY_df['V']
	XYZ_df['C'] = xyY_df['C']
	XYZ_df['X'] = X
	XYZ_df['Y'] = Y
	XYZ_df['Z'] = Z
	return XYZ_df


def XYZ_to_RGB(XYZ_df):
	RGB_df = pd.DataFrame(columns=['H', 'V', 'C', 'R', 'G', 'B'])

	for index, row in XYZ_df.iterrows():
		var_X = row['X'] / 100
		var_Y = row['Y'] / 100
		var_Z = row['Z'] / 100

		var_R = var_X *  3.2406 + var_Y * -1.5372 + var_Z * -0.4986
		var_G = var_X * -0.9689 + var_Y *  1.8758 + var_Z *  0.0415
		var_B = var_X *  0.0557 + var_Y * -0.2040 + var_Z *  1.0570

		if ( var_R > 0.0031308 ):
			var_R = 1.055 * ( var_R ** ( 1 / 2.4 ) ) - 0.055
		else:
			var_R = 12.92 * var_R
		if ( var_G > 0.0031308 ):
			var_G = 1.055 * ( var_G ** ( 1 / 2.4 ) ) - 0.055
		else:
			var_G = 12.92 * var_G
		if ( var_B > 0.0031308 ):
			var_B = 1.055 * ( var_B ** ( 1 / 2.4 ) ) - 0.055
		else:
			var_B = 12.92 * var_B

		sR = var_R * 255
		sG = var_G * 255
		sB = var_B * 255
		row = {'H':row['H'], 'V':row['V'], 'C':row['C'], 'R':sR, 'G':sG, 'B':sB}
		RGB_df = RGB_df.append(row, ignore_index=True)
		if (index % 250 == 0):
			print(index)
	return RGB_df

xyY_df = pd.read_table("munsell_xyY_data.dat", sep="\s+") # Munsell-xyY verisi

XYZ_df = xyY_to_XYZ(xyY_df) # xyY-XYZ dönüşümü
RGB_df = XYZ_to_RGB(XYZ_df) # XYZ-RGB dönüşümü
# XYZ-RGB dönüşümü lineer olmadığı için bazı RGB değerleri olması gereken,
# aralığın dışında değerler olabiliyor (negatif veya 255'ten büyük)

for index, row in RGB_df[['R', 'G', 'B']].iterrows(): 
	for element in row:
		if (element < 0 or element > 255):
			RGB_df = RGB_df.drop(index, axis=0)
			break

	if (index%250 == 0):
		print(index)
# bu hatalı değerlerden kurtulduk.

RGB_df.to_csv("RGB2munsell.dat", sep=" ")
print(RGB_df.head())