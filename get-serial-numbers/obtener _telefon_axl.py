import requests
from bs4 import BeautifulSoup


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

            <!--<devicePoolName>DP_ALCALA</devicePoolName>-->
         </searchCriteria>

         <returnedTags>

           <name></name>

             <!-- <model></model>

            <ownerUserName></ownerUserName> -->

         </returnedTags>

      </ns:listPhone>

   </soapenv:Body>

</soapenv:Envelope>"""
   r=requests.post('https://10.85.0.66/axl/',verify=False, auth=('administrator','password'),data=soaReq)
   #print(r.content)
   soup = BeautifulSoup(r.content, 'xml')
   #print (soup)
   lista_telefonos = soup.find_all ('name')
   longitud_lista=print(len(lista_telefonos))
   
   return (lista_telefonos)

def get_ip_telefonos(listdeviceName):
   requestSoap = add_item_soap(listdeviceName)
   #print (requestSoap)
   r=requests.post('https://10.85.0.66:8443/realtimeservice2/services/RISService70',verify=False, auth=('administrator','password'),data=requestSoap)
   #print(r.content)
   soup = BeautifulSoup(r.content, 'xml')
   #print (soup)
   lista_ip = soup.find_all ('ns1:IP')
   i=1
   for ip in lista_ip:
      print (i,": ", ip.text)
      i += 1
   print ("longitud lista ip es: ", len(lista_ip))



#def main():
    #get_telefonos()

    
    #modelo= soup.model   
    #print (modelo.text)       
    #serialnumber = soup.serialNumber
    #mac= soup.MACAddress

if __name__ == '__main__':
   #main()
   lista_telefonos=get_telefonos()
   get_ip_telefonos(lista_telefonos)
   print ("El numero de telefonos es: ", len(lista_telefonos))
 