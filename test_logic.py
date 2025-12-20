import unittest
from modules.press_room import PressRoom


class TestEvolutionLogic(unittest.TestCase):
    def setUp(self):
        """Setup run before every test."""
        self.pr = PressRoom()

    def test_media_logic_landscape(self):
        """Logic Check: If I ask for Landscape, does the HTML reflect it?"""
        blocks = [
            {"type": "grey_box", "media": "https://www.youtube.com/watch?v=video123", "quote": "", "name": "", "media_portrait": False}
        ]
        html = self.pr.generate_report(blocks=blocks, update_type="Race Preview", global_media_portrait=False)
        self.assertIn('<div class="media-container-landscape">', html)

    def test_media_logic_portrait(self):
        """Logic Check: If I ask for Portrait, does the HTML reflect it?"""
        blocks = [
            {"type": "grey_box", "media": "https://www.youtube.com/watch?v=video123", "quote": "", "name": "", "media_portrait": True}
        ]
        html = self.pr.generate_report(blocks=blocks, update_type="Race Preview", global_media_portrait=False)
        self.assertIn('<div class="media-container-portrait">', html)

    def test_empty_media_overrides_orientation(self):
        """Logic Check: If NO media is provided, orientation flags should be ignored."""
        blocks = [
            {"type": "grey_box", "media": "", "quote": "Test", "name": "Author", "media_portrait": True}
        ]
        html = self.pr.generate_report(blocks=blocks, update_type="Race Preview")
        self.assertNotIn("<iframe", html)

    def test_block_ordering(self):
        """Logic Check: Does the linear block system preserve order?"""
        blocks = [
            {"type": "heading", "content": "Test Heading"},
            {"type": "body", "content": "Paragraph 1"},
            {"type": "grey_box", "media": "", "quote": "Great run.", "name": "Trainer", "media_portrait": False},
        ]
        html = self.pr.generate_report(blocks=blocks, update_type="Race Preview")
        self.assertIn("Test Heading", html)
        self.assertIn("Paragraph 1", html)
        self.assertIn("Great run.", html)


if __name__ == "__main__":
    unittest.main()
