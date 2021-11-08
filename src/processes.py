from math import exp
##################################################################################################################

#computing leaf area index

def leaf_area_index(Lai,leaLaD,temperature):
    # With Matlab we found the polynomial extrapolation of specific leaf area
    sla=(0.0133333*(temperature**3))-(temperature**2)+(30.6666667*(temperature))-(80)
    #print(sla)
    if Lai<8:
        sla=sla+10
    lai=leaLaD*sla/10000
    return lai


######################################################################################################################

# Soil water balance

def soil_water_balance(lai,epan,pawp):
    k=0.8
    
    # ground cover portion
    scov= 1-(exp(-k*lai))

    #we stil need to investigate about the actual soil evaporation amount
    #according the procedure of Ritchie (1972)

    #potential vaporation
    pe=epan*(1-scov)
    
    #potential transpiration
    pt=epan*scov
    #or  for dryer soil
    cf=1
    gcov = 1 - exp(-cf*lai)
    pt1= epan*gcov

    # Now we calculate the uptake for each layer
    alpha1=3.2
    beta=1.67
    alpha2=5.6
    alpha3=6.7

     #For pawp see the studies of  "hommer goyne 1982" and "Johns smith (1975)"

    uptake1=alpha1*(pawp)**(beta)
    uptake2 = alpha2 * (pawp) ** (beta)
    uptake3 = alpha3 * (pawp) ** (beta)

    # to calculate the water stress index we need the potential extraction which is sum of uptakes

    PotEx=uptake1+uptake2+uptake3
    #we need to find a way to calculae this one daily since previous rainfall
    SI=(pt-PotEx)/pt #stress index
    if SI <0:
        SI=0
    return SI

########################################################################################################


#crop growth rate
def cgr(temperature,sr,lai,SI):


    #potential CGR
    a=21.7
    b=20.5
    c=0.27
    PCGR=a-(b*exp(-c*lai))

    #we initialise the multiplier
    #With Matlab we found the polynomial extrapolation of the multiplier

    tm=(0.0004666666666667*(temperature**3))-(0.04*(temperature**2))+(1.09833333333333*(temperature))-(8.75)
    #if temperature inferior to 15 or superior to 35 degree there is no growth
    if temperature<15 or temperature >= 35:
        tm=0
    rm=(1.063243345*(10**(-19))*(sr**4))-(6.844299531*(10**(-18))*(sr**3))+(-0.002*(sr**2))+(0.1*(sr))-(0.25)
    if sr <5:
        rm=0
    wsm=(1.041666667*(SI**3))-(2.5*(SI**2))-(0.04166666667*(SI))+(1)
    if SI >= 0.8:
        wsm=0

    CRG=PCGR*tm*rm*wsm
    return PCGR,CRG



#######################################################################################################

#assimilate distribution

def assimilate(temperature,lai,week,D,SI):
    if week <13:
        D=15

    DRS1=(0.011*temperature) + (0.0316*lai) + (0.0637*(D-10))

    #With Matlab we found the polynomial extrapolation of the multiplier

    sm=(-13.0208*(SI**5))+(28.6458*(SI**4))+(-19.2708*(SI**3))+(2.6042*(SI**2))+(0.0417*(SI))+1

    DRS=DRS1*sm

    #Then we can calculate shoot dry matter (sdm) based on a matlab polynomial extrapolation

    sdm=((DRS**2)-(0.9*DRS)+(0.14)*(10**4))

    return DRS,sdm

########################################################################################################
