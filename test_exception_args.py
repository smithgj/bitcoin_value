import traceback

sum = 0
try:
   sum = sum + "42"
except Exception as e:
    print('ouch ')
    print(e)
print('Done')
