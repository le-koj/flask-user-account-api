import requests, unittest
import random

BASE = "http://127.0.0.1:5000/"

class TestUserResource(unittest.TestCase):

    f_name = ['kojo', 'banney', 'silver', 'koj', 'wale']
    l_name = ['deblac', 'light', 'black', 'denull']

    emails = set()
    while len(emails) < 11:
        fname = f_name[random.randint(0, len(f_name)-1)]
        lname = l_name[random.randint(0, len(l_name)-1)]
        email_ext = "gmail.com"
        email = f"{fname}.{lname}@{email_ext}"
        emails.add(email)

    print(f"-----\nLength of Email: {len(emails)}\n-----")

    users = dict()
    for index in range(11):
        #print(f"-----\nLength of Email: {len(emails)}\n-----")
        user = {
            'first_name': f'{f_name[random.randint(0, len(f_name)-1)]}',
            'last_name': f'{l_name[random.randint(0, len(l_name)-1)]}',
            'email': emails.pop()
        }
        users[f"{random.randint(11, 120)}"] = user

    @unittest.skip("skipping 404 test")
    def test_user_dict(self):
        print(TestUserResource.users)

    #@unittest.skip("skipping 404 test")
    def test_put(self):
        """
            add 10 users to the table.
            -should return status code 201 or 409
        """
        for key, value in TestUserResource.users.items():
            response = requests.put(BASE + f"user/{int(key)}", value)
            print(response.status_code, end='\n')
            print(response.json(), end='\n')

    @unittest.skip("skipping 404 test")
    def test_update(self):
        """
            update 10 users to the table.
            -should return status code 200 or 404 or 409
        """
        for key, value in TestUserResource.users.items():
            response = requests.patch(BASE + f"user/{int(key)}", {"last_name": value['last_name']})
            print(response.status_code, end='\n')
            print(response.json(), end='\n')

    @unittest.skip("skipping test_delete")
    def test_delete(self):
        """
            delete 10 in the table.
            -should return status code 204 or 404 
        """
        for key, value in TestUserResource.users.items():
            response = requests.delete(BASE + f"user/{int(key)}")
            print(response.status_code, end='\n')
            print(response.text, end='\n')


    @unittest.skip("skipping 404 test")
    def test_get_404(self):
        """
            send invalid requests
        """
        queries = ["", "user", "email", "/user/1",
                    "user/1/koj", "user/koj@gmail.com"
                  ]
        for query in queries:          
            response = requests.get(BASE + f"{query}")
            self.assertEqual(response.status_code, 404, f"TestCase: {query} - Should be 404")
            #self.assertEqual(response.json(), {'message': 'user does not exit...'}, "Should be {'message': 'user does not exit...'}")


if __name__ == '__main__':
    unittest.main()

