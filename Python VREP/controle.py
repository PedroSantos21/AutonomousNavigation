import keras
from keras.models import Model
from keras.models import load_model
import numpy as np

model =  load_model('Redes/SLP_A.h5')# create the original model

slp_model = Model(inputs=model.input, outputs=model.output)

data = np.array([[0.138797557354, 0.179253721237, 1.0, 0.535036182404, 1.0, 0.738397884369, 0.330237340927, 1.0, 0.173112284301]])

output = slp_model.predict(data, batch_size=1, verbose=0, steps=None)


print output

