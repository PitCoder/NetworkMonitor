"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.snmplabs.com:161
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,

Functionally similar to:

| $ snmpget -v1 -c public localhost SNMPv2-MIB::sysDescr.0

"""#
from pysnmp.hlapi import *

def consultaSNMP(comunidad, host, port, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad, mpModel=0),
               UdpTransportTarget((host, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    resultado = ""

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[2]
            
    return resultado

def consultaWALKSNMP(comunidad, host, port, oid):
    resultado = []
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(), 
    CommunityData(comunidad), 
    UdpTransportTarget((host, port)), 
    ContextData(), 
    ObjectType(ObjectIdentity(oid)),
    lexicographicMode=False):

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            break
        else:
            for varBind in varBinds:
                if (varBind != 'None'  or varBind != ""):           
                    varB =(' = '.join([x.prettyPrint() for x in varBind]))
                    zipvarB = varB.split()
                    resultado.append(' '.join(zipvarB[2::]))
    return resultado
