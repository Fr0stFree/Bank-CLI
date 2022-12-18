# Bank App CLI

This project is a desktop CLI App. The application allows you to keep track of deposits and
withdrawals from the bank customers' accounts.

## Installation

1. Clone the repository from GitHub:
```bash
git clone git@github.com:Fr0stFree/Bank-CLI.git
```
2. Create a virtual environment:
```bash
python3 -m venv venv
```
3. Install the dependencies when you are in the project directory:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
python3 main.py
```

## Usage
- **The client is automatically created at the first successful deposit to the account. To make a
deposit, enter a command**:
```bash
deposit --client "John Doe" --amount 100 --description "Salary"
```
<details>
<summary> Comments </summary>
<ul>
 <li>the client's name must be string not longer than 50 characters and contain at least one letter;</li>
 <li>all parameters are <u>required</u>;</li>
 <li>the amount must be a positive integer of float number;</li>
 <li>the description must be string not longer than 255 characters.</li>
</ul>
</details>

- **To make a withdrawal, enter a command**:
```bash
withdraw --client "John Doe" --amount 50 --description "Rent"
```
<details>
<summary> Comments </summary>
<ul>
 <li><u>you won't be able to make a withdrawal if the amount is greater than the balance.</u></li>
 <li>all parameters are <u>required</u>;</li>
 <li>the client's name must be string not longer than 50 characters and contain at least one letter</li>
 <li>the amount must be a positive integer of float number;</li>
 <li>the description must be string not longer than 255 characters.</li>
</ul>
</details>

- **To list all client's transactions, enter a command**:
```bash
show_bank_statement --client "John Doe" --since "2021-01-01 00:00:00" --till "2023-01-31 00:00:00"
```
<details>
<summary> Comments </summary>
<ul>
 <li><code>--since</code> and <code>--till</code> parameters are <u>optional</u>;</li>
 <li>the datetime must be in the format "YYYY-MM-DD HH:MM:SS";</li>
 <li>if the <code>--since</code> and <code>--till</code> parameters are not specified
the bank statement will be shown for the whole period.</li>
</ul>
</details>

#### Expected ouput:

|           Date           | Description | Withdrawals | Deposits | Balance |
|:------------------------:|:------------|:------------|----------|---------|
|   18.12.2022 15:44:26    | Salary      |             | 100      | 100     |
|   18.12.2022 15:44:51    | Award       |             | 25       | 125     |
|   18.12.2022 15:45:12    | Stolen      |             | 90       | 215     |
|   18.12.2022 15:47:30    | Rent        | 50          |          | 165     |


- **To <u>exit</u> the application, enter a command**:
```bash
exit
```
###### _Note that app do not save the data. All data will be lost after closing the application._
