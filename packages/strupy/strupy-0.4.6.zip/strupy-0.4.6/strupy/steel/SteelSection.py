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

from MaterialSteel import MaterialSteel

from strupy.steel.SectionBase import SectionBase

class SteelSection(MaterialSteel):

    __base = SectionBase()
    #import sectionresistance as __sectionresistance

    def __init__(self):
        print "SteelSection init"
        MaterialSteel.__init__(self)
        #------------
        self.comment = 'No commenent'
        #------------
        self.sectname = 'none'
        #------------
        self.b = 0*u.cm
        self.h = 0*u.cm
        #------------
        self.A = 0*u.cm2
        self.A_yv = 0*u.cm2
        self.A_zv = 0*u.cm2
        self.W_ypl = 0*u.cm3
        self.W_zpl = 0*u.cm3
        self.W_yel = 0*u.cm3
        self.W_zel = 0*u.cm3
        #------resistance------
        self.N_tRd = 0*u.kN
        self.N_cRd = 0*u.kN
        self.M_ycRd = 0*u.kNm
        self.M_zcRd = 0*u.kNm
        self.V_zcRd = 0*u.kN
        self.V_ycRd = 0*u.kN

    def clear_soverresult(self):
        self.N_tRd = 0*u.kN
        self.N_cRd = 0*u.kN
        self.M_ycRd = 0*u.kNm
        self.M_zcRd = 0*u.kNm
        self.V_zcRd = 0*u.kN
        self.V_ycRd = 0*u.kN

    def get_sectinfo(self):
        return self.__dict__

    def set_sectionfrombase(self, sectname='IPE 270'):
        param = SteelSection.__base.get_sectionparameters(sectname)
        #------------
        self.sectname=param['sectionname']
        #self.x = param['mass']
        #self.x = param['surf']
        self.h = param['h']
        self.b = param['b']
        #self.x = param['ea']
        #self.x = param['es']
        #self.x = param['ra']
        #self.x = param['rs']
        #self.x = param['gap']
        self.A = param['Ax']
        self.A_yv = param['Ay']
        self.A_zv = param['Az']
        #self.x = param['Ix']
        #self.x = param['Iy']
        #self.x = param['Iz']
        #self.x = param['Iomega']
        #self.x = param['vy']
        #self.x = param['vpy']
        #self.x = param['vz']
        #self.x = param['vpz']
        self.W_ypl = param['Wply']
        self.W_zpl = param['Wplz']
        self.W_yel = param['Wy']
        self.W_zel = param['Wz']
        #self.x = param['Wtors']
        #self.x = param['gamma']
        self.sectioncontourpoints = SteelSection.__base.get_sectioncontourpoints(sectname)
        #------------
        self.clear_soverresult()
    
    def draw_contour(self, SomeGeometryObiect, annotation=1):
        SteelSection.__base.draw_sectiongeometry(SomeGeometryObiect, self.sectname, annotation)
        
    def draw_text_on_contour(self, SomeGeometryObiect, annotation=1):
        pass
        
    def draw_chart_on_contour(self, SomeGeometryObiect, annotation=1):
        pass
        
    def get_comment(self):
        return self.comment
        
# Test if main
if __name__ == '__main__':
    print ('test RcRecSect')
    a=SteelSection()
    print a.get_sectinfo()
    a.set_sectionfrombase('IPE 100')
    print  a.get_sectinfo()
