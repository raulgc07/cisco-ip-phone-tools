#lista de tuplas
tupla1 = (1,'Madrid')
tupla2 = (2,'Barcelon')

tupla3 = tupla1 + tupla2
tupla3 += (5,'Sevilla')
print ('tupla3: ',tupla3)
print (tupla1[1])

lista_tuplas = [tupla1, tupla2]
#print (lista_tuplas)
#print (len(lista_tuplas))

print (lista_tuplas[0][1])

dic = {}
dic = {1:'madrid'}
print (type(dic))
dic[2] = 'Barcelona'
print (dic[2])

lista1= ['Madrid', 'Barcelona', 'Servilla']
lista2= ['Munich', 'Lisboa']
lista3= lista1 + lista2
lista3 += ['Cadiz', 'Jerez']
lista3+= 'Raul'
print (lista3)

def suma (a:int , b: int) -> dict:
    print (a+b)

suma (3, 5)
print (suma.__annotations__ )