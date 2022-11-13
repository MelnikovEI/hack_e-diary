import random
import textwrap

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson

COMMENDATIONS = (
    'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
    'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
    'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
    'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!',
    'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
)


def get_schoolkid(kid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.MultipleObjectsReturned:
        raise Schoolkid.MultipleObjectsReturned(textwrap.dedent('''\
        Найдено несколько учеников с таким ФИО или Вы забыли написать его.
        Добавьте имя и/или фамилию и/или отчество и попробуйте снова.'''))
    except Schoolkid.DoesNotExist:
        raise Schoolkid.DoesNotExist(textwrap.dedent('''\
        Такой ученик не найден. Убедитесь, что ФИО написано точно как в журнале! И попробуйте снова.'''))
    return schoolkid


def fix_marks(kid_name):
    try:
        schoolkid = get_schoolkid(kid_name)
    except Exception as e:
        print(e)
        return
    Mark.objects.filter(schoolkid=schoolkid, points__lte=3).update(points=5)


def remove_chastisements(kid_name):
    try:
        schoolkid = get_schoolkid(kid_name)
    except Exception as e:
        print(e)
        return
    kid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    kid_chastisements.delete()


def create_commendation(kid_name, subject):
    try:
        schoolkid = get_schoolkid(kid_name)
    except Exception as e:
        print(e)
        return
    all_lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                        subject__title=subject)
    if not all_lessons:
        print("Указанный предмет не найден. Убедитесь, что предмет написан точно как в журнале и попробуте снова.")
        return
    commendation_dates = Commendation.objects.filter(schoolkid=schoolkid, subject__title=subject)\
        .values_list('created', flat=True)
    absent_commendation_lessons = all_lessons.exclude(date__in=commendation_dates)
    if not absent_commendation_lessons:
        print("Для указанного ученика по указанному предмету похвала уже проставлена на всех уроках!")
        return
    rand_lesson = random.choice(absent_commendation_lessons)
    Commendation.objects.create(created=rand_lesson.date, schoolkid=schoolkid, subject=rand_lesson.subject,
                                teacher=rand_lesson.teacher, text=random.choice(COMMENDATIONS))
