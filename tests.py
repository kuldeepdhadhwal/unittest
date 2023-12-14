import unittest
from unittest.mock import MagicMock, patch
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch('boto3.client')
    def test_lambda_handler_success(self, mock_boto3_client):
        # Mocking the SSM client
        mock_ssm_client = MagicMock()
        mock_boto3_client.return_value = mock_ssm_client

        # Mocking the response from SSM
        mock_ssm_client.get_parameter.return_value = {
            'Parameter': {
                'Value': 'MockParameterValue'
            }
        }

        # Simulating an event (this can be customized based on your actual Lambda input)
        event = {}
        context = {}

        # Invoking the Lambda function
        response = lambda_handler(event, context)

        # Asserting the expected response
        expected_response = {
            'statusCode': 200,
            'body': '{"parameter_value": "MockParameterValue"}'
        }
        self.assertEqual(response, expected_response)

        # Asserting that the SSM client was called with the correct parameter name
        mock_ssm_client.get_parameter.assert_called_once_with(
            Name='testparameter',
            WithDecryption=True
        )

    @patch('boto3.client')
    def test_lambda_handler_error(self, mock_boto3_client):
        # Mocking the SSM client to raise an exception
        mock_ssm_client = MagicMock()
        mock_ssm_client.get_parameter.side_effect = Exception('MockError')
        mock_boto3_client.return_value = mock_ssm_client

        # Simulating an event (this can be customized based on your actual Lambda input)
        event = {}
        context = {}

        # Invoking the Lambda function
        response = lambda_handler(event, context)

        # Asserting the expected error response
        expected_response = {
            'statusCode': 500,
            'body': '{"error": "MockError"}'
        }
        self.assertEqual(response, expected_response)

        # Asserting that the SSM client was called with the correct parameter name
        mock_ssm_client.get_parameter.assert_called_once_with(
            Name='testparameter',
            WithDecryption=True
        )

if __name__ == '__main__':
    unittest.main()
