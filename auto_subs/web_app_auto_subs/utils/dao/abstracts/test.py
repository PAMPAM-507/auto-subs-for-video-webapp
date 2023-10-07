from ClinicWebsite.utils.dao.dao import DAOForModels
import string

# class Model:
#
#     def __init__(self, pk, name, field):
#         self.pk = pk
#         self.name = name
#         self.field = field
#
#
# model = Model(1, 'andrey', '+79017877058')
#
# res = DAOForModels.fill_universal_data_class(pk=model.pk, name=model.name, field=model.field)
#
# print(res)


sql = """
    SELECT ClinicWebsite_listofvisits.id, 
    ClinicWebsite_listofvisits.dateOfVisit, 
    ClinicWebsite_listofvisits.confirmationOfVisit,
    Staff.name,
    ClinicWebsite_client.name

    FROM ClinicWebsite_listofvisits, auth_user, Staff, ClinicWebsite_client

    WHERE ClinicWebsite_listofvisits.employee_id = Staff.id AND
    auth_user.id = Staff.user_id AND Staff.user_id = %s AND
    ClinicWebsite_listofvisits.client_id = ClinicWebsite_client.id

    ORDER BY ClinicWebsite_listofvisits.dateOfVisit
    """


def sp(sql):
    r = sql.split(' ')
    print(len(r))
    print(r[4])
    z, v, c = 0, 0, 0
    for i in range(len(r)):
        if r[i] == 'SELECT' or r[i] == 'select':
            z = i
        if r[i] == 'FROM' or r[i] == 'from':
            v = i
        if r[i] == 'WHERE' or r[i] == 'where':
            c = i

    print(z, v, c)
    list_of_attrs, list_of_tables = r[z + 1:v - 1], r[v + 1:c]

    print(''.join(list_of_tables).replace(',', ' ').split())
    print(''.join(list_of_attrs).replace(',', ' ').split())

sp(sql)
