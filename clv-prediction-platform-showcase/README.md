Predictive Customer Segmentation and Lifetime Value Platform
Project Overview
For any business, understanding who the best customers are is critical for growth. The challenge is that this is often a difficult question to answer, especially for new customers. The goal of this project was to develop a system that could predict the future value of a customer based on their early interactions with an e-commerce platform.

This project documents the journey of building a sophisticated, two-stage machine learning model that first classifies customers into value tiers with high accuracy, and then predicts their potential lifetime spending. The final system provides a reliable, data-driven way to identify a company's best customers early, enabling smarter decisions in marketing, retention, and customer service.

Our Strategy: From a Hard Problem to a Smart Solution
Our initial attempts to predict the exact future dollar amount a customer would spend (a regression problem) proved to be very challenging. The primary issue was the "zero-inflated" nature of the data: a vast majority of customers make one or two purchases and never return. This creates a dataset where the target variable (future spending) is zero for most customers, making it difficult for a standard regression model to learn meaningful patterns without being overwhelmed by the non-spenders.

This led to a strategic pivot. Instead of chasing a precise dollar value, we reframed the problem into a more robust and actionable task: predictive segmentation. Our new goal was to predict a customer's future value tier ('Low', 'Medium', or 'High') based on their early behavior. This classification approach is less sensitive to extreme outliers and provides clear, actionable segments that a business can use immediately.

We then took this a step further by building a hybrid, two-stage model, also known as a "Mixture of Experts" model:

Stage 1 (Classification): A highly accurate classifier acts as a "router," predicting a new customer's lifetime value tier with high confidence.

Stage 2 (Regression): Based on the predicted tier, a specialized regression model, trained only on data from that specific segment, predicts the customer's final dollar value.

This approach is powerful because it allows each regression model to become an expert on its specific customer group. The "High-Value" model, for instance, doesn't get confused by the spending patterns of low-value customers, allowing it to achieve much higher precision.

The Dataset
This analysis was performed on the Olist Brazilian E-commerce Dataset, a large, multi-table dataset that provides a realistic and complex view of customer transactions, products, payments, and reviews. This rich dataset was crucial for engineering a wide range of behavioral features.

The Workflow: A Rigorous and Professional Approach
To ensure our model was robust and that its performance was trustworthy, we followed a strict validation process that mimics a real-world production environment.

The Holdout Set: From the very beginning, we split our entire customer base, locking 20% of customers away in a "holdout set." This data was not touched during any training or tuning. It was used only once, at the very end, to provide a completely unbiased evaluation of the final model's performance on new, unseen data.

"Early-Life" Feature Engineering: Our core hypothesis was that a customer's long-term value could be predicted from their initial interactions. We engineered a set of features that summarized a customer's behavior based only on their first 90 days of activity. This included metrics like their initial order frequency (frequency_90d), total spend (monetary_90d), and average payment installments, capturing early signs of engagement and investment.

Model Training: We trained our models (the main classifier and the three specialist regressors) using only the 80% development set. We used 5-fold cross-validation during this stage to ensure the classifier's performance was stable and not just the result of a single "lucky" data split.

Final Validation: The model's final performance was judged on its accuracy on the completely unseen holdout set. This proves its ability to generalize and make accurate predictions for new customers joining the platform.

Key Results
The hybrid model performed exceptionally well on the unseen holdout data, confirming the success of our strategy.

Classification Accuracy: The first-stage classifier achieved 97% accuracy in predicting a customer's final value tier. This high level of accuracy on an unseen holdout set confirms that a customer's long-term value is strongly indicated by their initial behavior.

High-Value Customer Precision: The classifier had 100% precision when identifying 'High' value customers. This is the most impactful business result, as it provides a zero-waste method for identifying future VIP customers. Marketing can confidently invest in these customers knowing the prediction is reliable.

Regression R-squared: The complete two-stage model achieved an R-squared of 0.92 in predicting the final dollar value. This demonstrates that once a customer is correctly segmented, their specific spending habits become much more predictable, proving the power of the specialized, two-stage approach.

Model Architecture: The "Brains" of the System
This repository contains the conceptual logic for the two stages of our model, explaining the architecture without the full implementation details.

classifier_logic.py: This file explains the "brain" of the first stage. It acts as a "router," taking a new customer's early-life features and sorting them into a value tier. We chose a LightGBM Classifier for this task. As a gradient boosting model, it builds an ensemble of simple decision trees sequentially, making it highly performant on tabular data. Its speed and memory efficiency are also key advantages for real-world applications.

regressor_logic.py: This file explains the logic of the second stage. It details the "mixture of experts" approach, where a specialist LightGBM regression model, trained only on data from a specific tier, is selected to provide the final, precise dollar-value prediction.

Future Work
The next logical step for this project would be to deploy this system and make it operational. This would involve:

Wrapping the two-stage prediction pipeline in a real-time API using a framework like FastAPI.

Containerizing the application with Docker to create a portable, scalable, and production-ready microservice.

Integrating the system with a database like PostgreSQL for data persistence and using a tool like MLflow for experiment tracking.