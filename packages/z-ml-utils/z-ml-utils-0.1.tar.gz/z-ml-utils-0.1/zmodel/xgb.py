import xgboost as xgb
from sklearn.cross_validation import train_test_split

def make_model_with_stopping(train, target, watchlist, params, early_stopping_rounds=100):
	params = list(params.items())

	X_train, X_valid, y_train, y_valid = train_test_split(train, target, test_size=0.33, random_state=42)

	train = xgb.DMatrix(train, label=target)
	train_partial = xgb.DMatrix(X_train, label=y_train)
	valid = xgb.DMatrix(X_valid, label=y_valid)

	model = xgb.train(params, train_partial, 1000000, watchlist, early_stopping_rounds=early_stopping_rounds)
	ideal_rounds = model.best_iteration

	return xgb.train(plst, train, ideal_rounds, watchlist)