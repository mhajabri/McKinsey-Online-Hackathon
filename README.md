# McKinsey Analytics Online Hackaton (07/2018)
***

McKinsey Analytics organized multiple online hackathons on **analyticsvidhya** during this past year but this one was the biggest of them. It lasted for 72 hours and gathered more than 1000 participants. I decided to be a part of it as the problem was quite nice and wasn't only about predicitons as you will see below.


## Problem Statement

Your client is an Insurance company and they want to know how likely is paying the renewal premium for each of their clients and, consequently, how to build an incentive plan for their agents depending on the client they'll work with, e.g : if an agent is going to work with a client that will most probably pay the renewal premium, then maybe we shoudln't invest much in that one.      
All in all, the company wants to maximize the net revenue : sum(renewal - incentives given to collect the renewal).
 
You have information about past transactions from the policy holders along with their demographics. The client has provided aggregated historical transactional data like number of premiums delayed by 3/6/12 months across all the products, number of premiums paid, customer sourcing channel and customer demographics like age, monthly income and area type.
 
In addition to the information above, the client has provided the following functions :

1. Effort in hours as a function of incentive provided : 
```
Y = 10*(1 - exp(-x/400))
```
2.  % improvement in renewal probability as a function of hours of efforts by an agent effort in hours :
```
Y = 20*(1 - exp(-x/5))
```

As you can notice, beyond a certain point, the agent can't work more and the same applied to the probability improvement. 
 
Given the information, the client wants you to predict the propensity of renewal collection and create an incentive plan for agents (at policy level) to maximise the net revenues from these policies.
Online hackaton participation 

## Evaluation Criteria

Solutions were evaluated on 2 criterias:
* A. Predicted probabilities of receiving a premium on a policy without considering any incentive.
* B. Monthly incentives given to agents (for each policy) to maximize the net revenue.
 
Part A:
The probabilities predicted by the participants would be evaluated using AUC ROC score.
 
Part B:
The net revenue is calculated as follows : 

`Net Revenue on policy = (p + dp) * premium on policy - Incentive on policy`

where 
* `p` - is the renewal probability predicted using a benchmark model by the insurance company (which is also the value that you're trying to approximate from Part A)
* `dp` - (% Improvement in renewal probability*`p`) is the improvement in renewal probability calculated from the agent efforts in hours.
* `Premium on policy` is the premium paid by the policy holder for the policy in consideration.
* `Incentive on policy` is the incentive given to the agent for increasing the chance of renewal for each policy.

So as you said before, it's not only a classification problem, there's also an optimization component to find the best compromise between incentive and revenue.

Overall Ranking was based on :
 
`Combined Score = 0.7*AUC-ROC value + 0.3*(net revenue collected from all policies)*lambda`
 
where `lambda` is a normalizing factor.

## Data

| Variable 	| Definition |
| :-----------:	| :--------: |
| `id` 		| Unique ID of the policy |
| `perc_premium_paid_by_cash_credit` | Percentage of premium amount paid by cash or credit card |
| `age_in_days` | Age in days of policy holder |
| `Income` | Monthly Income of policy holder |
| `Count_3-6_months_late` | No of premiums late by 3 to 6 months |
| `Count_6-12_months_late` | No  of premiums late by 6 to 12 months |
| `Count_more_than_12_months_late` | No of premiums late by more than 12 months |
| `application_underwriting_score` | Underwriting Score of the applicant at the time of application (No applications under the score of 90 are insured) |
| `no_of_premiums_paid` | Total premiums paid on time till now |
| `sourcing_channel` | Sourcing channel for application |
| `residence_area_type` | Area type of Residence (Urban/Rural) |
| `premium` | Monthly premium amount |
| `renewal` | Policy Renewed? (0 - not renewed, 1 - renewed) |

Training data (train.csv) and test data (test.csv) are stored in `data` directory.
