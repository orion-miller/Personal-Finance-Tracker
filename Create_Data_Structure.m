
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
    
    Data.Y2020(iMonth).Balances.WellsFargo = nan;
    Data.Y2020(iMonth).Balances.RobinHood = nan;
    Data.Y2020(iMonth).Balances.Assets = nan;    
    Data.Y2020(iMonth).Balances.FinnCU = nan; 
    Data.Y2020(iMonth).Balances.PayPal = nan;     
    Data.Y2020(iMonth).Balances.NSLSC = nan;    
    
    Data.Y2020(iMonth).Incomes.Job = nan;    
    Data.Y2020(iMonth).Incomes.Other = nan;     
      
    Data.Y2020(iMonth).Expenses.Bills = nan; %Rent plus any other bills
    Data.Y2020(iMonth).Expenses.Food = nan;
    Data.Y2020(iMonth).Expenses.Car = nan;      
    Data.Y2020(iMonth).Expenses.Transfers = nan;    
    Data.Y2020(iMonth).Expenses.WorkTravel = nan;     
    Data.Y2020(iMonth).Expenses.Other = nan;     
end

save('OM_Finance_Data','Data');
disp('Data Saved.')