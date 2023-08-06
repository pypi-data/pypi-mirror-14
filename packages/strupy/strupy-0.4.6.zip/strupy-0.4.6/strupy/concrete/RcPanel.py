'''
--------------------------------------------------------------------------
Copyright (C) 2016 Lukasz Laba <lukaszlab@o2.pl>

File version 0.3 date 2016-03-20

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
File version 0.2 changes:
- RcPanel class upgraded
File version 0.3 changes:
- RcPanel class upgraded
'''
import copy

import numpy as np

import strupy.units as u

from MaterialConcrete import MaterialConcrete
from MaterialRcsteel import MaterialRcsteel

class RcPanel(MaterialConcrete, MaterialRcsteel):

    def __init__(self):
        print "RcPanel init"
        self.PanelName = "Noname panel"
        #----
        MaterialConcrete.__init__(self)
        MaterialRcsteel.__init__(self)
        #----
        self.surfaceID = np.array([])
        #----
        self.h = np.array([])
        self.h_unit = u.cm
        #----
        self.coord_Xp = np.array([])
        self.coord_Yp = np.array([])
        self.coord_Zp = np.array([])
        self.coord_flatten_x = np.array([])
        self.coord_flatten_y = np.array([])
        self.coord_unit = u.m
        self.transf_matrix = np.matrix([    [1,0,0], 
                                            [0,1,0],
                                            [0,0,1]     ])
        #----
        self.ap=5.0*u.cm
        self.an=5.0*u.cm
        self.fip=20.0*u.mm
        self.fin=20.0*u.mm
        self.rysAp=1.0
        self.rysAn=1.0
        self.wlimp=0.3*u.mm
        self.wlimn=0.3*u.mm
        #----
        self.Apx= np.array([])
        self.Anx= np.array([])
        self.Apy= np.array([])
        self.Any= np.array([])
        self.Apscale = np.array([1, 3, 4, 5, 6, 7, 8, 9, float('inf')]) 
        self.Anscale = np.array([2, 6, 7, 10, 16, 17, 18, 30, float('inf')])
        self.A_unit = u.cm2
        #----
        self.rysx= np.array([])
        self.rysy= np.array([])  
        self.mimosx= np.array([])
        self.mimosy= np.array([]) 
        self.ksieffx= np.array([])
        self.ksieffy= np.array([])
        
    def clear_arrays_data(self):
        self.surfaceID = np.array([])
        #----
        self.h = np.array([])
        #----
        self.coord_Xp = np.array([])
        self.coord_Yp = np.array([])
        self.coord_Zp = np.array([])
        self.coord_flatten_x = np.array([])
        self.coord_flatten_y = np.array([])
        #----
        self.Apx= np.array([])
        self.Anx= np.array([])
        self.Apy= np.array([])
        self.Any= np.array([])
        #----
        self.rysx= np.array([])
        self.rysy= np.array([])  
        self.mimosx= np.array([])
        self.mimosy= np.array([]) 
        self.ksieffx= np.array([])
        self.ksieffy= np.array([])

    def clear_result(self):
        self.Apx= np.array([])
        self.Anx= np.array([])
        self.Apy= np.array([])
        self.Any= np.array([])
        #----
        self.rysx= np.array([])
        self.rysy= np.array([])  
        self.mimosx= np.array([])
        self.mimosy= np.array([]) 
        self.ksieffx= np.array([])
        self.ksieffy= np.array([])
        
    def named_views(self):
        view_dict = {   'Top':[     [1, 0, 0], 
                                    [0, 1, 0], 
                                    [0, 0, 1]  ],
                        'Bottom':[  [-1, 0, 0], 
                                    [0, 1, 0], 
                                    [0, 0, -1]  ],
                        'Right':[   [0, 1, 0], 
                                    [0, 0, 1], 
                                    [1, 0, 0]  ],
                        'Left':[    [0, -1, 0], 
                                    [0, 0, 1], 
                                    [-1, 0, 0]  ],
                        'Front':[   [1, 0, 0], 
                                    [0, 0, 1], 
                                    [0, -1, 0]  ],
                        'Back':[    [-1, 0, 0], 
                                    [0, 0, 1], 
                                    [0, 1, 0]  ]   }     
        return view_dict
        
    def set_transf_matrix_for_view(self, vievPoint='Top'):
        view_dict = self.named_views()
        if vievPoint in view_dict.keys():
            self.transf_matrix = np.matrix(view_dict[vievPoint])
            self.calculate_flatten_coordinates()
            
    def preset_Ascale_value(self):
        Ascale_dict = {}
        #----                            
        Ascale_dict['Wall'] = { 'Ap' :  np.array([3.14, 3.93, 5.65, 7.54, 11.31, 13.4, 20.11, 31.41, float('inf')]),
                                'An' :  np.array([3.14, 3.93, 5.65, 7.54, 11.31, 13.4, 20.11, 31.41, float('inf')])   }
        #----                    
        Ascale_dict['Slab'] = { 'Ap' :  np.array([3.14, 7.54, 11.31, 13.4, 20, 29, 88, 90, float('inf')]),
                                'An' :  np.array([3.14, 3.93, 5.65, 7.54, 11.31, 13.4, 20.11, float('inf'), float('inf')])   }
        #----                        
        Ascale_dict['FundSlab'] = { 'Ap' :  np.array([1, 3, 4, 5, 6, 7, 8, 9, float('inf')]),
                                    'An' :  np.array([1, 4, 8, 15, 10, 29, 88, 90, float('inf')])   } 
        #----
        return Ascale_dict

    def set_preset_Ascale_value(self, scaleName='Wall'):
        Ascale_dict = self.preset_Ascale_value()
        if scaleName in Ascale_dict.keys():
            self.Apscale[:] = Ascale_dict[scaleName]['Ap'][:]
            self.Anscale[:] = Ascale_dict[scaleName]['An'][:]
        
    def calculate_flatten_coordinates(self):
        def transformate(x,y,z):
            p = np.matrix([[x], [y], [z]])
            p_trans = self.transf_matrix * p
            return p_trans.item(0), p_trans.item(1)
        if len(self.coord_Xp) > 1:
            self.coord_flatten_x = np.array([])
            self.coord_flatten_x = np.array([])
            #----
            self.coord_flatten_x, self.coord_flatten_y = np.vectorize(transformate)(self.coord_Xp, self.coord_Yp, self.coord_Zp) 
        
    def Ascale_sort(self):
        self.Apscale.sort()
        self.Anscale.sort()
        
# Test if main
if __name__ == '__main__':
    print ('test RcPanel')
    panel=RcPanel()
    xi = []
    yi = []
    zi = []
    for x in range(34):
        for y in range (23):
            xi.append(float(x))
            yi.append(float(y))
            zi.append(float(1))
    panel.coord_Xp = np.array(xi)
    print panel.coord_Xp
    panel.coord_Yp = np.array(yi)
    print panel.coord_Yp
    panel.coord_Zp = np.array(zi)
    print panel.coord_Zp
    panel.h = np.array([100, 100, 100, 100, 100, 100, 100, 100])
    print panel.h