from enum import Enum


class DayOfWeek(Enum):
    Mon = "mon"
    Tue = "tue"
    Wed = "wed"
    Thu = "thu"
    Fri = "fri"
    Sat = "sat"
    Sun = "sun"

    @classmethod
    def get_weekday_number(cls, day: 'DayOfWeek') -> int:
        """Конвертирует DayOfWeek в число (0=Пн, 6=Вс), совместимое с datetime.weekday()."""
        mapping = {
            cls.Mon: 0,
            cls.Tue: 1,
            cls.Wed: 2,
            cls.Thu: 3,
            cls.Fri: 4,
            cls.Sat: 5,
            cls.Sun: 6,
        }
        return mapping[day]
