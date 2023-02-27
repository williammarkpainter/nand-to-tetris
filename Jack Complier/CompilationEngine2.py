"""
    Jack Compilation Engine takes a file or directory as an input and if there are .jack files, for each file
    it calls the JackTokenizer(2) and craetes the output xml as the step for processing .jack files

    This is part of the the nand2tetris learning - Chapter 10

    author: williammarkpainter@gmail.com
    date: 8-Oct-20220
    using python-version: 3.9
"""


from tabnanny import process_tokens
import FileList as fl
from pathlib import Path
from enum import Enum
import typing
import os

from JackTokenizer2 import JackTokenizer as jt
from JackTokenizer2 import tokenType as tt


class CompliationEngine():
    tokenizer: jt
    file_name: str = ""
    output_file_name: str = ""
    output_file: typing.TextIO
    output_file_open: bool = False

    currentIndent: int = 0          # supports formatting output file
    classLevel: bool = False   # differentiates between class and function level variables        

    def __init__(self, filename):
        self.file_name = filename
        file_extension = Path(filename).suffix
        self.output_file_name = filename[:-len(file_extension)] + ".xml"
        self.loaded_list = []
        self.tokenizer = jt(filename)
        self.tokenizer.load_file()

    def __del__(self):
        if self.output_file_open:
            self.output_file.close()
    
    def open_output_file(self):
        """
        Open the outfile for writing
        """
        self.output_file = open(self.output_file_name, "w")
        self.output_file_open = True

    def CompileClass(self):
        """
        Set information for Class, then run through the the structure of a class
        """
        #opening class tag
        self.output_file.write(" "*self.currentIndent + "<class>\r\n")
        self.currentIndent += 2     # increase indent

        self.output_file.write(self.tokenizer.write_Keyword(self.tokenizer.current_token,self.currentIndent))
        self.tokenizer.advance()

        self.classLevel = True      #   setting for class lel var dec

        # loop through tokens till a "}" is encountered

        while self.tokenizer.current_token != "}":
            self.process_token()
        self.process_token()    # process the final symbol "}"

        self.currentIndent -= 2     # decrease indent
        self.output_file.write(" "*self.currentIndent + "</class>\r\n")    # close class tag

    def CompileClassVarDec(self):

        #opening classVarDec tag
        self.output_file.write(" "*self.currentIndent + "<classVarDec>\r\n")
        self.currentIndent += 2     # increase indent

        self.output_file.write(self.tokenizer.write_Keyword(self.tokenizer.current_token,self.currentIndent))
        self.tokenizer.advance()

        # loop through tokens till a ";" is encountered
        
        while self.tokenizer.current_token != ";":
            self.process_token()
        self.process_token()    # process the final symbol "}"

        self.currentIndent -= 2     # decrease indent
        self.output_file.write(" "*self.currentIndent + "</classVarDec>\r\n")    # close classVarDec tag

    def CompileSubroutine(self):
        
        #opening class tag
        self.output_file.write(" "*self.currentIndent + "<subroutineDec>\r\n")
        self.currentIndent += 2     # increase indent

        self.output_file.write(self.tokenizer.write_Keyword(self.tokenizer.current_token,self.currentIndent))
        self.tokenizer.advance()

        self.classLevel = False      #   setting for non class lel var dec

        # loop through tokens till a "}" is encountered

        while self.tokenizer.current_token != "}":
            # check for start of parameter list
            if self.tokenizer.current_token == "(":
                self.process_token()    # process the ( symbol
                self.output_file.write(" "*self.currentIndent + "<parameterList>\r\n")
                self.currentIndent += 2     # increase indent
                while self.tokenizer.current_token != ")":
                    self.process_token()
                self.currentIndent -= 2     # decrease indent
                self.output_file.write(" "*self.currentIndent + "</parameterList>\r\n")
                self.process_token()    # process the ) symbol

            self.process_token()
        self.process_token()    # process the final symbol "}"

        self.currentIndent -= 2     # decrease indent
        self.output_file.write(" "*self.currentIndent + "</subroutineDec>\r\n")    # close class tag

    def compileParameterList(self):
        pass

    def compileVarDec(self):
        
        #opening varDec tag
        self.output_file.write(" "*self.currentIndent + "<varDec>\r\n")
        self.currentIndent += 2     # increase indent

        self.output_file.write(self.tokenizer.write_Keyword(self.tokenizer.current_token,self.currentIndent))
        self.tokenizer.advance()

        # loop through tokens till a ";" is encountered
        
        while self.tokenizer.current_token != ";":
            self.process_token()
        self.process_token()    # process the final symbol "}"

        self.currentIndent -= 2     # decrease indent
        self.output_file.write(" "*self.currentIndent + "</varDec>\r\n")    # close varDec tag

    def compileStatements(self):
        pass

    def compileDo(self):
        pass

    def compileLet(self):
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass

    def CompileExpression(self):
        pass

    def CompileTerm(self):
        pass

    def CompileExpressionList(self):
        pass






    def compileSection(self, sectionType:str, endIndicator:str):
        self.output_file.write(" "*self.currentIndent + "<"+sectionType+">\r\n")
        self.currentIndent += 2
        self.output_file.write(self.tokenizer.write_Keyword(self.tokenizer.current_token,self.currentIndent))
        self.tokenizer.advance()

        if sectionType == 'class':
            self.classLevel = True
        if sectionType in ['subroutineDec']:
            self.classLevel = False

        while self.tokenizer.current_token != endIndicator:
            self.process_token()
        self.process_token()

        self.currentIndent -= 2
        self.output_file.write(" "*self.currentIndent + "</"+sectionType+">\r\n")

    def processKeyword(self):

        if self.tokenizer.current_token in ['class', ]:
            self.CompileClass()
        elif self.tokenizer.current_token in ['function']:
            self.CompileSubroutine()
        elif self.tokenizer.current_token in ['if']:
            self.compileSection("ifStatement", "}")
        elif self.tokenizer.current_token in ['do']:
            self.compileSection("do", ";")
        elif self.tokenizer.current_token in ['var', 'static']:
            if self.classLevel:
                self.CompileClassVarDec()
            else:
                self.compileVarDec()
        else:
            self.output_file.write(self.tokenizer.write_Keyword(self.tokenizer.current_token,self.currentIndent))
            self.tokenizer.advance()

    def process_token(self):

        if self.tokenizer.current_token_type == tt.NONE:
            self.output_file.write("/n")
            self.tokenizer.advance()
        elif self.tokenizer.current_token_type == tt.KEYWORD:
            self.processKeyword()
        elif self.tokenizer.current_token_type == tt.SYMBOL:
            self.output_file.write(self.tokenizer.write_Symbol(self.tokenizer.current_token,self.currentIndent))
            self.tokenizer.advance()
        elif self.tokenizer.current_token_type == tt.IDENTIFIER:
            self.output_file.write(self.tokenizer.write_Identifier(self.tokenizer.current_token,self.currentIndent))
            self.tokenizer.advance()
        elif self.tokenizer.current_token_type == tt.INT_CONST:
            self.output_file.write(self.tokenizer.write_Int(self.tokenizer.current_token,self.currentIndent))
            self.tokenizer.advance()
        elif self.tokenizer.current_token_type == tt.STRING_CONST:
            self.output_file.write(self.tokenizer.write_StringConstant(self.tokenizer.current_token,self.currentIndent))
            self.tokenizer.advance()
        else:
            self.tokenizer.advance()


    def process_file(self):
        
        self.open_output_file()

        try:
            value = self.tokenizer.lookahead(250)
            print(value)
        except Exception as error:
            print(error)

        while self.tokenizer.has_more_tokens:

            self.process_token()
            

        self.output_file.close()
        self.output_file_open = False


def main(file_or_directory_name: str):

    fileList = fl.list_of_valid_files(file_or_directory_name, "jack")
    tk = []

    if len(fileList) ==  0:
        print("No files valid files found, exiting without executing")
        return

    for file in fileList:
        cEngine = CompliationEngine(file)
        cEngine.process_file()
        tk.append(cEngine.output_file_name)
        
    for tokens in tk:
       # print(tokens)
       pass

    return



if __name__ == "__main__":
    cwd = os.getcwd()
    main(cwd + "/Test Folder")

