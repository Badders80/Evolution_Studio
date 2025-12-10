import unittest
from modules.press_room import PressRoom


class TestEvolutionLogic(unittest.TestCase):
    def setUp(self):
        """Setup run before every test."""
        self.pr = PressRoom()
        self.base_data = {
            "heading": "Test Heading",
            "subheading": "Test Sub",
            "body": "Test Body",
            "update_type": "Race Preview",
            "quote1_text": "Great run.",
            "quote1_name": "Trainer",
        }

    def test_media_logic_landscape(self):
        """Logic Check: If I ask for Landscape, does the HTML reflect it?"""
        html = self.pr.generate_report(
            **self.base_data,
            media1="https://www.youtube.com/watch?v=video123",
            media_portrait=False,  # Request Landscape
        )
        # Look for the landscape container element
        self.assertIn('<div class="media-container-landscape">', html)

    def test_media_logic_portrait(self):
        """Logic Check: If I ask for Portrait, does the HTML reflect it?"""
        html = self.pr.generate_report(
            **self.base_data,
            media1="https://www.youtube.com/watch?v=video123",
            media_portrait=True,  # Request Portrait
        )
        self.assertIn('<div class="media-container-portrait">', html)

    def test_empty_media_overrides_orientation(self):
        """Logic Check: If NO media is provided, orientation flags should be ignored."""
        html = self.pr.generate_report(
            **self.base_data,
            media1="",  # Empty Media
            media_portrait=True,  # Ask for Portrait, but there is no media
        )
        # Result: Should NOT try to render an iframe at all
        self.assertNotIn("<iframe", html)

    def test_bonus_section_logic(self):
        """Logic Check: Does the bonus section stack correctly?"""
        bonus = [
            {"type": "quote", "content": "Bonus Quote", "name": "Author"}
        ]
        html = self.pr.generate_report(
            **self.base_data,
            bonus_elements=bonus,
        )
        self.assertIn("bonus-quote", html)
        self.assertIn("Bonus Quote", html)


if __name__ == "__main__":
    unittest.main()
