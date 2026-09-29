# ElectricBuddy
IT is an Electricity Bill calculator 



Features: 

Priority	Feature
Must have	Register and login (JWT), each user sees only their own data
	Tariff plan with slabs, stored in the database (seeded with one real plan)
	Add a bill: month, units (or previous and current meter readings), optional actual amount
	Slab-wise breakdown and estimated total for each bill
	Bill history list, with edit and delete

Should have	Charts: units per month and rupees per month
	Bill check: estimate vs actual amount, with the difference highlighted
	Trends: change from last month (%), highest month, lowest month, average
	What-if calculator: "if I use X units, what's my bill?"
	Fixed charge and tax settings
	Validation: no duplicate month, units never negative, current reading not below previous

Nice to have	Next-month projection from past bills
	CSV export
	Budget alert when the estimate crosses a limit
	PDF upload, then photo upload with OCR (only after everything else is deployed)