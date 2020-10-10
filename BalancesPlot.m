function BalancesPlot(app)

Months = 1:1:12;

cla(app.Balance_Axes)
hold(app.Balance_Axes, 'on')

Balances = [];
Balances.WellsFargo = [];
Balances.RobinHood = [];
Balances.Assets = [];
Balances.FinnCU = [];
Balances.PayPal = [];
Balances.NSLSC = [];

for iMonths = 1:12
    Balances.WellsFargo = [Balances.WellsFargo, app.Data.(app.YearName)(iMonths).Balances.WellsFargo];
    
    
end

plot(app.Balance_Axes, Months, Balances.WellsFargo)




end