import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate
from app.schemas.user import ChangeUser

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/{filename}')
def files(filename,
          name: str = '',
          surname: str = '',
          patronymic: str = '',
          phone: str = '',
          passport: str = '',
          address: str = '',
          familyComposition: str = '',
          birthday: str = '',
          gender: str = ''):

    seria = '' if passport is None else passport[:4]
    nomer = '' if passport is None else passport[5:]
    birthday_new = '' if birthday == datetime.date(3000, 1, 1) else birthday

    context = {'name': name,
               'surname': surname,
               'patronymic': patronymic,
               'phone': phone,
               'passport': passport,
               'seria': seria,
               'nomer': nomer,
               'address': address,
               'familyComposition': familyComposition,
               'birthday': birthday_new,
               'gender': gender}

    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=filename + '.docx')


@router.post('/{filename}')
def files(filename, user: ChangeUser):
    if user.gender == 'male':
        gender = 'Мужчина'
    elif user.gender == 'female':
        gender = 'Девушка'
    else:
        gender = ''

    seria = '' if user.passport is None else user.passport[:4]
    nomer = '' if user.passport is None else user.passport[5:]
    birthday = '' if user.birthday == datetime.date(3000, 1, 1) else user.birthday

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

    print(context)

    doc = DocxTemplate('app/files/templates/' + filename + '.docx')
    doc.render(context)
    doc.save('app/files/generated/' + filename + '.docx')

    return FileResponse('app/files/generated/' + filename + '.docx',
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        filename=filename + '.docx')
