function EXP = ExpensesReader(app)
%Reads in .csv expense sheets from bank, and returns to expenses_lists field
%of data struct

cd('D:\!Orion_Programs\!Source_Controlled\Finances\Expense_Sheets')
[FileNames, FilePath] = uigetfile('*.csv','Select Expense Spreadsheets','MultiSelect','on');

try
    cd(FilePath)
catch
    EXP = [];
    return
end

EXP = [];

for iFiles = 1:length(FileNames)    
    TempStruct = table2struct(readtable(FileNames{iFiles}));
    
    for iLines = 1:length(TempStruct)
        Idx = length(EXP)+1;

        if contains(TempStruct(iLines).Var5,{'Reverb','amazon','ebay','AMAZON','Amzn'})
            EXP(Idx).Type = 'Other';
        elseif contains(TempStruct(iLines).Var5,{'Wren Northlake','Mint','Duke','ENERGY','Anytime'})
            EXP(Idx).Type = 'Bills';            
        elseif contains(TempStruct(iLines).Var5,{'GEICO','FIRESTONE','MARATHON PETRO'})
            EXP(Idx).Type = 'Car';    
        elseif contains(TempStruct(iLines).Var5,{'ROBINHOOD','PAYPAL','Secured Card','SECURED CARD'})
            EXP(Idx).Type = 'Transfer';   
        elseif contains(TempStruct(iLines).Var5,{'VERDE','PUBLIX','CHICK-FIL-A','HARRIS TE','TARGET','5GUYS'})
            EXP(Idx).Type = 'Food';              
        else
            EXP(Idx).Type = '-';            
        end
        
        EXP(Idx).Amount = TempStruct(iLines).Var2;
        EXP(Idx).Description = TempStruct(iLines).Var5;     
    end    
end