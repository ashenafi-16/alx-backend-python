#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.
"""

import unittest
from unittest.mock import patch, PropertyMock
from typing import List

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for GithubOrgClient.
    """

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """
        Test that public_repos returns the expected list of repo names
        and that get_json and _public_repos_url are called properly.
        """
        fake_payload = [
            {'name': 'repo1', 'license': {'key': 'apache-2.0'}},
            {'name': 'repo2', 'license': {'key': 'mit'}},
            {'name': 'repo3', 'license': {'key': 'apache-2.0'}}
        ]

        mock_get_json.return_value = fake_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/test_org/repos"
            )

            client = GithubOrgClient('test_org')
            repos: List[str] = client.public_repos()

            expected = ['repo1', 'repo2', 'repo3']
            self.assertEqual(repos, expected)

            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos"
            )

            mock_repos_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()
