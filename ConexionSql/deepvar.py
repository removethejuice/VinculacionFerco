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
        "feat_dynamic_real": [inventory.astype(float)],
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
ts = list(ts_it)

rows = []

for i, forecast in enumerate(forecasts):
    item_code = item_codes[i % len(item_codes)]
    for ds, yhat, q10, q50, q90 in zip(forecast.index, forecast.mean, forecast.quantile(0.1), forecast.quantile(0.5), forecast.quantile(0.9)):
        rows.append({
            "ItemCode": item_code,
            "ds": ds,               # fecha de predicción
            "yhat": yhat,           # media de predicción
            "q10": q10,             # intervalo inferior
            "q50": q50,             # mediana
            "q90": q90              # intervalo superior
        })

df_forecasts = pd.DataFrame(rows)

df_forecasts.to_csv("predicciones_deepAR.csv", index=False)

print("✅ Predicciones guardadas en 'predicciones_deepAR.csv'")