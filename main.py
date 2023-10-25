from gurobipy import GRB, Model, quicksum
from random import randint, uniform
import pandas as pd

#Procesar datos


# Conjuntos
A = ... # conjunto de vehículos
M = range(1) # conjunto de paquetes
J = ... # conjunto de ubicaciones
L = ... # tiempo de contrato
i = range(37) # paquetes de la empresa m

# Parámetros
N = ... # cantidad de paquetes de la empresa m
E = ... # emisiones de carbono del vehículo a
C = ... # capacidad máxima de cada vehículo
D = ... # distancia de la empresa m a la ubicación j
D = ... # distancia de la ubicación j1 a j2
t = ... # tiempo que demora el vehículo a en recorrer un kilómetro
T = ... # tiempo total de las entregas
p = ... # pago extra
M = 10**10

# Crear un modelo vacio

model = Model()

# Creamos Variables de decision 

# Variables
X = model.addVars(A, M, J, vtype=GRB.BINARY, name="X")
W = model.addVars(A, J, J, vtype=GRB.BINARY, name="W")
Z = model.addVars(A, vtype=GRB.BINARY, name="Z")
Y = model.addVars(J, vtype=GRB.CONTINUOUS, name="Y")

# Llama al update para agregar las variables al modelo
model.update()

# Restricciones

# 1. Restricción de capacidad
for a in A:
    for j in J:
        model.addConstr(quicksum(X[a,m,i,j] for m in M for i in I) <= C[a])

# 2. Cada paquete es transportado por un solo vehículo
for m in M:
    for i in I:
        for j in J:
            model.addConstr(quicksum(X[a,m,i,j] for a in A) == 1)

# 3. Cada ubicación de entrega es atendida una vez
for i in I:
    model.addConstr(quicksum(W[a,i,j] for a in A for j in J) == 1)

# 4. Restricción de flujo
for a in A:
    for i in I:
        model.addConstr(quicksum(W[a,j,i] for j in J) == 1)
        model.addConstr(quicksum(W[a,i,j] for j in J) == 1)

# 5. Restricción de recorrido
for a in A:
    for i in range(1, len(I)):
        for j in range(i+1, len(J)+1):
            model.addConstr(Y[a,i] - Y[a,j] + len(J)*W[a,i,j] <= len(J) - 1)

# 6. Restricción de tiempo
for a in A:
    model.addConstr(T - quicksum(X[a,m,i,j]*D[m,i] + W[a,i,j]*D[i,j] for m in M for i in I for j in J) + M*Z[a] >= 1)
    model.addConstr(quicksum(X[a,m,i,j]*D[m,i] + W[a,i,j]*D[i,j] for m in M for i in I for j in J) - T + M*(1-Z[a]) >= 0)


# Funcion objetivo

objetivo = quicksum(X[a,m,i,j]*D[m,i]*E[a] + W[a,i,j]*D[i,j]*E[a] for a in A for m in M for i in I for j in J)
model.setObjective(objetivo, GRB.MINIMIZE)


#Optimiza el problema

model.optimize()


# Mostrar resultados
for v in m.getVars():
    print(f'{v.varName} = {v.x}')

print(f'Objetivo: {m.objVal}')