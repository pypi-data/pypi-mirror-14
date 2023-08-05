'''
--------------------------------------------------------------------------
Copyright (C) 2016 Lukasz Laba <lukaszlab@o2.pl>

File version 0.5 date 2016-03-21

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
- RFEMxlsloader() upgraded
File version 0.3 changes:
- RFEMxlsloader() upgraded for RFEM 5 output file
File version 0.4 changes:
- ROBOTcsvloader() added
File version 0.5 changes:
- multi loadcase import implemented
'''
import os

import numpy as np
import xlrd
import csv

import strupy.units as u

class RcPanelDataLoader():

    def __init__(self):
        print "RcPanelDataLoader init"
        self.initialdir=os.path.dirname(__file__)
        
    def RFEMxlsloader(self, rcpanel, rcpanelload, progress=None):
        #--deleting object data 
        rcpanel.clear_arrays_data()
        rcpanelload.clear_arrays_data()
        #--loading xls files and recognizing surface/result sheets
        from Tkinter import Tk
        from tkFileDialog import askopenfilenames
        surface_sheet = None
        result_sheet = None
        tryNumber = 1
        while not (surface_sheet and result_sheet):
            root = Tk()
            root.withdraw()
            #----
            ask_text = 'Choose'
            if not surface_sheet:
                ask_text += ' [surface]'
            if not result_sheet:
                ask_text += ' [result]' 
            ask_text += ' xls Rfem output file(s)'
            #----
            filename_list = askopenfilenames(parent=root,title=ask_text, filetypes=[('xls file', '*.xls')], initialdir=self.initialdir)
            for filename in filename_list:
                if not filename == '':
                    self.initialdir = os.path.dirname(filename)
                book = xlrd.open_workbook(filename)
                result_sheet_list = []
                case_list = []
                for i in book.sheet_names():
                    if '1.4' in i:
                        surface_sheet = book.sheet_by_name(i) #<<<<<<<< surface_sheet
                    if ('Surfaces - Base' in i) or ('Surfaces - Basic' in i) or ('Powierzchnie - Podst' in i)  :
                        result_sheet = book.sheet_by_name(i) #<<<<<<<< result_sheet
                        result_sheet_list.append(result_sheet)
                        case_list.append(i)
            if tryNumber == 4:
                return 0
            tryNumber +=1
        root.destroy()
        #----function for finding column number with some text
        def find_column(headerTextlist, sheet, row):
            find_result = None
            for i in range(40):
                for text in headerTextlist:
                    try:
                        if text == str(sheet.col_values(i)[row].encode('cp1250')):
                            find_result = [i, str(sheet.col_values(i)[row].encode('cp1250'))]
                            return find_result
                    except IndexError:
                        pass
            if not find_result:
                find_result = ['Not found', None]
            return find_result
        #----
        if progress:
            progress.setValue(20)
        #--finding solver data units
        #----thickness unit
        header = find_column(['d [mm]', 'd [cm]', 'd [m]'], surface_sheet, 1)[1]
        if '[mm]' in header:
            solverunit_thickness = u.mm
        elif '[cm]' in header:
            solverunit_thickness = u.cm
        elif '[m]' in header:
            solverunit_thickness = u.m
        else :
            solverunit_thickness = None
        #----coordinate unit   
        header = find_column([  'Grid Point Coordinates [m]',
                                'Grid Point Coordinates [cm]', 
                                'Grid Point Coordinates [mm]',
                                'Wsp\xf3\xb3rz\xeadne punkt\xf3w rastru [m]',
                                'Wsp\xf3\xb3rz\xeadne punkt\xf3w rastru [cm]',
                                'Wsp\xf3\xb3rz\xeadne punkt\xf3w rastru [mm]'], result_sheet, 0)[1]
        if 'mm' in header:
            solverunit_coord = u.m
        elif 'cm' in header:
            solverunit_coord = u.cm
        elif 'm' in header:
            solverunit_coord = u.m
        else :
            solverunit_coord = None      
        #----internale forces moment unit
        header = find_column([  'Moments [Nm/m]',
                                'Moments [kNm/m]',
                                'Momenty [Nm/m]',
                                'Momenty [kNm/m]'], result_sheet, 0)[1]
        if '[Nm/m]' in header:
            solverunit_moment = u.Nm
        elif '[kNm/m]' in header:
            solverunit_moment = u.kNm
        else :
            solverunit_moment = None      
        #----internale forces force unit
        #print result_sheet.col_values(10)[0].encode('cp1250')
        header = find_column([  'Axial Forces [N/m]',
                                'Axial Forces [kN/m]',
                                'Si\xb3y osiowe [N/m]',
                                'Si\xb3y osiowe [kN/m]'], result_sheet, 0)[1]
        if '[N/m]' in header:
            solverunit_force = u.N
        elif '[kN/m]' in header:
            solverunit_force = u.kN
        else :
            solverunit_force = None      
        #--preparing dictionary with surface number as keys
        col_surface_number = find_column(['Surface', 'Pow.'], surface_sheet, 0)[0]
        surface_number = np.array(surface_sheet.col_values(col_surface_number)[2:])
        surface_number  = np.vectorize(int)(surface_number)
        col_surface_thickness = find_column(['d [mm]', 'd [cm]', 'd [m]'], surface_sheet, 1)[0]
        surface_thickness = np.array(surface_sheet.col_values(col_surface_thickness)[2:])
        thicknessdict = dict(zip(surface_number, surface_thickness))
        emptyrecord = []
        for key in thicknessdict:
            if thicknessdict[key] == '':
                emptyrecord.append(key)
        for i in emptyrecord:
            thicknessdict.pop(i)
        for key in thicknessdict:
            thicknessdict[key] = float(thicknessdict[key])
        #----
        if progress:
            progress.setValue(40)
        #--panel properties in rcpanel
        col_surfaceID = find_column(['No.', 'nr'], result_sheet, 1)[0]
        rcpanel.surfaceID = result_sheet.col_values(col_surfaceID)[2:]
        for i in range(len(rcpanel.surfaceID)):
            if rcpanel.surfaceID[i] == '':
                rcpanel.surfaceID[i] = rcpanel.surfaceID[i-1]
        rcpanel.surfaceID = np.array(rcpanel.surfaceID)
        rcpanel.surfaceID  = np.vectorize(int)(rcpanel.surfaceID)
        col_coord_Xp = find_column(['X'], result_sheet, 1)[0]
        rcpanel.coord_Xp = np.array(result_sheet.col_values(col_coord_Xp)[2:]) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        col_coord_Yp = find_column(['Y'], result_sheet, 1)[0]
        rcpanel.coord_Yp  = np.array(result_sheet.col_values(col_coord_Yp)[2:]) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        col_coord_Zp = find_column(['Z'], result_sheet, 1)[0]
        rcpanel.coord_Zp = np.array(result_sheet.col_values(col_coord_Zp)[2:]) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.h = np.vectorize(lambda x: thicknessdict[x])(rcpanel.surfaceID) * (solverunit_thickness / rcpanel.h_unit).asNumber()
        #--unexpected value detect and replace in result data from RFEM
        def unexpected_replace(value):
            if value == '-':
                value = 0.0
            return float(value)
        #--panel internal forces in rcpanelload
        for case_number in range(len(result_sheet_list)):
            case_name = case_list[case_number][:4]
            result_sheet = result_sheet_list[case_number]
            #----
            col_moment_mx = find_column(['mx'], result_sheet, 1)[0]
            moment_mx = result_sheet.col_values(col_moment_mx)[2:]
            moment_mx = np.vectorize(unexpected_replace)(moment_mx)
            rcpanelload.moment_mx= np.array(moment_mx) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mx = []
            #----
            col_moment_my = find_column(['my'], result_sheet, 1)[0]
            moment_my = result_sheet.col_values(col_moment_my)[2:]
            moment_my = np.vectorize(unexpected_replace)(moment_my)      
            rcpanelload.moment_my= np.array(moment_my) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_my = []
            #----
            col_moment_mxy = find_column(['mxy'], result_sheet, 1)[0]
            moment_mxy = result_sheet.col_values(col_moment_mxy)[2:]
            moment_mxy = np.vectorize(unexpected_replace)(moment_mxy)
            rcpanelload.moment_mxy= np.array(moment_mxy) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mxy = []
            #----
            col_force_vx = find_column(['vx'], result_sheet, 1)[0]
            force_vx = result_sheet.col_values(col_force_vx)[2:]
            force_vx = np.vectorize(unexpected_replace)(force_vx)
            rcpanelload.force_vx= np.array(force_vx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vx = []
            #----
            col_force_vy = find_column(['vy'], result_sheet, 1)[0]
            force_vy = result_sheet.col_values(col_force_vy)[2:]
            force_vy = np.vectorize(unexpected_replace)(force_vy)
            rcpanelload.force_vy= np.array(force_vy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vy = []
            #----
            col_force_nx = find_column(['nx'], result_sheet, 1)[0]
            force_nx = result_sheet.col_values(col_force_nx)[2:]
            force_nx = np.vectorize(unexpected_replace)(force_nx)
            rcpanelload.force_nx= np.array(force_nx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nx = []
            #----
            col_force_ny = find_column(['ny'], result_sheet, 1)[0]
            force_ny = result_sheet.col_values(col_force_ny)[2:]
            force_ny = np.vectorize(unexpected_replace)(force_ny)
            rcpanelload.force_ny= np.array(force_ny) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_ny = []
            #----
            col_force_nxy = find_column(['nxy'], result_sheet, 1)[0]
            force_nxy = result_sheet.col_values(col_force_nxy)[2:]
            force_nxy = np.vectorize(unexpected_replace)(force_nxy)
            rcpanelload.force_nxy= np.array(force_nxy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nxy = []
            #---adding new case in load object
            rcpanelload.casename = case_name
            rcpanelload.add_loadcase()
            rcpanelload.set_activeloadcase(case_name)
        #----
        if progress:
            progress.setValue(80)
            progress.setValue(0)

    def ROBOTcsvloader(self, rcpanel, rcpanelload, progress=None):
        #--deleting object data 
        rcpanel.clear_arrays_data()
        rcpanelload.clear_arrays_data()
        #--loading csv files and recognizing surface, result and node sheets
        from Tkinter import Tk
        from tkFileDialog import askopenfilenames
        surface_sheet = None
        result_sheet = None
        node_sheet = None
        tryNumber = 1
        while not (surface_sheet and result_sheet and node_sheet):
            root = Tk()
            root.withdraw()
            #----
            ask_text = 'Choose'
            if not surface_sheet:
                ask_text += ' [surface]'
            if not result_sheet:
                ask_text += ' [result]' 
            if not node_sheet:
                ask_text += ' [node]' 
            ask_text += ' csv Robot output file(s)'
            #----
            filename_list = askopenfilenames(parent=root,title=ask_text, filetypes=[('csv file', '*.csv')], initialdir=self.initialdir)
            for filename in filename_list:
                if not filename == '':
                    self.initialdir = os.path.dirname(filename)
                csvfile = open(filename, 'rb')
                reader = csv.reader(csvfile, delimiter=';')
                #----extrating rows to temporary list
                sheet = []
                for row in reader:    
                    sheet.append(row)
                #----
                def IsInHeader(sheet, textlist):
                    answer = True
                    for text in textlist:
                        if not text in sheet[0]:
                            answer = False
                    return answer
                #----recognizing
                if IsInHeader(sheet, ['Panel', 'Grubo\x9c\xe6']):
                    surface_sheet = sheet #<<<<<<<< surface_sheet
                if IsInHeader(sheet, ['Panel', 'W\xeaze\xb3', 'Przypadek', 'MXX (kNm/m)', 'MYY (kNm/m)', 'MXY (kNm/m)', 'NXX (kN/m)', 'NYY (kN/m)', 'NXY (kN/m)', 'QXX (kN/m)', 'QYY (kN/m)']):
                    result_sheet = sheet #<<<<<<<< result_sheet
                if IsInHeader(sheet, ['W\xeaze\xb3', 'X (m)', 'Y (m)', 'Z (m)', 'Podpora']):
                    node_sheet = sheet #<<<<<<<< node_sheet
            #----
            if tryNumber == 6:
                return 0
            tryNumber +=1
        root.destroy()
        #----function for finding column number with some text
        def find_column(headerTextlist, sheet):
            find_result = None
            for i in range(len(sheet[0])):
                for text in headerTextlist:
                    if text in str(sheet[0][i]):
                        find_result = [i, str(sheet[0][i])]
            if not find_result:
                find_result = ['Not found', None]
            return find_result
        #--recognizing solver data units
        #----thickness unit(there is no thickness unit to recognize in surface_sheet from ROBOT)!!!!!????
        solverunit_thickness = u.cm
        #----point coordinate unit   
        header = find_column([  'X (m)',
                                'X (cm)', 
                                'X (mm)'], node_sheet)[1]
        if 'mm' in header:
            solverunit_coord = u.mm
        elif 'cm' in header:
            solverunit_coord = u.cm
        elif 'm' in header:
            solverunit_coord = u.m
        else :
            solverunit_coord = None
        #----internale forces - moment unit
        header = find_column([  'MXX (Nm/m)',
                                'MXX (kNm/m)'], result_sheet)[1]
        if '(Nm/m)' in header:
            solverunit_moment = u.Nm
        elif '(kNm/m)' in header:
            solverunit_moment = u.kNm
        else :
            solverunit_moment = None
        #----internale forces - force unit
        header = find_column([  'NXX (N/m)',
                                'NXX (kN/m)'], result_sheet)[1]
        if '(N/m)' in header:
            solverunit_force = u.N
        elif '(kN/m)' in header:
            solverunit_force = u.kN
        else :
            solverunit_force = None
        #--extracting loadcases to result_sheet_list
        col_case_name = find_column(['Przypadek'], result_sheet)[0]
        case_name_list = [row[col_case_name] for row in result_sheet][1:]
        case_name_list = list(set(case_name_list))#delete duplicates
        result_sheet_list = []
        for casename in case_name_list:
            tmp = []
            tmp.append(result_sheet[0])
            for row in result_sheet:
                if row[col_case_name] == casename:
                    tmp.append(row)
            result_sheet_list.append(tmp)
        del result_sheet # finaly deleting no more needed result_sheet 
        #--preparing thickness dictionary with surface number as keys
        col_surface_number = find_column(['Panel'], surface_sheet)[0]
        surface_number = [row[col_surface_number] for row in surface_sheet][1:]
        surface_number  = np.vectorize(int)(surface_number)
        col_surface_thickness = find_column(['Grubo\x9c\xe6'], surface_sheet)[0]
        surface_thickness = [row[col_surface_thickness] for row in surface_sheet][1:]
        def get_num(x):
            return int(''.join(ele for ele in x if ele.isdigit()))
        surface_thickness = np.vectorize(lambda x: get_num(x))(surface_thickness)
        surface_thickness  = np.vectorize(float)(surface_thickness)
        thicknessdict = dict(zip(surface_number, surface_thickness))
        #----
        if progress:
            progress.setValue(40)
        #--preparing coordinate dictionary with node number as keys
        col_node_number = find_column(['W\xeaze\xb3'], node_sheet)[0]
        node_number = [row[col_node_number] for row in node_sheet][1:]
        node_number.pop()#there is '*' on end in node sheet from ROBOT
        node_number  = np.vectorize(int)(node_number)
        #----
        col_coord_x = find_column(['X'], node_sheet)[0]
        coord_x = [row[col_coord_x] for row in node_sheet][1:]
        coord_x.pop()#there is '*' on end in node sheet from ROBOT
        coord_x = np.vectorize(lambda x: x.replace(',', '.'))(coord_x)
        coord_x = np.vectorize(float)(coord_x)
        #----
        col_coord_y = find_column(['Y'], node_sheet)[0]
        coord_y = [row[col_coord_y] for row in node_sheet][1:]
        coord_y.pop()#there is '*' on end in node sheet from ROBOT
        coord_y = np.vectorize(lambda x: x.replace(',', '.'))(coord_y)
        coord_y = np.vectorize(float)(coord_y)        
        #----
        col_coord_z = find_column(['Z'], node_sheet)[0]
        coord_z = [row[col_coord_z] for row in node_sheet][1:]
        coord_z.pop()#there is '*' on end in node sheet from ROBOT
        coord_z = np.vectorize(lambda x: x.replace(',', '.'))(coord_z)
        coord_z = np.vectorize(float)(coord_z)
        #----         
        coord_x_dict = dict(zip(node_number, coord_x))
        coord_y_dict = dict(zip(node_number, coord_y))
        coord_z_dict = dict(zip(node_number, coord_z))
        #--writing panel properties in rcpanel obiect
        col_surfaceID = find_column(['Panel'], result_sheet_list[0])[0]
        rcpanel.surfaceID = [row[col_surfaceID] for row in result_sheet_list[0]][1:]
        rcpanel.surfaceID = np.array(rcpanel.surfaceID)
        rcpanel.surfaceID  = np.vectorize(int)(rcpanel.surfaceID)
        #----
        col_nodeNum = find_column(['W\xeaze\xb3'], result_sheet_list[0])[0]
        nodeNum = [row[col_nodeNum] for row in result_sheet_list[0]][1:]
        nodeNum = np.array(nodeNum)
        nodeNum  = np.vectorize(int)(nodeNum)
        rcpanel.coord_Xp = np.vectorize(lambda x: coord_x_dict[x])(nodeNum) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.coord_Yp  = np.vectorize(lambda x: coord_y_dict[x])(nodeNum) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.coord_Zp = np.vectorize(lambda x: coord_z_dict[x])(nodeNum) * (solverunit_coord / rcpanel.coord_unit).asNumber()
        rcpanel.h = np.vectorize(lambda x: thicknessdict[x])(rcpanel.surfaceID) * (solverunit_thickness / rcpanel.h_unit).asNumber()
        #--writing internal forces in rcpanelload obiect
        rcpanelload.clear_arrays_data() # clear data in load obiect
        for case_number in range(len(result_sheet_list)):
            #----
            caseload_sheet = result_sheet_list[case_number]
            case_name = case_name_list[case_number]
            #----
            col_moment_mx = find_column(['MXX'], caseload_sheet)[0]
            moment_mx = [row[col_moment_mx] for row in caseload_sheet][1:]
            moment_mx = np.vectorize(lambda x: x.replace(',', '.'))(moment_mx)
            moment_mx = - np.vectorize(float)(moment_mx)
            rcpanelload.moment_mx= np.array(moment_mx) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mx = []
            #----
            col_moment_my = find_column(['MYY'], caseload_sheet)[0]
            moment_my = [row[col_moment_my] for row in caseload_sheet][1:]
            moment_my = np.vectorize(lambda x: x.replace(',', '.'))(moment_my)
            moment_my = - np.vectorize(float)(moment_my)
            rcpanelload.moment_my= np.array(moment_my) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_my = []
            #----
            col_moment_mxy = find_column(['MXY'], caseload_sheet)[0]
            moment_mxy = [row[col_moment_mxy] for row in caseload_sheet][1:]
            moment_mxy = np.vectorize(lambda x: x.replace(',', '.'))(moment_mxy)
            moment_mxy = np.vectorize(float)(moment_mxy)
            rcpanelload.moment_mxy= np.array(moment_mxy) * (solverunit_moment / rcpanelload.moment_unit).asNumber()
            moment_mxy = []
            #----
            col_force_vx = find_column(['QXX'], caseload_sheet)[0]
            force_vx = [row[col_force_vx] for row in caseload_sheet][1:]
            force_vx = np.vectorize(lambda x: x.replace(',', '.'))(force_vx)
            force_vx = np.vectorize(float)(force_vx)
            rcpanelload.force_vx= np.array(force_vx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vx = []
            #----
            col_force_vy = find_column(['QYY'], caseload_sheet)[0]
            force_vy = [row[col_force_vy] for row in caseload_sheet][1:]
            force_vy = np.vectorize(lambda x: x.replace(',', '.'))(force_vy)
            force_vy = np.vectorize(float)(force_vy)
            rcpanelload.force_vy= np.array(force_vy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_vy = []        
            #----
            col_force_nx = find_column(['NXX'], caseload_sheet)[0]
            force_nx = [row[col_force_nx] for row in caseload_sheet][1:]
            force_nx = np.vectorize(lambda x: x.replace(',', '.'))(force_nx)
            force_nx = np.vectorize(float)(force_nx)
            rcpanelload.force_nx= np.array(force_nx) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nx = []          
            #----
            col_force_ny = find_column(['NYY'], caseload_sheet)[0]
            force_ny = [row[col_force_ny] for row in caseload_sheet][1:]
            force_ny = np.vectorize(lambda x: x.replace(',', '.'))(force_ny)
            force_ny = np.vectorize(float)(force_ny)
            rcpanelload.force_ny= np.array(force_ny) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_ny = []
            #----
            col_force_nxy = find_column(['NXY'], caseload_sheet)[0]
            force_nxy = [row[col_force_nxy] for row in caseload_sheet][1:]
            force_nxy = np.vectorize(lambda x: x.replace(',', '.'))(force_nxy)
            force_nxy = np.vectorize(float)(force_nxy)
            rcpanelload.force_nxy= np.array(force_nxy) * (solverunit_force / rcpanelload.force_unit).asNumber()
            force_nxy = []
            #---adding new case in load object
            rcpanelload.casename = case_name
            rcpanelload.add_loadcase()
            rcpanelload.set_activeloadcase(case_name)
        #----
        if progress:
            progress.setValue(80)
            progress.setValue(0)

# Test if main
if __name__ == '__main__':
    from RcPanel import RcPanel
    from RcPanelLoad import RcPanelLoad
    panel = RcPanel()
    load = RcPanelLoad()
    loader = RcPanelDataLoader()
    panel.h_unit = u.mm
    panel.coord_unit = u.m
    load.moment_unit = u.kNm
    load.force_unit = u.kN
    #loader.RFEMxlsloader(panel, load)
    #loader.ROBOTcsvloader(panel, load)