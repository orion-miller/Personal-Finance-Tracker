
%Creates the initial struct to hold all the finances info. Should only be
%made once.

clc
clearvars
cd('D:\!Orion_Programs\!Source_Controlled\Finances')

Data = [];
Data.Y2020 = [];

for iMonth = 1:12
    Data.Y2020(iMonth).Balances = [];
    Data.Y2020(iMonth).Balance_Deltas = [];
    Data.Y2020(iMonth).Incomes = [];    
    Data.Y2020(iMonth).Expenses = [];
    Data.Y2020(iMonth).Notes = {''};
end

save('OM_Finance_Data','Data');