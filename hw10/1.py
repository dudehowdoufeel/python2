import numpy as np
import matplotlib.pyplot as plt

X=np.array([1,2,3,4,5])
Y=np.array([10,20,30,40,50])

def predict(beta_0, beta_1, X):
    return beta_0+beta_1*X

def cost_function(Y_pred, Y_actual):
    n = len(Y_actual)
    mse = (1 / n) * np.sum((Y_pred - Y_actual) ** 2)
    return mse

def gr(X,Y,beta_0,beta_1,alpha,ite):
    n=len(Y)
    for _ in range(ite):
        Y_pred=predict(beta_0,beta_1, X)
        d_beta_0=(2/n)*np.sum(Y_pred-Y) #partial der
        d_beta_1=(2/n)*np.sum((Y_pred-Y)*X)
        
        beta_0-=alpha*d_beta_0
        beta_1-=alpha*d_beta_1
    return beta_0,beta_1

beta_0=0  #initial cond #intercept
beta_1=1 #slope
alpha=0.01 
ite=500

optimized_b0, optimized_b1=gr(X, Y, beta_0, beta_1, alpha, ite) #gradient

X_test=np.array([6,10]) #hours
predictions=predict(optimized_b0, optimized_b1, X_test)

#graphik
plt.scatter(X, Y, color='blue', label='data pnt')
X_line=np.linspace(0,10,100)
Y_line=predict(optimized_b0, optimized_b1, X_line)
plt.plot(X_line, Y_line, color='red', label='best fit line')
plt.title('lin reg')
plt.xlabel('x, h')
plt.ylabel('y, saving')
plt.legend()
plt.grid()
plt.show()

print("intercept ", optimized_b0)
print("slope ", optimized_b1)
print("6h ", predictions[0])
print("10h ", predictions[1])
'''
outputs
intercept  0.4257785888899636
slope  9.882066158259107
6h  59.718175538444605
10h  99.24644017148104
 
'''