# Little-Snitch---Rule-Groups
This repo provide rule groups for Little Snitch based on unified host list to block ads, malware, fake news and porn

Python script will convert the unified host files provided and maintained by the great team and members at https://github.com/StevenBlack/hosts to the .lsrules files which can be directly subscribed in Little Snitch V4.1
as of now each rule group can hold maximum of 10,000 (rules, domain, hosts) script split the unified host file multiple small files each contains maximum of 10,000 rules to comply with Little Snitch limitation.

## Change log V2:
In this new version of [Rule-GroupsV2](https://rulegroups.com "Litle Snitch Rule-Groups") . I heard all the opinions and wrote everythng from scratch to make it moduler. Now lists are separated by source and respective category. It will make a singe list much smaller and easier to handle by rule manager in little snitch. Do check the page and subscribe to the rulegroups with just a click.  

## Change log V1.3:
As of Little Snitch 4.3 (5264) max domains per rule increased to 200,000. there is no need to create multiple rule group files with the previous limit of 10,000 rules per rule group. This version will generate single file in respective folder with the same name for easy subscription and management.
Still maintain and auto update old rules for a while.

## Change log V1.2:
Solve issue caused by inline comments in original hosts files.

Added functionality to convert all list in their respective folders.

List will be automatically updated on weekly basis.
