"""Guard the repository's GitHub Issues task-tracking policy."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TrackingPolicy(unittest.TestCase):
    def test_github_issues_replaces_beans(self):
        for relative in (
            '.beans.yml',
            '.github/instructions/tasks.instructions.md',
            '.agents/skills/beans-vscode/SKILL.md',
        ):
            with self.subTest(removed=relative):
                self.assertFalse((ROOT / relative).exists())
        with self.subTest(bean_files='absent'):
            self.assertEqual(
                [str(path.relative_to(ROOT)) for path in
                 (ROOT / '.beans').rglob('*') if path.is_file()],
                [],
            )
        with self.subTest(agent_policy='GitHub Issues'):
            text = (ROOT / 'AGENTS.md').read_text()
            self.assertIn('## Task tracking\n', text)
            policy = text.split('## Task tracking\n', 1)[1].split('\n## ', 1)[0]
            for phrase in (
                'GitHub Issues',
                'authoritative',
                'https://github.com/open-ortho/lectures/issues',
                'Do not create Beans',
            ):
                self.assertIn(phrase, policy)


if __name__ == '__main__':
    unittest.main()
