#!/usr/bin/env python
#   Copyright 2015-2016 See CONTRIBUTORS.md file
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import boto3
from tabulate import tabulate
from accloudtant.aws.instance import Instance
from accloudtant.aws.prices import Prices


class Reports(object):
    def __init__(self):
        ec2 = boto3.resource('ec2')
        self.instances = [Instance(i) for i in ec2.instances.all()]
        ec2_client = boto3.client('ec2')
        self.reserved_instances = ec2_client.describe_reserved_instances()
        self.prices = Prices()
        self.find_reserved_instance()

    def find_reserved_instance(self):
        for instance in self.instances:
            instance_region = self.prices.prices[instance.key][instance.region]
            instance_size = instance_region[instance.size]
            instance.current = float(instance_size['od'])
            if instance.state == 'stopped':
                instance.current = 0.0
            instance_allUpfront = instance_size['ri']['yrTerm3']['allUpfront']
            instance.best = float(instance_allUpfront['effectiveHourly'])
            for reserved in self.reserved_instances['ReservedInstances']:
                    if 'InstancesLeft' not in reserved.keys():
                        reserved['InstancesLeft'] = reserved['InstanceCount']
                    if instance.match_reserved_instance(reserved):
                        instance._reserved = True
                        instance.current = reserved['UsagePrice']
                        reserved['InstancesLeft'] -= 1
                        break

    def __repr__(self):
        headers = [
                'Id',
                'Name',
                'Type',
                'AZ',
                'OS',
                'State',
                'Launch time',
                'Reserved',
                'Current hourly price',
                'Renewed hourly price',
                ]
        table = []
        for instance in self.instances:
            row = [
                    instance.id,
                    instance.name,
                    instance.size,
                    instance.availability_zone,
                    instance.operating_system,
                    instance.state,
                    instance.launch_time.strftime('%Y-%m-%d %H:%M:%S'),
                    instance.reserved,
                    instance.current,
                    instance.best,
                    ]
            table.append(row)
        return tabulate(table, headers)
