from gurobipy import GRB, Model, quicksum
from random import randint, uniform
import pandas as pd

# Procesar datos


# Crear un modelo vacio

model = Model()

# Creamos Variables de decision 



# Llama al update para agregar las variables al modelo
model.update()

#Restricciones


# # 8. Relacion entre variables



# Funcion objetivo

objetivo = "completar"
model.setObjective(objetivo, GRB.MINIMIZE)


#Optimiza el problema

model.optimize()


model.computeIIS()
archivo = "encontrar_infactiblidad"
model.write(f"{archivo}.ilp")

# Mostrar valores de las soluciones

print(f"El valor objetivo es de: {model.ObjVal}")


# for constr in model.getConstrs():
#     print(constr, constr.getAttr("slack"))