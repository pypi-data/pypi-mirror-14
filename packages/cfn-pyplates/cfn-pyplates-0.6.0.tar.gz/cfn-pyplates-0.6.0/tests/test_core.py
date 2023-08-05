# Copyright (c) 2013 MetaMetrics, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
import json
import mock
import unittest
import warnings
from textwrap import dedent
from tempfile import NamedTemporaryFile

from cfn_pyplates import core, exceptions


class TestResource(core.JSONableDict):
    pass


class JSONableDictTestCase(unittest.TestCase):
    def test_crazy_addchild_ordering(self):
        # We should be able to add children to any element at any time,
        # before or after that element has been added to a parent.
        bm = core.JSONableDict()
        tr1 = TestResource({'Id': 1})
        tr2 = TestResource({'Id': 2})
        # Tack the TestResource onto the template
        bm.add(tr1)
        # .add should return the added resource
        added_resource = bm.add(tr1)
        self.assertIs(added_resource, tr1)
        # Add a child to tr1 *after* adding it to bm
        tr1.add(tr2)
        # Then make sure tr2 is visible from the template
        self.assertIn('TestResource', bm['TestResource'])
        # Double check Ids...
        self.assertEqual(bm['TestResource']['Id'], 1)
        self.assertEqual(bm['TestResource']['TestResource']['Id'], 2)

        # Now mess with the nested child, and make sure those changes
        # are still seen in the template
        tr2.update({'This Is': 'A Test'})
        self.assertEqual(bm['TestResource']['TestResource']['This Is'], 'A Test')

    def test_contructor_dict_arg(self):
        # Making sure that a resource instantiated with a params dict is updated correctly
        update_dict = {'Test': 'A custom custructydict'}
        bm = core.JSONableDict()
        bm.add(TestResource(update_dict))
        self.assertEqual(bm['TestResource'], update_dict)

    def test_naming(self):
        obj = TestResource(name='NormalName')
        # Getter method works?
        self.assertEqual(obj.name, 'NormalName')
        self.assertEqual(obj._name, 'NormalName')

        # Setter method works?
        obj.name = 'DifferentName'
        self.assertEqual(obj.name, 'DifferentName')
        self.assertEqual(obj._name, 'DifferentName')

        # Del method works?
        del(obj.name)
        self.assertEqual(obj.name, 'TestResource')
        self.assertIsNone(obj._name)

    def test_getsetattr(self):
        bm = core.JSONableDict()

        self.assertNotIn('TestResource', bm)
        bm.test_resource = TestResource()
        self.assertIn('TestResource', bm)
        del(bm.test_resource)
        self.assertNotIn('TestResource', bm)

    def test_addremoveerror(self):
        bm = core.JSONableDict()
        bm.attr = 'Not a JSON-able dict...'
        with self.assertRaises(exceptions.AddRemoveError):
            bm.remove(bm.attr)

    def test_remove_non_child(self):
        # Change the
        parent = core.JSONableDict(name="parent")
        parent.child = core.JSONableDict()
        bad_name = 'hahaha I did nefarious things!'
        parent.child.name = bad_name
        with warnings.catch_warnings(record=True) as caught:
            parent.remove(parent.child)

        # exactly one warning is expected to be caught related to the bad name
        self.assertEqual(len(caught), 1)
        self.assertTrue(bad_name in str(caught[0].message))

    def test_str_unicode(self):
        # string and unicode dunder methods return the same contents
        bm = core.JSONableDict()
        self.assertEqual(str(bm), unicode(bm))


class CloudFormationTemplateTestCase(unittest.TestCase):
    def test_has_template_attrs(self):
        description = 'Test Description!'
        cft = core.CloudFormationTemplate(description)
        self.assertEqual(cft['Description'], description)

        self.assertIn('Parameters', cft)
        self.assertIsInstance(cft.parameters, core.Parameters)

        self.assertIn('Mappings', cft)
        self.assertIsInstance(cft.mappings, core.Mappings)

        self.assertIn('Resources', cft)
        self.assertIsInstance(cft.resources, core.Resources)

        self.assertIn('Outputs', cft)
        self.assertIsInstance(cft.outputs, core.Outputs)

        self.assertIn('Metadata', cft)
        self.assertIsInstance(cft.metadata, core.Metadata)

    def test_no_description(self):
        cft = core.CloudFormationTemplate()
        self.assertNotIn('Description', cft)

    def test_jsonification(self):
        cft = core.CloudFormationTemplate('This is a test')
        cft.parameters.update({'These': 'are awesome!'})

        # We expect to see the AWSTemplateFormatVersion, the provided
        # description, and the provided parameters. We do not expect to
        # see empty Mappings, Resources, or Outputs.
        expected_out = dedent(u'''\
        {
          "AWSTemplateFormatVersion": "2010-09-09",
          "Description": "This is a test",
          "Parameters": {
            "These": "are awesome!"
          }
        }''')
        self.assertEqual(unicode(cft), expected_out)


class ResourcesTestCase(unittest.TestCase):
    def test_resource(self):
        # No properties for this one, just make sure the resource comes
        # out right
        cft = core.CloudFormationTemplate()
        cft.resources.test = core.Resource('TestResource', 'AWS::Resource::Test')

        # Should have a new 'TestResource' key in our template resources
        self.assertIn('TestResource', cft.resources)

        # And it should look like this...
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test"
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_properties(self):
        properties_dict = {'Key1': 'Value1', 'Key2': 'Value2'}
        properties = core.Properties(properties_dict)
        res = core.Resource('TestResource', 'AWS::Resource::Test', properties)
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the properties attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "Properties": {
            "Key2": "Value2",
            "Key1": "Value1"
          }
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_metadata(self):
        metadata = core.Metadata({"Object1": "Location1", "Object2": "Location2"})
        res = core.Resource('TestResource', 'AWS::Resource::Test', None, metadata)
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the metadata attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "Metadata": {
            "Object1": "Location1",
            "Object2": "Location2"
          }
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_creation_policy(self):
        creation_policy = core.CreationPolicy(42, 'NotActuallyValidatedYerOnYerOwn')
        res = core.Resource('TestResource', 'AWS::Resource::Test', None, creation_policy)
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the metadata attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "CreationPolicy": {
            "ResourceSignal": {
              "Count": 42,
              "Timeout": "NotActuallyValidatedYerOnYerOwn"
            }
          }
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_deletion_policy(self):
        deletion_policy = core.DeletionPolicy("Retain")
        res = core.Resource('TestResource', 'AWS::Resource::Test', None, deletion_policy)
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the metadata attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "DeletionPolicy": "Retain"
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_depends_on(self):
        depends_on = core.DependsOn("Location2")
        res = core.Resource('TestResource', 'AWS::Resource::Test', None, depends_on)
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the metadata attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "DependsOn": "Location2"
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_update_policy(self):
        update_policy = core.UpdatePolicy(
            {"MaxBatchSize": "Location1", "MinInstancesInService": "Location2", "PauseTime": "30"})
        res = core.Resource('TestResource', 'AWS::Resource::Test', None, update_policy)
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the metadata attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "UpdatePolicy": {
            "PauseTime": "30",
            "MaxBatchSize": "Location1",
            "MinInstancesInService": "Location2"
          }
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_extended_attributes(self):
        update_policy = core.UpdatePolicy({"Object1": "Location1", "Object2": "Location2"})
        metadata = core.Metadata({"Object1": "Location1", "Object2": "Location2"})
        deletion_policy = core.DeletionPolicy("Retain")
        depends_on = core.DependsOn("Location2")
        res = core.Resource('TestResource', 'AWS::Resource::Test', None,
                            [metadata, update_policy, deletion_policy, depends_on])
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the metadata attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "Metadata": {
            "Object1": "Location1",
            "Object2": "Location2"
          },
          "UpdatePolicy": {
            "Object1": "Location1",
            "Object2": "Location2"
          },
          "DeletionPolicy": "Retain",
          "DependsOn": "Location2"
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)

    def test_resource_with_condition(self):
        condition = core.Condition('TestCondition', {'Fn::Fake': 'ConditionValue'})
        res = core.Resource('TestResource', 'AWS::Resource::Test', None, condition)
        cft = core.CloudFormationTemplate()
        cft.resources.test = res

        # The output should have the metadata attached
        expected_out = dedent(u'''\
        {
          "Type": "AWS::Resource::Test",
          "Condition": "TestCondition"
        }''')
        self.assertEqual(unicode(cft.resources.test), expected_out)


class ConditionsTestCase(unittest.TestCase):
    def test_condition(self):
        cft = core.CloudFormationTemplate()
        cft.conditions.test = core.Condition('TestCondition', {'Fn::Fake': 'ConditionValue'})

        # Should have a new 'TestCondition' key in our template resources
        self.assertIn('TestCondition', cft.conditions)

        # And it should look like this...
        expected_out = dedent(u'''\
        {
          "Fn::Fake": "ConditionValue"
        }''')
        self.assertEqual(unicode(cft.conditions.test), expected_out)

    def test_condition_ref(self):
        cft = core.CloudFormationTemplate()
        cft.conditions.test = core.Condition('TestCondition', {'Ref': 'ReferencedThing'})

        # And it should look like this...
        expected_out = dedent(u'''\
        {
          "Ref": "ReferencedThing"
        }''')
        self.assertEqual(unicode(cft.conditions.test), expected_out)


class MetadataTestCase(unittest.TestCase):
    def test_metadata(self):
        cft = core.CloudFormationTemplate()
        cft.metadata = core.JSONableDict(name='Metadata')
        cft.metadata['TestKey'] = 'Test Value'

        # And it should look like this...
        expected_out = dedent(u'''\
        {
          "TestKey": "Test Value"
        }''')
        self.assertEqual(unicode(cft.metadata), expected_out)


class MiscElementsTestCase(unittest.TestCase):
    def test_mapping_element(self):
        mappings = core.Mappings()

        mapping_letters = core.Mapping('MappingKeyLetters',
            {
                'keya': 'valuea',
                'keyb': 'valueb'
            }
        )
        mapping_numbers = core.Mapping('MappingKeyNumbers',
            {
                'key1': 'value1',
                'key2': 'value2'
            }
        )

        mappings.add(mapping_letters)
        mappings.add(mapping_numbers)

        self.assertEqual(mappings['MappingKeyLetters']['keya'], 'valuea')
        self.assertEqual(mappings['MappingKeyLetters']['keyb'], 'valueb')
        self.assertEqual(mappings['MappingKeyNumbers']['key1'], 'value1')
        self.assertEqual(mappings['MappingKeyNumbers']['key2'], 'value2')

    def test_resource_element(self):
        resource = core.Resource('ResourceName',
            'AWS::Testing::ResourceType',
            {
                'Key1': 'Value1',
                'Key2': 'Value2',
            }
        )
        self.assertEqual(resource.name, 'ResourceName')
        self.assertIn('Properties', resource)
        properties = resource['Properties']
        self.assertEqual(properties['Key1'], 'Value1')
        self.assertEqual(properties['Key2'], 'Value2')

    def test_properties(self):
        properties = core.Properties({
            'Key1': 'Value1',
            'Key2': 'Value2',
        })
        # Create a resource, and test attaching properties to it
        resource = core.Resource('ResourceName',
            'AWS::Testing::ResourceType')
        resource.add(properties)

        self.assertEqual(resource.name, 'ResourceName')
        self.assertIn('Properties', resource)
        properties = resource['Properties']
        self.assertEqual(resource['Properties']['Key1'], 'Value1')
        self.assertEqual(resource['Properties']['Key2'], 'Value2')

    def test_parameter_element(self):
        parameter = core.Parameter('ParameterName',
            'String',
            {'Key': 'Value'})

        self.assertEqual(parameter.name, 'ParameterName')
        self.assertEqual(parameter['Type'], 'String')
        self.assertEqual(parameter['Key'], 'Value')

    def test_output_element(self):
        output = core.Output('OutputName',
            'Output Value',
            'Output Description')
        self.assertEqual(output.name, 'OutputName')
        self.assertEqual(output['Value'], 'Output Value')
        self.assertEqual(output['Description'], 'Output Description')

    def test_ec2_tags_element(self):
        tags = core.ec2_tags({
            'TestKey1': 'TestValue1',
            'TestKey2': 'TestValue2'
        })
        for entry in tags:
            self.assertIn('Key', entry)
            self.assertIn('Value', entry)
            if entry['Key'] == 'TestKey1':
                self.assertEqual(entry['Value'], 'TestValue1')
            if entry['Key'] == 'TestKey2':
                self.assertEqual(entry['Value'], 'TestValue2')


class CreationPolicyOptionalKwargs(unittest.TestCase):
    def test_creation_policy_no_args(self):
        creation_policy = core.CreationPolicy()
        resource_signal = creation_policy['ResourceSignal']

        # ResourceSignal should be an empty dict
        self.assertFalse(resource_signal)
        expected_out = dedent(u'''\
        {
          "ResourceSignal": {}
        }''')
        self.assertEqual(unicode(creation_policy), expected_out)

    def test_creation_policy_arg_casting(self):
        # Make sure the int and string type casts work correctly
        with self.assertRaises(ValueError):
            core.CreationPolicy(count='Raise a ValueError trying to cast this as an int.')

        creation_policy = core.CreationPolicy(count='0', timeout=15)
        resource_signal = creation_policy['ResourceSignal']
        self.assertTrue(isinstance(resource_signal['Count'], int))
        self.assertTrue(isinstance(resource_signal['Timeout'], str))

        expected_out = dedent(u'''\
        {
          "ResourceSignal": {
            "Count": 0,
            "Timeout": "15"
          }
        }''')
        self.assertEqual(unicode(creation_policy), expected_out)


class GenerateTestCase(unittest.TestCase):
    def test_callable_generate(self):
        # Make a pyplate that uses the options mapping
        pyplate_contents = dedent(u'''\
        cft = CloudFormationTemplate('This is a test')
        cft.parameters.update({
            'Exists': options['ThisKeyExists']
        })''')
        pyplate = NamedTemporaryFile()
        pyplate.write(pyplate_contents)
        pyplate.flush()

        # call generate directly with an options mapping, no CLI
        output = json.loads(core.generate_pyplate(pyplate.name, {'ThisKeyExists': True}))
        self.assertTrue(output['Parameters']['Exists'])

    @mock.patch('cfn_pyplates.exceptions.Error')
    def test_callable_generate_no_template(self, error):
        # Make a pyplate with no CloudFormationTemplate in it
        pyplate_contents = ''
        pyplate = NamedTemporaryFile()
        pyplate.write(pyplate_contents)
        pyplate.flush()

        error.return_value = Exception('I am a test mock, this traceback is expected.')

        core.generate_pyplate(pyplate.name)

        error.assert_called_once_with('No CloudFormationTemplate found in pyplate')
