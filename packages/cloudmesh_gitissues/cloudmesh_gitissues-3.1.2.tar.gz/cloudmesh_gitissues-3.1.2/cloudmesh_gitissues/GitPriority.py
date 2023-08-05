#!/usr/bin/env python
from __future__ import print_function
from pprint import pprint
import json
import requests
import sys


class GitPriority(object):

    columns = [
        ("priority", "P", 4),
        ("number", "N", 4),
        ("title", "title", 40),
        ("assignee", "assignee", 10),
        ("milestone", "milestone", 10),
        ("location", "location", 20),
        ("labels", "labels", 20),
    ]


    def __init__(self, user, repository):
        data={"user": user, "repository": repository}
        self.url = 'https://api.github.com/repos/{user}/{repository}/issues'.format(**data)
        self.issues = None

                #
        # setup format strings
        #
        header_format = ""
        row_format = ""
        self.header_elements = ['']
        self.row_elements = ['']
        self.headers = {}
        self.order = []
        for (attribute, header, length) in self.columns:
            self.headers[attribute] = header
            self.order.append(attribute)
            self.header_elements.append("{}{}{}{}{}".format("{", header, ":", length, "}"))
            self.row_elements.append("{}{}{}{}{}".format("{", attribute, ":", length, "}"))
        self.header_elements.append("")
        self.row_elements.append("")
        self.header_format = ' | '.join(self.header_elements).strip()
        self.row_format = ' | '.join(self.row_elements).strip()
        # print(row_format)
        # rint(header_format)

    def get(self):
        self.issues = []
        for page in range(1, 2):
            url = self.url + '?page={}&per_page=100'.format(page)
            r = requests.get(url)
            self.issues.extend(r.json())

    def sanitize(self, username, repository):
        print("SANITIZE", len(self.issues))

        sanitized = []

        if self.issues is None:
            return
        for issue in self.issues:

            if "assignee" not in issue:
                issue["assignee"] = {"login":""}
            elif issue["assignee"] is None:
                issue["assignee"] = {"login":""}

            if "milestone" not in issue:
                issue["milestone"] = {"title": ""}
            elif issue["milestone"] is None:
                issue["milestone"] = {"title": ""}

            if "labels" not in issue:
                issue["labels"] = [
                    {'color': '5319e7',
                    'name': '',
                    'url': ''}]

            priority = 999
            if "body" not in issue:
                issue["body"] = None
            else:
                body = issue["body"].splitlines()
                if len(body) >= 1:
                    line = str(body[0])

                    if "P:" in line:
                        priority = line.split("P:")[1]

            issue[u"location"] = "{}/{}".format(username,repository)
            issue[u"priority"] = int(priority)
            sanitized.append(dict(issue))
        self.issues = sanitized
        # pprint(self.issues)

    def __str__(self):
        return json.dumps(self.issues, indent=4)

    def table(self, compact=True):
        #
        # Print header
        #
        issue = {}
        for (attribute, header, length) in self.columns:
            issue[attribute] = header
        print(self.row_format.format(**issue))
        #
        # Print header line
        #
        issue = {}
        for (attribute, header, length) in self.columns:
            issue[attribute] = "-" * length
        print(self.row_format.format(**issue))

        issue_table = []

        for page in range(1, 2):

            for issue in self.issues:
                pprint (issue)
                row = {}
                if "assignee" in issue:
                    if issue["assignee"] is not None:
                        issue["assignee"] = issue["assignee"]["login"]
                    else:
                        issue["assignee"] = "None"

                if "milestone" in issue:
                    if issue["milestone"] is not None:
                        issue["milestone"] = issue["milestone"]["title"]
                    else:
                        issue["milestone"] = "None"

                if "labels" in issue:
                    if issue["labels"] is not None:
                        content = []
                        for label in issue["labels"]:
                            content.append(label["name"])
                        issue["labels"] = ", ".join(content)
                    else:
                        issue["labels"] = "None"

                priority = 999
                if "body" in issue:
                    if issue["body"] is not None:
                        body = issue["body"].splitlines()
                        if len(body) >= 1:
                            line = str(body[0])

                            if "P:" in line:
                                priority = line.split("P:")[1]

                issue["priority"] = int(priority)

                content = ""
                for (attribute, header, length) in self.columns:
                    data = str(issue[attribute])
                    if compact and len(data) > length:
                        issue[attribute] = data[:length - 3] + "..."
                    else:
                        issue[attribute] = data
                    row[attribute] = issue[attribute]
                issue_table.append(row)

        #
        # print the table
        #

        return issue_table


    def dump(self):
        issues = self.table()
        content = ""
        for row in issues:
            content += self.row_format.format(**row) + "\n"
        return content

if __name__ == "__main__":
    issues = GitPriority("cloudmesh", "client")
    issues.get()
    print (issues)
    print (issues.dump())
