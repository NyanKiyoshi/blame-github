import unittest

from shell_helper import GitRemoteEntry
from blame_github import parse_remote_as_github_url


class TestBlameGitHub(unittest.TestCase):
    def test_parse_remote_as_github_url__correct_remotes(self):
        cases = (
            (('github', 'repo1'), 'https://www.github.com/github/repo1'),
            (('new-github', 'repo2'), 'http://github.com/new-github/repo2'),
            (('ssh-org', 'ssh-repo'), 'git@github.com:ssh-org/ssh-repo.git'),
        )

        for case in cases:
            expected_url, test_url = case
            expected_url = 'https://github.com/{}/{}'.format(*expected_url)
            test_url = GitRemoteEntry(remote_name='origin', url=test_url, type_='push')
            res = parse_remote_as_github_url(test_url)
            self.assertEqual(expected_url, res)

    def test_parse_remote_as_github_url__invalid_remotes(self):
        cases = (
            'https://ww.github.com/github/repo1',
            'https://www.github.comx/github/repo1',
            'http://bitbucket.com/new-github/repo2',
            '@github.com:ssh-org/ssh-repo.git',
            '/github.com/ssh-org/ssh-repo.git',
        )

        for case in cases:
            test_url = GitRemoteEntry(remote_name='origin', url=case, type_='push')
            with self.assertRaises(RuntimeError) as ctx:
                parse_remote_as_github_url(test_url)
            self.assertEqual(str(ctx.exception), '{} is not a valid GitHub repository URL'.format(case))
