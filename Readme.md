tkg-interfaces
=======================

Main aim of data collection is using it to create a Neural Network Trading Bot

With current developments in Cryptocurrency market, 
hot topic is applying deep learning models into trading and then predicting the price trends using those models and trading automatically with bots.

Deep learning is different than traditional machine learning and it is highly dependent on how much and how good your data is.

When we want to train a model using Python and Keras we will face the problem with data availability which we try to solve with this repo. 
Data collected is useful for all sorts of different uses. Not only predicting future price predictions, 
deep learning can also be used for uncovering the price changes between different exchanges, 
unrevealing arbitrage opportunities before it happens.

1. Use ccxt library to fetch data from Binance, Kucoin, ...
2. Store it in InfluxDB
3. Easily fetch it from InfluxDb as Pandas DataFrame for streaming analyzing


