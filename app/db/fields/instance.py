"""
Instance
"""
from enum import Enum


class Instance(Enum):
    """
    Status for the projects, documents and job
    """
    cluster_id = 'cluster_id'
    instancename = 'instance_name'
    region = 'region'
    type = 'type'
    state = 'state'
    created_date = 'created_date'
    updated_date = 'updated_date'
    properties = 'properties'
    tags = {'rel': 'tags', 'abs': 'properties.tags'}
    tags_key = {'rel': 'key', 'abs': 'properties.tags.key'}
    tags_value = {'rel': 'value', 'abs': 'properties.tags.value'}
    instancetype = {'rel':'instance_type', 'abs':'properties.instance_type'}
    image = {'rel': 'image', 'abs': 'properties.image'}
    os = {'rel': 'os', 'abs': 'properties.image.os'}
    virtualization = {'rel': 'virtualization', 'abs': 'properties.image.virtualization'}
    architecture = {'rel': 'architecture', 'abs': 'properties.image.architecture'}
    storage = {'rel': 'os', 'abs': 'properties.image.storage'}
    ip = {'rel': 'ip_address', 'abs': 'properties.image.ip_address'}
    keypair = {'rel':'keypair', 'abs': 'properties.keypair'}
    keypair_name = {'rel':'name', 'abs': 'properties.keypair.name'}
    keypair_format = {'rel':'format', 'abs': 'properties.keypair.format'}
    securitygroups = {'rel': 'security_groups', 'abs': 'properties.security_groups'}
    securitygroups_name = {'rel': 'name', 'abs': 'properties.security_groups.name'}
    securitygroups_vpc = {'rel': 'vpc', 'abs': 'properties.security_groups.vpc'}



