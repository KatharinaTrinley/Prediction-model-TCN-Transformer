# install tensorflow==2.13.1 first

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from sklearn.metrics import r2_score

# data preparation
eingang_ts = ['date_EINGANGSDATUM_UHRZEIT', 'time_EINGANGSDATUM_UHRZEIT', 'weekday_EINGANGSDATUM_UHRZEIT']
verpackt_ts = ['date_VERPACKT_DATUM_UHRZEIT', 'time_VERPACKT_DATUM_UHRZEIT',
               'weekday_VERPACKT_DATUM_UHRZEIT', 'secs_VERPACKT_DATUM_UHRZEIT']
auftragsnummer_ts = ['date_AUFTRAGANNAHME_DATUM_UHRZEIT', 'time_AUFTRAGANNAHME_DATUM_UHRZEIT',
                     'weekday_AUFTRAGANNAHME_DATUM_UHRZEIT', 'secs_AUFTRAGANNAHME_DATUM_UHRZEIT']
lieferschein_ts = ['date_LIEFERSCHEIN_DATUM_UHRZEIT', 'time_LIEFERSCHEIN_DATUM_UHRZEIT',
                   'weekday_LIEFERSCHEIN_DATUM_UHRZEIT', 'secs_LIEFERSCHEIN_DATUM_UHRZEIT']
auftragannahme_ts = ['date_AUFTRAGANNAHME_DATUM_UHRZEIT', 'time_AUFTRAGANNAHME_DATUM_UHRZEIT',
                     'weekday_AUFTRAGANNAHME_DATUM_UHRZEIT', 'secs_AUFTRAGANNAHME_DATUM_UHRZEIT']
bereitgestellt_ts = ['date_BEREITGESTELLT_DATUM_UHRZEIT', 'time_BEREITGESTELLT_DATUM_UHRZEIT',
                     'weekday_BEREITGESTELLT_DATUM_UHRZEIT', 'secs_BEREITGESTELLT_DATUM_UHRZEIT']
TA_ts = ['weekday_TA_DATUM_UHRZEIT', 'date_TA_DATUM_UHRZEIT', 'time_TA_DATUM_UHRZEIT', 'secs_TA_DATUM_UHRZEIT']

package_data = ['LAENGE_IN_CM', 'BREITE_IN_CM', 'HOEHE_IN_CM', 'GEWICHT_IN_KG', 'count_PACKSTUECKART=BEH',
                'count_PACKSTUECKART=CAR', 'count_PACKSTUECKART=GBP', 'count_PACKSTUECKART=PAL',
                'count_PACKSTUECKART=PKI', 'count_PACKSTUECKART=UNKNOWN', 'PACKAGE_COUNT']
auftragsnummer = ['category_AUFTRAGSNUMMER=DSGA', 'category_AUFTRAGSNUMMER=RBMANUSHIP', 'category_AUFTRAGSNUMMER=return']
land = ['LAND=AT', 'LAND=AUT', 'LAND=BE', 'LAND=BR', 'LAND=CH', 'LAND=CN', 'LAND=CZ', 'LAND=DE', 'LAND=DK', 'LAND=DR',
        'LAND=ES', 'LAND=FCA', 'LAND=FR', 'LAND=HU', 'LAND=IE', 'LAND=IN', 'LAND=IT', 'LAND=JP', 'LAND=KR', 'LAND=MX',
        'LAND=NL', 'LAND=None', 'LAND=PL', 'LAND=RO', 'LAND=RU', 'LAND=TR', 'LAND=UK', 'LAND=US']
sonderfahrt = ['SONDERFAHRT']
dienstleister = ['DIENSTLEISTER=DHL', 'DIENSTLEISTER=None', 'DIENSTLEISTER=TNT', 'DIENSTLEISTER=UPS']

step_1_features = eingang_ts + sonderfahrt
step_2_features = step_1_features + verpackt_ts + auftragsnummer_ts + package_data + auftragsnummer
step_3_features = step_2_features + land + auftragannahme_ts + auftragannahme_ts + lieferschein_ts
step_4_features = step_3_features + bereitgestellt_ts
step_5_features = step_4_features + TA_ts + dienstleister

data = pd.read_csv('preprocessed.txt')

X = data[step_5_features]
y = np.array(data['PROCESSING'])

scaler_X = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y_scaled, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

def augment_data(X_train, y_train, num_augmentations=3):
    augmented_X = X_train.copy()
    augmented_y = y_train.copy()

    for _ in range(num_augmentations):
        temp_X = X_train.copy()
        temp_y = y_train.copy()

        # applying random noise to the 'PROCESSING' feature, assumed to be the first feature
        temp_X[:, 0] += np.random.normal(0, 0.01, size=temp_X[:, 0].shape)

        augmented_X = np.concatenate((augmented_X, temp_X), axis=0)
        augmented_y = np.concatenate((augmented_y, temp_y), axis=0)

    return augmented_X, augmented_y

X, y = augment_data(X_train, y_train, num_augmentations=3)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dropout, Flatten, Dense, LSTM, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback
from tensorflow.keras import backend as K
import tensorflow as tf

def r2score(y_true, y_pred):
    SS_res = K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return 1 - SS_res/(SS_tot + K.epsilon())

def r2score(y_true, y_pred):
    return tf.py_function(r2_score, [y_true, y_pred], tf.double)

class MetricsCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"Epoch {epoch+1} - loss: {logs['loss']:.4f} - val_loss: {logs['val_loss']:.4f} - mae: {logs['mae']:.4f} - val_mae: {logs['val_mae']:.4f} - mse: {logs['mse']:.4f} - val_mse: {logs['val_mse']:.4f}")

model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(78, 1)))
model.add(Dropout(0.1))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(Dropout(0.1))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))

model.add(Bidirectional(LSTM(64, return_sequences=True)))
model.add(Bidirectional(LSTM(64)))

model.add(Flatten())
model.add(Dense(64, activation='relu', kernel_regularizer='l2'))
model.add(Dense(16, activation='relu', kernel_regularizer='l2'))
model.add(Dense(1))

optimizer = Adam(learning_rate=5e-5)
model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mae', 'mse', r2score])
model.summary()

history = model.fit(X, y, epochs=100, batch_size=64, validation_data=(X_val, y_val), callbacks=[MetricsCallback()])

loss, mae, mse, r2 = model.evaluate(X_test, y_test)

print(f'Test MAE: {mae}')
print(f'Test MSE: {mse}')
print(f'Test R2: {r2}')

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()