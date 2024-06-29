# Processing Time Prediction with TCN + Transformer and TCN + LSTM

We implement a hybrid TCN-Transformer and a hybrid TCN-LSTM architecture to improve the accuracy of shipment processing time predictions. By combining the efficient processing and temporal dependency capturing capabilities of TCNs with the self-attention mechanism of Transformers, or the sequential data handling strengths of LSTMs—specifically their ability to learn order dependencies in sequence prediction problems—this hybrid approach offers a robust solution for forecasting processing times in manufacturing contexts, among others:

![Brainstorming](https://github.com/KatharinaTrinley/Prediction-model-TCN-Transformer/assets/152901977/9e712f20-9827-4937-ba4e-633864136b50)


`preprocessed.txt` Contains the preprocessed data used for training the model:

Each line represents a data point, showing various stages of the shipment process and associated attributes. The preprocessing included turning the timestamps to Unix format and extract date, time, and weekday components, aggregate package dimensions and counts per order, handling missing values, one-hot encode categorical data, remove outliers, and normalize features using Min-Max scaling & Z-score normalization.

`tcn_transformer.py` Main file that includes the TCN Transformer model:

A TCN layer acts as the initial feature extractor, using dilated causal convolutions to deal with temporal dependencies. 
Stacked TCN layers are used to process the data and extract hierarchical temporal features. 
The Attention Mechanism enhances the model's ability to focus on relevant features for prediction by computing attention weights.
With multi-head attention mechanism different parts of the input sequence are dealt with. 
Next, the extracted features are input to a Transformer Decoder, where the self-attention layers and feed-forward neural networks learn the relationships across the input sequences. 
Finally, a dense layer produces the final forecasted shipment processing time.

`tcn_transformer_sparse-self-attention.py` File which includes the TCN Transformer model with sparse self attention.

`TCN.py` Implements only a TCN. Baseline Model I

`LSTM.py` Implements a LSTM. Baseline Model II.

`lin_reg.py` Implements a linear regression model. Baseline Model III.


