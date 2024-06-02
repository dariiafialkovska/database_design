## Notes

- I decided not to utilize the data from salary_survey-3 because the columns for "Annual Base Pay," "Signing Bonus," and "Annual Bonus" lacked specific currency information. Additionally, the "Additional Comments" column only occasionally mentioned currencies. Relying on this dataset could potentially introduce inaccuracies due to inconsistent currency data.

- Based on salary_survey-1, which had many different currencies, I created an exchange rate table and a function that populates and sets the exchange rates, so the compensation results were based on USD only.

- If I had more time, I would want to put my code into Docker to set up PostgreSQL and be able to run it in any environment. I also wanted to create a query based on average salaries in USD by currency, as well as queries based on education level, job level, and industry.

- While importing data from CSV 1, I noticed that some salaries were written with a dollar or other currency signs, or were written with dots or commas. So, I wrote a function that removes only special characters and uses only usable values to calculate correct results.

- Primarily, I have used location as a variable for the employee, but since CSV 1 and CSV 2 had two different location metrics and I needed to calculate the city average, I created a table for location which included city, country, and full location. Since the data in CSV 1 could not be separated into city and country, I decided to create a variable as full location.

- In config.py, I created dictionaries to connect columns to the variables, in case a new dataset is added; users can put dataset columns there and it would upload to the database.

- All strings are stored as uppercase since survey data had many different entries which are the same, so I could better connect the data.