class Person(object):
    def __init__(
        self,
        birth: int,
        children_left: int,
        gender: str,
    ) -> None:
        self.birth = birth
        self.gender= gender
        self.alive = True
        self.partner = None
        self.crying = False
        self.children_left = children_left

    def age(self, time: int):
        return time - self.birth

    def have_children(self, count: int):
        assert self.alive, "Must be alive in order to have children"
        self.children_left -= count

    def get_lonely(self):
        assert self.alive, "Must be alive in order to get lonely"
        assert self.partner is not None, "Must have a partner to get lonely"
        self.partner = None
        self.crying = True

    def move_on(self):
        assert self.alive, "Must be alive in order to move on"
        assert self.crying, "Must be crying to move on"
        self.crying = False

    def match(self, partner: "Person"):
        assert self.alive, "Must be alive in order to be matched"
        assert self.partner is None, "Shouldn't have a partner when being matched"
        assert not self.crying, "Can't be crying to match"
        assert self.gender != partner.gender, "Opposite genders needed for match"
        self.partner = partner

    def die(self):
        assert self.alive, "Must be alive in order to die"
        self.alive = False


class Female(Person):
    def __init__(self, age: int, children_left: int) -> None:
        super().__init__(age, children_left, "female")
        self.pregnant = False

    def get_pregnant(self):
        self.pregnant = True

    def have_children(self, count: int):
        assert self.pregnant, "Must be pregnant to have child"
        super().have_children(count)
        self.pregnant = False


class Male(Person):
    def __init__(self, age: int, children_left: int) -> None:
        super().__init__(age, children_left, "male")
