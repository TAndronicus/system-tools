from sklearn.neural_network import MLPRegressor
from random import Random
reg = MLPRegressor()
#pol sen jap kol
#pol:kol 0:3
#sen:kol 0:1
#jap:pol 0:1
#X = [[0, 0, 2, 1], [1, 2, 0, 0], [0, 2, 2, 0], [0, 0, 0, 3], [0, 0, 0, 1], [1, 0, 0, 0]]
iters = 100
sum = 0
for _ in range(iters):
    X = [[3, 4], [1, 2], [2, 3], [1, 4], [2, 4], [1, 3]]
    y = [1, -1, 0, -3, -1, 1]
    ind = Random().randint(1, 4)
    X1 = X.pop(ind)
    y1 = y.pop(ind)
    reg.fit(X, y)
    #print(X1)
    #print(y1)
    pr = reg.predict([X1])
    #print(pr)
    #print(round(pr[0]))
    sum += abs(y1 - round(pr[0]))
sum /= iters
print(sum)
