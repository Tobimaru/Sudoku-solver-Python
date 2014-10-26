##--------------------------------------------------------------------
##Sudoku puzzle solver implemented for the coding challenge of
##the Insight Data Engineering Program (insightdataengineering.com)
##
##The implementation is based on examples as explained on the internet
##--------------------------------------------------------------------

import sys
import os
import numpy as np

##Class with data structures and subroutines to solve Sudoku
##---------------------------------------------------------
##It is assumed that the possible values for a cell are given
##by the integer range between 1 and the dimension of the sudoku grid

class SudokuSolver(object):

    def __init__(self):
        self.InputFile = ''
        self.Grid = []
        self.BlockMask = []
        self.BlockInds = []
        self.GridDim = 0
        self.BlockDim = 0
        self.BlockSize = 0
                     
    def read_sudoku(self,sudoku_file):
      ##read in the sudoku grid from csv file
        try: 
            self.Grid = np.genfromtxt(sudoku_file,dtype=np.int64,delimiter=',')
            if not self._format_check():
                return False
        except ValueError: 
            print('Input sudoku is in wrong format!' + os.linesep +
                  'Make sure comma separators are used and' + os.linesep +
                  'each line in the file contains one row.')
            return False
        except IOError:
            print('Input file not found!')
            return False    
            
        self.InputFile = sudoku_file  
        self.GridDim = self.Grid.shape[0]
        self.BlockDim = np.int64(np.sqrt(self.GridDim))
        self.BlockSize = np.int64(self.BlockDim*self.BlockDim)
        self._initiate_block_data()
        
        return True
                
    def _format_check(self):
      ##check if sudoku grid has correct format
        if self.Grid.shape[0] != self.Grid.shape[-1]: 
           print('Input sudoku grid is not square shaped!')
           return False
            
        sub_dim = np.sqrt(self.Grid.shape[0])
        if (sub_dim - np.ceil(sub_dim)) != 0.0:
           print('Input sudoku grid dimension cannot contain blocks!')                                 
           return False
                
        return True     
                   
    def _initiate_block_data(self):
      ##initiate data structures
        self.BlockMask = np.zeros((self.GridDim,self.GridDim),np.int64)
        self.BlockInds = []
    
      ##construct a mask of the grid to locate the blocks    
        for row_ind in range(self.BlockDim):
            frow = row_ind*self.BlockDim
            lrow = (row_ind+1)*self.BlockDim
            for col_ind in range(self.BlockDim):
                fcol = col_ind*self.BlockDim
                lcol = (col_ind+1)*self.BlockDim
                self.BlockMask[frow:lrow,fcol:lcol] = frow + col_ind          
        
      ##save the cell indices per block                  
        for block_ind in range(self.BlockSize):
            self.BlockInds.append(np.nonzero(self.BlockMask == block_ind))  
    
    def save_solution(self):
      ##extract the save directory and filename
        save_dir,save_name = os.path.split(self.InputFile)
        try:
            save_name = save_name[:save_name.index('.')]
        except ValueError: pass
      ##save solved grid to file  
        np.savetxt(os.path.join(save_dir,save_name + '_solution.csv'),
                   self.Grid,"%d",",")
                           
    def _check_valid_value(self,row_ind,col_ind,val):
      ##check if value is in same row (given cell is assumed to contain zero)
        if np.all(self.Grid[row_ind,:] != val):
          ##check if value is in same column
            if np.all(self.Grid[:,col_ind] != val):
              ##check if value is in same block
                block_ind = self.BlockMask[row_ind,col_ind] 
                if np.all(self.Grid[self.BlockInds[block_ind]] != val): 
                    return True
      ##If check fails, value is invalid
        return False
    
    def _find_next_cell(self,flat_ind):
        #look for next cell containing zero
        for next_ind in range(flat_ind,self.Grid.size):
            if self.Grid.flat[next_ind] == 0: 
              return next_ind
        #if none is found, return -1
        return -1            
                                    
    def solve(self,i=0):
        
        ##Find next cell to complete. 
        nxt_cell = self._find_next_cell(i);     
        ##If no more cells left, solution has been found and exit.
        if nxt_cell < 0: return True

        ##Otherwise, iterate over values.
        nxt_row,nxt_col = np.unravel_index(nxt_cell,(self.GridDim,self.GridDim)) 
        
        for new_val in range(1,self.GridDim+1):
           ##If value is valid, fill in grid and recursively call solve. 
           if self._check_valid_value(nxt_row,nxt_col,new_val):
               self.Grid[nxt_row,nxt_col] = new_val
               if self.solve(nxt_cell): return True
               ##if recursive call fails, reset current cell to zero for backtracking
               self.Grid[nxt_row,nxt_col] = 0 
               
        ##if no value is valid, partial solution is wrong
        return False       
                                                                                                                                    
##support function
##----------------
  
def init_check(sys_args):
    
    ##check if arguments are ok
    
    file_string = "path to csv-file containing sudoku";
    
    if len(sys_args) == 1:
        print('Use "-help" or ' + file_string + ' as argument.'); 
        return False;
    
    if len(sys_args) > 2:
        print("Only one argument expected!!");
        print("Please give " + file_string); 
        return False;
        
    if sys_args[1] == "-help":
       print("This application solves sudoku problems using" + os.linesep +
             "recursive backtracking algorithm" + os.linesep +
             "(http://en.wikipedia.org/wiki/Backtracking)." + os.linesep +
             "As argument, " + file_string + " is expected." + os.linesep +
             "The solution will be saved in the same directory" + os.linesep + 
             "that contains the input file.");
       return False;
       
    return True;   
    
##Main function that is called when executing application   
##-------------------------------------------------------
if __name__ == "__main__":

     if init_check(sys.argv):
        susol = SudokuSolver()
        print('Reading sudoku from: ' + sys.argv[1]) 
         
        if susol.read_sudoku(sys.argv[1]):
            print("Solving sudoku ...")
            
            if susol.solve(): 
                print(susol.Grid)
                susol.save_solution()
            else:
                print("Sudoku has no solution!")  
        
            
         
         
         
       
         
                
    