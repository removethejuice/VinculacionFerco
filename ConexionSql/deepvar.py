from gluonts.dataset.common import ListDataset
import pandas as pd
import numpy as np
from gluonts.mx.model.deepar import DeepAREstimator
from gluonts.mx.trainer import Trainer
# Read your dataset (convert ds to datetime)
df = pd.read_csv("ventas_formato_prophet_aceites.csv")  
df['ds'] = pd.to_datetime(df['ds'])

# Make sure it’s sorted
df = df.sort_values(['ItemCode', 'ds'])

# Group by product
product_datasets = []
item_codes = df['ItemCode'].unique()

for item in item_codes:
    group = df[df['ItemCode'] == item]
    sales = group['y'].values
    inventory = group['inventario'].values
    start = group['ds'].min()

    product_datasets.append({
        "target": sales.astype(float),
        "start": start,
        "dynamic_real_features": [inventory.astype(float)],
    })

train_ds = ListDataset(
    product_datasets,
    freq="1M"
)



estimator = DeepAREstimator(
    prediction_length=3,  # or however many months ahead you want to forecast
    context_length=6,
    freq="1M",
    use_feat_dynamic_real=True,
    trainer=Trainer(epochs=50),
)

predictor = estimator.train(train_ds)
from gluonts.evaluation.backtest import make_evaluation_predictions

forecast_it, ts_it = make_evaluation_predictions(
    dataset=train_ds,
    predictor=predictor,
    num_samples=100
)

forecasts = list(forecast_it)
import matplotlib.pyplot as plt

forecast = forecasts[0]
ts = list(ts_it)[0]

ts[-30:].plot(label="actual")
forecast.plot(prediction_intervals=[50, 90])
plt.grid(True)
plt.legend()
plt.show()
