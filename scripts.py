import random
import textwrap

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson


def get_schoolkid(kid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.MultipleObjectsReturned:
        return textwrap.dedent('''\
        Найдено несколько учеников с таким ФИО или Вы забыли написать его.
        Добавьте имя и/или фамилию и/или отчество и попробуйте снова.''')
    except Schoolkid.DoesNotExist:
        return '''Такой ученик не найден. Убедитесь, что ФИО написано точно как в журнале! И попробуйте снова.'''
    return schoolkid


def fix_marks(kid_name):
    schoolkid = get_schoolkid(kid_name)
    if type(schoolkid) is str:
        print(schoolkid)
        return
    kid_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    for mark in kid_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(kid_name):
    schoolkid = get_schoolkid(kid_name)
    if type(schoolkid) is str:
        print(schoolkid)
        return
    kid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    kid_chastisements.delete()


def create_commendation(kid_name, subject):
    texts = ('Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
             'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
             'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
             'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
             'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!',
             'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
             'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
             'Теперь у тебя точно все получится!',
             )
    schoolkid = get_schoolkid(kid_name)
    if type(schoolkid) is str:
        print(schoolkid)
        return
    lessons = list(Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                         subject__title=subject))
    if not lessons:
        print("Указанный предмет не найден. Убедитесь, что предмет написан точно как в журнале и попробуте снова.")
        return
    while lessons:
        lesson = random.choice(lessons)
        if Commendation.objects.filter(created=lesson.date, schoolkid=schoolkid, subject=lesson.subject):
            lessons.remove(lesson)
            continue
        else:
            Commendation.objects.create(created=lesson.date, schoolkid=schoolkid, subject=lesson.subject,
                                        teacher=lesson.teacher, text=random.choice(texts))
            break
    else:
        print("Для указанного ученика по указанному предмету похвала уже проставлена на всех уроках!")
