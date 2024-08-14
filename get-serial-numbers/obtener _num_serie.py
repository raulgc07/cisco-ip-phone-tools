import requests
from bs4 import BeautifulSoup

user_info={}

def get_user_info():
   
   user_info['nombre']=input("Introduzca Usuario: ")
   user_info['pwd']=input("Introduzca contraseña: ")
   


def add_item_soap(listdeviceName):
   soapReq1 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://schemas.cisco.com/ast/soap">
   <soapenv:Header/>
   <soapenv:Body>
      <soap:selectCmDevice>
         <soap:StateInfo></soap:StateInfo>
         <soap:CmSelectionCriteria>
            <soap:MaxReturnedDevices>1000</soap:MaxReturnedDevices>
            <soap:DeviceClass>Any</soap:DeviceClass>
            <soap:Model>255</soap:Model>
            <soap:Status>Any</soap:Status>
            <soap:NodeName></soap:NodeName>
            <soap:SelectBy>Name</soap:SelectBy>
            <soap:SelectItems>"""
            
   soapReq2 = """</soap:SelectItems>
            <soap:Protocol>Any</soap:Protocol>
            <soap:DownloadStatus>Any</soap:DownloadStatus>
         </soap:CmSelectionCriteria>
      </soap:selectCmDevice>
   </soapenv:Body>
</soapenv:Envelope>"""
   
   cadena =""
   for devicename in listdeviceName:
      cadena = cadena +"""<soap:item>
                  <soap:Item>""" + devicename.text + """</soap:Item>
               </soap:item>"""
   return (soapReq1 + cadena + soapReq2)




def get_telefonos():
   soaReq = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/11.5">

   <soapenv:Header/>

   <soapenv:Body>

      <ns:listPhone>

         <searchCriteria>

            <!--Optional:-->

            <name>SEP%</name>

            <devicePoolName>DP_LAS_PALMAS%</devicePoolName>
         </searchCriteria>

         <returnedTags>

           <name></name>

             <!-- <model></model>

            <ownerUserName></ownerUserName> -->

         </returnedTags>

      </ns:listPhone>

   </soapenv:Body>

</soapenv:Envelope>"""
   r=requests.post('https://10.85.0.66/axl/',verify=False, auth=(user_info['nombre'],user_info['pwd']),data=soaReq)
   #print(r.content)
   soup = BeautifulSoup(r.content, 'xml')
   #print (soup)
   lista_telefonos = soup.find_all ('name')
   longitud_lista=print(len(lista_telefonos))
   
   return (lista_telefonos)

def get_ip_telefonos(listdeviceName):
   requestSoap = add_item_soap(listdeviceName)
   #print (requestSoap)
   r=requests.post('https://10.85.0.66:8443/realtimeservice2/services/RISService70',verify=False, auth=(user_info['nombre'],user_info['pwd']),data=requestSoap)
   #print(r.content)
   soup = BeautifulSoup(r.content, 'xml')
   #print (soup)
   lista_device_ip= soup.find_all ('ns1:CmDevices')  #Obtenemos una lista con todos los devices en cada serviro, yaque si buscabamos por ns1:IP tambíen nos salian los servidores
   lista_device = []  #Se inicializa lista en la que obtendremos todos los device name
   lista_ip2 = []  # Se inicializa lista en la que obtendremnos todas las ip de los teléfonos
   for contador in range(3) :
      lista_device += lista_device_ip[contador].findChildren('ns1:Name')
      lista_ip2 += lista_device_ip[contador].findChildren('ns1:IP')
      print ("longitud lista_device_ip es: ", len(lista_device))
      print ("longitud lista ip2: ", len(lista_ip2))
   contador=0
   lista_ip={}  # Inicializamos el diccionario donde van a estar como campo clave la ip y valor el device name
   for device in lista_device:    
      #print (device.text, lista_ip2[contador].text)
      lista_ip[lista_ip2[contador]] = device   #Vamos añadiendo los datos al diccionario desde las listas lista device y lista_ip2
      contador += 1

   return (lista_ip)
   

def GetSerialNumber (lista_ip):
   payload={}
   headers = {}
   string_info_telefono=""
   
   fichero = open ('numeros_de_serie.csv','w')
   fichero.write ("ip,Modelo,MAC,Serial Number\n")
   for ip in lista_ip:
      try:
         
         url="http://"+ ip.text +"/DeviceInformationX"
         response = requests.request("GET", url, headers=headers, data=payload, timeout=1)
         string_xml=response.content
         soup = BeautifulSoup(string_xml, 'xml')
         modelo= soup.modelNumber         
         serialnumber = soup.serialNumber
       
         mac= soup.MACAddress
         print (ip.text, modelo.text, mac.text, serialnumber.text)
         string_info_telefono = (ip.text+","+modelo.text+","+ mac.text+","+serialnumber.text+"\n")
         fichero.write(string_info_telefono)

      except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) :
         print (ip.text,",",lista_ip[ip].text ," No se ha podido conectar al teléfono")
         string_info_telefono=(ip.text+",no,"+lista_ip[ip].text+",no se ha podido conectar\n")
         fichero.write(string_info_telefono)
         
      except AttributeError:
         modelo= soup.ModelNumber         
         serialnumber = soup.SerialNumber
         mac= soup.MACAddress
         print (ip.text, modelo.text, mac.text, serialnumber.text)
         string_info_telefono = (ip.text+","+modelo.text+","+ mac.text+","+serialnumber.text+"\n")
         fichero.write(string_info_telefono)

   fichero.close  
  
   

if __name__ == '__main__':
   #main()
   get_user_info()
   lista_telefonos=get_telefonos()
   lista_ip = get_ip_telefonos(lista_telefonos)
   print ("El numero de telefonos es: ", len(lista_telefonos))
   GetSerialNumber (lista_ip)
 