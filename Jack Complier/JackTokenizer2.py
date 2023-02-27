"""
    Jack Tokenizer takes a file or dirextory as an input and if there are .jack files, for each file
    a xml that is a list of tokens are an interim step in the compile process for the .jack files

    This is part of the the nand2tetris learning - Chapter 10

    author: williammarkpainter@gmail.com
    date: 8-Oct-20220
    using python-version: 3.9
"""
import typing
from pathlib import Path
from enum import Enum

from sympy import det

import FileList as fl
import os
import re

class tokenType(Enum):
    NONE, KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST = range(6)

class JackTokenizer:

    file_name: str
    opened_file: typing.TextIO
    output_file: typing.TextIO
    output_file_open: bool = False
    file_processed: bool = False
    has_more_tokens: bool = False
    loaded_list = []
    output_file_name: str = ""
    symbol_list: str = '\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~'
    regex_list: str = '([' + symbol_list + '\ \n\t])'
    keywords_list = ['class', 'constructor', 'function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
    symbol_list = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    clean_up_list = [" ", "\n", "", "\t"]
    string_literal_counter: int = 0
    string_mappings = []
    outputCounter: int = 0
    current_token_type: tokenType = None
    current_token: str = ""

    def __init__(self, fileName):
        self.file_name = fileName
        self.output_file_name = fileName[:-5] + "T.xml"
        self.loaded_list = []

    def __del__(self):
        if self.output_file_open:
            self.output_file.close()

    def load_file(self)->bool:
        """
        File opened and split case on symbol_list
        """
        self.opened_file = open(self.file_name, "r+")

        # loop through all lines and split based on regex
        for line in self.opened_file.readlines():
            # removed single line commnets
            parsedLine = self.trim_single_line_comments(line)
            parsedLine = self.replace_string_literals(parsedLine)

            # split line and add any non spaces, empty, or newline items to the loaded list
            for items in re.split(self.regex_list, parsedLine): 
                if items not in self.clean_up_list: #items != " " and items != "\n" and items != "" and items != null:
                    self.loaded_list.append(items)

        self.opened_file.close()    # close the file

        # Clean up multiline comments marked with /* as opening and */ as closing
        self.remove_multi_line_comments()
        
        # Replace the string literals
        self.return_string_literals()

        # Print
        # self.printdata()

        self.has_more_tokens = True
        self.file_loaded = True

        return True

    def open_file_for_output(self) -> bool:
        """
        open the xlm file for output
        """
        self.output_file = open(self.output_file_name, "w")
        self.output_file_open = True

    def lookahead(self, steps: int)->str:

        if self.outputCounter + steps <= len(self.loaded_list):
            return self.loaded_list[self.outputCounter + steps]
        else:
            raise ValueError("Step value applied is greater than the remaining list capacity")

    def advance(self)-> None:
        """
        advance through the processing of the loaded_list to find the next keyword, symbol, constant, or identifier
        """
        line = self.loaded_list[self.outputCounter]
        self.current_token = line
        if line[:1] == '"' and line[-1:]=='"':                  # if a token start and ends with a " it is a stringContant
            self.current_token_type = tokenType.STRING_CONST
        elif line in self.keywords_list:                        # if a token is in the key words list
            self.current_token_type = tokenType.KEYWORD
        elif line in self.symbol_list:                          # if a token is in the symbol list
            self.current_token_type = tokenType.SYMBOL
        elif line.isnumeric():                                  # if token as string could be a standalone number, it is an integer constant
            self.current_token_type = tokenType.INT_CONST
        else:
            self.current_token_type = tokenType.IDENTIFIER

        # Advance the outputCounter set 
        self.outputCounter += 1
        if self.outputCounter == len(self.loaded_list):
            self.has_more_tokens = False

        
    def printdata(self):
        """
        TESTING -> Print out the list of all loaded tokens in to self.loaded_list
        """
        for items in self.loaded_list:
            print(items)

    def write_StringConstant(self, line, indent: int = 0) -> str:
        return_string = " "*indent
        return_string += "<stringConstant>"
        return_string += " " + line[1:-1] + " "
        return_string += "</stringConstant>\r\n"
        return return_string

    def write_Keyword(self, line, indent: int = 0) -> str:
        return_string = " "*indent
        return_string +=  "<keyword>"
        return_string += " " + line + " "
        return_string += "</keyword>\r\n"
        return return_string

    def write_Symbol(self, line, indent: int = 0) -> str:
        return_string = " "*indent
        return_string +=  "<symbol>"
        if line == "<":
            return_string += " &lt; "
        elif line == ">":
            return_string += " &gt; "
        elif line == "&":
            return_string += " &amp; "
        elif line == '"':
            return_string += " &quot; "
        else:
            return_string += " " + line + " "
        return_string += "</symbol>\r\n"
        return return_string

    def write_Int(self, line, indent: int = 0) -> str:
        return_string = " "*indent
        return_string +=  "<integerConstant>"
        return_string += " " + line + " "
        return_string += "</integerConstant>\r\n"
        return return_string

    def write_Identifier(self, line, indent: int = 0) -> str:
        return_string = " "*indent
        return_string += "<identifier>"
        return_string += " " + line + " "
        return_string += "</identifier>\r\n"
        return return_string


    def print_current_item(self)->bool:
        """
        prints current item to the output file
        """
        
        # return false if the output file is not open
        if self.output_file_open == False:
            return False

        line = self.current_token
        if self.current_token_type == tokenType.STRING_CONST:   # if a token start and ends with a " it is a stringContant
            self.output_file.write(self.write_StringConstant(line))
        elif self.current_token_type == tokenType.KEYWORD:      # if a token is in the key words list
            self.output_file.write(self.write_Keyword(line))
        elif self.current_token_type == tokenType.SYMBOL:
            self.output_file.write(self.write_Symbol(line))
        elif self.current_token_type == tokenType.INT_CONST:    # if token as string could be a standalone number, it is an integer constant
            self.output_file.write(self.write_Int(line))
        elif self.current_token_type == tokenType.IDENTIFIER:
            self.output_file.write(self.write_Identifier(line))

        return True 
        

    def output_file(self):
        """
        loop thrugh all items and print to output file 
        """
        # open output file and add first tag
        self.open_file_for_output()
        self.output_file.write("<tokens>\r\n")
        
        while self.has_more_tokens:
            self.advance()
            self.print_current_item()


        # close output file and add close tag
        self.output_file.write("</tokens>\r\n")
        self.output_file.close()

    def clear_loaded_data(self):

        # clear text
        self.file_processed = False
        self.loaded_list = []
        self.output_file_name = ""
        self.file_name = ""
    
    def trim_single_line_comments(self, line:str)->str:
        """
        Check if there is a // in the string, and return everything to the left of it 
        """
        return line.split('//')[0]

    def replace_string_literals(self, line:str)->str:
        """
        Simple process to loop through a line, and if there is a string literal it, it is replaced with '[int]_stringL'
        Mutliple String Literals can be added to mapping list from one line
        """
        i: int = 0
        while i < len(line):
            if line[i] == '"':
                startRef = i
                endRef = len(line)  # Default to assume that the string ends at the end of the line
                for i in range(i+1, len(line)):
                    if line[i] == '"':
                        endRef = i + 1
                        break
                # Set outer while loop value of i to the last value of the string
                i = endRef
                # Find the value of the string
                string_value = line[startRef: endRef]
                string_literal_name = str(self.string_literal_counter) + "_string_literal"
                # Add values to the string mapping list and increment counter
                self.string_mappings.append(string_value)
                self.string_literal_counter += 1
                # Replace value of the strign literal in the original line
                line = line.replace(string_value, string_literal_name)
                continue
            i += 1

        return line


    def remove_multi_line_comments(self)->None:
        """
        clean up multiline comments marked with /* as opening and */ as closing
        """
        delList = []
        # run through loaded_list and identify areas of multi-line comments
        for i in range(len(self.loaded_list)-1):
            if self.loaded_list[i] == "/" and self.loaded_list[i+1] == "*":
                # we have found the start of the multuline comment
                startRef = i
                endRef = len(self.loaded_list) # default end of file unless we find a */
                for i in range(i + 1, len(self.loaded_list)-1):
                    if self.loaded_list[i] == "*" and self.loaded_list[i+1] == "/":
                        endRef = i + 1
                        break
                
                delList.append([startRef, endRef])
                

        #run back through delList to remove entries between the multi line comments
        for i in reversed(range(len(delList))):
            startRef = delList[i][0]
            endRef = delList[i][1]
            del self.loaded_list[startRef:endRef+1]

    def return_string_literals(self):
        """
        Run through the final data and return the string literals
        """
        for x in range(len(self.loaded_list)):
            line = self.loaded_list[x]
            if line[-15:] == "_string_literal":
                strPos = line[0:-15]
                intPos: int = int(strPos)
                self.loaded_list[x] = self.string_mappings[intPos][0:]

def main(file_or_directory_name: str):

    fileList = fl.list_of_valid_files(file_or_directory_name, "jack")
    tk = []

    if len(fileList) ==  0:
        print("No files valid files found, exiting without executing")
        return

    for file in fileList:
        jToken = JackTokenizer(file)
        jToken.load_file()
        jToken.output_file()
        jToken.clear_loaded_data()
        tk.append(jToken.output_file_name)
        
    for tokens in tk:
       # print(tokens)
       pass

    return



if __name__ == "__main__":
    cwd = os.getcwd()
    main(cwd + "/Test Folder")