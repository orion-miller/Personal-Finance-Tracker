function EXP = ExpensesReader(app)

cd('D:\!Orion_Programs\!Source_Controlled\Finances\Expense_Sheets')
[FileNames, FilePath] = uigetfile('*.csv','Select Expense Spreadsheets','MultiSelect','on');
% cd(FilePath)

EXP = [];

for iFiles = 1:length(FileNames)

TempTable = readtable(FileNames{iFiles});

for iLines = length(TempTable)
    
    
    
    
    
end




end