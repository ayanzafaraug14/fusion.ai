from sklearn.tree import DecisionTreeClassifier

# Example training data
X = [[4], [2], [0]]   # legs
y = ["Dog", "Chicken", "Snake"]

model = DecisionTreeClassifier()
model.fit(X, y)

def predict_animal(legs):
    return model.predict([[legs]])[0]
