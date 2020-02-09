"""
cluster
"""
from enum import Enum


class Cluster(Enum):
    """
    Status for the projects, documents and job
    """
    template = 'templateformat'
    type = 'type'
    cluster_name = 'cluster_name'
    properties = 'properties'
    region = 'region'
    created_date = 'created_date'
    updated_date = 'updated_date'
    cluster_settings_name = {'rel': 'name', 'abs': 'properties.clustersettings.name'}
    cluster_settings_value = {'rel': 'value', 'abs': 'properties.clustersettings.value'}
    tags = {'rel': 'tags', 'abs': 'properties.tags'}
    tags_key = {'rel': 'key', 'abs': 'properties.tags.key'}
    tags_value = {'rel': 'value', 'abs': 'properties.tags.value'}
