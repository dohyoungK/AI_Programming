'''201624419/KimDoHyoung/010-2399-0652'''

firstName = input("Enter first name: ")
lastName = input("Enter last name: ")
salary = float(input("Enter current salary: "))

if salary > 40000:
    salary = (salary + 2000) + ((salary-40000)/100*2)
else:
    salary += salary/100*5

salary = str(salary)
idx = salary.find('.')
while idx-3 > 0:
    salary = salary[:idx-3] + ',' + salary[idx-3:]
    idx -= 3

idx = salary.find('.')
print("New salary for {} {}: ${}{:.2f}".format(firstName, lastName, salary[:idx-3], float(salary[idx-3:])))

