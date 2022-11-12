import random
import sys

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson


def fix_marks(schoolkid: Schoolkid):
    kid_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    for mark in kid_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid: Schoolkid):
    kid_chastisments = Chastisement.objects.filter(schoolkid=schoolkid)
    kid_chastisments.delete()


def create_commendation(kid_name, subject):
    texts = ('Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
             'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
             'Сказано здорово – просто и ясно!',
             )
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.MultipleObjectsReturned:
        print("I've found several schoolkids with such name")
        sys.exit(1)
    except Schoolkid.DoesNotExist:
        print("No schoolkid with such mane")
        sys.exit(1)
    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                    subject__title=subject)
    lesson = random.choice(lessons)
    Commendation.objects.create(created=lesson.date, schoolkid=schoolkid, subject=lesson.subject,
                                teacher=lesson.teacher, text=random.choice(texts))
