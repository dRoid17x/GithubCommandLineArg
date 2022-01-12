# GithubCommandLineArg

A command line tool to list 5 projects of any organization (provided as argument) which need attention by open-source contributors.
The 5 projects are decided based on, the ratio of no of open issues and no of contributors involved in the repository, let's call this as the IC ratio.

To run the tool, provide your personal access token instead of <$your-personal-access-token> at line 12.

The tool takes two arguements, 
-o or --Org followed by the name of the organization for which the tool should run.
-c or --CSV to indicate that the tool should write to a report, if this option is not used then the output is displayed directly to the command line interface.

The tool also runs on a cron job as defined below,
1. */5 * * * * /usr/bin/python3 /home/manmeet/code.py -o vmware -c
2. 0 0 * * * /usr/bin/python3 /home/manmeet/code.py -o vmware -c

The first cron job runs every 5 minutes and writes the output to a CSV for organization named 'vmware'
The second cron job is the same as the first one but instead runs everyday at 12:00 am
