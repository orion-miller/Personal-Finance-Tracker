function IncomeExpensePlot(app)

Months = 1:1:12;

AX = app.IncExp_Axes;
cla(AX)
hold(AX, 'on')

Incomes = [];
Incomes.Job = [];
Incomes.Other = [];

Expenses = [];
Expenses.Bills = []; %Rent plus any other bills
Expenses.Food = [];
Expenses.Car = [];      
Expenses.Transfers = [];    
Expenses.WorkTravel = [];     
Expenses.Other = []; 

for iMonths = 1:12
    Incomes.Job = [Incomes.Job, app.Data.(app.YearName)(iMonths).Incomes.Job];
    Incomes.Other = [Incomes.Other, app.Data.(app.YearName)(iMonths).Incomes.Other];
    
    Expenses.Bills = [Expenses.Bills, app.Data.(app.YearName)(iMonths).Expenses.Bills];
    Expenses.Food = [Expenses.Food, app.Data.(app.YearName)(iMonths).Expenses.Food];
    Expenses.Car = [Expenses.Car, app.Data.(app.YearName)(iMonths).Expenses.Car];    
    Expenses.Transfers = [Expenses.Transfers, app.Data.(app.YearName)(iMonths).Expenses.Transfers];    
    Expenses.WorkTravel = [Expenses.WorkTravel, app.Data.(app.YearName)(iMonths).Expenses.WorkTravel];    
    Expenses.Other = [Expenses.Other, app.Data.(app.YearName)(iMonths).Expenses.Other];        
end

%% INCOME AND EXPENSE PLOT
%Plot Incomes and Expense
plot(AX, Months, Incomes.Job, 'Color',[1,1,1], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')
plot(AX, Months, Incomes.Other, 'Color',[0.74,0.08,0.20], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')

plot(AX, Months, Expenses.Bills, 'Color',[0.07,0.62,1.00], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')
plot(AX, Months, Expenses.Food, 'Color',[0.00,1.00,0.53], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')
plot(AX, Months, Expenses.Car, 'Color',[0.72,0.27,1.00], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')
plot(AX, Months, Expenses.Transfers, 'Color',[1.00,0.60,0.16], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')
plot(AX, Months, Expenses.WorkTravel, 'Color',[0.74,0.65,0.49], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')
plot(AX, Months, Expenses.Other, 'Color',[1.00,0.00,0.00], 'LineWidth',1.5, 'LineStyle','-', 'Marker','o')

%Axes props
AX.XAxis.Exponent = 0;
AX.YAxis.Exponent = 0;
AX.XGrid = 'on';
AX.YGrid = 'on';
AX.Title.Color = [1 1 1];
AX.Title.String = 'Balances by Month';

%Legend
legend(AX,'Incomes.Job','Incomes.Other','Expenses.Bills','Expenses.Food','Expenses.Car','Expenses.Transfers','Expenses.WorkTravel','Expenses.Other');
AX.Legend.Color = [0.15 0.15 0.15];
AX.Legend.EdgeColor = [1 1 1];
AX.Legend.TextColor = [1 1 1];
AX.Legend.Location = 'northwest';


%% INCOME PIE PLOT
AX2 = app.IncPie_Axes;
cla(AX2)
hold(AX2, 'on')

IncX = [Incomes.Job(app.Month) Incomes.Other(app.Month)];

pie(AX2, IncX)

%Axes props
% AX.XAxis.Exponent = 0;
% AX.YAxis.Exponent = 0;
% AX.XGrid = 'on';
% AX.YGrid = 'on';
AX.Title.Color = [1 1 1];
AX.Title.String = 'Income Breakdown';

%% EXPENSE PIE PLOT
AX3 = app.ExpPie_Axes;
cla(AX3)
hold(AX3, 'on')

ExpX = [Expenses.Bills(app.Month),Expenses.Food(app.Month),Expenses.Car(app.Month),Expenses.Transfers(app.Month),Expenses.WorkTravel(app.Month),Expenses.Other(app.Month)];

pie(AX3, abs(ExpX))

%Axes props
% AX.XAxis.Exponent = 0;
% AX.YAxis.Exponent = 0;
% AX.XGrid = 'on';
% AX.YGrid = 'on';
AX3.Title.Color = [1 1 1];
AX3.Title.String = 'Expense Breakdown';

end