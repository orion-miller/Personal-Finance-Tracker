
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
    
    Data.Y2020(iMonth).Balances.WellsFargo = [];
    Data.Y2020(iMonth).Balances.RobinHood = [];
    Data.Y2020(iMonth).Balances.Assets = [];    
    Data.Y2020(iMonth).Balances.FinnCU = []; 
    Data.Y2020(iMonth).Balances.PayPal = [];     
    Data.Y2020(iMonth).Balances.NSLSC = [];    
    
    Data.Y2020(iMonth).Incomes.Job = [];    
    Data.Y2020(iMonth).Incomes.Other = [];     
      
    Data.Y2020(iMonth).Expenses.Bills = []; %Rent plus any other bills
    Data.Y2020(iMonth).Expenses.Food = [];
    Data.Y2020(iMonth).Expenses.Car = [];      
    Data.Y2020(iMonth).Expenses.Transfers = [];    
    Data.Y2020(iMonth).Expenses.WorkTravel = [];     
    Data.Y2020(iMonth).Expenses.Other = [];    
    
    
    
end

save('OM_Finance_Data','Data');