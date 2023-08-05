import pytest

from sigopt.objects import *

class TestBase(object):
  def test_equality(self):
    assert Experiment({}) == Experiment({})
    assert Experiment({}) != {}
    assert {} != Experiment({})
    assert Bounds({}) != Experiment({})

    assert Experiment({'a': 'b'}) == Experiment({'a': 'b'})
    assert Experiment({'a': 'b'}) != Experiment({})
    assert Experiment({'a': 'b'}) != Experiment({'a': 'c'})
    assert Experiment({'a': 'b'}) != Experiment({'a': 'b', 'c': 'd'})

  def test_repr(self):
    assert repr(Experiment({})) == 'Experiment({})'
    assert repr(Experiment({'a': 'b'})) == 'Experiment({"a": "b"})'
    assert repr(Bounds({'a': 'b'})) == 'Bounds({"a": "b"})'

  def test_json(self):
    assert Experiment({}).to_json() == {}
    assert Experiment({'bounds': {'min': 1, 'max': 2}}).to_json() == {'bounds': {'min': 1, 'max': 2}}


class TestObjects(object):
  def test_experiment(self):
    experiment = Experiment({
      'object': 'experiment',
      'id': '123',
      'name': 'Test Experiment',
      'type': 'offline',
      'created': 321,
      'state': 'active',
      'metric': {
        'object': 'metric',
        'name': 'Revenue',
      },
      'can_be_deleted': True,
      'client': '678',
      'progress': {
        'object': 'progress',
        'observation_count': 3,
        'first_observation': {
          'object': 'observation',
          'id': '1',
          'assignments': {
            'a': 1,
            'b': 'c',
          },
          'value': 3.1,
          'value_stddev': None,
          'failed': False,
          'created': 451,
          'suggestion': '11',
          'experiment': '123',
        },
        'last_observation': {
          'object': 'observation',
          'id': '2',
          'assignments': {
            'a': 2,
            'b': 'd',
          },
          'value': 3.1,
          'value_stddev': 0.5,
          'failed': False,
          'created': 452,
          'suggestion': '12',
          'experiment': '123',
        },
        'best_observation': {
          'object': 'observation',
          'id': '3',
          'assignments': {
            'a': 3,
            'b': 'd',
          },
          'value': None,
          'value_stddev': None,
          'failed': True,
          'created': 453,
          'suggestion': '13',
          'experiment': '123',
        },
      },
      'parameters': [
        {
          'object': 'parameter',
          'tunable': True,
          'name': 'a',
          'type': 'double',
          'bounds': {
            'object': 'bounds',
            'min': 1,
            'max': 2,
          },
          'categorical_values': None,
          'precision': 3,
          'default_value': 2,
        },
        {
          'object': 'parameter',
          'tunable': False,
          'name': 'b',
          'type': 'categorical',
          'bounds': None,
          'categorical_values': [
            {'name': 'c', 'enum_index': 1},
            {'name': 'd', 'enum_index': 2},
          ],
          'precision': None,
          'default_value': None,
        },
      ],
    })

    assert experiment.id == '123'
    assert experiment.name == 'Test Experiment'
    assert experiment.type == 'offline'
    assert experiment.created == 321
    assert isinstance(experiment.metric, Metric)
    assert experiment.metric.name == 'Revenue'
    assert experiment.can_be_deleted is True
    assert experiment.client == '678'
    assert isinstance(experiment.progress, Progress)
    assert experiment.progress.observation_count == 3
    assert isinstance(experiment.progress.first_observation, Observation)
    assert experiment.progress.first_observation.id == '1'
    assert isinstance(experiment.progress.first_observation.assignments, Assignments)
    assert experiment.progress.first_observation.assignments.get('a') == 1
    assert experiment.progress.first_observation.assignments.get('b') == 'c'
    assert experiment.progress.first_observation.value == 3.1
    assert experiment.progress.first_observation.value_stddev is None
    assert experiment.progress.first_observation.failed is False
    assert experiment.progress.first_observation.created == 451
    assert experiment.progress.first_observation.suggestion == '11'
    assert experiment.progress.first_observation.experiment == '123'
    assert isinstance(experiment.progress.last_observation, Observation)
    assert experiment.progress.last_observation.id == '2'
    assert isinstance(experiment.progress.last_observation.assignments, Assignments)
    assert experiment.progress.last_observation.assignments.get('a') == 2
    assert experiment.progress.last_observation.assignments.get('b') == 'd'
    assert experiment.progress.last_observation.value == 3.1
    assert experiment.progress.last_observation.value_stddev is 0.5
    assert experiment.progress.last_observation.failed is False
    assert experiment.progress.last_observation.created == 452
    assert experiment.progress.last_observation.suggestion == '12'
    assert experiment.progress.last_observation.experiment == '123'
    assert isinstance(experiment.progress.best_observation, Observation)
    assert experiment.progress.best_observation.id == '3'
    assert isinstance(experiment.progress.best_observation.assignments, Assignments)
    assert experiment.progress.best_observation.assignments.get('a') == 3
    assert experiment.progress.best_observation.assignments.get('b') == 'd'
    assert experiment.progress.best_observation.value is None
    assert experiment.progress.best_observation.value_stddev is None
    assert experiment.progress.best_observation.failed is True
    assert experiment.progress.best_observation.created == 453
    assert experiment.progress.best_observation.suggestion == '13'
    assert experiment.progress.best_observation.experiment == '123'
    assert len(experiment.parameters) == 2
    assert isinstance(experiment.parameters[0], Parameter)
    assert experiment.parameters[0].tunable is True
    assert experiment.parameters[0].name == 'a'
    assert experiment.parameters[0].type == 'double'
    assert isinstance(experiment.parameters[0].bounds, Bounds)
    assert experiment.parameters[0].bounds.min == 1
    assert experiment.parameters[0].bounds.max == 2
    assert experiment.parameters[0].categorical_values is None
    assert experiment.parameters[0].precision == 3
    assert experiment.parameters[0].default_value == 2
    assert isinstance(experiment.parameters[1], Parameter)
    assert experiment.parameters[1].tunable is False
    assert experiment.parameters[1].name == 'b'
    assert experiment.parameters[1].type == 'categorical'
    assert experiment.parameters[1].bounds is None
    assert len(experiment.parameters[1].categorical_values) == 2
    assert isinstance(experiment.parameters[1].categorical_values[0], CategoricalValue)
    assert experiment.parameters[1].categorical_values[0].name == 'c'
    assert experiment.parameters[1].categorical_values[0].enum_index == 1
    assert experiment.parameters[1].categorical_values[1].name == 'd'
    assert experiment.parameters[1].categorical_values[1].enum_index == 2
    assert experiment.parameters[1].precision is None
    assert experiment.parameters[1].default_value is None

  def test_client(self):
    client = Client({
      'object': 'client',
      'id': '1',
      'name': 'Client',
      'created': 123,
    })
    assert isinstance(client, Client)
    assert client.id == '1'
    assert client.name == 'Client'
    assert client.created == 123

  def test_suggestion(self):
    suggestion = Suggestion({
      'object': 'suggestion',
      'id': '1',
      'assignments': {
        'a': 1,
        'b': 'c',
      },
      'state': 'open',
      'experiment': '1',
      'created': 123,
    })
    assert isinstance(suggestion, Suggestion)
    assert suggestion.id == '1'
    assert isinstance(suggestion.assignments, Assignments)
    assert suggestion.assignments.get('a') == 1
    assert suggestion.assignments.get('b') == 'c'
    assert suggestion.state == 'open'
    assert suggestion.experiment == '1'
    assert suggestion.created == 123

  def test_pagination(self):
    pagination = Pagination(Experiment, {
      'object': 'pagination',
      'count': 5,
      'data': [
        {'object': 'experiment'},
      ],
      'paging': {
        'before': '1',
        'after': '2',
      },
    })

    assert isinstance(pagination, Pagination)
    assert pagination.count == 5
    assert len(pagination.data) == 1
    assert isinstance(pagination.data[0], Experiment)
    assert isinstance(pagination.paging, Paging)
    assert pagination.paging.before == '1'
    assert pagination.paging.after == '2'
