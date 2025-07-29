import pandas as pd
from gluonts.dataset.common import ListDataset
from gluonts.dataset.field_names import FieldName
from gluonts.torch.model.deepvar import DeepVAREstimator
from gluonts.torch.distributions import StudentTOutput
from gluonts.mx.trainer import Trainer
from gluonts.evaluation.backtest import make_evaluation_predictions
from gluonts.evaluation import MultivariateEvaluator

# --- Load Dataset ---
df = pd.read_csv("ventas_formato_prophet_aceites.csv", parse_dates=["ds"])  # Update filename if needed
df = df.sort_values(by=["ItemCode", "ds"])

# --- Prepare Dataset ---
series_list = []
for item_code in df["ItemCode"].unique():
    item_df = df[df["ItemCode"] == item_code]
    target_array = item_df[["y", "inventario"]].to_numpy().T  # (2, T)
    
    series = {
        FieldName.START: item_df["ds"].min(),
        FieldName.TARGET: target_array,
        FieldName.ITEM_ID: str(item_code),
    }
    series_list.append(series)

train_ds = ListDataset(series_list, freq="D")


estimator = DeepVAREstimator(
    freq="D",
    prediction_length=7,
    target_dim=2,
    trainer=Trainer(epochs=10)
)


predictor = estimator.train(train_ds)

# --- Make Predictions ---
forecast_it, ts_it = make_evaluation_predictions(
    dataset=train_ds,
    predictor=predictor,
    num_samples=100
)

forecasts = list(forecast_it)
tss = list(ts_it)

# --- Evaluate ---
evaluator = MultivariateEvaluator(target_agg_methods=["sum"])
agg_metrics, item_metrics = evaluator(tss, forecasts)

print("\nAggregate Forecast Metrics:")
for k, v in agg_metrics.items():
    print(f"{k:30s}: {v:.4f}")

import matplotlib.pyplot as plt

forecast = forecasts[0]
ts = tss[0]

for i, target_name in enumerate(["Price", "Inventory"]):
    plt.figure(figsize=(10, 4))
    ts[i].plot(label="Actual")
    forecast.quantile(0.5)[i].plot(label="Forecast (Median)")
    plt.title(f"Forecast for {target_name}")
    plt.legend()
    plt.show()
