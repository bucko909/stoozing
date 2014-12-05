#!/usr/bin/python
# -*- coding: utf8
from math import *

import cgi

form = cgi.FieldStorage()

months = int(form.getfirst("months", 12))
amount_per_month = int(form.getfirst("amount_per_month", 100))
interest_after_tax = float(form.getfirst("interest_after_tax", 3))
minimum_payment_abs = int(form.getfirst("minimum_payment_abs", 5))
minimum_payment_percent = float(form.getfirst("minimum_payment_percent", 1))

print "Content-type: text/html; charset=utf-8"
print "Silver: strict compliant"
print
print '''<html><head><title>Credit Card Stoozing Benefits</title></head><body><h1>Credit Card Stoozing Benefits</h1><p>This tool is meant to tell you for how long an interest-free card is better than a cashback card. Put your details below and stop using the card when the monthly earnings drop below what you can get on cashback.</p><p>For example, if you get 12-month deal, get 3%% after-tax interest, spend £100 per month and need to pay 1%% minimum each month, you'll want to switch to a 1%% cashback card after 7 months.</p><p>If you don't pay off your card in full each month, stop reading now. You will never get a good deal from a credit card.</p><p>The interest rate should be the rate on the account the money will end up in, <i>not</i> the highest rate you have.</p><h2>Tweak values</h2><form>
<input type="text" name="months" value="%i" /> &lt;-- months of interest free credit<br/>
<input type="text" name="amount_per_month" value="%i" /> &lt;-- amount you pay on your card each month<br/>
<input type="text" name="interest_after_tax" value="%0.3f" /> &lt;-- annual percentage interest you get on your savings, after tax<br/>
<input type="text" name="minimum_payment_abs" value="%i" /> &lt;-- minimum payment<br />
<input type="text" name="minimum_payment_percent" value="%0.3f" /> &lt;-- minimum percent of balance to pay<br />
<input type="submit"/>
</form>

<h2>Simulation</h2>''' % (months, amount_per_month, interest_after_tax, minimum_payment_abs, minimum_payment_percent)

monthly_interest = (1.0 + interest_after_tax/100.0) ** (1/12.0)

total_debt = 0.0

# We attribute all of the rounding due to minimums here
wasted = 0.0
earnings = 0.0
for month in range(1,months+1):
	total_debt += amount_per_month
	factor = monthly_interest ** (months - month) - 1.0
	if total_debt < minimum_payment_abs:
		wasted += total_debt * factor
		total_debt = 0.0
	elif total_debt * minimum_payment_percent/100.0 < minimum_payment_abs:
		wasted += (minimum_payment_abs - total_debt * minimum_payment_percent/100.0) * factor
		total_debt -= minimum_payment_abs
	else:
		total_debt *= (100-minimum_payment_percent)/100.0

	month_earnings_factor = factor
	remaining = 1.0
	# Subtract off everything we'l end up paying
	for i in range(month+1, months+1):
		#print "<p>", month, i, (monthly_interest ** (months - i) - 1.0), remaining, "</p>"
		month_earnings_factor -= (monthly_interest ** (months - i) - 1.0) * remaining * minimum_payment_percent / 100.0
		remaining *= (100-minimum_payment_percent)/100.0
	earnings += month_earnings_factor * amount_per_month
	print "<p>For purchases in month %i, you'll earn %i months of bank interest on up to %i%% of your spend, which is equivalent to a cashback of %0.2f%%.<br/>Debt so far is £%0.2f and eventual earnings will be £%0.2f.</p>" % (
			month,
			months-month,
			remaining * 100,
			month_earnings_factor*100,
			total_debt,
			earnings
		)

print "<p>You'll waste £%0.2f of your earnings detailed above on paying the card minimums (sorry, this isn't rolled into the above values).</p>" % (wasted,)

print "<p>Total debt will be £%0.2f, and total earnings from interest will be £%0.2f.</p>" % (total_debt, earnings)

print "</body></html>"
