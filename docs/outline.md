# /users
| method | path                          |definition                |
|--------|-------------------------------|--------------------------|
| list   |[path]/api/[version]/users     |lists all users           |
| create |[path]/api/[version]/users     |create new user           |
| get    |[path]/api/[version]/users/{id}|get specific user by id   |
| delete |[path]/api/[version]/users/{id}|delete specific user by id|
| update |[path]/api/[version]/users/{id}|update specific user by id|

# /budgets
| method | path                            |definition                    |
|--------|---------------------------------|------------------------------|
| list   |[path]/api/[version]/budgets     |lists all budgets             |
| create |[path]/api/[version]/budgets     |create new budget             |
| get    |[path]/api/[version]/budgets/{id}|get specific budget by id     |
| delete |[path]/api/[version]/budgets/{id}|delete specific budget by id  |
| update |[path]/api/[version]/budgets/{id}|update specific budget by id  |

# /categories
| method | path                                            |definition                    |
|--------|-------------------------------------------------|------------------------------|
| list   |[path]/api/[version]/budgets/{id}/categories     |lists all categories          |
| create |[path]/api/[version]/budgets/{id}/categories     |create new category           |
| get    |[path]/api/[version]/budgets/{id}/categories/{id}|get specific category by id   |
| delete |[path]/api/[version]/budgets/{id}/categories/{id}|delete specific category by id|
| update |[path]/api/[version]/budgets/{id}/categories/{id}|update specific category by id|

# /accounts
| method | path                                          |definition                   |
|--------|-----------------------------------------------|-----------------------------|
| list   |[path]/api/[version]/budgets/{id}/accounts     |lists all accounts           |
| create |[path]/api/[version]/budgets/{id}/accounts     |create new account           |
| get    |[path]/api/[version]/budgets/{id}/accounts/{id}|get specific account by id   |
| delete |[path]/api/[version]/budgets/{id}/accounts/{id}|delete specific account by id|
| update |[path]/api/[version]/budgets/{id}/accounts/{id}|delete specific account by id|

# /payees
| method | path                                        |definition                 |
|--------|---------------------------------------------|---------------------------|
| list   |[path]/api/[version]/budgets/{id}/payees     |lists all payees           |
| create |[path]/api/[version]/budgets/{id}/payees     |create new payee           |
| get    |[path]/api/[version]/budgets/{id}/payees/{id}|get specific payee by id   |
| delete |[path]/api/[version]/budgets/{id}/payees/{id}|delete specific payee by id|
| update |[path]/api/[version]/budgets/{id}/payees/{id}|update specific payee by id|

# /payeeLocations
| method | path                                                                  |definition                          |
|--------|-----------------------------------------------------------------------|------------------------------------|
| list   |[path]/api/[version]/budgets/{id}/payees/{payee_id}/payeeLocations     |lists all payee locations           |
| create |[path]/api/[version]/budgets/{id}/payees/{payee_id}/payeeLocations     |create new payee location           |
| get    |[path]/api/[version]/budgets/{id}/payees/{payee_id}/payeeLocations/{id}|get specific payee location by id   |
| delete |[path]/api/[version]/budgets/{id}/payees/{payee_id}/payeeLocations/{id}|delete specific payee location by id|
| update |[path]/api/[version]/budgets/{id}/payees/{payee_id}/payeeLocations/{id}|update specific payee location by id|

# /transactions
| method | path                                              |definition                       |
|--------|---------------------------------------------------|---------------------------------|
| list   |[path]/api/[version]/budgets/{id}/transactions     |lists all transactions           |
| create |[path]/api/[version]/budgets/{id}/transactions     |create new transaction           |
| get    |[path]/api/[version]/budgets/{id}/transactions/{id}|get specific transaction by id   |
| delete |[path]/api/[version]/budgets/{id}/transactions/{id}|delete specific transaction by id|
| update |[path]/api/[version]/budgets/{id}/transactions/{id}|update specific transaction by id|