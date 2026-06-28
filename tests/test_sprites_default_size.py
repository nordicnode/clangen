"""Test for issue #2513 - Cat sprite not generating correctly when init with no arguments.

When Cat() is instantiated with default/no arguments, sprites.size was None,
causing TypeError when creating pygame Surfaces. This test verifies that
sprites.size returns a valid integer even before load_all() is called.
"""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

pygame.init()

from scripts.cat.sprites.load_sprites import Sprites


class TestSpritesDefaultSize(unittest.TestCase):
    """Test that Sprites.size returns a valid integer even before load_all()"""

    def test_sprites_size_not_none_before_load_all(self):
        """Sprites.size should never be None — it must default to 50."""
        test_sprites = Sprites()
        self.assertIsNotNone(test_sprites.size)

    def test_sprites_size_is_int_before_load_all(self):
        """Sprites.size should be an integer (or at least numeric) before load_all."""
        test_sprites = Sprites()
        self.assertIsInstance(test_sprites.size, (int, float))

    def test_sprites_default_size_is_50(self):
        """Before load_all, Sprites.size should default to 50."""
        test_sprites = Sprites()
        self.assertEqual(test_sprites.size, 50)

    def test_sprites_size_setter_works(self):
        """The size setter should correctly update _size."""
        test_sprites = Sprites()
        test_sprites.size = 100
        self.assertEqual(test_sprites.size, 100)

    def test_sprites_size_set_to_none_returns_default(self):
        """If size is set back to None, the property should return 50."""
        test_sprites = Sprites()
        test_sprites.size = 100
        self.assertEqual(test_sprites.size, 100)
        test_sprites.size = None
        self.assertEqual(test_sprites.size, 50)

    def test_pygame_surface_creation_with_sprites_size(self):
        """pygame.Surface should be creatable using sprites.size before load_all."""
        test_sprites = Sprites()
        # This was the original failure: pygame.Surface((None, None), ...) raises TypeError
        surface = pygame.Surface(
            (test_sprites.size, test_sprites.size), pygame.HWSURFACE | pygame.SRCALPHA
        )
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_width(), 50)
        self.assertEqual(surface.get_height(), 50)


if __name__ == "__main__":
    unittest.main()
