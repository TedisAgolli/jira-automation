from jira import JIRA
import json


def loadTicketInfo():
    with open("config.json") as f:
        info = json.load(f)
    return (info["credentials"], info["ticket"])


# example
# def getAllUsers():
# for user in jira.group_members("API"):
# print(jira.user(user))
# for group in jira.groups():
# print(group)


if __name__ == "__main__":

    (credentials, ticketInfo) = loadTicketInfo()
    jira = JIRA(
        options={"server": credentials["server"]},
        basic_auth=(credentials["username"], credentials["password"]),
    )
    for assignee in ticketInfo["assignees"]:
        newIssue = jira.create_issue(
            project=ticketInfo["project"],
            summary=ticketInfo["summary"],
            description=ticketInfo["description"],
            issuetype={"name": ticketInfo["issueType"]},
            assignee={"accountId": assignee["id"]},
        )

        for attachmentName in ticketInfo["attachmentNames"]:
            with open(attachmentName, "rb") as f:
                jira.add_attachment(newIssue, f)
        print("Created ticket %s and assigned it to %s" % (newIssue, assignee["name"]))
