'''
Herhangi geçerli RGB üçlüsünü en yakın munsell rengine dönüştüren algoritma.
Kameradan gelen RGB değeriyle Munsell-RGB veri setindeki RGB değerleriyle karşılaştırıp
RGB uzayında en yakın (hata payı en az) olan değerini buluyor.
En yakın değeri bulmak için öklid uzaklığı formülünü kullanıyor.
(Uzaklık (hata payı)) = sqrt((R_cam - R_data)^2 + (G_cam - G_data)^2 + (B_cam - B_data)^2)

'''

import numpy as np
import pandas as pd

RGB_munsell_df = pd.read_table("RGB2munsell.dat", sep="\s+")
RGB_df = RGB_munsell_df[['R', 'G', 'B']]

example_rgb = np.array([125, 80, 55])

RGB_df = RGB_df - example_rgb
RGB_df = RGB_df ** 2
RGB_df['error'] = np.sqrt(np.abs(RGB_df['R'] + RGB_df['G'] + RGB_df['B']))

min_error_index = RGB_df[['error']].idxmin()
#print(RGB_df[['error']])
print("Example rgb value: ")
print(example_rgb)
print("\n")
print("closest munsell approximation: ")
print(RGB_munsell_df.loc[min_error_index, :])