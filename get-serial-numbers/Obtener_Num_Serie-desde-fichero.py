import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup

"""
Script para obtener número de serie de los teléfonos dados de alta en el callmanager. Para ellos hay que generar un fichero con las ip's de los teléfonos
y las ip's tienen que ser alcanzables Una ip por cada linea. El fichero se llama ip.txt

"""

def GetSerialNumber (url,ip):
    payload={}
    headers = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload, timeout=1)
        string_xml=response.content
        soup = BeautifulSoup(string_xml, 'xml')
        modelo= soup.modelNumber         
        serialnumber = soup.serialNumber
       
        mac= soup.MACAddress
        print (ip, modelo.text, mac.text, serialnumber.text)

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) :
        print (ip, " No se ha podido conectar al teléfono")
    except AttributeError:
        modelo= soup.ModelNumber         
        serialnumber = soup.SerialNumber
        mac= soup.MACAddress
        print (ip, modelo.text, mac.text, serialnumber.text)
        
      
       

def main():
    try:
        with open('ip.txt', 'r') as file:    
            linea = file.readline().rstrip('\n')
            while linea != '':
                url="http://"+linea+"/DeviceInformationX"
                GetSerialNumber (url, linea)
                linea = file.readline().rstrip('\n')
    except FileNotFoundError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == '__main__':
    main()



