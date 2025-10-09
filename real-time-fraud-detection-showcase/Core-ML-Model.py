
# Description:  This file showcases the "brain" of the operation—the XGBoost
#               model—and the crucial strategy used to train it.


import xgboost as xgb

def build_fraud_model_config():
    """
    Defines the configuration for our XGBoost model.

    For a project like this, the model's "architecture" isn't just the code,
    it's the strategic decisions made during setup. The most critical decision
    was how to handle the massive class imbalance in the data.

    This function returns the hyperparameters that define our model's behavior.
    """
    # This is the secret sauce for handling imbalanced data like fraud.
    # A typical dataset might have 99.8% legitimate transactions and only 0.2%
    # fraud. This `scale_pos_weight` parameter is a lever we pull to tell the
    # model: "Pay hundreds of times more attention to the rare fraud cases.
    # They are the ones that matter most."
    # The value would be calculated from the training data, e.g., count(negative)/count(positive).
    calculated_scale_pos_weight = 500 # Example value for a highly imbalanced dataset

    model_params = {
        'objective': 'binary:logistic',
        'eval_metric': 'aucpr', # Area Under Precision-Recall Curve, great for imbalanced data.
        'use_label_encoder': False,
        'scale_pos_weight': calculated_scale_pos_weight, # Here's where we apply the magic lever.
        'random_state': 42
    }

    # The actual training step (`model.fit()`) is intentionally left out.
    # This snippet is all about the blueprint and the strategy.
    return model_params
