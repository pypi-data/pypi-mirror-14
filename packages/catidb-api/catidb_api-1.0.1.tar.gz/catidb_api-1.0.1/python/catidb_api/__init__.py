# -*- coding: utf-8 -*-
from __future__ import print_function

import requests
import os
import traceback
import uuid

catidb_hostname = 'cati'
catidb_url = 'https://cati.cea.fr/catidb3'
api_prefix = '/api/1'
global_study_name = 'cati'
indexation_lock = '/tmp/indexation.lock'
# Format of datetime used in action file name
action_ftime = '%Y%m%d_%H%M%S'

from catidb_api.store_passwords import find_login_and_password


class CatiDB(object):
    def __init__(self, url, login, password):
        if url.endswith('/'):
            self.url = url[:-1] + api_prefix
        else:
            self.url = url + api_prefix
        self.login = login
        self.password = password
        # After login, an encrypted cookie is sent by the server and must
        # be kept and send in all requests for authentication.
        self.cookies = {}

    def test_connection(self, timeout=10):
        """
        Test if we can login to the server. On success the method returns True.
        Otherwise, it raises an exception. Common cases are:
            requests.exceptions.ConnectionError: the server is not reachable
            requests.exceptions.HTTPError with code 403: bad login/passwd
        """
        response = requests.post(self.url + '/login',
                                 data={'login': self.login,
                                        'password': self.password},
                                 timeout=timeout)
        # Raises the requests exception if login failed
        response.raise_for_status()
        # Login is successful, store the authentication cookie
        self.cookies = response.cookies
        return True

    def call_server(self, route, method="get", params=None, files=None):
        '''
        method
        ------

        method can be one of "get", "post", "put", and "delete".
        '''
        def send(route, method, params, files=None):
            if method == "post":
                kwargs = {}
                kwargs["data"] = params
                kwargs["files"] = files
                kwargs["cookies"] = self.cookies
                return requests.post(url, **kwargs)
            elif method == "get":
                return requests.get(url, params=params,
                                    cookies=self.cookies)
            elif method == "put":
                return requests.put(url, data=params,
                                    cookies=self.cookies)
            elif method == "delete":
                kwargs = {}
                kwargs["params"] = params
                kwargs["files"] = files
                kwargs["cookies"] = self.cookies
                return requests.delete(url, **kwargs)
            else:
                raise ValueError("method %s cannot be recognized." % method)

        if route.startswith('/'):
            url = self.url + route
        else:
            url = self.url + '/' + route

        # Try to get an answer with the current authentication information
        response = send(url, method, params, files)
        if response.status_code == requests.codes.ok:
            # Request is successful
            if response.cookies:
                # For security reason, the server can update the cookie
                # from time to time. If a new cookie is sent, we update
                # self.cookies
                self.cookies = response.cookies
            # Return the dictionary extracted from the JSON answer
            return response.json()
        if response.status_code in (requests.codes.forbidden,
                                    requests.codes.UNAUTHORIZED,
                                    500):
            # Authorization is not known by the server => try to login
            response = requests.post(self.url + '/login',
                                     data={
                                         'login': self.login,
                                         'password': self.password})
            # Raises the requests exception if login failed
            response.raise_for_status()
            # Login is successful, store the authentication cookie
            self.cookies = response.cookies
            # Now retry the call with new cookie coming from login
            response = send(url, method, params, files)
        # Raises exception if any
        response.raise_for_status()
        return response.json()

    def call_server_get(self, route, **params):
        return self.call_server(route, method="get", params=params)

    def call_server_post(self, route, params, files=None):
        return self.call_server(route, method="post", params=params,
                                files=files)

    def call_server_put(self, route, params, files=None):
        return self.call_server(route, method="put", params=params,
                                files=files)

    def call_server_delete(self, route, params, files=None):
        return self.call_server(route, method="delete", params=params,
                                files=files)

    def study_codes(self):
        '''
        Returns the identifier of all accessible studies.
        '''
        studies_name = [i[0] for i in self.call_server_get(
            'studies',
            _fields='name',
            _as_list=True)]
        return sorted(studies_name)

    def study_info(self, study_code):
        '''
        Returns a dictionary with study information
        '''
        return self.call_server_get(
            'studies',
            name=study_code)

    def timepoints(self, study):
        '''
        Returns the list of timepoints for a given study
        '''
        return [i[0] for i in self.call_server_get(
            '%s/time_points' % study.lower(),
            _fields='label',
            _as_list=True,
            _order_by='order_')]

    def add_timepoint(self, study, label, order, study_label=None):
        """
        Add a timepoint to a study.
        """
        # Collect arguments in a dict
        params = {
            "label": label, "order": order, "study_label": study_label
        }
        route = '%s/time_points' % study.lower()
        return self.call_server_post(route, params=params)

    #def groups(self, study):
        #'''
        #Returns the groups belonging to a given study
        #'''
        #raise NotImplementedError()

    def subject_codes(self, study):
        '''
        Returns the subject code for each subject involved in a given study.
        If center is not None, returns only the subjects of that center.
        '''
        return [i[0] for i in self.call_server_get(
            '%s/subjects' % study.lower(),
            _fields='subject_code',
            _as_list=True,
            _order_by='subject_code')]

    def subjects_info(self, study, subject_codes=None):
        '''
        Returns a list of subjects information eventually limited
        to the given subject codes.
        '''
        raise NotImplementedError()

    def recruitment_center_codes(self, study):
        '''
        Returns the recruitment center code for each center involved in a given study.
        except global_study_name
        '''
        return [i[0] for i in self.call_server_get(
            '%s/action/recruitment_center' % study.lower(),
            _fields='code',
            _distinct=True,
            _as_list=True,
            _orderby='code')]

    #def center_info(self, study, center_code):
        #'''
        #Returns the full name of the center given its code and the study it
        #belongs to.
        #'''
        #return [i[0] for i in self.call_server_get(
            #'%s/action/new_center' % study.lower(),
            #_fields='label',
            #_distinct=True,
            #_as_list=True) if i[0] is not None]

    def action_names(self, study):
        '''
        Returns a generic list of the different actions existing on the database.
        Can be filter by study
        '''
        return [i[0] for i in self.action_attribute_definition(
            study,
            _fields='action_name',
            _distinct=True,
            _as_list=True) if i[0] is not None]

    def paths(self, study, **kwargs):
        '''
        Return a list of dictionaries containing information for selected
        files.
        '''
        return self.call_server_get(
            '%s/paths' % study.lower(),
            **kwargs)

    def action_files_info(self, study, **filter):
        '''

        1. Return the actions which has been indexed.

        [{"last_modification": "2015-08-27 09:48:50.789817",
          "center_code": "101",
          "subject_code": "101_S_0001",
          "actions_file": "fake/ACTIONS/101/101_S_0001/M0/IRM/freesurfer_20150624_105212.actions.json",
          "time_point": "M0", "action_id": 3}, ]

        '''
        return self.call_server_get(
            '%s/indexed_actions' % study.lower(),
            **filter)

    def action_contents(self, study, action_name, **filter):
        '''
        Returns a list of dictionaries containing information about actions
        '''
        return self.call_server_get(
            '%s/action/%s' % (study.lower(), action_name),
            **filter)

    def action_attribute_definition(self, study, action_name=None, **filter):
        '''
        Returns the actions attributes of a given study.
        If action_name is None, returns all the actions attributes.
        '''
        if action_name is None:
            return self.call_server_get(
                '%s/actions' % study.lower(),
                **filter)
        return self.call_server_get(
            '%s/actions' % study.lower(),
            action_name=action_name,
            **filter)

    #def subject_from_path(self, study, path):
        #'''
        #Returns the subject code related to a filepath existing on the database.
        #'''
        #return [i[0] for i in self.paths(study,
                                         #path=path,
                                         #_fields='subject_code',
                                         #_as_list=True,
                                         #_distinct=True)
                #if i[0] is not None]

    def get_study_from_path(self, path):
        '''
        Returns the study name associated to a given path
        '''
        return path.split(os.sep)[0].lower()

    def delete_actions_file(self,
                            study,
                            rpath,
                            ):
        '''
        rpath
        -----
        relative path for the action file. For example:
            "fake/ACTIONS/new_center_20150413_120501.actions.json"
        '''
        params = {"path": rpath}
        route = "/%s/delete_action_by_path" % study
        try:
            json_ret = self.call_server_post(route, params=params)
        except:
            print(traceback.format_exc())
            return False
        if json_ret["msg"] == "success":
            return True
        else:
            print(json_ret["msg"])
            return False

    def input_paths_from_output_path(self, path):
        '''
        Returns a list of dictionaries containing inputs name and path
        from a given path
        '''
        #get study name
        study = self.get_study_from_path(path)
        #get action name
        d = self.call_server_get('%s/paths' % study.lower(),
                                 path=path,
                                 _fields='generated_by_action, action_id')
        action_name = d[0]['generated_by_action']
        action_id = d[0]['action_id']
        #get input parameter from action name
        input_parameters = [e['parameter'] for e in
                            self.action_attribute_definition(study, action_name)
                            if e['is_output'] is False]
        return self.action_contents(study,
                                    action_name=action_name,
                                    action_id=action_id,
                                    _fields=input_parameters)

    def get_float_attributes_names(self, study, action_name):
        '''
        Returns a list containing all float attributes names
        (or label of the attribute name if it exists) from an action name given
        '''
        return [e['label'] if 'label' in e else e['parameter'] for e in
                self.action_attribute_definition(study, action_name)
                if e['trait_type'] == 'Float']

    def fli_iam_set_study(self, study, num_files=0, is_published=False):
        params = {
            "is_published": is_published,
            "num_files": num_files
            }
        return self.call_server_put("%s/fli_iam_study" % study, params)

    def acquisition_descriptions(self, **filter):
        """
        Returns the description of the acquisition.
        """
        return self.call_server_get('acquisition_portfolio',
                                    **filter)

    def add_acquisition_description(self, code, modality, short_description,
                                    description):
        """
        Add an acquisition to the acquisition portfolio
        """
        # Collect arguments in a dict
        params = {
            "code": code,
            "modality": modality,
            "short_description": short_description,
            "description": description
        }
        return self.call_server_post('acquisition_portfolio', params=params)

    def expected_acquisitions(self, study, timepoint):
        """
        Return the expected acquisitions for the given study & timepoint.
        """
        route = "{study}/expected_acquisitions".format(study=study)
        return self.call_server_get(route,
                                    timepoint=timepoint)

    def add_expected_acquisition(self, study, timepoint,
                                 acquisition_description_uuid):
        """
        Insert the acquisition represented by acquisition_description_uuid for
        the given study & timepoint.
        """
        # Collect arguments in a dict
        params = {
            "timepoint": timepoint,
            "acquisition_description_uuid": acquisition_description_uuid
        }
        route = "{study}/expected_acquisitions".format(study=study)
        return self.call_server_post(route, params=params)

    def remove_expected_acquisition(self, study, timepoint,
                                    acquisition_description_uuid):
        """
        Remove the acquisition represented by acquisition_description_uuid for
        the given study & timepoint.
        """
        # Collect arguments in a dict
        params = {
            "timepoint": timepoint,
            "acquisition_description_uuid": acquisition_description_uuid
        }
        route = "{study}/expected_acquisitions".format(study=study)
        return self.call_server_delete(route, params=params)


def get_catidb(login=None, password=None, server=None, test_connection=True):
    '''
    Returns a CatiDB derived instance or raise an exception.

    Example
    -------
    >>> import sys
    >>> try:
    ...     db = get_catidb()
    ... except requests.exceptions.ConnectionError:
    ...     print("Can't contact server", file=sys.stderr)
    ... except requests.exceptions.HTTPError as e:
    ...     if e.response.status_code == requests.codes.FORBIDDEN:
    ...         print("Invalid login/passwd", file=sys.stderr)
    ...     else:
    ...         print("Unkwown HTTP error", file=sys.stderr)
    ... except Exception as e:
    ...         print("Unkwown error", file=sys.stderr)
    '''
    if server is None:
        server = catidb_url
    if login is None:
        login, password = find_login_and_password(server)
    db = CatiDB(server, login, password)
    # Test
    if test_connection:
        db.test_connection()
    return db


def create_uuid():
    """
    Return a standard uuid to use for Cati DB objects.
    """
    return uuid.uuid4()
