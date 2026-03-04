import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Membuat data 60 hari agar tren lebih terlihat jelas
dates = [datetime.now() - timedelta(days=i) for i in range(60)]
dates.reverse()

data = {
    'tanggal': dates * 3,
    'komoditas': ['Cabai Rawit']*60 + ['Bawang Merah']*60 + ['Beras Premium']*60,
    'harga': np.concatenate([
        # Cabai: Tren naik tajam (Inflasi)
        np.linspace(40000, 85000, 60) + np.random.randint(-3000, 3000, 60), 
        # Bawang: Tren turun (Panen raya)
        np.linspace(35000, 25000, 60) + np.random.randint(-1500, 1500, 60), 
        # Beras: Stabil
        [15000]*60 + np.random.randint(-300, 300, 60)
    ])
}

df = pd.DataFrame(data)
df.to_csv('harga_pangan.csv', index=False)
print("✅ File 'harga_pangan.csv' berhasil dibuat!")