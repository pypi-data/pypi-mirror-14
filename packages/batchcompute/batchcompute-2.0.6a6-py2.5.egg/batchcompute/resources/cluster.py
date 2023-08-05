import copy

from batchcompute.utils import (partial, add_metaclass, CamelCasedClass)
from batchcompute.utils.jsonizable import Jsonizable
from batchcompute.utils.constants import (STRING, NUMBER, TIME)

class GroupDescription(Jsonizable):
    '''
    Description class of the group resource type in batchcompute service.
    '''
    descriptor_type = 'data descriptor'
    descriptor_map = {
        'DesiredVMCount': NUMBER,
        'InstanceType': STRING,
        'ResourceType': STRING,
    }
    required = [
        'DesiredVMCount'
    ]

    def __init__(self, dct={}):
        super(GroupDescription, self).__init__(dct)
        if 'ResourceType' not in self._d:
            self.setproperty('ResourceType', 'OnDemand')
        if 'InstanceType' not in self._d:
            self.setproperty('InstanceType', '')
GroupDescription = add_metaclass(GroupDescription, CamelCasedClass)

class ClusterDescription(Jsonizable):
    '''
    Description class of the cluster resource type in batchcompute service.
    '''
    resource_name = 'clusters'
    descriptor_type = 'data descriptor'
    descriptor_map = {
        'Name': STRING,
        'Description': STRING,
        'ImageId': STRING,
        'UserData': dict,
        'Groups': dict,
    }
    required = [
        'Name', 
        'ImageId', 
        'Groups'
    ]

    def __init__(self, dct={}):
        super(ClusterDescription, self).__init__(dct)
        if 'Groups' not in self._d:
            self.setproperty('Groups', {})
        if 'UserData' not in self._d:
            self.setproperty('UserData', {})

    def setproperty(self, key, value):
        super_set = super(ClusterDescription, self).setproperty
        if key == 'Groups' and isinstance(value, dict):
            new_value = {}
            for group_name in value:
                new_value[group_name] = self._validate_group(value[group_name])
        else:
            new_value = value
        super_set(key, new_value)

    def _validate_group(self, group):
        return copy.deepcopy(group) if isinstance(group, GroupDescription) else GroupDescription(group)

    def add_group(self, group_name, group):
        if not group_name and not isinstance(group_name, STRING):
            raise TypeError('''Task name must be str and can't be empty ''')
        self._d['Groups'][group_name] = self._validate_group(group)

    def delete_group(self, group_name):
        if group_name in self._d['Groups']:
            del self._d['Groups'][group_name]
        else:
            pass

    def get_group(self, group_name):
        if group_name in self._d['Groups']:
            return self._d['Groups'][group_name]
        else:
            raise KeyError(''''%s' is not a valid group name''' % group_name)
ClusterDescription = add_metaclass(ClusterDescription, CamelCasedClass)
