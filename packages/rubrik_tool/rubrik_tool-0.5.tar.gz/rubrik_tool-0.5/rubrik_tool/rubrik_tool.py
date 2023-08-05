#!/usr/bin/env python

'''
Created on Apr 3, 2014

@author: arvind
'''

import os
import sys

from SdRestClient import SdRestClient
from distutils.spawn import find_executable
from logging_utils import init_logging
import argparse
from dateutil.parser import parse
import logging
import inspect
import json
import pytz
import random
import requests
import sdconf
import shutil
import subprocess
import time

log = logging.getLogger(os.path.basename(__file__))

JOB_INSTANCE_LOG_STATUS_INTERVAL_SECS = 60.0

JQ = 'jq'

# Use this decorator on a route to set it as visible in the "help" list
def visible_method(func):
    func.func_dict['user_visible_method'] = True
    return func

class JobStates:
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'
    FINAL_STATES = [SUCCEEDED, FAILED, CANCELED]

# TODO(adam|kt): How to better organize this file.
class RubrikTool(object):
    PUBLIC_JOB_TYPES = [
        'mount',
        'unmount',
        'restore',
        'export',
        'download',
        'download_file'
    ]

    # This function cannot be inlined since the lambda parameters are
    # passed by reference.
    # See: http://goo.gl/dNvE0H
    def __create_authenticate_lambda(self, api_base_url, username, password):
        return lambda: self.__authenticate(api_base_url, username, password)

    def __init__(self, api_base_urls, username=None, password=None):
        assert api_base_urls
        if not isinstance(api_base_urls, list):
            api_base_urls = [api_base_urls]
        PREFIX = 'https://'
        self.username = username
        api_base_urls = map(lambda x: (x if x.startswith(PREFIX)
                                       else PREFIX + x),
                            api_base_urls)

        logging.debug('Initializing api tool for %s %s/%s' %
                      (api_base_urls, username, password))

        self.local_token = None
        try:
            self.local_token = sdconf.getConfEntry('sprayServerLocalToken')
        except Exception as e:
            logging.debug(
                "Couldn't load local token from configuration file, so " +
                "proceeding with normal username/password authentication." +
                "Encountered error %s" % str(e))

        self.rest_clients = []
        for api_base_url in api_base_urls:
            rest_client = SdRestClient(
                api_base_url,
                self.__create_authenticate_lambda(api_base_url,
                                                  username,
                                                  password))
            self.rest_clients.append(rest_client)

        # TODO(sujeet, nitro): re-enable randomization
        #                      once we figure out how to sync
        #                      in-memory caches across nodes
        self.chosen_rest_client = self._get_random_client()

    @staticmethod
    def from_args(args):
        return RubrikTool(args.rubrik_host,
                          args.rubrik_user,
                          args.rubrik_password)

    def _get_random_client(self):
        return random.choice(self.rest_clients)

    def __authenticate(self, api_base_url, username, password):
        if self.local_token is not None and username is None:
            return self.local_token

        rest = SdRestClient(api_base_url)
        loginResponse = rest.post('/login', data={
            'userId': username,
            'password': password
        })
        status = loginResponse['status']
        description = loginResponse['description']
        if (status == 'Failure'):
            # NB(dar): LOG THIS NO HIGHER THAN DEBUG LEVEL (to prevent
            # near-password strings from being logged).
            log.debug(
                'Login error (username: %s, password %s)' % (
                    username,
                    password))
            raise Exception(
                'login error with username: %s, %s' % (username, description))
        return loginResponse['token']

    @visible_method
    def get_vm_summaries(self,
                         sla_domain_id=None,
                         primary_cluster_filter='local'):
        url = '/vm'
        parameters = []
        if sla_domain_id:
            parameters.append(
                'slaDomainIdOpt=%s' % sla_domain_id)
        if primary_cluster_filter:
            parameters.append(
                'primaryClusterUuidOpt=%s' % primary_cluster_filter)
        if parameters:
            url += '?' + '&'.join(parameters)
        return self.chosen_rest_client.get(url)

    def get_virtual_disks_for_virtual_machine(self, vm_id):
        response_data = self.chosen_rest_client.get('/vm/%s' % vm_id)
        log.info(repr(response_data))
        return response_data['virtualDiskIds']

    def get_full_snapshot_disk(self, virtual_disk_id, location_id):
        response_data = self.chosen_rest_client.post(
            '/internal/snapshot_disk/full_snapshot_disks',
            data={
                'virtualDiskId': virtual_disk_id,
                'locationId': location_id
            }
        )
        return response_data['diskIds']

    def are_disks_gced(self, expired_disk_ids, location_id):
        response_data = self.chosen_rest_client.post(
            '/internal/snapshot_disk/garbage_collect_status',
            data={
                'diskIds': expired_disk_ids,
                'locationId': location_id
            }
        )
        return response_data['status']

    def are_snapshots_gced(self, snapshot_ids, vm_id):
        response_data = self.chosen_rest_client.post(
            '/internal/snapshot/garbage_collect_status',
            data={
                'snapshotIds': snapshot_ids,
                'virtualMachineId': vm_id
            }
        )
        return response_data['status']

    def are_snapshots_gced_on_archive(
            self,
            snapshot_id_and_date_tuples,
            vm_id,
            location_id):
        tuples = ["%s:::%s" % tup for tup in snapshot_id_and_date_tuples]
        response_data = self.chosen_rest_client.post(
            '/internal/snapshot/archive_garbage_collect_status',
            data={
                'snapshotDateTuples': tuples,
                'virtualMachineId': vm_id,
                'locationId': location_id
            }
        )
        return response_data['status']

    @visible_method
    def find_a_vm_by_name(self,
                          vm_name,
                          retries=0,
                          primary_cluster_filter='local'):
        for i in range(retries + 1):
            response_data = self.get_vm_summaries(
                primary_cluster_filter=primary_cluster_filter)
            vm_ids = [resp_entry['id'] for resp_entry in response_data
                      if resp_entry['name'] == vm_name]
            if vm_ids:
                return vm_ids[0]
            if i < retries:
                time.sleep(30)

        raise Exception('Could not find VM %s' % vm_name)

    def find_a_vm_managed_id_by_name(self,
                                     vm_name,
                                     primary_cluster_filter='local'):
        response_data = self.get_vm_summaries(
            primary_cluster_filter=primary_cluster_filter)
        vm_ids = [resp_entry['managedId'] for resp_entry in response_data
                  if resp_entry['name'] == vm_name]
        if vm_ids:
            return vm_ids[0]

        raise Exception('Could not find VM %s' % vm_name)

    def find_all_vm_ids_by_name(self,
                                vm_name,
                                retries=0,
                                primary_cluster_filter='local'):
        for i in range(retries + 1):
            response_data = self.get_vm_summaries(
                primary_cluster_filter=primary_cluster_filter)
            vm_ids = [resp_entry['id'] for resp_entry in response_data
                      if resp_entry['name'] == vm_name]
            if vm_ids:
                return vm_ids
            if i < retries:
                time.sleep(30)

        raise Exception('Could not find VM %s' % vm_name)

    def find_a_ds_by_name(self, ds_name):
        response_data = \
            self.chosen_rest_client.get('/datastore', data={}).get('data')
        ds_ids = [resp_entry['id'] for resp_entry in response_data
                  if resp_entry['name'] == ds_name]
        assert(len(ds_ids) > 0)
        return ds_ids[0]

    @visible_method
    def find_all_datastores(self):
        response_data = \
            self.chosen_rest_client.get('/datastore', data={}).get('data')
        datastores = [(resp_entry['name'],
                       resp_entry['dataStoreType'],
                       resp_entry['capacity']) for resp_entry in response_data]
        return datastores

    @visible_method
    def create_sla_domain(self,
                          name,
                          frequencies,
                          allowed_backup_windows,
                          disallowed_backup_windows,
                          replication_specs):
        return self.chosen_rest_client.post('/slaDomain', data={
            'name': name,
            'frequencies': frequencies,
            'allowedBackupWindows': allowed_backup_windows,
            'disallowedBackupWindows': disallowed_backup_windows,
            'replicationSpecs': replication_specs
        })

    @visible_method
    def get_sla_domains(self):
        return self.chosen_rest_client.get('/slaDomain')

    @visible_method
    def delete_sla_domain(self, name):
        return self.chosen_rest_client.delete('/slaDomain/%s' % name)

    @visible_method
    def find_a_sla_domain_by_name(self, sla_domain_name):
        response = self.get_sla_domains()
        sla_domains = [response_entry for response_entry in response
                       if response_entry['name'] == sla_domain_name]
        if (len(sla_domains) != 1):
            self.exit_status = -1
            raise RuntimeError(
                'Expected exactly 1 SLA domain matching name %s, got %d.' %
                (repr(sla_domain_name), len(sla_domains)))

        return sla_domains[0]

    @visible_method
    def find_a_vmware_host_by_name(self,
                                   host_name,
                                   primary_cluster_filter='local'):
        url = '/vmware/host'
        if primary_cluster_filter:
            url += '?primaryClusterUuidOpt=%s' % primary_cluster_filter
        response_data = self.chosen_rest_client.get(url, data={})
        host_ids = [resp_entry['id'] for resp_entry in response_data
                    if ('name' in resp_entry and
                        resp_entry['name'] == host_name)]
        assert len(host_ids) > 0, ('%s not found in %s' %
                                   (host_name,
                                    [x['name'] for x in response_data]))
        return host_ids[0]

    @visible_method
    def vm_name_for_mount(self, mount_id):
        rest_client = self.chosen_rest_client
        mount_vm = rest_client.get("/mount/%s" % mount_id)["virtualMachine"]
        return mount_vm["name"]

    @visible_method
    def vm_name_for_snapshot(self, snapshot_id):
        snapshot = self.chosen_rest_client.get("/snapshot/%s" % snapshot_id)
        snapshot_vm = snapshot["virtualMachine"]
        return snapshot_vm["name"]

    @visible_method
    def get_vcenters(self):
        return self.chosen_rest_client.get('/vcenter')

    def add_vcenter(self, vcenter_server, username, password,
                    wait_for_refresh=False):
        response = self.chosen_rest_client.post('/vcenter', data={
            'ip': vcenter_server,
            'username': username,
            'password': password
        })

        if wait_for_refresh:
            self.wait_for_vcenter_refresh(vcenter_server)

        return response

    def update_vcenter(self, vcenter_id, vcenter_ip, username, password):
        return self.chosen_rest_client.patch('/vcenter/%s' % vcenter_id,
                                             data={
                                                 'ip': vcenter_ip,
                                                 'username': username,
                                                 'password': password
                                             })

    def add_cloud_creds(self,
                        object_store_config):
        response = \
            self.chosen_rest_client.post('/data_location/cloud',
                                         data=object_store_config)
        assert response['status'] is 0, response['message']
        # Add location job id
        return response['message']

    # returns reconnect job id, which needs to be polled
    def reconnect_cloud(self, object_store_spec):
        response = self.chosen_rest_client.post(
            '/data_location/reconnect/cloud',
            data=object_store_spec)
        assert response['status'] is 0, response['message']
        return response['message']

    # returns reconnect job id, which needs to be polled
    def reconnect_nfs(self, nfs_spec):
        response = self.chosen_rest_client.post(
            '/data_location/reconnect/nfs',
            data=nfs_spec)
        assert response['status'] is 0, response['message']
        return response['message']

    # returns recovery job id, which needs to be polled
    def recover_archived_metadata(self, location_id):
        response = self.chosen_rest_client.post(
            '/data_location/recover_archived_metadata',
            data={
                'dataLocationId': location_id
            })
        assert response['status'] is 0, response['message']
        return response['message']

    def get_cloud_locations(self):
        return self.chosen_rest_client.get('/data_location/cloud').get('data')

    def get_nfs_locations(self):
        return self.chosen_rest_client.get('/data_location/nfs').get('data')

    def add_nfs_storage_location(self, nfs_config):
        response = self.chosen_rest_client.post('/data_location/nfs',
                                                data=nfs_config)
        assert response['status'] is 0, response['message']
        # nfs job id
        return response['message']

    def update_vm_sla_domain(self, vm_id, sla_domain_id):
        # Allow specifying sla_domain_id == None to clear the sla domain.
        data = {}
        if sla_domain_id:
            data['slaDomainId'] = sla_domain_id
        else:
            # Empty string means to remove SLA domain
            data['slaDomainId'] = ''
        return self.chosen_rest_client.patch('/vm/%s' % vm_id, data=data)

    def assign_sla(self, sla_domain_id, managed_ids):
        return self.chosen_rest_client.patch(
            '/slaDomainAssign/%s' % sla_domain_id, data={
                'managedIds': managed_ids
            })

    @visible_method
    def assign_vm_to_sla_by_name(self, sla_domain_name, vm_name):
        vm_managed_id = self.find_a_vm_managed_id_by_name(vm_name)
        sla_domain_id = self.find_a_sla_domain_by_name(sla_domain_name)['id']
        return self.assign_sla(sla_domain_id, [vm_managed_id])

    def update_user(self,
                    user_id,
                    updated_by,
                    role=None,
                    password=None,
                    email=None):
        data = {
            'id': user_id,
            'updateById': updated_by
        }
        if role is not None:
            data['role'] = role
        if password is not None:
            data['password'] = password
        if email is not None:
            data['emailAddress'] = email

        return self.chosen_rest_client.patch('/user', data=data)

    def get_user(self, user_id):
        return self.chosen_rest_client.get('/user/%s' % user_id)

    def list_users(self, username=None, auth_domain_id=None):
        params = {}
        if username is not None:
            params['username'] = username
        if auth_domain_id is not None:
            params['auth_domain_id'] = auth_domain_id
        return self.chosen_rest_client.get('/user', params=params)

    def get_cluster_name(self):
        return self.chosen_rest_client.get('/clusterName')

    def get_cluster_info(self):
        return self.chosen_rest_client.get('/cluster')

    def get_system_version(self):
        return self.chosen_rest_client.get('/system/version')

    def remove_replication_partner(self, partner_uid):
        rest_end_point = '/data_location/replication_target/%s' % partner_uid
        return self.chosen_rest_client.delete(rest_end_point)

    def add_replication_partner(self,
                                partner_ip,
                                username,
                                password):
        data = {
            'targetClusterAddress': partner_ip,
            'username': username,
            'password': password,
            'replicationSetup': "Private Network"
        }
        end_point = '/data_location/replication_target'
        return self.chosen_rest_client.post(end_point, data=data)

    def add_replication_partner_with_nat(self,
                                         source_gateway_ip,
                                         source_gateway_ports,
                                         target_gateway_ip,
                                         target_gateway_ports,
                                         username,
                                         password):
        data = {
            'sourceGateway': {
                'address': source_gateway_ip,
                'ports': source_gateway_ports
            },
            'targetGateway': {
                'address': target_gateway_ip,
                'ports': target_gateway_ports
            },
            'username': username,
            'password': password,
            'replicationSetup': 'NAT'
        }
        end_point = '/data_location/replication_target'
        return self.chosen_rest_client.post(end_point, data=data)

    def get_replication_source_partners(self):
        end_point = '/data_location/replication_source'
        return self.chosen_rest_client.get(end_point).get('data')

    def get_replication_target_partners(self):
        end_point = '/data_location/replication_target'
        return self.chosen_rest_client.get(end_point).get('data')

    def delete_user(self, user_id):
        return self.chosen_rest_client.delete('/user/%s' % user_id)

    def add_user(self, username, password, is_admin, create_by):
        data = {
            'id': username,
            'password': password,
            'isAdmin': is_admin,
            'createdById': create_by
        }
        return self.chosen_rest_client.post('/user', data=data)

    @visible_method
    def find_a_user_by_username(self, username, auth_domain_id=None):
        users = self.list_users(username=username,
                                auth_domain_id=auth_domain_id)
        if len(users) >= 1:
            return users[0]['id']
        auth_domain_msg = ''
        if auth_domain_id is not None:
            auth_domain_msg = ' auth_domain_id=%s' % repr(auth_domain_id)
        raise Exception('No user with username=%s%s found.' %
                        (repr(username), auth_domain_msg))

    @visible_method
    def get_notifications(self, user_id, query='limit=25'):
        return self.chosen_rest_client.get(
            '/userNotification/%s?%s' % (user_id, query)).get('data')

    def get_config(self, namespace, key=None):
        end_point = '/internal/config/%s' % namespace
        log.debug(repr('get_config (%s)' % end_point))
        if key is not None:
            return self.chosen_rest_client.get(end_point)[key]
        else:
            return self.chosen_rest_client.get(end_point)

    def update_config(self, namespace, key, value):
        end_point = '/internal/config/%s' % namespace
        data = {
            key: value
        }
        log.debug(repr('update_config (%s): %s = %s'
                       % (end_point, key, value)))
        return self.chosen_rest_client.patch(end_point, data=data)

    # Get the top level job details. i.e. the container (not instance) level
    # Currently, there is no REST end point of GET nature that simply fetches
    # the job level details. We need to create an API like that. See CDM-12660
    # Currently, the patch call with no fields implies nothing is changing and
    # the call works like a GET operation, thus accomplishing the same as above
    def get_job_details(self, job_id):
        end_point = '/job/%s' % job_id
        data = {
        }
        log.debug(repr('get_job_details (%s):  %s ' % (end_point, job_id)))
        return self.chosen_rest_client.patch(end_point, data=data)

    def enable_job(self, job_id):
        end_point = '/job/%s' % job_id
        data = {
            'enabled': True
        }
        log.debug(repr('enable_job (%s):  %s ' % (end_point, job_id)))
        return self.chosen_rest_client.patch(end_point, data=data)

    def disable_job(self, job_id):
        end_point = '/job/%s' % job_id
        data = {
            'enabled': False
        }
        log.debug(repr('disable_job (%s):  %s ' % (end_point, job_id)))
        return self.chosen_rest_client.patch(end_point, data=data)

    def get_job_instances(self, job_id):
        end_point = '/internal/job/instances'
        data = {
            'jobId': job_id
        }
        log.debug(repr('get_job_instances (%s):  %s ' % (end_point, job_id)))
        return self.chosen_rest_client.post(end_point, data=data)

    def get_job_instance(self, job_instance_id):
        end_point = '/job/instance/%s' % job_instance_id
        log.debug(repr('get_job_instance (%s):  %s ' %
                       (end_point, job_instance_id)))
        job_details = self.chosen_rest_client.get(end_point)
        log.debug("job_details => %s" % str(job_details))
        return job_details

    def create_job(self, job_type, job_config):
        if job_type in RubrikTool.PUBLIC_JOB_TYPES:
            job_type_api_fmt = '/job/type/%s'
        else:
            job_type_api_fmt = '/internal/job/type/%s'

        log.debug('create_job (%s):  %s ' % (job_type, job_config))
        return self.chosen_rest_client.post(job_type_api_fmt % job_type,
                                            data=job_config)

    def wait_for_job_instance(self, job_instance_id, wait_function=None):
        (job_instance, timedout) = \
            self.wait_for_job_transition(job_instance_id,
                                         JobStates.FINAL_STATES,
                                         -1,
                                         wait_function)
        assert not timedout
        status = job_instance['status']
        if (status != JobStates.SUCCEEDED):
            result = ''
            if 'result' in job_instance:
                result = job_instance['result']
            log.error('Job instance %s of type %s has failed ' %
                      (repr(job_instance_id), repr(job_instance['jobType'])) +
                      'with status = %s. ' % repr(status) +
                      'Result:\n%s' % result)
            raise RuntimeError(
                'Job instance %s of type %s has failed ' %
                (repr(job_instance_id), repr(job_instance['jobType'])) +
                'with status = %s. ' % repr(status) +
                'Result:\n%s' % result)
        return job_instance

    def wait_for_job_cleanup(self, job_instance_id, timeout_seconds):
        (job_instance, timedout) = \
            self.wait_for_job_transition(job_instance_id,
                                         JobStates.FINAL_STATES,
                                         timeout_seconds)
        return (job_instance, timedout)

    def get_job_instance_status(self, job_instance_id):
        rest_client = self.chosen_rest_client
        job_instance = rest_client.get('/job/instance/%s' % job_instance_id)
        job_type = job_instance['jobType']
        status = job_instance['status']
        return "Job " + job_type, status

    def wait_for_job_transition(self,
                                job_instance_id,
                                final_state_list,
                                timeout_seconds,
                                wait_function=None):
        timedout = self.wait_for_transition(
            transition_elem_instance_id=job_instance_id,
            final_state_list=final_state_list,
            timeout_seconds=timeout_seconds,
            get_status_cb=self.get_job_instance_status,
            wait_function=wait_function)
        job_instance = self.chosen_rest_client.get(
            '/job/instance/%s' % job_instance_id)

        return job_instance, timedout

    def get_vcenter_refresh_status(self, vcenter_id):
        return "vCenter Refresh", self.chosen_rest_client.get(
               '/vcenter/refresh_status/%s' % vcenter_id)

    def wait_for_vcenter_refresh(self, vcenter_hostname):
        vcenter = filter(lambda vc: vc['ip'] == vcenter_hostname,
                         self.get_vcenters())
        assert len(vcenter) == 1, 'vCenter %s not found' % vcenter_hostname
        vcenter_id = vcenter[0]["id"]
        self.wait_for_transition(
            transition_elem_instance_id=vcenter_id,
            final_state_list=JobStates.FINAL_STATES,
            timeout_seconds=900,
            get_status_cb=self.get_vcenter_refresh_status)
        _, status = self.get_vcenter_refresh_status(vcenter_id)
        assert status == JobStates.SUCCEEDED

    def wait_for_transition(self,
                            transition_elem_instance_id,
                            final_state_list,
                            timeout_seconds,
                            get_status_cb,
                            wait_function=None):
        def default_wait_function():
            time.sleep(1)
        status = None
        log.debug('Waiting for %s finish...' %
                  repr(transition_elem_instance_id))

        last_log_status_time = None
        start_time_s = time.time()
        timedout = False
        if wait_function is None:
            wait_function = default_wait_function
        while True:
            try:
                current_time_s = time.time()
                if(timeout_seconds != -1 and
                   current_time_s - start_time_s > timeout_seconds):
                    timedout = True
                    break

                transition_elem_type, status = get_status_cb(
                    transition_elem_instance_id)

                now = time.time()
                if last_log_status_time is None or (last_log_status_time +
                   JOB_INSTANCE_LOG_STATUS_INTERVAL_SECS) <= now:
                    log.debug(
                        'Transition element of type %s instance'
                        ' %s has status %s.' %
                        (repr(transition_elem_type),
                         repr(transition_elem_instance_id),
                         repr(status)))
                    last_log_status_time = now

                if (status in final_state_list):
                    log.debug(
                        'Transition element of type %s instance'
                        ' %s has terminated with status %s.'
                        % (repr(transition_elem_instance_id),
                           repr(transition_elem_type), repr(status)))
                    break
                else:
                    wait_function()
            except Exception as e:
                log.debug("Exception reading job status" + str(e))
                time.sleep(1)
        return timedout

    # Part of the public API.
    @visible_method
    def request_on_demand_snapshot(self, vm_id):
        log.debug('Requesting on-demand snapshot for %s' % vm_id)
        job_config = {'vmId': vm_id}
        return self.chosen_rest_client.post(
            '/job/type/backup',
            data=job_config)

    @visible_method
    def request_on_demand_snapshot_by_name(self, vm_name):
        # Let error propogate if vm not found
        vm_id = self.find_a_vm_by_name(vm_name)
        return self.request_on_demand_snapshot(vm_id)

    # Internally request a snapshot job.
    def request_snapshot_job(self, vm_id, preferred_node=None):
        job_config = {'vmId': vm_id}
        if preferred_node:
            job_config['preferredReplicas'] = [preferred_node]
        return self.create_job('backup', job_config)

    # Will return the description of the Status object returned, which on
    # success is the job_id of the job created.
    def create_snapshot_job(self, vm_id, preferred_node=None):
        status = self.request_snapshot_job(vm_id, preferred_node)
        return status['description']

    def reverse_increment_job(self,
                              vm_id,
                              min_increments,
                              min_change_rate):
        return self.create_job('reverseIncrement', {
            'vmId': vm_id,
            'minNumberOfSnapshotsToReverse': min_increments,
            'minChangeRateToReverse': min_change_rate
        })

    def cross_increment_job(self, vm_id, cut_off_time):
        return self.create_job('crossIncrement', {
            'vmId': vm_id,
            'cutoffTimeInSeconds': cut_off_time
        })

    def create_restore_job(self, snapshot_id, datastore_id):
        restoreJobConfig = {
            'snapshotId': snapshot_id
        }
        if(datastore_id != ''):
            restoreJobConfig['datastoreId'] = datastore_id
        return self.create_job('restore', restoreJobConfig)

    # TODO(adam): Rename this to remove 'job'.
    def create_export_job(self, snapshot_id, datastore_id, vm_name, host_id,
                          disableNetwork=False):
        exportJobConfig = {
            'snapshotId': snapshot_id,
            'datastoreId': datastore_id,
            'hostId': host_id,
            'disableNetwork': disableNetwork
        }
        if (vm_name != ''):
            exportJobConfig['vmName'] = vm_name
        return self.create_job('export',
                               exportJobConfig)

    def create_mount_job(self, snapshot_id, host_id, vm_name,
                         disableNetwork=False, preferred_node=None):
        mountJobConfig = {
            'snapshotId': snapshot_id,
            'hostId': host_id,
            'disableNetwork': disableNetwork
        }

        if preferred_node:
            mountJobConfig['nodeAffinity'] = [preferred_node]

        if (vm_name != ''):
            mountJobConfig['vmName'] = vm_name
        return self.create_job('mount',
                               mountJobConfig)

    def create_unmount_job(self, mount_id):
        return self.create_job('unmount', {
            'mountId': mount_id
        })

    def create_snapshot_integrity_job(self, vm_id, snapshot_ids=[]):
        return self.create_job('snapshot_integrity', {
            'vmId': vm_id,
            'snapshotIds': snapshot_ids
        })

    def create_refresh_job(self, vcenter_id):
        return self.create_job('refresh', {
            'vCenterId': vcenter_id
        })

    # The path has the following caveat
    # For windows, the backslash must be replaced with forward slash
    def create_download_file_job(self, snapshot_id, path):
        return self.create_job('download_file', {
            'snapshotId': snapshot_id,
            'path': path
        })

    # corrupt incremental snapshot 'corrupt_snapshot_id' by redirecting its
    # base blob pointers to 'dest_snapshot_id'
    def corrupt_snapshot_chain(self, vm_id, corrupt_snapshot_id):
        corrupt_chain = '/internal/snapshot/corrupt_chain'
        config = {
            'vmId': vm_id,
            'corruptSnapshotId': corrupt_snapshot_id
        }
        return self.chosen_rest_client.post(corrupt_chain, data=config)

    def handle_corrupt_snapshots_job(self, snapshot_ids):
        return self.create_job('handleCorruptSnapshots', {
            'snapshotIds': snapshot_ids
        })

    def delete_snapshot(self, snapshot_id):
        return self.chosen_rest_client.delete(
            '/snapshot/%s' % snapshot_id)

    def internal_expire_snapshot(self, snapshot_id, location_id=None):
        internal_expire = '/internal/snapshot/expire'
        config = {
            'snapshotId': snapshot_id
        }
        if location_id:
            config['locationId'] = location_id
        return self.chosen_rest_client.post(internal_expire, data=config)

    def internal_expire_snapshot_disk(self, snapshot_disk_id, location_id):
        internal_expire = '/internal/snapshot_disk/expire_snapshot_disk_chain'
        config = {
            'snapshotDiskId': snapshot_disk_id,
            'locationId': location_id
        }
        response_data = \
            self.chosen_rest_client.post(internal_expire, data=config)
        return response_data['diskIds']

    def consolidate_job(self, vm_id):
        return self.create_job('consolidate', {
            'vmId': vm_id
        })

    def index_job(self, vm_id):
        return self.create_job('index', {
            'vmId': vm_id
        })

    def start_download_from_cloud(self, vm_id, snapshot_id):
        return self.chosen_rest_client.post('/job/type/download_snapshot',
                                            data={
                                                'vmId': vm_id,
                                                'snapshotId': snapshot_id
                                            })

    @visible_method
    def get_vm(self, vm_id):
        return self.chosen_rest_client.get('/vm/%s' % vm_id)

    @visible_method
    def get_snapshot(self, snapshot_id):
        return self.chosen_rest_client.get('/snapshot/%s' % snapshot_id)

    def get_snapshot_disk(self, snapshot_disk_id):
        return self.chosen_rest_client.get(
            '/snapshot_disk/%s' % snapshot_disk_id)

    def get_snapshot_disk_and_blobs(self, snapshot_id, location_id):
        disks_and_blobs = '/internal/snapshot/disks_and_blobs'
        config = {
            'snapshotId': snapshot_id,
            'locationId': location_id
        }
        return self.chosen_rest_client.post(disks_and_blobs, data=config)

    @visible_method
    def get_snapshots_for_vm(self, vm_id):
        return self.chosen_rest_client.get('/snapshot', params={
            'vm': vm_id
        })

    def get_missed_snapshots_for_vm(self, vm_id):
        return self.chosen_rest_client.get('/snapshot/missed', params={
            'vm': vm_id
        })

    def add_guest_cred(self, domain, username, password):
        return self.chosen_rest_client.post('/guest_credential', data={
            'domain': domain,
            'username': username,
            'password': password
        })

    def get_mount(self, mount_id):
        return self.chosen_rest_client.get('/mount/%s' % mount_id)

    def get_is_bootstrapped(self):
        return self.chosen_rest_client.get('/isBootstrapped')

    def get_member_hostnames(self):
        return self.chosen_rest_client.get('/memberhostnames')

    def get_member_cluster_ips(self):
        return self.chosen_rest_client.get('/clusterIps')

    def modify_cluster_ips(self, ips):
        return self.chosen_rest_client.post('/clusterIps', data=ips)

    def get_cluster_ip_owner(self, ip):
        return self.chosen_rest_client.get('/cluster_ip/owner/%s' % ip)

    def get_protected_primary_storage(self):
        return self.chosen_rest_client.get('/stats/protectedPrimaryStorage')

    def get_mount_count(self):
        return self.chosen_rest_client.get('/mount/count')

    def get_snapshot_count(self):
        return self.chosen_rest_client.get('/snapshot/count')

    @visible_method
    def get_vm_count(self):
        return self.chosen_rest_client.get('/vm/count')

    def get_cross_compression(self):
        return self.chosen_rest_client.get('/stats/crossCompression')

    def get_live_snapshot_storage(self):
        return self.chosen_rest_client.get('/stats/liveSnapshotStorage')

    def get_physical_storage(self):
        return self.chosen_rest_client.get('/stats/physicalStorage')

    def get_physical_snapshot_storage(self):
        return self.chosen_rest_client.get('/stats/physicalSnapshotStorage')

    def get_available_storage(self):
        return self.chosen_rest_client.get('/stats/availableStorage')

    def get_logical_storage(self):
        return self.chosen_rest_client.get('/stats/logicalStorage')

    def get_ingested_storage(self):
        return self.chosen_rest_client.get('/stats/ingestedBytes')

    def get_cloud_storage(self):
        return self.chosen_rest_client.get('/stats/cloudStorage')

    def get_total_storage(self):
        return self.chosen_rest_client.get('/stats/totalStorage')

    def get_per_vm_storage(self, vm_id):
        return self.chosen_rest_client.get('/stats/perVmStorage/%s' % vm_id)

    def get_per_vm_physical_storage(self, vm_id):
        storage = self.get_per_vm_storage(vm_id)
        physical_storage =\
            storage['exclusivePhysicalBytes'] +\
            storage['sharedPhysicalBytes'] +\
            storage['indexStorageBytes']
        return physical_storage

    def get_total_mount_storage(self):
        return self.chosen_rest_client.get('/stats/liveSnapshotStorage')

    def get_per_mount_storage(self, mount_id):
        rest_client = self.chosen_rest_client
        return rest_client.get('/stats/perMountStorage/%s' % mount_id)

    def get_sla_domain_storage(self, sla_domain_id):
        rest_client = self.chosen_rest_client
        return rest_client.get('/stats/slaDomainStorage/%s' % sla_domain_id)

    def get_total_sla_domain_storage(self):
        return self.chosen_rest_client.get('/stats/slaDomainStorage')

    def get_physical_ingest(self):
        return self.chosen_rest_client.get('/stats/physicalIngest')

    def get_logical_ingest(self):
        return self.chosen_rest_client.get('/stats/logicalIngest')

    def get_snapshot_ingest(self):
        return self.chosen_rest_client.get('/stats/snapshotIngest')

    def get_streams(self):
        return self.chosen_rest_client.get('/stats/streams')

    def get_cloud_credentials(self):
        return self.chosen_rest_client.get('/cloud_credentials')

    def get_events(self, query=('limit=%s' % 25)):
        # TODO: Convert this to a GET call with URL/PATH params
        return self.chosen_rest_client.get('/events?%s' % query).get('data')

    def cancel_event(self, event_id):
        return self.chosen_rest_client.post('/event/cancel/%s' % event_id)

    def get_job_status(self, event_id):
        return self.chosen_rest_client.get('/job_status/%s' % event_id)

    @visible_method
    def search(self, vm_id, query):
        rest_client = self.chosen_rest_client
        return rest_client.get('/search?vmId=%s&query_string=%s' %
                               (vm_id, query))

    @visible_method
    def get_file_global(self, query):
        vm_summaries = self.get_vm_summaries()
        vm_ids = [resp_entry['id'] for resp_entry in vm_summaries if
                  resp_entry['snapshotCount'] > 0]
        results = {}

        for vm_id in vm_ids:
            try:
                search_results = self.search(vm_id, query)
                if search_results:
                    results[vm_id] = search_results
            except:
                # Do nothing TODO: fix once API error codes are made consistent
                pass
        return results

    def browse(self, snapshot_id, path):
        rest_client = self.chosen_rest_client
        return rest_client.get('/browse?snapshotId=%s&path=%s' %
                               (snapshot_id, path))

    def download(self, file_metadata_id):
        rest_client = self.chosen_rest_client
        return (rest_client,
                rest_client.get('/download/' + file_metadata_id))

    def download_file(self, handle, download_key):
        return handle.stream('/download_dir/' + download_key)

    @visible_method
    def download_closest_file(self, vm_name, filepath, target_date,
                              file_dest='.'):
        # Input date and time can be in any format dateutil.parser understands
        # If a timezone is included, all user-printable text will format using
        # it. Currently supports timezones in the nautical format (e.g. +0500).
        # Does not support all American timezone abbreviations as they are not
        # universal. However, it supports some (e.g. PST).
        # Filepath must be absolute, but file_dest can be relative or absolute.
        DISPLAY_DATE_FORMAT = "%Y-%m-%d %H:%M %z"

        try:
            filename = filepath.split('/')[-1]
        except:
            print 'Invalid filepath:', filepath

        try:
            target_date = parse(target_date)
        except:
            print ('Invalid target date:', target_date,
                   '. Example target date: 2016-03-10 19:04 -0500')

        # If target_date is a naive datetime, convert it to aware
        if not target_date.tzinfo:
            target_date = pytz.utc.localize(target_date)
        target_tz = target_date.tzinfo

        print 'Searching for the backup closest to', target_date

        vm_id = self.find_a_vm_by_name(vm_name)
        files = self.search(vm_id, filepath)
        files = [f['fileVersions'] for f in files if f['path'] == filepath][0]
        if not files:
            return 'No backups of', filename, 'on', vm_name, 'exist.'

        file_time_deltas = [(abs(parse(f['lastModified']) - target_date),
                            f['snapshotId'], parse(f['lastModified']))
                            for f in files]

        _, closest_snapshot_id, last_modified = min(file_time_deltas)

        print 'Identified snapshot where file was last modified on', \
              last_modified.astimezone(target_tz).strftime(DISPLAY_DATE_FORMAT)

        download_job_id = self.create_download_file_job(closest_snapshot_id,
                                                        filepath)
        print "Preparing your file... this may take a moment."
        self.wait_for_job_instance(download_job_id)

        current_user = self.find_a_user_by_username(self.username)
        notifications = self.get_notifications(current_user)

        # Gets most recent download (TODO: fix when API returns file download
        # metadata id directly)
        file_dl_metadata_id = None
        for notification in reversed(notifications):
            if notification['name'] == 'DOWNLOAD_FILE':
                info = json.loads(notification['notificationInfo'])
                if info['jobId'] == download_job_id:
                    file_dl_metadata_id = info['fileDownloadMetadataId']
                    break

        if not file_dl_metadata_id:
            raise Exception('Failed to download requested file.')

        handle, download_result = self.download(file_dl_metadata_id)
        content = download_result['contentPath']
        download_key = content.replace('download_dir/', '')
        downloaded_file = self.download_file(handle, download_key)
        desired_filename = '/'.join([file_dest, filename])
        shutil.move(downloaded_file, desired_filename)

        return 'File successfully downloaded to ' + desired_filename

    def add_iscsi_autodiscover(self,
                               target_hostname,
                               target_port,
                               username=None,
                               password=None,
                               username_in=None,
                               password_in=None,
                               auth_discovery=False):
        portalDetails = {
            'host': target_hostname,
            'port': target_port,
        }
        if username:
            portalDetails['username'] = username
            portalDetails['password'] = password
        if username_in:
            portalDetails['usernameIn'] = username_in
            portalDetails['passwordIn'] = password_in

        rest_client = self.chosen_rest_client
        try:
            rest_client.post('/addIscsiAutoDiscover', data={
                'portalDetails': portalDetails,
                'authDiscovery': auth_discovery
            })
        except Exception:
            raise Exception('Failed to connect to iscsi target %s' %
                            target_hostname)

    def add_oracle_db(self,
                      connect_string,
                      username,
                      password,
                      mount_prefix,
                      ip_addresses):
        rest_client = self.chosen_rest_client
        database_config = {
            'connect_string': connect_string,
            'username': username,
            'password': password,
            'mount_prefix': mount_prefix,
            'ip_addresses': ip_addresses
        }
        return rest_client.post('/oracledb', data=database_config)

    def delete_oracle_db(self, dbid):
        rest_client = self.chosen_rest_client
        return rest_client.delete('/oracledb/%s' % dbid)

    def update_oracle_db(self,
                         dbid,
                         connect_string=None,
                         username=None,
                         password=None,
                         mount_prefix=None,
                         ip_addresses=None):
        update_info = {
            'connect_string': connect_string,
            'username': username,
            'password': password,
            'mount_prefix': mount_prefix,
            'ip_addresses': ip_addresses
        }

        # Remove all None entries
        update_info = {key: value for key, value
                       in update_info.iteritems() if value is not None}

        rest_client = self.chosen_rest_client
        return rest_client.patch('/oracledb/%s' % dbid, data=update_info)

    def get_oracle_backups_for_db(self, dbid):
        rest_client = self.chosen_rest_client
        return rest_client.get('/oracledb_backup?db=%s' % dbid)

    def get_datacenter(self, datacenter_id):
        rest_client = self.chosen_rest_client
        return rest_client.get('/data_center/%s' % datacenter_id)

    def get_root_vm_folder(self, datacenter_id):
        rest_client = self.chosen_rest_client
        return rest_client.get('/folder/vm/%s' % datacenter_id)

    def get_folder(self, folder_id):
        rest_client = self.chosen_rest_client
        return rest_client.get('/folder/%s' % folder_id)

    def get_datastore(self, datastore_id):
        rest_client = self.chosen_rest_client
        return rest_client.get('/datastore/%s' % datastore_id)

    def find_folder_id(self, folder_path, parent_folder):
        folder_name = folder_path[0]
        folder_id = [e['id'] for e in parent_folder['entities']
                     if e['name'] == folder_name and
                     e['entityType'] == 'Folder'][0]
        if len(folder_path) == 1:
            return folder_id
        else:
            folder = self.get_folder(folder_id)
            return self.find_folder_id(folder_path[1:], folder)

    def add_auth_domain(self, dns_name, admin_username, admin_password):
        rest_client = self.chosen_rest_client
        return rest_client.post('/auth_domain',
                                data={
                                    'dnsName': dns_name,
                                    'adminUserName': admin_username,
                                    'adminPassword': admin_password
                                })

    def get_auth_domains(self):
        return self.chosen_rest_client.get('/auth_domain')

    def delete_auth_domain(self, auth_domain_id):
        return self.chosen_rest_client\
            .delete('/auth_domain/%s' % auth_domain_id)

    def get_backup_jobs_daily_report_summary(self):
        rest_client = self.chosen_rest_client
        return rest_client.post('/report/backupJobs/summary', data={
            'reportType': 'daily'
        })

    def get_backup_jobs_weekly_report_summary(self):
        rest_client = self.chosen_rest_client
        return rest_client.post('/report/backupJobs/summary', data={
            'reportType': 'weekly'
        })

    def get_sla_compliance_report_summary(self):
        rest_client = self.chosen_rest_client
        return rest_client.get('/report/slaCompliance/summary')

    def get_system_capacity_report_summary(self):
        rest_client = self.chosen_rest_client
        return rest_client.get('/report/systemCapacity/summary')

    def get_backup_jobs_daily_report_detail(self):
        rest_client = self.chosen_rest_client
        return rest_client.post('/report/backupJobs/detail', data={
            'reportType': 'daily'
        })

    def get_backup_jobs_weekly_report_detail(self):
        rest_client = self.chosen_rest_client
        return rest_client.post('/report/backupJobs/detail', data={
            'reportType': 'weekly'
        })

    def get_sla_compliance_report_detail(self):
        rest_client = self.chosen_rest_client
        return rest_client.get('/report/slaCompliance/detail')

    def get_system_capacity_report_detail(self):
        rest_client = self.chosen_rest_client
        return rest_client.get('/report/systemCapacity/detail')

    def disconnect_datalocation(self, datalocation_id):
        rest_client = self.chosen_rest_client
        response = rest_client.post('/internal/data_location/disconnect',
                                    data={'dataLocationId': datalocation_id})
        assert response['status'] is 0, response['message']

    def get_virtual_disk(self, virtual_disk_id):
        rest_client = self.chosen_rest_client
        return rest_client.get('/virtual/disk/%s' % virtual_disk_id)

    def register_host(self,
                      ip_address):
        rest_client = self.chosen_rest_client
        return rest_client.post('/host', data={
            'hostname': ip_address
        })

    def get_host(self,
                 host_uuid):
        rest_client = self.chosen_rest_client
        return rest_client.get('/host/%s' % host_uuid)

    def get_all_hosts(self):
        rest_client = self.chosen_rest_client
        return rest_client.get('/host')

    def add_fileset(self,
                    hostUuid,
                    uuid,
                    name,
                    includes):
        rest_client = self.chosen_rest_client
        return rest_client.post('/fileset', data={
            'hostId': hostUuid,
            'id': uuid,
            'name': name,
            'managedId': '',
            'primaryClusterId': '',
            'includes': includes
        })

    def get_fileset(self,
                    host_uuid,
                    fileset_uuid):
        rest_client = self.chosen_rest_client
        return rest_client.get('/fileset/%s' % (
            host_uuid + ":::" + fileset_uuid)).get('data')

    def open_support_tunnel(self):
        return self.chosen_rest_client.post('/support/tunnel')

    def close_support_tunnel(self):
        return self.chosen_rest_client.delete('/support/tunnel')

    @visible_method
    def export_vm_by_name(self, vm_name, vmware_host_name, datastore_name,
                          target_date):
        DISPLAY_DATE_FORMAT = "%Y-%m-%d %H:%M %z"
        vm_id = self.find_a_vm_by_name(vm_name)
        host_id = self.find_a_vmware_host_by_name(vmware_host_name)
        datastore_id = self.find_a_ds_by_name(datastore_name)
        snapshots = self.get_snapshots_for_vm(vm_id)

        try:
            target_date = parse(target_date)
        except:
            print ('Invalid target date:', target_date,
                   '. Example target date: 2016-03-10 19:04 -0500')

        # If target_date is a naive datetime, convert it to aware
        if not target_date.tzinfo:
            target_date = pytz.utc.localize(target_date)
        target_tz = target_date.tzinfo

        print 'Searching for the snapshot closest to', target_date

        snapshot_time_deltas = [(abs(parse(snapshot['date']) - target_date),
                                snapshot['id'], parse(snapshot['date']))
                                for snapshot in snapshots]

        _, closest_snapshot_id, snapshot_date = min(snapshot_time_deltas)

        print 'Identified snapshot taken on', \
              snapshot_date.astimezone(target_tz).strftime(DISPLAY_DATE_FORMAT)

        print 'Requesting export. This might take a few minutes...'
        export_job_id = self.create_export_job(closest_snapshot_id,
                                               datastore_id, vm_name, host_id)

        self.wait_for_job_instance(export_job_id)

        current_user = self.find_a_user_by_username(self.username)
        notifications = self.get_notifications(current_user)

        # Check for export job status
        notificationInfo = None
        for notification in reversed(notifications):
            if notification['name'] == 'EXPORT_SNAPSHOT':
                notificationInfo = json.loads(notification['notificationInfo'])
                if notificationInfo['jobId'] == export_job_id:
                    break

        if not notificationInfo:
            raise Exception('Failed to export requested snapshot.')

        return notificationInfo


def method_usage_string(method, method_name):
    (args, varargs, keywords, defaults) = inspect.getargspec(method)
    if defaults is None:
        defaults = []
    optional_arg_index = len(args) - len(defaults)

    required_arg_strings = map(lambda arg_name: '<%s>' % arg_name,
                               args[1:optional_arg_index])
    optional_arg_strings = map(lambda arg_name: '[%s]' % arg_name,
                               args[optional_arg_index:])
    return '%s %s' % (method_name,
                      ' '.join(required_arg_strings + optional_arg_strings))


def result_string(result):
    return json.dumps(result, indent=2, sort_keys=True)


def print_result(result):
    output = result_string(result)

    jq_path = find_executable(JQ)
    if sys.stdout.isatty() and jq_path is not None:
        child = subprocess.Popen([jq_path, '.'], stdin=subprocess.PIPE)
        child.communicate(output)
    else:
        print(output)


def eval_or_str(arg):
    try:
        # Use eval with global variables simulating lower case keywords so the
        # overall syntax is a superset of JSON while also offering conveniences
        # of Python such as single quoted strings and doing dynamic
        # computations.
        return eval(
            arg,
            {
                'true': True,
                'false': False,
                'null': None
            })
    except:
        return str(arg)

def main(argv=None):
    # NB(dar): By default, do not log debug-level messages to disk, since these
    # include passwords. This setting may be overwritten in a test/dev
    # environment by setting the LOG_FILE_LEVEL environment variable.
    if argv is None:
        argv = sys.argv

    init_logging(log_file_level='INFO')

    tmp_tool = RubrikTool(['localhost'], None, None)

    def is_visible_method(name):
        return (inspect.ismethod(getattr(tmp_tool, name)) and
                not name.startswith('_') and
                not name[0].isupper() and
                'user_visible_method' in getattr(tmp_tool, name).func_dict)

    all_method_names = dir(tmp_tool)
    method_names = sorted(filter(is_visible_method, all_method_names))

    parser = argparse.ArgumentParser(
        description='Interact with the Rubrik REST API.',
        epilog='AVAILABLE METHOD TARGETS: ' + ', '.join(method_names))
    parser.add_argument('-H', '--host', dest='host', type=str,
                        action='append',
                        help='REST API host, can be passed multiple times ' +
                             'to use multiple hosts')
    parser.add_argument('-X', '--request', dest='request_method', type=str,
                        default='GET', help='HTTP request method')
    parser.add_argument('-d', '--data', dest='data', type=str,
                        help='HTTP request body')
    parser.add_argument('-t', '--target-help', dest='target_help',
                        action='store_true', help='Get help on the target')
    parser.add_argument('-p', '--password', dest='password', type=str,
                        help='REST API password')
    parser.add_argument('-u', '--username', dest='username', type=str,
                        help='REST API username')
    parser.add_argument('target', type=str,
                        help='tool_method or /rest_path')
    parser.add_argument('target_args', type=str, nargs='*',
                        help='arguments for target')

    args = parser.parse_args(argv[1:])

    if args.host is None or len(args.host) == 0:
        hosts = ['localhost']
    else:
        hosts = args.host
    api_base_urls = map(lambda host: 'https://%s' % host, hosts)

    tool = RubrikTool(api_base_urls, args.username, args.password)
    try:
        if args.target.startswith('/'):
            endpoint = args.target

            if (args.target_help):
                log.error('Target help not available for raw endpoints.')
                sys.exit(1)

            rest = tool.chosen_rest_client
            result = rest.request(args.request_method, endpoint,
                                  data=eval_or_str(args.data))
            print_result(result)
        else:
            method_name = args.target
            try:
                method = getattr(tool, method_name)
            except AttributeError:
                log.error('No method named %s' % repr(method_name))
                sys.exit(1)

            if args.target_help:
                print('Usage:\n    %s %s' %
                      (os.path.basename(__file__),
                       method_usage_string(method, method_name)))
            else:
                target_arg_values = map(eval_or_str, args.target_args)
                result = method(*target_arg_values)
                print_result(result)
    except requests.exceptions.HTTPError as e:
        log.exception('Server returned HTTP error %s. Response content:\n%s' %
                      (repr(e.response.status_code), e.response.content))
        sys.exit(1)
    except Exception as e:
        log.exception('Encountered error.')

def cli_entry_point():
    main(sys.argv)

if __name__ == "__main__":
    main(sys.argv)
