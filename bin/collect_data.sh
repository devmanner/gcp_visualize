#!/bin/bash

if [ "$1" == "" ]; then
	echo "Usage: $0 output.json"
	exit -1
fi

output=$1
tempdir=$(mktemp -d /tmp/collect_data-XXXXXXXX)
projectdir=$tempdir/projects
disks=$tempdir/disks.json
firewall_rules=$tempdir/firewall-rules.json
instances=$tempdir/instances.json
networks=$tempdir/networks.json
routes=$tempdir/routes.json
all=$tempdir/all.json

mkdir $projectdir

for p in $(gcloud projects list | cut -f 1 -d " "| grep -v PROJECT_ID); do
	gcloud compute instances list --format=json --project=$p > $instances
    gcloud compute disks list --format=json --project=$p > $disks
    gcloud compute firewall-rules list --format=json --project=$p > $firewall_rules
    gcloud compute networks list --format=json --project=$p > $networks
    gcloud compute routes list --format=json --project=$p > $routes

	jq -s '{"project": "'$p'", "disks": .[0], "firewall-rules": .[1], "instances": .[2], "networks": .[3], "routes": .[4]}' $disks $firewall_rules $instances $networks $routes > $projectdir"/"$p".json"
done

jq -s "." $projectdir/* > $output 

rm -fr $tempdir

