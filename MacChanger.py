from subprocess import Popen,PIPE
from randmac import RandMac
import os
from time import sleep
os.environ["COMSPEC"] = 'powershell'
def getNIC():
    p = Popen(['Get-NetAdapter'],shell=True, stdin=PIPE,stdout=PIPE,stderr=PIPE)
    output = p.communicate()
    return output[0].decode('utf-8').split()[12]
def getMac():
    p = Popen(['GetMac'],shell=True, stdin=PIPE,stdout=PIPE,stderr=PIPE)
    outputPs = p.communicate()
    InicialMAC=outputPs[0].decode('utf-8').split()[6]
    return InicialMAC

def GenMac():
    p = Popen(['GetMac'],shell=True, stdin=PIPE,stdout=PIPE,stderr=PIPE)
    outputPs = p.communicate()
    InicialMAC=outputPs[0].decode('utf-8').split()[6][0:8]
    macex = "00-00-00-00-00-00"
    genMac = str(RandMac(macex, True))
    exGenMac=genMac.replace("00-00-00",InicialMAC)
    LastMac=exGenMac.upper()
    return LastMac
def replaceMac(genMac,getNic):
    Popen(['Start-Process','powershell','-ArgumentList',f"\'Set-NetAdapter -Name \"{getNic}\" -MacAddress \"{genMac}\" -Confirm:$false\'",'-verb','runas'],shell=True, stdin=PIPE,stdout=PIPE,stderr=PIPE)

    #querry=f"powershell Start-Process powershell -ArgumentList 'Set-NetAdapter -Name \"{getNic}\" -MacAddress \"{genMac}\"' -verb runas"
    #os.system(querry)
     
macGen = GenMac()
print(getNIC()," - ",getMac(),"\nGenerated Mac:",macGen)

replaceMac(macGen,getNIC())
print("Waiting for Mac to Update\n")
sleep(10)
print("MAC Changed Sucefully ("+getMac()+")")
