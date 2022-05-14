import requests
from bs4 import BeautifulSoup

# Define secured creditor claim

class secureddebtclaim:
    def __init__(self, name, amount, value, currentpayment, arrears, planrate, ninetenstatus):
        self.name = str(name)
        self.amount = float(amount)
        self.value = float(value)
        self.currentpayment = float(currentpayment)
        self.arrears = float(arrears)
        self.planrate = float(planrate)
        self.ninetenstatus = str(ninetenstatus)

# Preliminary global variable instantiation and setting

abovemedian = str("False")
commitmentperiod = int(36)
medianincome = float(0)
disposableincome = float(0)
firstmortgage = secureddebtclaim(None, 0, 0, 0, 0, 0, "N")
secondmortgage = secureddebtclaim(None, 0, 0, 0, 0, 0, "N")
housevalue = float(0)
car1 = secureddebtclaim(None, 0, 0, 0, 0, 0, "N")
car2 = secureddebtclaim(None, 0, 0, 0, 0, 0, "N")

# Input gathering

county = str(input("Enter county of residence: "))
householdsize = int(input("Enter household size: "))
currentmonthlyincome = float(input("Enter current monthly income (Line 15b, Form 122C-1): $ "))
housequery = str(input("Is there a house? (Y or N): "))

if housequery == "Y":
    housevalue = float(input("Enter value of house: $ "))
    firstmortgagequery = str(input("Is there a first mortgage? (Y or N): "))
    if firstmortgagequery == "Y":
        firstmortgage.name = str(input("Enter name of first mortgage creditor: "))
        firstmortgage.amount = float(input("Enter total amount owed on first mortgage: $ "))
        firstmortgage.value = housevalue
        firstmortgage.currentpayment = float(input("Enter amount of regular monthly PITI payment: $ "))
        firstmortgage.arrears = float(input("Enter total amount of arrears: $ "))
        secondmortgagequery = str(input("Is there a second mortgage? (Y or N): "))
        if secondmortgagequery == "Y":
            secondmortgage.name = str(input("Enter name of second mortgage creditor: "))
            secondmortgage.amount = float(input("Enter total amount owed on second mortgage: $ "))
            secondmortgage.value = housevalue - firstmortgage.value
            if secondmortgage.value < 0:
                secondmortgage.value = 0
            secondmortgage.currentpayment = float(input("Enter amount of regular monthly payment: $ "))
            secondmortgage.arrears = float(input("Enter total amount of arrears: $ "))
        else:
            secondmortgage.amount = 0
            secondmortgage.currentpayment = 0
    else:
        firstmortgage.amount = 0
        firstmortgage.currentpayment = 0
        secondmortgagequery = str(input("Is there a HELOC? (Y or N): "))
        if secondmortgagequery == "Y":
            secondmortgage.name = str(input("Enter name of HELOC creditor: "))
            secondmortgage.amount = float(input("Enter total amount owed on HELOC: $ "))
            secondmortgage.value = housevalue
            if secondmortgage.value < 0:
                secondmortgage.value = 0
            secondmortgage.currentpayment = float(input("Enter amount of regular HELOC payment: $ "))
            secondmortgage.arrears = float(input("Enter total amount of HELOC arrears: $ "))
        else:
            firstmortgage.amount = 0
            firstmortgage.currentpayment = 0
            secondmortgage.amount = 0
            secondmortgage.currentpayment = 0
else:
    firstmortgage.amount = 0
    firstmortgage.currentpayment = 0
    secondmortgage.amount = 0
    secondmortgage.currentpayment = 0

carclaimquery = int(input("How many cars with liens are there? (0, 1, or 2): "))

if carclaimquery > 0:
    car1.name = str(input("Enter the name of Car #1 creditor: "))
    car1.amount = float(input("Enter the total amount owed on Car #1: $ "))
    car1.value = float(input("Enter the value of Car #1: $ "))
    car1.currentpayment = float(input("Enter amount of regular monthly payment on Car #1: $ "))
    car1.planrate = 0.0525
    car1.ninetenstatus = str(input("Is this a 910 car claim? (Y or N): "))
    if carclaimquery > 1:
        car2.name = str(input("Enter the name of Car #2 creditor: "))
        car2.amount = float(input("Enter the total amount owed on Car #2: $ "))
        car2.value = float(input("Enter the value of Car #2: $ "))
        car2.currentpayment = float(input("Enter amount of regular monthly payment on Car #2: $ "))
        car2.planrate = 0.0525
        car2.ninetenstatus = str(input("Is this a 910 car claim? (Y or N): "))

carownedquery = int(input("How many cars without liens are there?: "))

pmsiclaimsquery = int(input("Enter the total number of PMSI or other lien claims: "))
pmsiclaimslist = []
for claim in range(pmsiclaimsquery):
    creditorname = str(input("Enter name of creditor: "))
    creditoramount = float(input("Enter total amount of claim: $ "))
    creditorvalue = float(input("Enter value of collateral securing claim: $ "))
    creditorcurrentpayment = float(input("Enter the current amount of the monthly payment, if any: $ "))
    creditorarrears = float(input("Enter the current amount of arrears on the claim: $ "))
    creditorplanrate = float(input("Enter the amount of interest to pay for this claim under plan: "))
    creditorninetenstatus = "N"
    claim = secureddebtclaim(creditorname, creditoramount, creditorvalue, creditorcurrentpayment,
                             creditorarrears, creditorplanrate, creditorninetenstatus)
    pmsiclaimslist.append(claim)

unsecuredpriorityclaimsquery = int(input("Enter number of priority claims: "))
unsecuredprioritysclaimslist = []
for claim in range(unsecuredpriorityclaimsquery):
    creditorname = str(input("Enter name of priority creditor: "))
    creditoramount = float(input("Enter total amount of priority claim: $ "))
    unsecuredprioritysclaimslist.append(claim)

income = float(input("Enter total income from Schedule I, Line 12: $ "))
expenses = float(input("Enter total expenses from Schedule J, Line 22C: $ "))

chapter7dividend = float(input("Enter total amount of hypothetical distribution in Chapter 7 case: $ "))
toydividend = float(input("Enter total amount of toy dividend to be distributed pro rata: $ "))

# Function that defines the short-form means test logic

def form122c1():
    global medianincome, abovemedian, householdsize, currentmonthlyincome
    georgia0 = [None, float(55600), float(71504), float(79980), float(96622)]

    if householdsize <= 4:
        medianincome = georgia0[householdsize]
    elif householdsize > 4:
        medianincome = georgia0[4] + (9900 * (householdsize - 4))

    currentmonthlyincomecompare = float(currentmonthlyincome) * float(12)

    if currentmonthlyincomecompare > medianincome:
        abovemedian = "True"

# Function that defines the extra means test logic if debtor(s) is/are "above median"

def form122c2():
    global abovemedian, commitmentperiod, disposableincome, firstmortgage, secondmortgage, housevalue, car1, car2, householdsize, currentmonthlyincome
    commitmentperiod = int(60)
    meanstestdeductions = float(0)
    foodclothingandother = float(0)
    oophealthcare = int(0)
    housholdunder65 = int(input("Enter number of household members under 65: "))
    householdover65 = int(input("Enter number of household members over 65: "))
    currentmonthlytaxes = float(input("Enter current amount of monthly taxes paid: $ "))
    taxrefund = float(input("Enter expected tax refund: $ "))
    involuntarydeductions = float(input("Enter monthly amount of involuntary payroll deductions: $ "))
    lifeinsurance = float(input("Enter monthly amount of life insurance premiums: $ "))
    courtorderedpayments = float(input("Enter monthly amount of court-ordered child support and/or alimony: $ "))
    education = float(input("Enter monthly amount of education expenses: $ "))
    childcare = float(input("Enter monthly amount of childcare expenses: $ "))
    healthcare = float(input("Enter monthly amount of additional healthcare expenses: $ "))
    telephone = float(input("Enter monthly amount of telephone expenses: $ "))
    insurance = float(input("Enter monthly amount total of health insurance, disability insurance, and HSA contributions: $ "))
    familycare = float(input("Enter monthly amount of care for chronically ill family members: $ "))
    familyviolence = float(input("Enter monthly amount of family violence protection expenses: $ "))
    homeenergycosts = float(input("Enter monthly amount of additional home energy costs: $ "))
    minoreducation = float(input("Enter monthly amount for minor education: $ "))
    additionalfoodandclothing = float(input("Enter monthly amount for additional food and clothing: $ "))
    charitablecontributions = float(input("Enter monthly amount of charitable contributions: $ "))
    childsupport = float(input("Enter total amount received for child support each month: $ "))
    retirementcontributions = float(input("Enter amount of monthly retirement contributions + loan repayments: $ "))

    georgia1 = [None, float(785), float(1410), float(1610), float(1900)]
    if householdsize <= 4:
        foodclothingandother = georgia1[householdsize]
    elif householdsize > 4:
        foodclothingandother = georgia1[4] + (344 * (householdsize - 4))

    meanstestdeductions += foodclothingandother

    oophealthcare += (housholdunder65 * 75) + (householdover65 * 153)

    meanstestdeductions += float(oophealthcare)

    r0 = requests.get('https://www.justice.gov/ust/eo/bapcpa/20220515/bci_data/housing_charts/irs_housing_charts_GA.htm')
    r1 = r0.text
    soup3 = BeautifulSoup(r1, 'html.parser')
    housingoperating0 = soup3.find("td", class_="hctablecellleft", string=county)
    housingoperating1 = housingoperating0.find_next_siblings("td")
    housingoperating1person = float(str(housingoperating1[1].string.extract()).replace("$", "").replace(",", ""))
    housingoperating2people = float(str(housingoperating1[3].string.extract()).replace("$", "").replace(",", ""))
    housingoperating3people = float(str(housingoperating1[5].string.extract()).replace("$", "").replace(",", ""))
    housingoperating4people = float(str(housingoperating1[7].string.extract()).replace("$", "").replace(",", ""))
    housingoperating5people = float(str(housingoperating1[9].string.extract()).replace("$", "").replace(",", ""))
    housingmortgageandrent1person = float(str(housingoperating1[2].string.extract()).replace("$", "").replace(",", ""))
    housingmortgageandrent2people = float(str(housingoperating1[4].string.extract()).replace("$", "").replace(",", ""))
    housingmortgageandrent3people = float(str(housingoperating1[6].string.extract()).replace("$", "").replace(",", ""))
    housingmortgageandrent4people = float(str(housingoperating1[8].string.extract()).replace("$", "").replace(",", ""))
    housingmortgageandrent5people = float(str(housingoperating1[10].string.extract()).replace("$", "").replace(",", ""))
    claimedmortgage1person = housingmortgageandrent1person - firstmortgage.currentpayment - secondmortgage.currentpayment
    claimedmortgage2people = housingmortgageandrent2people - firstmortgage.currentpayment - secondmortgage.currentpayment
    claimedmortgage3people = housingmortgageandrent3people - firstmortgage.currentpayment - secondmortgage.currentpayment
    claimedmortgage4people = housingmortgageandrent4people - firstmortgage.currentpayment - secondmortgage.currentpayment
    claimedmortgage5people = housingmortgageandrent5people - firstmortgage.currentpayment - secondmortgage.currentpayment
    if householdsize == 1:
        meanstestdeductions += (claimedmortgage1person + housingoperating1person)
    elif householdsize == 2:
        meanstestdeductions += (claimedmortgage2people + housingoperating2people)
    elif householdsize == 3:
        meanstestdeductions += (claimedmortgage3people + housingoperating3people)
    elif householdsize == 4:
        meanstestdeductions += (claimedmortgage4people + housingoperating4people)
    elif householdsize >= 5:
        meanstestdeductions += (claimedmortgage5people + housingoperating5people)

    if carclaimquery or carownedquery == 1:
        if county == "Butts County" or "Jasper County" or "Lamar County" or "Morgan County" or "Walton County":
            meanstestdeductions += 320
        else:
            meanstestdeductions += 242
    elif carclaimquery or carownedquery == 2:
        if county == "Butts County" or "Jasper County" or "Lamar County" or "Morgan County" or "Walton County":
            meanstestdeductions += 640
        else:
            meanstestdeductions += 584
    if carclaimquery or carownedquery == 1:
        claimedcar1 = float(533) - car1.currentpayment
        if claimedcar1 < 0:
            claimedcar1 = 0
        meanstestdeductions += claimedcar1
    if carclaimquery or carownedquery == 2:
        claimedcar1 = float(588) - car1.currentpayment
        if claimedcar1 < 0:
            claimedcar1 = 0
        claimedcar2 = float(588) - car2.currentpayment
        if claimedcar2 < 0:
            claimedcar2 = 0
        meanstestdeductions += (claimedcar1 + claimedcar2)

    claimedtaxes = currentmonthlytaxes - (taxrefund / 12)
    meanstestdeductions += claimedtaxes

    meanstestdeductions += (involuntarydeductions + lifeinsurance + courtorderedpayments + education + childcare +
                            healthcare + telephone + insurance + familycare + familyviolence + homeenergycosts +
                            minoreducation + additionalfoodandclothing + charitablecontributions)

    secureddebtpayments = (firstmortgage.currentpayment + secondmortgage.currentpayment + (car1.amount / 60) +
                           (car2.amount / 60))
    for claim in pmsiclaimslist:
        secureddebtpayments += (claim.amount / 60) + (claim.arrears / 60)

    meanstestdeductions += secureddebtpayments

    priorityclaimpayments = float(0)
    for claim in unsecuredprioritysclaimslist:
        priorityclaimpayments += (claim.amount / 60)

    meanstestdeductions += priorityclaimpayments

    projectedadminexpense = (income - expenses) * 0.06

    meanstestdeductions += (projectedadminexpense + childsupport + retirementcontributions)

    disposableincome = float(currentmonthlyincome) - float(meanstestdeductions)

    if disposableincome < 0:
        disposableincome = 0

# Description: Function that defines the plan logic

def plan():
    global abovemedian, commitmentperiod, firstmortgage, secondmortgage, car1, car2, pmsiclaimslist, unsecuredprioritysclaimslist, disposableincome
    monthlycost = float(0)
    car1planpayment = float(0)
    car2planpayment = float(0)
    param0dividend = float(0)
    param1dividend = float(0)
    param2dividend = float(0)
    param3dividend = float(0)

    monthlycost += (firstmortgage.currentpayment + (firstmortgage.arrears / float(commitmentperiod)) +
                    secondmortgage.currentpayment + (secondmortgage.arrears / float(commitmentperiod)))

    if car1.amount != 0:
        if car1.ninetenstatus == "Y":
            car1.amount = car1.value

        car1planpayment = (car1.planrate * car1.amount) / (
                12.0 * (1.0 - (1.0 + (car1.planrate / 12.0)) ** (-1.0 * float(commitmentperiod))))

    if car2.amount != 0:
        if car2.ninetenstatus == "Y":
            car2.amount = car2.value

        car2planpayment = (car2.planrate * car2.amount) / (
                12.0 * (1.0 - (1.0 + (car2.planrate / 12.0)) ** (-1.0 * float(commitmentperiod))))

    monthlycost += car1planpayment + car2planpayment

    for claim in pmsiclaimslist:
        monthlycost += (claim.planrate * claim.amount) / (
                12.0 * (1.0 - (1.0 + (claim.planrate / 12.0))**(-1.0 * float(commitmentperiod))))

    for claim in unsecuredprioritysclaimslist:
        monthlycost += (claim.amount / float(commitmentperiod))

    if abovemedian == "True":
        param1dividend = float(disposableincome) * float(60)
    if chapter7dividend > 0:
        param2dividend = chapter7dividend
    if toydividend > 0:
        param3dividend = toydividend

    param0dividend = max(param1dividend, param2dividend, param3dividend) / float(60)

    monthlycost += param0dividend

    monthlycost += 100

    monthlycost += (monthlycost * 0.08)

    print("Monthly Cost: $", round(monthlycost, 2))

    if commitmentperiod != 60:

        rerun = str(input("Do you want to rerun the calculation with a different commitment period? (Y or N): "))

        if rerun == "Y":
            commitmentperiod = int(input("Enter new commitment period: "))
            plan()
        elif rerun == "N":
            quit()
    else:
        quit()

# Actual program starts here:

form122c1()

if abovemedian == "True":
    print("Case is ABOVE MEDIAN.")
    form122c2()
    plan()
elif abovemedian == "False":
    print("Case is BELOW MEDIAN.")
    plan()








