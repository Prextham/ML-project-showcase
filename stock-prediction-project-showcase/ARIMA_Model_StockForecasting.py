# ARIMA Model for Stock Forecasting

# This file showcases the ARIMA model, which played a very special role in
# my final ensemble: "The Conservative Statistician."
#
# Unlike the neural networks, this model is intentionally simple. It's completely
# blind to all the complex features like news sentiment or market volatility.
# It only looks at the raw price history, providing a stable, trend-based
# forecast that acts as a valuable "sanity check" for the other models.
#
# Its job wasn't to be the most accurate, but to provide a different
# perspective and protect the ensemble from overfitting to noisy signals.

import pmdarima as pm

def find_best_arima_model(price_series):
    """
    Finds the best ARIMA model parameters using an automated search.

    For a classical model like ARIMA, the "architecture" is defined by its
    (p, d, q) parameters. Instead of picking them manually, I used auto_arima
    to perform a data-driven search for the optimal combination. It's like
    running an architecture search for a statistical model.

    Args:
        price_series (pd.Series): A pandas Series of historical stock prices.

    Returns:
        Fitted pmdarima model: The fitted ARIMA model object, which contains
                               the optimal parameters and coefficients.
    """
    # This function automatically searches for the best (p,d,q) parameters.
    # It's the core of the "architecture" definition for this model.
    arima_model = pm.auto_arima(
        price_series,
        start_p=1,
        start_q=1,
        test='adf',          # Use the ADF test to find the right amount of differencing (d)
        max_p=3, max_q=3,    # Keep the search space reasonable
        m=1,                 # m=1 for daily, non-seasonal data
        d=None,              # Let the test find 'd' for us
        seasonal=False,      # Explicitly state there's no seasonality
        trace=False,         # Set to True to see the search steps
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True        # Use a faster, stepwise search method
    )

    return arima_model

# The output of this function—the fitted model with its specific (p,d,q)
# orders—is the final "architecture" for the ARIMA component of the ensemble.
