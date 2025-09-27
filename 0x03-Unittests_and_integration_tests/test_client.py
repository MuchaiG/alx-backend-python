#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value and calls get_json once."""

        # Mock return value for get_json
        mock_get_json.return_value = {"login": org_name}

        # Instantiate client and call .org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assertions
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"login": org_name})


if __name__ == "__main__":
    unittest.main()
