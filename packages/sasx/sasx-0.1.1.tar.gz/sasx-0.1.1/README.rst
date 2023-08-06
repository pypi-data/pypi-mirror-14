======
 SASX
======
Data manipulation in Python for SAS users, with the %%sasx magic command.

SASX (Simple dAta SyntaX) has the best of both worlds:

- Full access to python, numpy, pandas (like Python)
- A few extra keywords to allow row-by-row operations (like SAS)

Same result, different syntax
------------------------------

SAS:
::
   data weight_loss;
      set weight;
      Percent_loss = min(current_weight - initial_weight, 0)  / initial_weight;
      keep Name Percent_loss;
   run;

SASX (Simple dAta SyntaX):
::
   %%sasx
   data weight_loss:
      set weight
      Percent_loss = min(current_weight - initial_weight, 0)  / initial_weight
      keep Name Percent_loss


Python:
::
    weight_loss = weight[['Name']].copy()
    weight_loss['Percent_loss'] = np.minimum(weight.current_weight - weight.initial_weight, 0) / weight.initial_weight

Installing
----------

Install the lastest release with:
::
	pip install sasx
