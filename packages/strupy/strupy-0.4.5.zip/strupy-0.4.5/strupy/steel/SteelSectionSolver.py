'''
--------------------------------------------------------------------------
Copyright (C) 2015 Lukasz Laba <lukaszlab@o2.pl>

File version 0.1 date 2015-11-23

This file is part of StruPy.
StruPy is a structural engineering design Python package.
http://strupy.org/

StruPy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

StruPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import strupy.units as u

from SteelSection import SteelSection
from SteelSectionLoad import SteelSectionLoad

import math

class SteelSectionSolver():
    
    import section_resistance as __resistance
    import section_capacity_conditions as __conditions

    def __init__(self):
        print "SteelSectionSolver init"        

    def calculate_resistance (self, sect):
        sect.N_tRd = self.__resistance.N_tRd(sect.A, sect.f_y())
        sect.N_cRd = self.__resistance.N_cRd(sect.A, sect.f_y())
        #------------
        sect.M_ycRd = self.__resistance.M_cRd(sect.W_ypl, sect.W_yel, sect.f_y())
        sect.M_zcRd = self.__resistance.M_cRd(sect.W_zpl, sect.W_zel, sect.f_y())
        #------------
        sect.V_ycRd = self.__resistance.V_cRd(sect.A_yv, sect.f_y())
        sect.V_zcRd = self.__resistance.V_cRd(sect.A_zv, sect.f_y())
    
    def check_section_for_load(self, section, load):
        self.calculate_resistance(section)
        #------------
        capacity_is_true = False
        loadcase = []
        resultcomment = []
        failurecode = []
        condition_value = []
        #------------
        for i in range(len(load.Name)):
            if load.caseactiv[i]:
                condition_N_Mx_My = self.__conditions.condition_N_Mx_My(load.N_Ed[i], section.N_tRd, load.M_yEd[i], section.M_ycRd, load.M_zEd[i], section.M_zcRd)
                condition_Vz = self.__conditions.condition_V(load.V_zEd[i], section.V_zcRd)
                condition_Vy = self.__conditions.condition_V(load.V_yEd[i], section.V_ycRd)
                #------------
                loadcase.append(i)
                failurecode.append(min(condition_N_Mx_My[0], condition_Vz[0], condition_Vy[0]))
                condition_value.append(max(condition_N_Mx_My[1], condition_Vz[1], condition_Vy[1]))
                resultcomment.append(condition_N_Mx_My[2] + '\n' + 'shear in z dir. ' + condition_Vz[2] + '\n' + 'shear in y dir. ' + condition_Vy[2])
        #------------
        if not False in failurecode:
            capacity_is_true = True
        return [capacity_is_true, loadcase, failurecode, resultcomment, condition_value]
        
    def get_sigmaxx_stress (self, section, load):
        return [sigmaxx_z_p, sigmaxx_z_n, sigmaxx_y_p]
    
# Test if main
if __name__ == '__main__':
    print ('SteelSectionSolver')
    section=SteelSection()
    solver=SteelSectionSolver()
    load=SteelSectionLoad()
    load.add_loadcase({"Name": 'ULS_case1', "M_yEd": 10*u.kNm, "M_zEd": 10*u.kNm, "T_Ed": 2*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 9*u.kN, "V_zEd": 8*u.kN})
    load.add_loadcase({"Name": 'ULS_case2', "M_yEd": 20*u.kNm, "M_zEd": 20*u.kNm, "T_Ed": 2*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 9*u.kN, "V_zEd": 8*u.kN})
    load.add_loadcase({"Name": 'ULS_case3', "M_yEd": 120*u.kNm, "M_zEd": 80*u.kNm, "T_Ed": 2*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 9*u.kN, "V_zEd": 5000*u.kN})
    print '-----------------1-------------------'
    print load.get_loadcases()
    print '-----------------2-------------------'
    print section.get_sectinfo()
    print '-----------------2-------------------'
    section.set_sectionfrombase('IPE 300')
    print section.get_sectinfo()
    print '-----------------3-------------------'
    solver.calculate_resistance(section)
    print section.get_sectinfo()
    print '-----------------4-------------------'
    result = solver.check_section_for_load(section, load)
    print result
    print '-----Raprot-----'
    print result[4]
    print '>>>>>>> ' + str(result[0]) + ' <<<<<<<'
    for i in range(len(result[1])):
        print'loadcase no. ' + str(result[1][i]) + ' -> ' +  str(result[2][i]) + '\n' + str(result[3][i])

    print result[1]
