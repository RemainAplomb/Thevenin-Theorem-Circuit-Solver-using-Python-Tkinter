from tkinter import *
from tkinter import messagebox

from decimal import Decimal
import math

from PIL import Image, ImageTk

class support:
    def __init__ ( self ) :
        self.EPrefixList = [ [ "k" , "M" , "G" , "T" ], [ "m" , "u" , "n" , "p" ] ]
        self.EPrefixDic = { "k" : 1E3 , "M" : 1E6 , "G" : 1E9 , "T" : 1E12,
                            "m" : 1E-3 , "u" : 1E-6 , "n" : 1E-9 , "p" : 1E-12 }
        self.trueValueDic = { "k" : "E3" , "M" : "E6" , "G" : "E9" , "T" : "E12",
                            "m" : "E-3" , "u" : "E-6" , "n" : "E-9" , "p" : "E-12" }
        self.unrecognizableChars = "abcdefghijloqrstvwxyzABCDEFHIJKLNOPQRSUV!@#$%^&*()_+={}[]|\;:?/><,~`"
        
    def makeENotation ( self , value , format = "%s" ):
        self.value = value
        self.sign = ""
        if self.value < 0:
            self.value = -self.value
            self.sign = "-"
        try:
            self.exponent = int ( math.floor ( math.log10( self.value )))
        except:
            self.exponent = 1
        self.Eexponent = self.exponent - ( self.exponent % 3 )
        self.Evalue = self.value / ( 10 ** self.Eexponent )
        if self.Eexponent == 0:
            self.Eexponent_value = ""
        else:
            self.Eexponent_value = "e%s" % self.Eexponent
        return ( "%s" + format + "%s" ) % ( self.sign, self.Evalue, self.Eexponent_value )
        
    def make4Decimals ( self, value ):
        self.value = value
        self.__EPrefixValue = self.makeEPrefix( self.value )
        self.__tempList = self.__EPrefixValue.split(" ")
        self.dropped = float(math.floor( float( self.__tempList[0]) * 10 ** 4 ) / 10 ** 4)
        if len(self.__tempList) > 1:
            self.__partialResult = self.dropped * self.EPrefixDic[ self.__tempList[1] ]
        else:
            self.__partialResult = self.dropped
        print( self.__partialResult )
        self.__result = self.makeENotation( self.__partialResult )
        return self.__result
        
        
    def makeEPrefix ( self , value , seperator = " " ) :
        self.value = float(value)
        try:
            self.EPrefixType = int ( math.floor ( math.log10( math.fabs(self.value) ) / 3 ) )
        except:
            self.EPrefixType = 0
        if self.EPrefixType != 0:
            self.tempPointer = self.EPrefixType/ math.fabs ( self.EPrefixType )
            if self.tempPointer == 1:
                try:
                    EPrefix = self.EPrefixList[0][ self.EPrefixType - 1 ]
                except:
                    EPrefix = self.EPrefixList[0][-1]
                    self.EPrefixType = len ( self.EPrefixList[0] )
            elif self.tempPointer == -1:
                try:
                    EPrefix = self.EPrefixList[1][ -self.EPrefixType - 1]
                except:
                    EPrefix = self.EPrefixList[1][-1]
                    self.EPrefixType = -len( self.EPrefixList[1] )
            adjusted = self.make4Decimals(float ( self.value * math.pow( 1000 , -self.EPrefixType )))
            self.result = "{adjusted}{seperator}{EPrefix}".format(adjusted = adjusted,
                                                                  seperator = seperator,
                                                                  EPrefix = EPrefix)
        else:
            self.result = "{value}".format(value = value)

        return self.result

    def trueValue( self, data ):
        self.data = str( data )
        self.dataAsList = list( data )
        self.tempList = list( self.trueValueDic )
        self.tempPrefix = None
        for i in range ( len ( self.dataAsList ) ):
            try:
                if self.dataAsList[i] == " ":
                    self.dataAsList.remove(" ")
                if self.dataAsList[i] in self.unrecognizableChars:
                    return False
            except:
                pass
            
        for i in range ( len ( self.tempList ) ):
            if self.tempList[i] in self.dataAsList:
                self.tempPrefix = self.tempList[i]
                self.dataAsList.remove( self.tempList[i] )
                break
        self.splitTest = self.data.split(self.tempPrefix)
        print(self.splitTest)
        if len(self.splitTest) > 1 and self.splitTest[1] != "" and self.splitTest[1] != " ":
            return False
        if self.tempPrefix != None:
            self.data = float ("".join( self.dataAsList ) + self.trueValueDic[ self.tempPrefix ])
        else:
            self.data = float ( "".join( self.dataAsList ) )
        return self.data
    

s = support()

class circuitSolver:
    def __init__(self):
        pass

    def step1( self, SourceVx , R1 , Vx):
        self.SourceVx = SourceVx
        self.R1 = R1
        self.Vx = -Vx

        self.s1Result = []
        
        self.s1I2A = -self.SourceVx * self.Vx
        self.s1Result.append( self.s1I2A )
        
        self.temp_s1I1 = self.R1
        self.s1I2B = -self.R1
        self.s1I2 = self.s1I2A + self.s1I2B
        self.s1Result.append( self.s1I2 )
        

        try:
            self.s1I1 = -self.s1I2 / self.temp_s1I1
        except ZeroDivisionError:
            self.s1I1 = 0
        self.s1Result.append( float(s.make4Decimals(self.s1I1)))
        
        return self.s1Result

    def step2( self, R3 , R1 , R4 , s1Result):
        self.R3 = R3
        self.R1 = R1
        self.R4 = R4
        self.s1Result = s1Result

        self.s2Result = []

        self.s2R3I2 = self.R3
        self.s2R1I2 = self.R1
        self.temp_s2R1I1 = -self.R1
        self.s2R4I2 = self.R4
        self.s2R4I3 = -self.R4

        self.s2R1I1 = self.temp_s2R1I1 * self.s1Result
        self.s2Result.append( self.s2R1I1 )

        self.s2TotalI2 = self.s2R3I2 + self.s2R1I2 + self.s2R1I1 + self.s2R4I2
        self.s2Result.append( self.s2TotalI2 )
        
        self.s2I2 = -self.s2R4I3 / self.s2TotalI2
        self.s2Result.append( float(s.make4Decimals(self.s2I2)))

        return self.s2Result

    def step3( self, R4 , R2 , V0 , s2I2 ):
        self.R4 = R4
        self.R2 = R2
        self.V0 = V0
        self.s2I2 = s2I2

        self.s3Result = []

        self.s3R4I3 = self.R4
        self.temp_s3R4I2 = -self.R4
        self.s3R2I3 = self.R2

        self.s3R4I2 = self.temp_s3R4I2 * self.s2I2
        self.s3Result.append(self.s3R4I2)
        self.temp_s3I3 = self.s3R4I3 + self.s3R2I3
        self.s3Result.append(self.temp_s3I3)


        self.total_s3I3 = self.temp_s3I3 + self.s3R4I2
        self.s3Result.append(self.total_s3I3)

        self.s3I3 = (-self.V0) / self.total_s3I3
        self.s3Result.append( float(s.make4Decimals(self.s3I3)))

        return self.s3Result

    def step4 ( self, s3Result , V0 ):
        self.s3I3 = s3Result
        self.V0 = V0

        self.s4Result = []

        self.s4I0 = -self.s3I3 
        self.s4Rth = self.V0 / self.s4I0
        print ( self.s4I0)
        self.s4Result.append(float(s.make4Decimals(self.s4Rth)))

        return self.s4Result

    def step5 ( self , I1 , R3 , R1 , R4 , SourceVx):
        self.I1 = I1
        self.R3 = R3
        self.R1 = R1
        self.R4 = R4
        self.SourceVx = SourceVx

        self.s5Result = []

        self.temp_s5R3I1 = -self.R3
        self.temp_s5R1I3 = -self.R1

        self.temp_s5RI2 = self.R3 + self.R1 + self.R4
        self.s5Result.append( self.temp_s5RI2 )
        self.s5R3I1 = self.I1 * self.temp_s5R3I1 # 20
        self.s5Result.append(self.s5R3I1)

        try:
            self.s5SVx = self.temp_s5R1I3 * (self.SourceVx / self.R1)
        except ZeroDivisionError:
            self.s5SVx = 0
        self.s5Result.append(self.s5SVx)
        try:
            self.s5R1I2 = self.temp_s5R1I3 * ( self.R1 / self.R1)
        except ZeroDivisionError:
            self.s5R1I2 = 0
        self.s5Result.append(self.s5R1I2)

        self.s5RI2 = self.temp_s5RI2 + self.s5R1I2
        self.s5Result.append(self.s5RI2)

        self.s5R1VxA = self.s5SVx * ( self.R3 * self.I1 )
        self.s5Result.append(self.s5R1VxA)
        self.s5R1VxB = self.s5SVx * (-self.R3 )
        self.s5Result.append(self.s5R1VxB)

        self.s5WholeNumber = -(self.s5R3I1 + self.s5R1VxA)
        self.s5Result.append(self.s5WholeNumber)

        self.s5RI2 = self.s5RI2 + self.s5R1VxB
        self.s5Result.append(self.s5RI2)

        self.s5I2 = self.s5WholeNumber / self.s5RI2
        self.s5Result.append( float(s.make4Decimals(self.s5I2)))

        return self.s5Result
    
    def step6 ( self , R3 , R1 , R4 , SourceVx ):
        self.R3 = R3
        self.R1 = R1
        self.R4 = R4
        self.SourceVx = SourceVx

        self.s6Result = []

        try:
            self.s6VxI3 = 2 * ( self.R1 / self.SourceVx )
        except ZeroDivisionError:
            self.s6VxI3 = 0
        self.s6Result.append(self.s6VxI3)
        try:
            self.s6VxI2 =  2 * (-( self.R1 / self.SourceVx ))
        except ZeroDivisionError:
            self.s6VxI2 = 0
        self.s6Result.append(self.s6VxI2)

        self.s6R1I2 = 2 * (-self.R1)
        self.s6Result.append(self.s6R1I2)
        
        self.s6R1I3 = 2 * (-self.R1 * -1)
        self.s6Result.append(self.s6R1I3)

        self.s6R4I2 = 2 * (-self.R4)
        self.s6Result.append(self.s6R4I2)

        self.partial_s6RI2 = self.s6R1I2 + self.s6R4I2
        self.s6Result.append(self.partial_s6RI2)
        
        self.s6RI2 = self.partial_s6RI2 + (-self.s6VxI2)
        self.s6Result.append(self.s6RI2)

        self.s6RI3 = self.s6R1I3 + (-self.s6VxI3)
        self.s6Result.append(self.s6RI3)

        try:
            self.s6I3 = (-self.s6RI2) / self.s6RI3
        except:
            self.s6I3 = 0
        self.s6Result.append( float(s.make4Decimals(self.s6I3)))

        return self.s6Result

    def step7 ( self , SourceVx , R1 , s6I3 ):
        self.SourceVx = SourceVx
        self.R1 = self.R1
        self.s6I3 = s6I3

        self.s7Result = []

        self.s7I2 = self.R1 * ( self.s6I3 - 1 ) 
        self.s7Result.append(self.s7I2)

        try:
            self.s7result = self.s7I2 / self.SourceVx
        except ZeroDivisionError:
            self.s7result = 0
        self.s7Result.append( float(s.make4Decimals(self.s7result)))

        return self.s7Result

    def step8 ( self , s7result , s5I2 ):
        self.s7result = s7result
        self.s5I2 = s5I2
        self.s8Result = []

        self.s8result = self.s7result * self.s5I2
        self.s8Result.append( float(s.make4Decimals(self.s8result)))

        return self.s8Result

    def solve ( self , SourceVx , CurrentSource , R1 , R2 , R3 , R4 ):
        self.sSourceVx = SourceVx
        self.sCurrentSource = CurrentSource
        self.sV0 = 1
        self.sR1 = R1
        self.sR2 = R2
        self.sR3 = R3
        self.sVx = R3
        self.sR4 = R4

        self.solutionData = []

        self.s1resultList = self.step1( self.sSourceVx , self.sR1 , self.sVx)
        self.solutionData.append( self.s1resultList )
        self.s1result = self.s1resultList[-1]
        
        self.s2resultList = self.step2( self.sR3 , self.sR1 , self.sR4 , self.s1result)
        self.solutionData.append( self.s2resultList )
        self.s2result = self.s2resultList[-1]

        self.s3resultList = self.step3( self.sR4 , self.sR2 , self.sV0 , self.s2result )
        self.solutionData.append( self.s3resultList )
        self.s3result = self.s3resultList[-1]
        #print( self.s3resultList[-1])
        
        self.s4resultList = self.step4( self.s3result , self.sV0 )
        self.solutionData.append( self.s4resultList )
        self.s4result = self.s4resultList[-1]
        
        self.s5resultList = self.step5( self.sCurrentSource , self.sR3 , self.sR1 , self.sR4 , self.sSourceVx)
        self.solutionData.append( self.s5resultList )
        self.s5result = self.s5resultList[-1]
        
        self.s6resultList = self.step6( self.sR3 , self.sR1 , self.sR4 , self.sSourceVx )
        self.solutionData.append( self.s6resultList )
        self.s6result = self.s6resultList[-1]
        
        self.s7resultList = self.step7( self.sSourceVx , self.sR1 , self.s6result )
        self.solutionData.append( self.s7resultList )
        self.s7result = self.s7resultList[-1]
        
        self.s8resultList = self.step8( self.s7result , self.s5result )
        self.solutionData.append( self.s8resultList )
        self.s8result = self.s8resultList[-1]


        return self.solutionData

cS= circuitSolver()

class circuitUI:
    def __init__( self ):
        self.mcUI_width = 500
        self.mcUI_height = 500
        
        self.createGUI()


    def filterEntry(self , entry):
        self.entry = entry
        self.entryAsList = list ( self.entry )
        
        for i in range ( len ( self.entry ) ):
            if self.entryAsList[i] == "\n" :
                del self.entryAsList[i]
        self.filterResult = "".join(self.entryAsList)
        return self.filterResult
        
    def mainCircuit( self ):
        self.mcUI_backgroundImage_open = Image.open( "background5.jpg" )
        self.mcUI_backgroundImage_resized = self.mcUI_backgroundImage_open.resize( (510 , 510), Image.ANTIALIAS )
        self.mcUI_backgroundImage = ImageTk.PhotoImage( self.mcUI_backgroundImage_resized )
        self.mcUI_backgroundImage_LBL = Label( self.mC , image = self.mcUI_backgroundImage )
        self.mcUI_backgroundImage_LBL.place( x = -2 , y = -2 )

        self.mcUI_mainCircuitImage_open = Image.open( "mainCircuit.png" )
        self.mcUI_mainCircuitImage_resized = self.mcUI_mainCircuitImage_open.resize( (480 , 300), Image.ANTIALIAS )
        self.mcUI_mainCircuitImage = ImageTk.PhotoImage( self.mcUI_mainCircuitImage_resized )
        self.mcUI_mainCircuitImage_LBL = Label( self.mC , image = self.mcUI_mainCircuitImage )
        self.mcUI_mainCircuitImage_LBL.place( x = 10 , y = 50 )

        self.TheveninsText = Label ( text = "THEVENIN'S THEOREM" , bg = "lightblue" , fg = "black" , width = "20" , height = "1" ,
                               font = ( "Courier" , 25 , "bold" ))
        self.TheveninsText.place ( x = 50 , y = 4 )
        
        self.mcUI_SolveBTN = Button ( self.mC , font = ( "Courier" , 15 , "bold" ) , text = "SOLVE" , width = "20"
                                , height = "50" ,bg = "green" , fg = "black" , command = self.solveBTN_clicked )
        self.mcUI_SolveBTN.place ( x = 130 , y = 370 , height = 40 )

        self.mcUI_ExitBTN = Button ( self.mC , font = ( "Courier" , 15 , "bold" ) , text = "EXIT PROGRAM" , width = "20"
                                , height = "50" ,bg = "green" , fg = "black" , command = self.ext )
        self.mcUI_ExitBTN.place ( x = 130 , y = 430 , height = 40 )

        self.mcUI_SourceVx_Entry = Text ( self.mC , bd = 0 , bg = "LightGrey" , width = "9" , height = "1" , font = "Arial" )
        self.mcUI_SourceVx_Entry.place( x = 195 , y = 100 )

        self.mcUI_Vx_LBL = Label ( text = "Vx" , bg = "white" , fg = "black" , width = "2" , height = "1" ,
                               font = ( "Arial" , 8 , "bold" ))
        self.mcUI_Vx_LBL.place ( x = 280 , y = 100 , )

        self.mcUI_R1_Entry = Text ( self.mC , bd = 0 , bg = "LightGrey" , width = "9" , height = "1" , font = "Arial" )
        self.mcUI_R1_Entry.place( x = 195 , y = 195 )

        self.mcUI_R2_Entry = Text ( self.mC , bd = 0 , bg = "LightGrey" , width = "9" , height = "1" , font = "Arial" )
        self.mcUI_R2_Entry.place( x = 380 , y = 195 )

        self.mcUI_CurrentSource_Entry = Text ( self.mC , bd = 0 , bg = "LightGrey" , width = "5" , height = "1" , font = "Arial" )
        self.mcUI_CurrentSource_Entry.place( x = 15 , y = 238 )

        self.mcUI_R3_Entry = Text ( self.mC , bd = 0 , bg = "LightGrey" , width = "9" , height = "1" , font = "Arial" )
        self.mcUI_R3_Entry.place( x = 180 , y = 260 )

        self.mcUI_R4_Entry = Text ( self.mC , bd = 0 , bg = "LightGrey" , width = "9" , height = "1" , font = "Arial" )
        self.mcUI_R4_Entry.place( x = 335 , y = 271 )

        self.mcUI_ohmsSymbol1_LBL = Label ( text = "Ω" , bg = "white" , fg = "black" , width = "1" , height = "1" ,
                               font = ( "Arial" , 8 , "bold" ))
        self.mcUI_ohmsSymbol1_LBL.place( x= 280 , y = 195 )

        self.mcUI_ohmsSymbol2_LBL = Label ( text = "Ω" , bg = "white" , fg = "black" , width = "1" , height = "1" ,
                               font = ( "Arial" , 8 , "bold" ))
        self.mcUI_ohmsSymbol2_LBL.place( x= 465 , y = 195 )

        self.mcUI_ohmsSymbol3_LBL = Label ( text = "Ω" , bg = "white" , fg = "black" , width = "1" , height = "1" ,
                               font = ( "Arial" , 8 , "bold" ))
        self.mcUI_ohmsSymbol3_LBL.place( x= 265 , y = 260 )

        self.mcUI_ohmsSymbol4_LBL = Label ( text = "Ω" , bg = "white" , fg = "black" , width = "1" , height = "1" ,
                               font = ( "Arial" , 8 , "bold" ))
        self.mcUI_ohmsSymbol4_LBL.place( x= 420 , y = 271 )
        

    def solveBTN_clicked( self ):
        self.solve_Error = False
        if messagebox.askyesno( "Solve Circuit?" , "Are your Inputs final?" )== True :
            try:
                self.mcUI_SourceVx = float (s.trueValue( self.filterEntry( self.mcUI_SourceVx_Entry.get( "0.0" , END ) ) ))
                if self.mcUI_SourceVx == False:
                    messagebox.showinfo( "Input Error Detected" , "Unrecognizable character detected at SourceVx Entry." )
                    self.solve_Error = True
                self.mcUI_R1 = float (s.trueValue( self.filterEntry( self.mcUI_R1_Entry.get( "0.0" , END ) ) ))
                if self.mcUI_R1 == False:
                    messagebox.showinfo( "Input Error Detected" , "Unrecognizable character detected at R1 Entry." )
                    self.solve_Error = True
                self.mcUI_R2 = float (s.trueValue( self.filterEntry( self.mcUI_R2_Entry.get( "0.0" , END ) ) ))
                if self.mcUI_R2 == False:
                    messagebox.showinfo( "Input Error Detected" , "Unrecognizable character detected at R2 Entry." )
                    self.solve_Error = True
                self.mcUI_CurrentSource = float (s.trueValue( self.filterEntry( self.mcUI_CurrentSource_Entry.get( "0.0" , END ) ) ))
                if self.mcUI_CurrentSource == False:
                    messagebox.showinfo( "Input Error Detected" , "Unrecognizable character detected at Current Source Entry." )
                    self.solve_Error = True
                self.mcUI_R3 = float (s.trueValue( self.filterEntry( self.mcUI_R3_Entry.get( "0.0" , END ) ) ))
                if self.mcUI_R3 == False:
                    messagebox.showinfo( "Input Error Detected" , "Unrecognizable character detected at R3 Entry." )
                    self.solve_Error = True
                self.mcUI_R4 = float (s.trueValue( self.filterEntry( self.mcUI_R4_Entry.get( "0.0" , END ) ) ))
                if self.mcUI_R4 == False:
                    messagebox.showinfo( "Input Error Detected" , "Unrecognizable character detected at R4 Entry." )
                    self.solve_Error = True
            except:
                self.solve_Error = True
                messagebox.showinfo( "Error Detected" , "Please make sure you are inputting the values right." )                
            if self.solve_Error == False :
                self.mcUI_mainCircuitImage_LBL.destroy()
                self.TheveninsText.destroy()
                self.mcUI_SolveBTN.destroy()
                self.mcUI_ExitBTN.destroy()
                self.mcUI_SourceVx_Entry.destroy()
                self.mcUI_Vx_LBL.destroy()
                self.mcUI_R1_Entry.destroy()
                self.mcUI_R2_Entry.destroy()
                self.mcUI_CurrentSource_Entry.destroy()
                self.mcUI_R3_Entry.destroy()
                self.mcUI_R4_Entry.destroy()
                self.mcUI_ohmsSymbol1_LBL.destroy()
                self.mcUI_ohmsSymbol2_LBL.destroy()
                self.mcUI_ohmsSymbol3_LBL.destroy()
                self.mcUI_ohmsSymbol4_LBL.destroy()
                self.mcUI_backgroundImage_LBL.destroy()

                self.solutionData = cS.solve( self.mcUI_SourceVx , self.mcUI_CurrentSource ,
                                              self.mcUI_R1 , self.mcUI_R2 , self.mcUI_R3 , self.mcUI_R4 )
                self.circuitSolution( self.solutionData )

    def delay1( self ):
        self.csUI_firstRedrawImage_open = Image.open( "redraw1.png" )
        self.csUI_firstRedrawImage_resized = self.csUI_firstRedrawImage_open.resize( (320 , 200), Image.ANTIALIAS )
        self.csUI_firstRedrawImage = ImageTk.PhotoImage( self.csUI_firstRedrawImage_resized )
        self.csUI_firstRedrawImage_LBL = Label( self.mC , image = self.csUI_firstRedrawImage )
        self.csUI_firstRedrawImage_LBL.place( x = 10 , y = 5 )

        self.csUI_delay11_LBL = Label ( text = str(s.makeEPrefix(self.mcUI_SourceVx)) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay11_LBL.place ( x = 80 , y = 5 )

        self.csUI_delay12_LBL = Label ( text = str(s.makeEPrefix(self.mcUI_R1)) + "Ω" , bg = "white" , fg = "black" , width = "10" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay12_LBL.place ( x = 90 , y = 90 )

        self.csUI_delay13_LBL = Label ( text = str(s.makeEPrefix(self.mcUI_R2)) + "Ω" , bg = "white" , fg = "black" , width = "10" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay13_LBL.place ( x = 180 , y = 90 )

        self.csUI_delay14_LBL = Label ( text = str(s.makeEPrefix(self.mcUI_R3)) + "Ω" , bg = "white" , fg = "black" , width = "10" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay14_LBL.place ( x = 10 , y = 140 )

        self.csUI_delay15_LBL = Label ( text = str(s.makeEPrefix(self.mcUI_R4)) + "Ω" , bg = "white" , fg = "black" , width = "10" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay15_LBL.place ( x = 170 , y = 140 )

        

    def delay2( self ):
        self.csUI_solution1Image_open = Image.open( "solution1.png" )
        self.csUI_solution1Image_resized = self.csUI_solution1Image_open.resize( (320 , 200), Image.ANTIALIAS )
        self.csUI_solution1Image = ImageTk.PhotoImage( self.csUI_solution1Image_resized )
        self.csUI_solution1Image_LBL = Label( self.mC , image = self.csUI_solution1Image )
        self.csUI_solution1Image_LBL.place( x = 10 , y = 215 )

        self.csUI_sol11_LBL = Label ( text = str(-self.mcUI_SourceVx) + "Vx + (" + str(self.mcUI_R1) + ")(i1 - i2) = 0" , bg = "white" , fg = "black" , width = "30" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol11_LBL.place ( x = 15 , y = 240 )

        self.csUI_sol12_LBL = Label ( text = "Vx = " + str(self.mcUI_R1/self.mcUI_SourceVx) + "i1 + (" + str(-self.mcUI_R1/self.mcUI_SourceVx) + "i2) " , bg = "white" , fg = "black" , width = "30" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol12_LBL.place ( x = 15 , y = 265 )
        
        self.csUI_sol13_LBL = Label ( text = " i1 = " + str(self.solutionData[0][-1]) +" i2", bg = "white" , fg = "black" , width = "30" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol13_LBL.place ( x = 15 , y = 305 )

        self.csUI_sol14_LBL = Label ( text = " i1 = " + str(self.solutionData[0][-1]) +" i2", bg = "white" , fg = "black" , width = "30" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol14_LBL.place ( x = 15 , y = 305 )

        self.csUI_sol15_LBL = Label ( text = str(self.mcUI_R3) + " + (" + str(self.mcUI_R1) + ")(i2 -i1) + (" + str(self.mcUI_R4) + ")(i2 - i3) = 0" , bg = "white" , fg = "black" , width = "40" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol15_LBL.place ( x = 15 , y = 355 )
        
        self.csUI_sol16_LBL = Label ( text = str(self.mcUI_R4) + "(i3 -i2) + (" + str(self.mcUI_R1) + "i3) + 1 = 0 " , bg = "white" , fg = "black" , width = "40" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol16_LBL.place ( x = 15 , y = 375 )

        self.csUI_solution2Image_open = Image.open( "solution2.png" )
        self.csUI_solution2Image_resized = self.csUI_solution2Image_open.resize( (320 , 200), Image.ANTIALIAS )
        self.csUI_solution2Image = ImageTk.PhotoImage( self.csUI_solution2Image_resized )
        self.csUI_solution2Image_LBL = Label( self.mC , image = self.csUI_solution2Image )
        self.csUI_solution2Image_LBL.place( x = 10 , y = 425 )

        self.csUI_sol21_LBL = Label ( text = "i3 = " + str(s.makeEPrefix(self.solutionData[2][-1])) + "A" , bg = "white" , fg = "black" , width = "40" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol21_LBL.place ( x = 25 , y = 450 )
        
        self.csUI_sol22_LBL = Label ( text = str(s.makeEPrefix(-self.solutionData[2][-1])) + "A" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol22_LBL.place ( x = 100 , y = 473 )

        self.csUI_sol23_LBL = Label ( text = "1V" , bg = "white" , fg = "black" , width = "2" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol23_LBL.place ( x = 120 , y = 490 )

        self.csUI_sol24_LBL = Label ( text = str(s.makeEPrefix(-self.solutionData[2][-1])) + "A" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol24_LBL.place ( x = 100 , y = 510 )
        
        self.csUI_sol25_LBL = Label ( text = str(s.makeEPrefix( s.make4Decimals(1 / (-self.solutionData[2][-1])))) + " ohms" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol25_LBL.place ( x = 170 , y = 500 )

        self.csUI_sol26_LBL = Label ( text = " i1 = " + str(s.makeEPrefix( self.mcUI_CurrentSource )) , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol26_LBL.place ( x = 100 , y = 550 )

        self.csUI_sol27_LBL = Label ( text = str(-self.mcUI_SourceVx) + "Vx + (" + str(self.mcUI_R1) + ")(i3 - i2) = 0 "  , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol27_LBL.place ( x = 100 , y = 580 )
        
        self.csUI_sol27_LBL = Label ( text = str(-self.mcUI_SourceVx) + "Vx + (" + str(self.mcUI_R1) + ")(i3 - i2) = 0 "  , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol27_LBL.place ( x = 100 , y = 600 )
        
    def delay3( self ):
        self.csUI_secondRedrawImage_open = Image.open( "redraw2.png" )
        self.csUI_secondRedrawImage_resized = self.csUI_secondRedrawImage_open.resize( (320 , 200), Image.ANTIALIAS )
        self.csUI_secondRedrawImage = ImageTk.PhotoImage( self.csUI_secondRedrawImage_resized )
        self.csUI_secondRedrawImage_LBL = Label( self.mC , image = self.csUI_secondRedrawImage )
        self.csUI_secondRedrawImage_LBL.place( x = 340 , y = 5 )

        self.csUI_solution3Image_open = Image.open( "solution3.png" )
        self.csUI_solution3Image_resized = self.csUI_solution3Image_open.resize( (320 , 200), Image.ANTIALIAS )
        self.csUI_solution3Image = ImageTk.PhotoImage( self.csUI_solution3Image_resized )
        self.csUI_solution3Image_LBL = Label( self.mC , image = self.csUI_solution3Image )
        self.csUI_solution3Image_LBL.place( x = 340 , y = 215 )

        self.csUI_sol31_LBL = Label ( text = str(self.solutionData[4][0]) + " + (" + str(-self.mcUI_R3) + "i2) + (" + str(-self.mcUI_R1) + "i3) = 0"  , bg = "white" , fg = "black" , width = "30" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol31_LBL.place ( x = 350 , y = 245 )

        self.csUI_sol32_LBL = Label ( text = " i2 = " + str(self.solutionData[4][-1])  , bg = "white" , fg = "black" , width = "25" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol32_LBL.place ( x = 425 , y = 310 )

        self.csUI_sol33_LBL = Label ( text = " Vx = Voc = " + str(self.solutionData[7][0]) + "V"  , bg = "white" , fg = "black" , width = "25" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol33_LBL.place ( x = 425 , y = 350 )

        self.csUI_solution4Image_open = Image.open( "solution4.png" )
        self.csUI_solution4Image_resized = self.csUI_solution4Image_open.resize( (320 , 200), Image.ANTIALIAS )
        self.csUI_solution4Image = ImageTk.PhotoImage( self.csUI_solution4Image_resized )
        self.csUI_solution4Image_LBL = Label( self.mC , image = self.csUI_solution4Image )
        self.csUI_solution4Image_LBL.place( x = 340 , y = 425 )

        self.csUI_sol34_LBL = Label ( text = " Vx = " + str( s.makeEPrefix( s.make4Decimals(self.solutionData[7][0]))) + "V"  , bg = "white" , fg = "black" , width = "25" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol34_LBL.place ( x = 400 , y = 500 )

        self.csUI_sol35_LBL = Label ( text = " Rth = " + str( s.makeEPrefix( s.make4Decimals(self.solutionData[3][0]))) + " ohms"  , bg = "white" , fg = "black" , width = "25" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_sol35_LBL.place ( x = 400 , y = 530 )

        

        self.csUI_delay31_LBL = Label ( text = str(s.makeEPrefix( s.make4Decimals(self.mcUI_SourceVx))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay31_LBL.place ( x = 470 , y = 5 )
        
        self.csUI_delay32_LBL = Label ( text = str(s.makeEPrefix( s.make4Decimals(self.mcUI_R1))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay32_LBL.place ( x = 470 , y = 95 )

        self.csUI_delay33_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals( self.mcUI_R2))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay33_LBL.place ( x = 565 , y = 95 )

        self.csUI_delay34_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals( self.mcUI_CurrentSource))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay34_LBL.place ( x = 380 , y = 90 )
        

        self.csUI_delay35_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals( self.mcUI_R3))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay35_LBL.place ( x = 385 , y = 138 )
        
        self.csUI_delay36_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals( self.mcUI_R4))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 8))
        self.csUI_delay36_LBL.place ( x = 560 , y = 140 )


    def delay4( self ):
        pass

    def delay5( self ):
        
        self.csUI_thirdRedrawImage_open = Image.open( "thevenin.png" )
        self.csUI_thirdRedrawImage_resized = self.csUI_thirdRedrawImage_open.resize( (320 , 200), Image.ANTIALIAS )
        self.csUI_thirdRedrawImage = ImageTk.PhotoImage( self.csUI_thirdRedrawImage_resized )
        self.csUI_thirdRedrawImage_LBL = Label( self.mC , image = self.csUI_thirdRedrawImage )
        self.csUI_thirdRedrawImage_LBL.place( x = 670 , y = 5 )

        self.csUI_delay51_LBL = Label ( text = str(s.makeEPrefix(self.solutionData[3][-1])) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10))
        self.csUI_delay51_LBL.place ( x = 750 , y = 25 )

        self.csUI_delay52_LBL = Label ( text = str(s.makeEPrefix(self.solutionData[-1][-1])) + "V" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10))
        self.csUI_delay52_LBL.place ( x = 738 , y = 115 )
        
    def delay6( self ):
        self.csUI_delay61_LBL = Label ( text = "RESISTOR" , bg = "lightGreen" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay61_LBL.place ( x = 672 , y = 222 )
        
        self.csUI_delay611_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.mcUI_R1))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay611_LBL.place ( x = 672 , y = 252 )

        self.csUI_delay612_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.mcUI_R3))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay612_LBL.place ( x = 672 , y = 282 )

        self.csUI_delay613_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.mcUI_R4))) + "Ω" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay613_LBL.place ( x = 672 , y = 312 )

        self.csUI_delay614_LBL = Label ( text = "" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay614_LBL.place ( x = 672 , y = 342 )


        
        self.csUI_delay62_LBL = Label ( text = "CURRENT" , bg = "lightGreen" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay62_LBL.place ( x = 781 , y = 222 )
        
        self.csUI_delay621_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.solutionData[2][-1]))) + "A" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay621_LBL.place ( x = 781 , y = 252 )
        
        self.csUI_delay622_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.mcUI_CurrentSource))) + "A" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay622_LBL.place ( x = 781 , y = 282 )

        self.csUI_delay623_LBL = Label ( text = str(s.makeEPrefix(self.solutionData[4][-1])) + "A" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay623_LBL.place ( x = 781 , y = 312 )

        self.csUI_delay624_LBL = Label ( text = "" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay624_LBL.place ( x = 781 , y = 342 )

        
        self.csUI_delay63_LBL = Label ( text = "VOLTAGE" , bg = "lightGreen" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay63_LBL.place ( x = 890 , y = 222 )

        self.voltage1 = (self.solutionData[-1][-1]) * ( self.mcUI_R3 / self.mcUI_R4 )

        self.voltage2 = (self.solutionData[-1][-1]) * ( self.mcUI_R1 / self.mcUI_R4 )

        self.csUI_delay631_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.voltage1))) + "V" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay631_LBL.place ( x = 890 , y = 252 )

        self.csUI_delay632_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.solutionData[-1][-1]))) + "V" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay632_LBL.place ( x = 890 , y = 282 )

        self.csUI_delay633_LBL = Label ( text = str(s.makeEPrefix(s.make4Decimals(self.voltage2))) + "V" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay633_LBL.place ( x = 890 , y = 312 )

        self.csUI_delay634_LBL = Label ( text = "" , bg = "white" , fg = "black" , width = "12" , height = "1" ,
                               font = ( "Arial" , 10 , "bold"))
        self.csUI_delay634_LBL.place ( x = 890 , y = 342 )


    def delay7( self ):
        self.csUI_backBTN = Button ( self.mC , font = ( "Courier" , 15 , "bold" ) , text = "BACK" , width = "20"
                                , height = "50" ,bg = "green" , fg = "black" , command = self.backBTN1 )
        self.csUI_backBTN.place ( x = 200 , y = 650 , height = 40 )

        self.csUI_exitBTN = Button ( self.mC , font = ( "Courier" , 15 , "bold" ) , text = "EXIT PROGRAM" , width = "20"
                                , height = "50" ,bg = "green" , fg = "black" , command = self.ext )
        self.csUI_exitBTN.place ( x = 520 , y = 650 , height = 40 )

    def circuitSolution( self , solutionData ):
        self.solutionData = solutionData

        self.mcUI_width = 1000
        self.mcUI_height = 700

        self.monitorWidth = self.mC.winfo_screenwidth()
        self.mcUI_Xplacement = ( (self.monitorWidth/2) - (self.mcUI_width/2) )
        
        self.csUI_backgroundImage_open = Image.open( "background8.jpg" )
        self.csUI_backgroundImage_resized = self.csUI_backgroundImage_open.resize( (1010 , 710), Image.ANTIALIAS )
        self.csUI_backgroundImage = ImageTk.PhotoImage( self.csUI_backgroundImage_resized )
        self.csUI_backgroundImage_LBL = Label( self.mC , image = self.csUI_backgroundImage )
        self.csUI_backgroundImage_LBL.place( x = -2 , y = -2 )
        
        self.mC.geometry("%dx%d+%d+%d" % (self.mcUI_width, self.mcUI_height, self.mcUI_Xplacement, 0) )
        
        self.mC.after( 800 , self.delay1 )
        self.mC.after( 1600 , self.delay2 )
        self.mC.after( 2600 , self.delay3 )
        self.mC.after( 3400 , self.delay4 )
        self.mC.after( 4400 , self.delay5 )
        self.mC.after( 5000 , self.delay6 )
        self.mC.after( 5800 , self.delay7 )
        
        
        
    def ext( self ):
        if messagebox.askyesno( "Exit Program" , "Are you sure you want to Exit the Program?" )== True :
            self.mC.destroy()

    def backBTN1( self ):
        self.mC.destroy()
        self.createGUI()

    def createGUI( self ):
        self.mcUI_width = 500
        self.mcUI_height = 500
        self.mC = Tk()

        self.monitorWidth = self.mC.winfo_screenwidth()
        self.monitorHeight = self.mC.winfo_screenheight()

        self.mcUI_Xplacement = ( (self.monitorWidth/2) - (self.mcUI_width/2) )
        self.mcUI_Yplacement = ( (self.monitorHeight/2) - (self.mcUI_height/2) )

        self.mC.geometry("%dx%d+%d+%d" % (self.mcUI_width, self.mcUI_height, self.mcUI_Xplacement, self.mcUI_Yplacement) )
        self.mC.config( bg = "orange" )
        self.mC.resizable( width = False , height = False )
        self.mC.title( "Circuit Solver" )

        self.mainCircuit()

    def run(self):
        self.mC.mainloop()
        

cg = circuitUI()
cg.run()
