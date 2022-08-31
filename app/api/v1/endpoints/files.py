import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate
from app.schemas.user import ChangeUser

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/{filename}')
def files(filename):
    context = {'name': '',
               'surname': '',
               'patronymic': '',
               'phone': '',
               'passport': '',
               'seria': '',
               'nomer': '',
               'address': '',
               'familyComposition': '',
               'birthday': '',
               'gender': ''}

    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=filename + '.docx')


@router.post('/{filename}')
def files(filename, user: ChangeUser):
    if user.passport is not None:
        seria = user.passport[:4]
        nomer = user.passport[5:]
    else:
        seria = ''
        nomer = ''

    if user.gender == 'male':
        gender = 'Мужчина'
    elif user.gender == 'female':
        gender = 'Девушка'
    else:
        gender = ''

    if user.birthday == datetime.date(3000, 1, 1):
        birthday = ''
    else:
        birthday = user.birthday

    context = {'name': user.name,
               'surname': user.surname,
               'patronymic': user.patronymic,
               'phone': user.phone,
               'passport': user.passport,
               'seria': seria,
               'nomer': nomer,
               'address': user.address,
               'familyComposition': user.familyComposition,
               'birthday': birthday,
               'gender': gender}

    print(user.birthday)
    print(birthday)
    print(context)

    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=filename + '.docx')


@router.put('/{filename}')
def files(filename, user: ChangeUser):
    if user.passport is not None:
        seria = user.passport[:4]
        nomer = user.passport[5:]
    else:
        seria = ''
        nomer = ''

    if user.gender == 'male':
        gender = 'Мужчина'
    elif user.gender == 'female':
        gender = 'Девушка'
    else:
        gender = ''

    if user.birthday == datetime.date(3000, 1, 1):
        birthday = ''
    else:
        birthday = user.birthday

    context = {'name': user.name,
               'surname': user.surname,
               'patronymic': user.patronymic,
               'phone': user.phone,
               'passport': user.passport,
               'seria': seria,
               'nomer': nomer,
               'address': user.address,
               'familyComposition': user.familyComposition,
               'birthday': birthday,
               'gender': gender}

    print(user.birthday)
    print(birthday)
    print(context)

    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=filename + '.docx')
