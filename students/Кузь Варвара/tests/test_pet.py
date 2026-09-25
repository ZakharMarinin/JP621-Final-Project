import unittest
from models.pet import Dragon, RobotDog, Cat, PetIsSleepingError


class TestPetProperties(unittest.TestCase):
    """Проверяем инкапсуляцию — валидацию границ 0-100."""

    def test_hunger_clamps_to_100(self):
        d = Dragon("Рекс")
        d.hunger = 500
        self.assertEqual(d.hunger, 100)

    def test_energy_clamps_to_0(self):
        d = Dragon("Рекс")
        d.energy = -50
        self.assertEqual(d.energy, 0)

    def test_health_clamps_to_100(self):
        d = Dragon("Рекс")
        d.health = 200
        self.assertEqual(d.health, 100)

    def test_mood_clamps_to_0(self):
        d = Dragon("Рекс")
        d.mood = -10
        self.assertEqual(d.mood, 0)


class TestPetActions(unittest.TestCase):
    """Проверяем кормление, игру, сон."""

    def test_feed_decreases_hunger(self):
        d = Dragon("Рекс")
        d.hunger = 50
        d.feed()
        self.assertEqual(d.hunger, 30)

    def test_feed_increases_mood(self):
        d = Dragon("Рекс")
        d.mood = 40
        d.feed()
        self.assertEqual(d.mood, 45)

    def test_play_needs_energy(self):
        d = Dragon("Рекс")
        d.energy = 5
        result = d.play()
        self.assertIn("устал", result)
        self.assertEqual(d.mood, 80)   # настроение не изменилось

    def test_feed_raises_when_sleeping(self):
        d = Dragon("Рекс")
        d.sleep()                       # усыпили
        with self.assertRaises(PetIsSleepingError):
            d.feed()


class TestSpeciesBehavior(unittest.TestCase):
    """Проверяем, что виды отличаются поведением."""

    def test_sounds_are_different(self):
        self.assertEqual(Dragon("А").make_sound(), "Р-р-р!")
        self.assertEqual(RobotDog("Б").make_sound(), "Бип-буп!")
        self.assertEqual(Cat("В").make_sound(), "Мяу!")

    def test_robot_sick_only_at_zero_energy(self):
        r = RobotDog("Бобик")
        r.energy = 50
        r.hunger = 100          # у других видов это болезнь
        self.assertFalse(r.is_sick())   # а робот не болеет от голода

        r.energy = 0
        self.assertTrue(r.is_sick())    # а при нуле энергии — болеет


if __name__ == "__main__":
    unittest.main()