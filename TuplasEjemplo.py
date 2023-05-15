
filtrado =[] 
autos = [("fiat", 10000, 5, "uno"), ("ford", 12000, 3, "fiesta"), ("fiat", 9000, 4, "siena")]

precioMaximo = 9500
marca = "fiat"

for i in autos:
    if (i[0] == marca and i[1] <= precioMaximo):
        filtrado.append(i)

print(filtrado)





