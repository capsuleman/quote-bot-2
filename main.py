from dao import DAO

dao = DAO()

dao.add_quote('C\'est pour tester', 'capsule_man')
dao.get_last_quotes(1)