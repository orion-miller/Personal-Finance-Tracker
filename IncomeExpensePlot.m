function IncomeExpensePlot(app)

Months = 1:1:12;

cla(app.Balance_Axes)
hold(app.Balance_Axes, 'on')

plot(app.Balance_Axes, app.Data.(app.YearName)(1:12).Balances.WellsFargo)




end