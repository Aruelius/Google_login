import json
import os
import re

import requests


class Google(object):
    def __init__(self):
        """
        identifier is very very important!!!
        identifier is very very important!!!
        identifier is very very important!!!
        The important thing should say three times.
        """
        self.identifier = ""
        self.username = ""
        self.password = ""
        self.session = requests.session()
        self.session.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        })
        self.sms_url = lambda sms_tl: f"https://accounts.google.com/_/signin/selectchallenge?hl=en&TL={sms_tl}"
        self.challenge_url = lambda TL: f"https://accounts.google.com/_/signin/challenge?hl=en&TL={TL}"
        self.SERVICE = "youtube"
        self.YOUTUBE_URL = "https://www.youtube.com"
        self.LOOKUP_URL = "https://accounts.google.com/_/lookup/accountlookup?hl=zh-CN"
        self.SERVICE_LOGIN_URL = "https://accounts.google.com/ServiceLogin"
        self.CONTINUE_URL = "https://www.youtube.com/signin?action_handle_signin=true&app=desktop&hl=zh-CN&next=https%3A%2F%2Fwww.youtube.com%2F"

    def req(self, url: str, f_req: list, xsrf: str, bghash=None):
        data = {
            "continue": self.CONTINUE_URL,
            "service": self.SERVICE,
            "hl": "zh-CN",
            "f.req": json.dumps(f_req),
            "bgRequest": json.dumps(["identifier", self.identifier]),
            # 'at': xsrf,
            "azt": xsrf,
            "deviceinfo": json.dumps([None,None,None,[],None,"US",None,None,[],"GlifWebSignIn",None,[None,None,[],None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,[],None,None,None,[],[]],None,None,None,None,2])
        }
        if bghash: data["bghash"] = bghash
        r = self.session.post(
            url=url,
            data=data
        )
        response = json.loads(r.text.replace(")]}'",""))
        return response

    def service_login(self):
        r = self.session.get(
            url=self.SERVICE_LOGIN_URL,
            params={
                "service": self.SERVICE,
                "continue": self.CONTINUE_URL,
                "hl": "zh-CN",
            }
        ).text
        xsrf = re.findall(r"window.WIZ_global_data = (.+?);", r)[0].split('"')[10].replace("\\", "")
        config_list = re.findall(r'data-initial-setup-data="%(.*?);]', r, re.S)[0].replace("&quot", '"').split('";')
        bghash = config_list[-1][:-2]
        user_hash = config_list[3]
        self.session.headers.update({
            "google-accounts-xsrf": "1",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8"
        })
        return xsrf, bghash, user_hash

    def account_lookup(self):
        xsrf, bghash, user_hash = self.service_login()
        lookup_req = [
            self.username, user_hash, [],
            None, "US", None, None, 2, False, True, [None,None,[2,1,None,1,"https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=True&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3DTrue%26app%3Ddesktop%26hl%3Dzh-CN%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=zh-CN&ec=65620",None,[],4,[],"GlifWebSignIn",None,[]],1,[None,None,[],None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,[],None,None,None,[],[]],None,None,None,True],self.username,None,None,None,True,True,[]
        ]
        response = self.req(self.LOOKUP_URL, lookup_req, xsrf)
        try:
            TL = response[1][-1]
        except IndexError:
            print("identifier invalid")
            os._exit(0)
        return TL, xsrf, bghash, response[0][2]

    def send_sms(self, sms_tl: str, xsrf: str):
        """
        ONLY SUPPORT SMS VERIFICATION
        """
        sms_req = [
            3, "SMS", None, None, [
                9, None, None, None, None, None, None, None,
                ['SMS']
            ]
        ]
        response = self.req(self.sms_url(sms_tl), sms_req, xsrf)
        if "SEND_SUCCESS" in response:
            print("SEND_SUCCESS")
            return response[0][1][-1]
        else:
            print(response)

    def login(self):
        challenge_tl, xsrf, bghash, user_hash = self.account_lookup()
        challenge_req = [
            user_hash, None, 1, None, [
                1 ,None ,None ,None , [
                    self.password ,None, True
                ]
            ]
        ]
        response = self.req(self.challenge_url(challenge_tl), challenge_req, xsrf)
        if "LoginDoneHtml" in str(response):
            self.session.get(response[0][-1][2])
            # Now the login is successful, you can do everything you want.

        elif "LOGIN_CHALLENGE" in str(response) and "SMS" in str(response):
            print("need verification...")
            sms_tl = response[0][1][-1]
            for challenge in response[0][0][-1][0]:
                for k, v in challenge[-1].items():
                    print(k, v)
            sms_challenge_tl = self.send_sms(sms_tl, xsrf)
            sms_code = input("SMS verification code:")
            sms_challenge_req = [
                user_hash, None, 3, None, [
                    9, None, None, None, None, None, None, None, [
                        None, sms_code, None, 2
                    ]
                ]
            ]
            response = self.req(
                self.challenge_url(sms_challenge_tl),
                sms_challenge_req, xsrf, bghash
            )
            print(response)

if __name__ == "__main__":
    google = Google()
    google.login()
