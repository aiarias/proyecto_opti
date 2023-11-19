from gurobipy import GRB, Model, quicksum
from random import randint, uniform
import pandas as pd

#Procesar datos

# Escribe los datos de distnacia en D_e y D
file_path = 'distancias_santiago.xlsx'
df = pd.read_excel(file_path, engine='openpyxl', sheet_name='Sheet1')  # Asegúrate de usar el nombre correcto de la hoja

# Eliminando cualquier fila o columna que no contenga datos
# df.dropna(how="all", inplace=True)
# df.dropna(axis=1, how="all", inplace=True)

# Asumiendo que la primera columna es 'Direcciones' y contiene todas las direcciones
direcciones = df['Direcciones'].tolist()

# Distancia de la empresa m a la ubicación j
# Suponiendo que 'Camino Lo Boza, 120, Pudahuel, Chile' es la empresa m
D_e = df.set_index('Direcciones')['Camino Lo Boza, 120, Pudahuel, Chile'].to_dict()

# Distancia entre cada ubicación
D = {}
for i in direcciones:
    for j in direcciones:
        #if i != j:
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
I = direcciones # conjunto de ubicaciones
L = 0 # tiempo de contrato

# print(I)
# print(D["Camino Lo Boza, 120, Pudahuel, Chile", "policarpo toro 173, MAIPU, Chile"])

# Parámetros 
N = 37 # cantidad de paquetes de la empresa m
E = emisiones_dict # emisiones de carbono del vehículo a
C = capacidad_dict # capacidad máxima de cada vehículo
#D_e = ... # distancia de la empresa m a la ubicación j
#D = ... # distancia de la ubicación j1 a j2
t = 0.0263 # velocidad promedio de un auto en recorrer un kilometro
T = 8.3 # tiempo total de las entregas
p = 4500 # pago extra
M = 10**10

# for i in I:
#     for j in I:
#         print(D[i, j])

# Crear un modelo vacio

model = Model()

# Creamos Variables de decision 

# Variables
Y = model.addVars(A, I, vtype=GRB.BINARY, name="Y")
X = model.addVars(A, I, I, vtype=GRB.BINARY, name = "X")
Z = model.addVars(A, vtype=GRB.BINARY, name = "Z")
R = model.addVars(I, vtype=GRB.CONTINUOUS, name = "R")
U = model.addVars(A, I, vtype=GRB.INTEGER, name = "U")

# Llama al update para agregar las variables al modelo
model.update()

# Restricciones

# 1. Restricción de capacidad

# model.addConstrs((C[a] >= quicksum(X[a,i,j] for i in I) for a in A for j in J), name="R1")
model.addConstrs((C[a] >= quicksum(Y[a, i] for i in I) for a in A), name = "R1")

# 2. Cada paquete es transportado por un solo vehículo

# model.addConstrs((1 == quicksum(X[a,i,j] for a in A) for i in I for j in J), name="R2")
model.addConstrs((1 == quicksum(Y[a, i] for a in A) for i in I), name = "R2")

# 3. Cada ubicación de entrega es atendida una vez

# model.addConstrs((1 == quicksum(X[a,i,j] for a in A) for i in I for j in J), name="R3")
model.addConstrs((1 == quicksum(X[a, i, j] for a in A for j in I) for i in I), name = "R3")

# 4. Restricción de flujo

model.addConstrs((1 == quicksum(X[a, 'Camino Lo Boza, 120, Pudahuel, Chile', j] for i in I) - quicksum(X[a, j, 'Camino Lo Boza, 120, Pudahuel, Chile'] for i in I) \
    for j in I for a in A), name = "Flujo1")
model.addConstrs((0 == quicksum(X[a, i, j] for i in I if i != 'Camino Lo Boza, 120, Pudahuel, Chile') - quicksum(X[a, j, i] for i in I if i != 'Camino Lo Boza, 120, Pudahuel, Chile') \
    for j in I if j != 'Camino Lo Boza, 120, Pudahuel, Chile' for a in A), name = "Flujo2")
model.addConstrs((-1 == quicksum(X[a, 'Camino Lo Boza, 120, Pudahuel, Chile', j] for i in I) - quicksum(X[a, j, 'Camino Lo Boza, 120, Pudahuel, Chile'] for i in I) \
    for j in I for a in A), name = "Flujo3")


#5. Sub-tours

model.addConstrs((C[a] - 1 >= U[a, i] - U[a, j] + C[a]*X[a, i, j] for i in I for j in I for a in A), name = "Sub-tours1")
model.addConstrs((C[a] >= U[a, j] for j in I for a in A), name = "Sub-tours2")
model.addConstrs((1 <= U[a, j] for j in I for a in A), name = "Sub-tours3")


# 6. Restricción de tiempo

model.addConstrs((T - quicksum(X[a, i, j]*D[i, j]*t for i in I for j in I) + M*Z[a] >= 1 for a in A), name="Tiempo1")
model.addConstrs((quicksum(X[a, i, j]*D[i, j]*t for i in I for j in I) - T + M*(1 - Z[a]) >= 0 for a in A), name="Tiempo2")



# 7. Relación entre variables

#model.addConstrs((Y[i, a] == quicksum(X[a, i, j] for a in A) for i in I for j in I), name = "Relación1")
model.addConstrs((Y[a, i] == quicksum(X[a, i, j] for i in I) for j in I for a in A), name="Relacion1")

model.addConstrs((Y[a, 'Camino Lo Boza, 120, Pudahuel, Chile'] == quicksum(X[a, i, 'Camino Lo Boza, 120, Pudahuel, Chile'] for i in I) for a in A), name = "Relación2")


# model.addConstrs((Y[i, a] == quicksum(X[a, i, j] for j in I) for i in I for a in A), name="Relacion1")
# model.addConstrs((Y[a] == quicksum(X[a, i, j] for i in I) for a in A), name="Relacion2")

#model.addConstrs((Yd[a] == quicksum(X[a, i, d] for i in I) for a in A), name="Relacion2")


# Funcion objetivo

#objetivo = quicksum(X[a,m,j]*D[m,i]*E[a] + W[a,i,j]*D[i,j]*E[a] for a in A for m in M for i in I for j in J)
objetivo = quicksum(X[a, i, j]*D[i, j]*E[a] for a in A for i in I for j in I)
model.setObjective(objetivo, GRB.MINIMIZE)


#Optimiza el problema

model.optimize()


# print(f"El valor objetivo es de: {model.ObjVal}")

# print("\n"+"-"*9+" Restricciones Activas "+"-"*9)
# for constr in model.getConstrs():
#     if constr.getAttr("slack") == 0:
#         print(f"La restriccion {constr.name} está activa")

recorrido_total = []
for a in A:
    recorrido = ['Camino Lo Boza, 120, Pudahuel, Chile']
    for i in I:
        for j in I:
            print(X[a, i, j].x)
            if Y[a, i].x == 1:
                if X[a, i, j].x == 1:
                    print(f"El vehículo {a} va de {i} a {j}")
                    recorrido.append(j)
    
    # if Z[a].x == 1:
    #     print(f"El vehículo {a} sobrepasó el tiempo de contrato")
    
    recorrido_total.append(recorrido)

print(recorrido_total)