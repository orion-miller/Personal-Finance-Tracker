
%Creates the initial struct to hold all the finances info. Should only be
%made once.

clc
clearvars
cd('D:\!Orion_Programs\!Source_Controlled\Finances')

Data = [];
Data.Y2020 = [];
Data.Y2021 = [];
Data.Y2022 = [];
Data.Y2023 = [];
Data.Y2024 = [];
Data.Y2025 = [];

for iYear = 1:6
    switch iYear
        case 1
            YearName = 'Y2020';           
        case 2
            YearName = 'Y2021';            
        case 3
            YearName = 'Y2022';           
        case 4
            YearName = 'Y2023';           
        case 5
            YearName = 'Y2024';            
        case 6
            YearName = 'Y2025';            
    end

for iMonth = 1:12
    Data.(YearName)(iMonth).Balances = [];    
    Data.(YearName)(iMonth).Balance_Deltas = [];
    Data.(YearName)(iMonth).Incomes = [];    
    Data.(YearName)(iMonth).Expenses = [];
    Data.(YearName)(iMonth).Expenses_Lists = [];    
    Data.(YearName)(iMonth).Notes = {''};
    
    Data.(YearName)(iMonth).Balances.WellsFargo = 0;
    Data.(YearName)(iMonth).Balances.RobinHood = 0;
    Data.(YearName)(iMonth).Balances.Assets = 0;    
    Data.(YearName)(iMonth).Balances.FinnCU = 0; 
    Data.(YearName)(iMonth).Balances.PayPal = 0;     
    Data.(YearName)(iMonth).Balances.NSLSC = 0;    
    
    Data.(YearName)(iMonth).Incomes.Job = 0;    
    Data.(YearName)(iMonth).Incomes.Other = 0;     
      
    Data.(YearName)(iMonth).Expenses.Bills = 0; %Rent plus any other bills
    Data.(YearName)(iMonth).Expenses.Food = 0;
    Data.(YearName)(iMonth).Expenses.Car = 0;      
    Data.(YearName)(iMonth).Expenses.Transfers = 0;    
    Data.(YearName)(iMonth).Expenses.WorkTravel = 0;     
    Data.(YearName)(iMonth).Expenses.Other = 0;     
end
end

save('OM_Finance_Data','Data');
disp('Data Saved.')