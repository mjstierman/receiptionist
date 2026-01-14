# Receiptionist
### Track receipts and spending

> [!NOTE]
> I wrote this app for my own personal use, and build it on my own time, if and when available. If you find it useful for your needs as well, that's great!

> [!WARNING]
> Do not expect all features to be immediately available, regular updates, releases, bug fixes, etc. 

## Summary

The purpose of this app is to use data to display information in a web browser helpful to making informed decisions and achieving realistic goals with your finances.

Tracking spending and saving combined with analytics helps detect fraud and anomolies, identify problem areas, show milestones, explore scenarios, and facilitates long-term financial planning.

## Use Cases

Interfacing with the data should be simple and answer questions the user would ask. This could be in the form of visual reports, dashboards, calculators, etc.

For example:\
:coffee: "How much money did I spend on coffee in 2023?"\
:chart: "What was my net worth on 7 July 2024? Today?"\
:dollar: "If I got a new job making this salary, what would be my monthly net income?"\
:money_with_wings: "How does my monthly budget change if I pay off this loan in full?"\
:exclamation: "How much to I need to save for emergencies? How long will it take to save?"

## Interfacing

### General Use

The tool should be able to ingest CSV files to import history and data, and have an interface to manually input data. The tool should be able to attach images of receipts to records.

### Human Interface Guidelines

The app should be as simple and easy-to-use as possible, while maintaining the ability for fine-tuning based on the user's preference. 

The end user should be presented with sane defaults, and a pre-configured dashboard. 

The user should not need to know structured queries to perform searches against the database.

# Application Architecture

This application will be designed to be self-hosted as a web application. The runtimes, databases, engines, will all run locally on a user's machine. No Internet should be required for operating the app -- except in the case of the user linking to their bank account(s).

The intended use case is distribution via OCI platform -- for example Docker.

| Station | Platform |
|---------- | ------- |
| Front end | HTML/CSS/JS |
| Back end | Python Flask |
| Database | SQLite |

# Contributing

If there's a scenario or question that can't be answered with the exsting tooling, new tooling can be built. Please submit your feature request as a discussion topic.

If there's an error preventing the software from operating, please submit an Issue.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Input from data science professionals, accountants are always welcome in the discussions. 

# License

This software is licensed under:

[GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.html)

## Third Party licenses

Receiptionist uses libraries licensed under the following:

GPLv3
- [cs50](https://pypi.org/project/cs50/)

BSD 3-Clause
- [flask](https://flask.palletsprojects.com/en/stable/license/)
- [pytz](https://pypi.org/project/pytz/)

MIT
- [bootstrap](https://github.com/twbs/bootstrap/blob/main/LICENSE)