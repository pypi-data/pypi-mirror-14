"""
awslimitchecker/services/rds.py

The latest version of this package is available at:
<https://github.com/jantman/awslimitchecker>

################################################################################
Copyright 2015 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of awslimitchecker, also known as awslimitchecker.

    awslimitchecker is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    awslimitchecker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with awslimitchecker.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/pydnstest> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import abc  # noqa
import logging

from .base import _AwsService
from ..limit import AwsLimit

logger = logging.getLogger(__name__)


class _RDSService(_AwsService):

    service_name = 'RDS'
    api_name = 'rds'

    def find_usage(self):
        """
        Determine the current usage for each limit of this service,
        and update corresponding Limit via
        :py:meth:`~.AwsLimit._add_current_usage`.
        """
        logger.debug("Checking usage for service %s", self.service_name)
        self.connect()
        for lim in self.limits.values():
            lim._reset_usage()
        self._find_usage_instances()
        self._find_usage_snapshots()
        self._find_usage_param_groups()
        self._find_usage_subnet_groups()
        self._find_usage_option_groups()
        self._find_usage_event_subscriptions()
        self._find_usage_security_groups()
        self._find_usage_reserved_instances()
        self._have_usage = True
        logger.debug("Done checking usage.")

    def _find_usage_instances(self):
        """find usage for DB Instances and related limits"""
        count = 0
        allocated_gb = 0

        paginator = self.conn.get_paginator('describe_db_instances')
        for page in paginator.paginate():
            for instance in page['DBInstances']:
                count += 1
                allocated_gb += instance['AllocatedStorage']
                self.limits['Read replicas per master']._add_current_usage(
                    len(instance['ReadReplicaDBInstanceIdentifiers']),
                    aws_type='AWS::RDS::DBInstance',
                    resource_id=instance['DBInstanceIdentifier']
                )

        self.limits['DB instances']._add_current_usage(
            count,
            aws_type='AWS::RDS::DBInstance'
        )

        self.limits['Storage quota (GB)']._add_current_usage(
            allocated_gb,
            aws_type='AWS::RDS::DBInstance'
        )

    def _find_usage_reserved_instances(self):
        """find usage for reserved instances"""
        count = 0

        paginator = self.conn.get_paginator('describe_reserved_db_instances')
        for page in paginator.paginate():
            for inst in page['ReservedDBInstances']:
                count += 1
        self.limits['Reserved Instances']._add_current_usage(
            count,
            aws_type='AWS::RDS::DBInstance'
        )

    def _find_usage_snapshots(self):
        """find usage for (manual) DB snapshots"""
        count = 0

        paginator = self.conn.get_paginator('describe_db_snapshots')
        for page in paginator.paginate():
            for snap in page['DBSnapshots']:
                if snap['SnapshotType'] == 'manual':
                    count += 1
        self.limits['DB snapshots per user']._add_current_usage(
            count,
            aws_type='AWS::RDS::DBSnapshot'
        )

    def _find_usage_param_groups(self):
        """find usage for parameter groups"""
        count = 0

        paginator = self.conn.get_paginator('describe_db_parameter_groups')
        for page in paginator.paginate():
            for group in page['DBParameterGroups']:
                count += 1
        self.limits['DB parameter groups']._add_current_usage(
            count,
            aws_type='AWS::RDS::DBParameterGroup'
        )

    def _find_usage_subnet_groups(self):
        """find usage for subnet groups"""
        count = 0

        paginator = self.conn.get_paginator('describe_db_subnet_groups')
        for page in paginator.paginate():
            for group in page['DBSubnetGroups']:
                count += 1
                self.limits['Subnets per Subnet Group']._add_current_usage(
                    len(group['Subnets']),
                    aws_type='AWS::RDS::DBSubnetGroup',
                    resource_id=group["DBSubnetGroupName"],
                )
        self.limits['Subnet Groups']._add_current_usage(
            count,
            aws_type='AWS::RDS::DBSubnetGroup',
        )

    def _find_usage_option_groups(self):
        """find usage for option groups"""
        count = 0

        paginator = self.conn.get_paginator('describe_option_groups')
        for page in paginator.paginate():
            for group in page['OptionGroupsList']:
                count += 1
        self.limits['Option Groups']._add_current_usage(
            count,
            aws_type='AWS::RDS::DBOptionGroup',
        )

    def _find_usage_event_subscriptions(self):
        """find usage for event subscriptions"""
        count = 0

        paginator = self.conn.get_paginator('describe_event_subscriptions')
        for page in paginator.paginate():
            for group in page['EventSubscriptionsList']:
                count += 1
        self.limits['Event Subscriptions']._add_current_usage(
            count,
            aws_type='AWS::RDS::EventSubscription',
        )

    def _find_usage_security_groups(self):
        """find usage for security groups"""
        vpc_count = 0
        classic_count = 0

        paginator = self.conn.get_paginator('describe_db_security_groups')
        for page in paginator.paginate():
            for group in page['DBSecurityGroups']:
                if 'VpcId' not in group or group['VpcId'] is None:
                    classic_count += 1
                else:
                    vpc_count += 1
                self.limits['Max auths per security group']._add_current_usage(
                    len(group["EC2SecurityGroups"]) + len(group["IPRanges"]),
                    aws_type='AWS::RDS::DBSecurityGroup',
                    resource_id=group['DBSecurityGroupName']
                )

        self.limits['DB security groups']._add_current_usage(
            classic_count,
            aws_type='AWS::RDS::DBSecurityGroup',
        )

        self.limits['VPC Security Groups']._add_current_usage(
            vpc_count,
            aws_type='AWS::RDS::DBSecurityGroup',
        )

    def get_limits(self):
        """
        Return all known limits for this service, as a dict of their names
        to :py:class:`~.AwsLimit` objects.

        :returns: dict of limit names to :py:class:`~.AwsLimit` objects
        :rtype: dict
        """
        if self.limits != {}:
            return self.limits
        limits = {}
        limits['DB instances'] = AwsLimit(
            'DB instances',
            self,
            40,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBInstance',
        )
        limits['Reserved Instances'] = AwsLimit(
            'Reserved Instances',
            self,
            40,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBInstance',
        )
        limits['Storage quota (GB)'] = AwsLimit(
            'Storage quota (GB)',
            self,
            100000,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBInstance',
        )
        limits['DB snapshots per user'] = AwsLimit(
            'DB snapshots per user',
            self,
            50,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBSnapshot',
        )
        limits['DB parameter groups'] = AwsLimit(
            'DB parameter groups',
            self,
            50,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBParameterGroup',
        )
        limits['DB security groups'] = AwsLimit(
            'DB security groups',
            self,
            25,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBSecurityGroup',
        )
        limits['VPC Security Groups'] = AwsLimit(
            'VPC Security Groups',
            self,
            5,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBSecurityGroup',
        )
        limits['Subnet Groups'] = AwsLimit(
            'Subnet Groups',
            self,
            20,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBSubnetGroup',
        )
        limits['Subnets per Subnet Group'] = AwsLimit(
            'Subnets per Subnet Group',
            self,
            20,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBSubnetGroup',
        )
        limits['Option Groups'] = AwsLimit(
            'Option Groups',
            self,
            20,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBOptionGroup',
        )
        limits['Event Subscriptions'] = AwsLimit(
            'Event Subscriptions',
            self,
            20,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBEventSubscription',
        )
        limits['Read replicas per master'] = AwsLimit(
            'Read replicas per master',
            self,
            5,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBInstance',
        )
        # this is the number of rules per security group
        limits['Max auths per security group'] = AwsLimit(
            'Max auths per security group',
            self,
            20,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::RDS::DBSecurityGroup',
            limit_subtype='AWS::RDS::DBSecurityGroupIngress',
        )
        self.limits = limits
        return limits

    def required_iam_permissions(self):
        """
        Return a list of IAM Actions required for this Service to function
        properly. All Actions will be shown with an Effect of "Allow"
        and a Resource of "*".

        :returns: list of IAM Action strings
        :rtype: list
        """
        return [
            "rds:DescribeDBInstances",
            "rds:DescribeDBParameterGroups",
            "rds:DescribeDBSecurityGroups",
            "rds:DescribeDBSnapshots",
            "rds:DescribeDBSubnetGroups",
            "rds:DescribeEventSubscriptions",
            "rds:DescribeOptionGroups",
            "rds:DescribeReservedDBInstances",
        ]
