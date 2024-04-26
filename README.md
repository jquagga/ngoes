# ngoes

Polls Global Entry appointments and sends apprise notifications when it finds one.

## Running
This should be something you quickly set up and just run the docker.  You need to set 2 environmental variables:

```NGOES_LOCATIONID``` which is the 4 digit ID number for the site you want to poll.  You can find that from the listing [here!](https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry).  Just do a find on that page.  

```NGOES_NOTIFY_URL``` is the [apprise](https://github.com/caronc/apprise) url to send notification.  I use ntfy but you can use discord, slack, mastodon, sms - whatever apprise supports.  You just have to format the url correctly.

Putting that together into a docker command:

```
docker run -d --init --name goes-notifier -e NGOES_LOCATIONID=5005 -e NGOES_NOTIFY_URL=ntfy://mynotifystring --restart unless-stopped ghcr.io/jquagga/ngoes:main

```
