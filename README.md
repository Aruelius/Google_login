# Google_login
YouTube，Google，Gmail ...  Google Family Bucket.

## How to use
1. Open ``google_login.py``
2. Change the following three values
~~~python
self.identifier = ""
self.username = ""
self.password = ""
~~~
>The ``username`` is your Google Account.  
>Of course the ``password`` is your Google Account Password.  

## How to get **identifier**
1. Open [Youtube Login URL](https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dzh-CN%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=zh-CN&ec=65620)
2. Input your Gmail or another mail address.
3. Click Next.
4. Press <kbd>F12</kbd> and open **Console**.
5. Paste this code to **Console**.
```JavaScript
window.botguard.bg(JSON.parse('[' + document.querySelector('[data-initial-setup-data]').dataset.initialSetupData.substr(4))[18], void 0).invoke(null, false, {})
```
6. The result is **identifier**, copy it to ``google_login.py``.

## attention
**identifier** is tied to your account.  
So if you change your ``username``, please make sure also change the **identifier**.  
The **identifier** seem to not expire. I don't test it.  
At your first login, maybe need verification, and we only support SMS verification, it won't be after.
