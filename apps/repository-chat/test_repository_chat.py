import unittest
from repository_chat import repository_system_prompt, search_repositories

class RepositoryChatTests(unittest.TestCase):
    def test_prompt_boundary(self):
        class Context:
            full_name = "example/repo"
            metadata = {"default_branch": "main"}
            readme = "README"
            tree = []
            commits = []
        prompt = repository_system_prompt(Context())
        self.assertIn("Speak AS THE REPOSITORY", prompt)
        self.assertIn("do not pretend that the repository is conscious", prompt)
        self.assertIn("Never invent", prompt)

    def test_search_exists(self):
        self.assertTrue(callable(search_repositories))

if __name__ == "__main__":
    unittest.main()
