#!/usr/bin/env python3
import unittest
from unittest.mock import PropertyMock, patch, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean based on license key."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

    @patch("client.get_json")  # ✅ patch where it's used
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""

        mock_get_json.return_value = {
            "login": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }

        client = GithubOrgClient(org_name)
        result = client.org  # ✅ Access as a property

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result["login"], org_name)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL from org payload."""

        # Define the fake payload the org property should return
        fake_org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch the 'org' property so it returns the fake payload
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_org_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url  # Access the property we’re testing

            # Assertions
            self.assertEqual(result, fake_org_payload["repos_url"])  # ✅ correct value
            mock_org.assert_called_once()

    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos."""

        # Mocked JSON payload returned by get_json
        fake_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = fake_repos_payload

        # Mock _public_repos_url property
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Assertions
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)  # ✅ Correct list of repo names
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")
            mock_repos_url.assert_called_once()

    @parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level mocks before any tests run."""

        # Patch requests.get
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Define a helper function to return different payloads based on URL
        def get_json_side_effect(url):
            if url == "https://api.github.com/orgs/google":
                mock_response = Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            if url == cls.org_payload["repos_url"]:
                mock_response = Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return None

        # Set side_effect so mock returns correct payload per URL
        mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for .public_repos with no license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for .public_repos filtering by license."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
