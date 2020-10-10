
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
    Data.Y2020(iMonth).Expenses_Lists = [];    
    Data.Y2020(iMonth).Notes = {''};
    
    Data.Y2020(iMonth).Balances.WellsFargo = 0;
    Data.Y2020(iMonth).Balances.RobinHood = 0;
    Data.Y2020(iMonth).Balances.Assets = 0;    
    Data.Y2020(iMonth).Balances.FinnCU = 0; 
    Data.Y2020(iMonth).Balances.PayPal = 0;     
    Data.Y2020(iMonth).Balances.NSLSC = 0;    
    
    Data.Y2020(iMonth).Incomes.Job = 0;    
    Data.Y2020(iMonth).Incomes.Other = 0;     
      
    Data.Y2020(iMonth).Expenses.Bills = 0; %Rent plus any other bills
    Data.Y2020(iMonth).Expenses.Food = 0;
    Data.Y2020(iMonth).Expenses.Car = 0;      
    Data.Y2020(iMonth).Expenses.Transfers = 0;    
    Data.Y2020(iMonth).Expenses.WorkTravel = 0;     
    Data.Y2020(iMonth).Expenses.Other = 0;     
end

save('OM_Finance_Data','Data');
disp('Data Saved.')