- Sentiment Analysis
- Content Classification - Text to test needs to be at LEAST 20 words long. Anything shorter and the program will throw an error.
- Entities Analysis
- Entity Sentiment Analysis
- Syntax Analysis


There are two methods for analysis:
- Bulk URL Check ~ Meaning a list of URLs can be run and analyzed in succession.
- Direct Check ~ Meaning that content is copied from a webpage/or custom written and only this content is analyzed.

The two files that need to be created locally to pull URLs/content from:
- Bulk URL Check ~ 'gnl-bulk-check.txt'
- Direct Check ~ 'gnl-direct-check.txt'

*NOTE* ~ The bulk url check option does not support the 'Syntax Analysis' test because it would be very unwieldy if analyzing many URLs. I've instead relegated this analysis to just the direct check option.