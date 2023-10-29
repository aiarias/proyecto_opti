from gurobipy import GRB, Model, quicksum
from random import randint, uniform
import pandas as pd

#Procesar datos

# Escribe los datos de distnacia en D_e y D
file_path = 'distancias_santiago.xlsx'
df = pd.read_excel(file_path, engine='openpyxl', sheet_name='Sheet1')  # Asegúrate de usar el nombre correcto de la hoja

# Eliminando cualquier fila o columna que no contenga datos
df.dropna(how="all", inplace=True)
df.dropna(axis=1, how="all", inplace=True)

# Asumiendo que la primera columna es 'Direcciones' y contiene todas las direcciones
direcciones = df['Direcciones'].tolist()

# Distancia de la empresa m a la ubicación j
# Suponiendo que 'Camino Lo Boza, 120, Pudahuel, Chile' es la empresa m
D_e = df.set_index('Direcciones')['Camino Lo Boza, 120, Pudahuel, Chile'].to_dict()

# Distancia entre cada ubicación
D = {}
for i in direcciones:
    for j in direcciones:
        if i != j:
            D[(i, j)] = df.loc[df['Direcciones'] == i, j].values[0]


# Cargamos informacion vehiculo/emisiones
df_emisiones = pd.read_excel("Datos.xlsx", sheet_name="Emisiones")

# Crear un diccionario con los nombres de los vehículos como claves y sus emisiones como valores
emisiones_dict = dict(zip(df_emisiones['Tipo de Vehículo / Combustible'], df_emisiones['Emisiones de CO2 (g CO2/km)']))

#cargar datos capacidad 
df_capacidad = pd.read_excel("Datos.xlsx", sheet_name="Capacidad")

# Crear un diccionario con los nombres de los vehículos como claves y sus capacidades como valores
capacidad_dict = dict(zip(df_capacidad['Tipo de Vehiculo / Combustible'], df_capacidad['Capacidad (unidades)']))


# Conjuntos
A = list(emisiones_dict.keys()) # conjunto de vehículos
M = list(['Camino Lo Boza, 120, Pudahuel, Chile']) # empresas
J = direcciones # conjunto de ubicaciones
L = 0 # tiempo de contrato
I = range(37) # paquetes de la empresa m

# print(A)
# print(M)
print(J)
print(D['Camino Lo Boza, 120, Pudahuel, Chile', 'Glaciar Aguila Dos 2592, MAIPÚ, Chile'])

# Parámetros
N = 100 # cantidad de paquetes de la empresa m
E = emisiones_dict # emisiones de carbono del vehículo a
C = capacidad_dict # capacidad máxima de cada vehículo
#D_e = ... # distancia de la empresa m a la ubicación j
#D = ... # distancia de la ubicación j1 a j2
t = 30 # velocidad promedio de un auto en recorrer un kilometro
T = ... # tiempo total de las entregas
p = 4500 # pago extra
#M = 10**10

# Crear un modelo vacio

model = Model()

# Creamos Variables de decision 

# Variables
X = model.addVars(A, I, J, vtype=GRB.BINARY, name="X")
W = model.addVars(A, J, J, vtype=GRB.BINARY, name="W")
Z = model.addVars(A, vtype=GRB.BINARY, name="Z")
Y = model.addVars(J, vtype=GRB.CONTINUOUS, name="Y")

# Llama al update para agregar las variables al modelo
model.update()

# Restricciones

# 1. Restricción de capacidad
#for a in A:
#    for j in J:
#        model.addConstr(quicksum(X[a,m,i,j] for m in M for i in I) <= C[a])

model.addConstrs((C[a] >= quicksum(X[a,i,j] for i in I) for a in A for j in J), name="R1")

# 2. Cada paquete es transportado por un solo vehículo
# for m in M:
#     for i in I:
#         for j in J:
#             model.addConstr(quicksum(X[a,m,i,j] for a in A) == 1)

model.addConstrs((1 == quicksum(X[a,i,j] for a in A) for i in I for j in J), name="R2")

# 3. Cada ubicación de entrega es atendida una vez
# for i in I:
#     model.addConstr(quicksum(W[a,i,j] for a in A for j in J) == 1)

model.addConstrs((1 == quicksum(X[a,i,j] for a in A for j in J) for i in I), name="R3")

# 4. Restricción de flujo
# for a in A:
#     for i in I:
#         model.addConstr(quicksum(W[a,j,i] for j in J) == 1)
#         model.addConstr(quicksum(W[a,i,j] for j in J) == 1)
model.addConstrs((1 == quicksum(W[a,j1,j2] for j1 in J) for j2 in J for a in A), name="Flujo1")
model.addConstrs((1 == quicksum(W[a,j1,j2] for j2 in J) for j1 in J for a in A), name="Flujo2")


# 5. Restricción de recorrido
# for a in A:
#     for i in range(1, len(I)):
#         for j in range(i+1, len(J)+1):
#             model.addConstr(Y[i] - Y[j] + len(J)*W[a,i,j] <= len(J) - 1)

#model.addConstrs((Y[j1] - Y[j2] + len(J)*W[a,j1,j2] <= len(J) - 1 for a in A for j1 in J for j2 in J if j1 != j2 if j1 >= 1 if j2 >= 1 if j1 <= (len(J) + 1) if j2 <= (len(J) + 1)), name="R5")

# 6. Restricción de tiempo
# for a in A:
#     model.addConstr(T - quicksum(X[a,m,i,j]*D[m,i] + W[a,i,j]*D[i,j] for m in M for i in I for j in J) + M*Z[a] >= 1)
#     model.addConstr(quicksum(X[a,m,i,j]*D[m,i] + W[a,i,j]*D[i,j] for m in M for i in I for j in J) - T + M*(1-Z[a]) >= 0)

#model.addConstrs((1 < T - quicksum(X[a,i,m,j] * )))


# Funcion objetivo

#objetivo = quicksum(X[a,m,j]*D[m,i]*E[a] + W[a,i,j]*D[i,j]*E[a] for a in A for m in M for i in I for j in J)
objetivo = quicksum(X[a,i,j] * D[m,j] * E[a] for m in M for a in A for i in I for j in J if j != m) + quicksum(W[a,j1,j2] * D[j1,j2] * E[a] for a in A for j1 in J for j2 in J)
model.setObjective(objetivo, GRB.MINIMIZE)


#Optimiza el problema

model.optimize()


# Mostrar resultados
for v in m.getVars():
    print(f'{v.varName} = {v.x}')

print(f'Objetivo: {m.objVal}')