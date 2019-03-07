# http://cronklab.wikidot.com/calculation-of-vapour-pressure-deficit
# For consideration but not used for formulas
# https://physics.stackexchange.com/questions/4343/how-can-i-calculate-vapor-pressure-deficit-from-temperature-and-relative-humidit

def SaturationVaporPressure(temp):
    '''Saturation vapor pressure for a temperature'''
    return 610.7 * (10 **(7.5 * temp / (temp + 237.3)))

def ActualVaporPressure(rh, svp):
    '''Actual vapor pressure from relative humidity and saturation vapor pressure'''
    return (rh*svp)/100

def VaporPressureDeficit3(avp, svp):
    '''Vapor Pressure Deficit from actual and saturation'''
    return svp-avp

def VaporPressureDeficit2(rh, svp):
    '''Vapor pressure deficit from relative humidity and saturation'''
    return ((100.0-rh)/100.0)*svp

def VaporPressureDeficit(temp, rh):
    '''Vapor Pressure Deficit from temp and relative humidity'''
    return VaporPressureDeficit2(rh, SaturationVaporPressure(temp))

def test():
    temp=25.0
    rh=80  #relative humidity
    print("Temperature: " + str(temp))
    print("Relative Humidity: " + str(rh))
    
    svp, avp, vpd = main(temp, rh)
    print("Saturation Vapor Pressure: " + str(svp))
    print("Actual Vapor Pressure: " + str(avp))
    print("Vapor Pressure Deficit: " + str(vpd))
    print("Done")
    
def main(temp, rh):    
    svp=SaturationVaporPressure(temp)
    avp=ActualVaporPressure(rh, svp)
    vpd=VaporPressureDeficit(temp, rh)
    return svp, avp, vpd
    vpd=VaporPressureDeficit3(avp, svp)
    print("Vapor Pressure Deficit3: " + str(vpd))
    vpd=VaporPressureDeficit2(temp, svp)
    print("Vapor Pressure Deficit (temp, rh): " + str(vpd))



if __name__ == '__main__':
    test()
