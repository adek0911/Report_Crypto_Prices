# Report_Crypto_Prices
Short information about actual prices of crypto with 3 months overview.

It is a script in python that downloads current data, saves it, prepares a report (table to the reading transmitter) and sends a ready e-mail with the data.
The current price list is downloaded via the API of one of the most popular websites with current currency prices called "coingecko".
After taking over and saving the processed data in to email format and sending it using smtplib and the gmail email sending library.
The report is sent periodically via the "pythonanywhere" website where it runs as a task every day.
