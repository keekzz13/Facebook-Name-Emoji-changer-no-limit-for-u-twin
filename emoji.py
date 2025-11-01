import requests, json, re, uuid, time, os, sys

R = '\033[1;91m'; V = '\033[1;92m'; B = '\033[1;97m'; S = '\033[0m'; C = '\033[96m'
v = '\033[7;92m'

logo = f'''

{V} ███████╗███╗░░░███╗░█████╗░░░░░░██╗██╗       Made
{R} ██╔════╝████╗░████║██╔══██╗░░░░░██║██║         by
 █████╗░░██╔████╔██║██║░░██║░░░░░██║██║          zvynx
{C} ██╔══╝░░██║╚██╔╝██║██║░░██║██╗░░██║██║
{S} ███████╗██║░╚═╝░██║╚█████╔╝╚█████╔╝██║
{B} ╚══════╝╚═╝░░░░░╚═╝░╚════╝░░╚════╝░╚═╝{S}'''

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def base_headers(cookie):
    return {
        "Host": "accountscenter.facebook.com",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/137.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-User": "?1"
    }

def checking(cookie):
    try:
        r = requests.get(
            "https://accountscenter.facebook.com/profiles",
            headers=base_headers(cookie),
            allow_redirects=True
        )
        if r.url != "https://accountscenter.facebook.com/profiles":
            return {"status":"fail","message":"Cookie Invalid or Expired"}
        html = r.text.replace("\\","")
        ig = re.search(r'"identity_type"\s*:\s*"IG_USER".*?"username"\s*:\s*"([^"]+)"', html)
        uid = re.search(r'"actorID"\s*:\s*"(\d+)"', html)
        if not ig: return {"status":"fail","message":"Instagram Account Not Linked"}
        if not uid: return {"status":"fail","message":"Failed to get user_id"}
        return {"status":"success","uid":uid.group(1),"ig_uname":ig.group(1)}
    except requests.ConnectionError:
        return {"status":"fail","message":"Connection Error"}

def step1(cookie, uid):
    try:
        r = requests.get(
            f"https://accountscenter.facebook.com/connected_experiences/single_sign_on_dialog/{uid}",
            headers=base_headers(cookie), timeout=30
        )
        html = r.text.replace("\\","")
        dtsg = re.search(r'\["DTSGInitialData".*?"token"\s*:\s*"([^"]+)"', html)
        lsd = re.search(r'\["LSD".*?"token"\s*:\s*"([^"]+)"', html)
        igv2 = re.search(r'"__typename"\s*:\s*"XFBFXIGAccountInfo".*?"id"\s*:\s*"(\d+)"', html)
        if not all([dtsg, lsd, igv2]): return {"status":"fail","message":"Cookie Invalid or Expired"}
        return {"status":"success","DTSG":dtsg.group(1),"LSD":lsd.group(1),"fbid_v2":igv2.group(1)}
    except requests.ConnectionError:
        return {"status":"fail","message":"Connection Error"}

def step2(cookie, uid, DTSG, LSD):
    try:
        var = {"input":{"client_mutation_id":"1","actor_id":uid,
                       "enable_share_all_logins":False,"fdid":"device_id_fetch_datr"}}
        data = {
            "locale":"en_US","__user":uid,"fb_dtsg":DTSG,"lsd":LSD,
            "fb_api_caller_class":"RelayModern","fb_api_req_friendly_name":"useFXSSOChangeSettingMutation",
            "server_timestamps":"true","doc_id":"9427448270675232","av":uid,
            "variables":json.dumps(var)
        }
        r = requests.post(
            "https://accountscenter.facebook.com/api/graphql",
            data=data, headers={**base_headers(cookie),"Content-Type":"application/x-www-form-urlencoded"}
        ).json()
        return {"status":"success"} if "FXCALSettingsMutationReturnDataSuccessWithNodeConfig" in str(r) else {"status":"fail","message":"Please re-link Your Instagram Account"}
    except requests.ConnectionError:
        return {"status":"fail","message":"Connection Error"}

def enable_sso(cookie, uid, DTSG, LSD, fbid_v2, direction):
    initiator = {"id":uid, "type":"FACEBOOK"} if direction=="FB2IG" else {"id":fbid_v2,"type":"INSTAGRAM"}
    target = {"id":fbid_v2, "type":"INSTAGRAM"} if direction=="FB2IG" else {"id":uid, "type":"FACEBOOK"}
    var = {"input":{"client_mutation_id":"1","actor_id":uid,
                    "enable_sso":True,"initiator_account":initiator,
                    "target_account":target,"fdid":"device_id_fetch_datr"}}
    data = {
        "locale":"en_US","__user":uid,"fb_dtsg":DTSG,"lsd":LSD,
        "fb_api_caller_class":"RelayModern","fb_api_req_friendly_name":"useFXSSOChangeDirectionalSSOMutation",
        "server_timestamps":"true","doc_id":"9253258021410000","av":uid,
        "variables":json.dumps(var)
    }
    r = requests.post(
        "https://accountscenter.facebook.com/api/graphql",
        data=data, headers={**base_headers(cookie),"Content-Type":"application/x-www-form-urlencoded"}
    ).json()
    if "FXCALSettingsMutationErrorRequiresReauth" in str(r):
        return {"status":"fail","message":"Please re-link accounts"}
    if "updated_node" in str(r) and "advanced_sso_settings" in str(r):
        return {"status":"success"}
    return {"status":"fail","message":"An unknown error occurred"}

def step5(cookie, uid, DTSG, LSD, fbid_v2, name):
    var = {
        "client_mutation_id": str(uuid.uuid4()),
        "family_device_id": "device_id_fetch_datr",
        "identity_ids": [fbid_v2],
        "full_name": name, "first_name": name,
        "middle_name": "", "last_name": "",
        "interface": "FB_WEB"
    }
    data = {
        "locale":"en_US","fb_api_caller_class":"RelayModern",
        "fb_dtsg":DTSG,"lsd":LSD,"fb_api_req_friendly_name":"useFXIMUpdateNameMutation",
        "variables":json.dumps(var),"av":uid,"__user":uid,
        "server_timestamps":"true","doc_id":"28573275658982428"
    }
    r = requests.post(
        "https://accountscenter.facebook.com/api/graphql",
        data=data, headers={**base_headers(cookie),"Content-Type":"application/x-www-form-urlencoded"}
    ).json()
    if "fxim_update_identity_name" in str(r):
        return {"status":"success"}
    if "Please try again later." in str(r):
        return {"status":"fail","message":"Rate-limit – try later"}
    return {"status":"fail","message":"IG update failed"}

def step6(cookie, uid, DTSG, LSD, fbid_v2):
    var = {
        "client_mutation_id": str(uuid.uuid4()),
        "accounts_to_sync": [fbid_v2, uid],
        "resources_to_sync": ["NAME","PROFILE_PHOTO"],
        "resources_to_unsync": None,
        "scale": 3,
        "source_of_truth_array": [{"resource_source":"IG"},{"resource_source":"FB"}],
        "source_account": uid,
        "family_device_id": "device_id_fetch_datr",
        "username_unsync_params": None,
        "platform": "FACEBOOK",
        "sync_logging_params": {"client_flow_type":"IM_SETTINGS"},
        "interface": "FB_WEB",
        "feta_profile_sync": False
    }
    data = {
        "locale":"en_US","fb_dtsg":DTSG,"__user":uid,
        "variables":json.dumps(var),"av":uid,
        "fb_api_req_friendly_name":"useFXIMUpdateNameMutation",
        "fb_api_caller_class":"RelayModern",
        "server_timestamps":"true","doc_id":"9388416374608398"
    }
    r = requests.post(
        "https://accountscenter.facebook.com/api/graphql",
        data=data, headers={**base_headers(cookie),"Content-Type":"application/x-www-form-urlencoded"}
    ).json()
    if "fxim_update_name" in str(r) or ("updated_node" in str(r) and "FXCALSettingsMutationError" not in str(r)):
        return {"status":"success"}
    if "Please try again later." in str(r):
        return {"status":"fail","message":"Rate-limit – try later"}
    return {"status":"fail","message":"Sync failed"}

def step7(cookie, uid, DTSG, LSD, name):
    var = {
        "client_mutation_id": str(uuid.uuid4()),
        "family_device_id": "device_id_fetch_datr",
        "identity_ids": [uid],
        "full_name": name, "first_name": name,
        "middle_name": "", "last_name": "",
        "interface": "FB_WEB"
    }
    data = {
        "locale":"en_US","fb_api_caller_class":"RelayModern",
        "fb_dtsg":DTSG,"lsd":LSD,"fb_api_req_friendly_name":"useFXIMUpdateNameMutation",
        "variables":json.dumps(var),"av":uid,"__user":uid,
        "server_timestamps":"true","doc_id":"28573275658982428"
    }
    r = requests.post(
        "https://accountscenter.facebook.com/api/graphql",
        data=data, headers={**base_headers(cookie),"Content-Type":"application/x-www-form-urlencoded"}
    ).json()
    return {"status":"success"} if "fxim_update_identity_name" in str(r) else {"status":"fail","message":"FB direct update failed"}

def main():
    clear(); print(logo); print()
    cookie = input(f"{B}[{R}?{B}] Facebook Cookie: {V}")
    clear(); print(logo); print()
    print(f"{B}[+] Verifying cookie...{S}")
    chk = checking(cookie)
    if chk["status"] != "success":
        print(f"{B}[{R}x{B}] {chk['message']}{S}"); exit()
    uid = chk["uid"]
    print(f"{B}[{V}Success{B}] Cookie OK – UID {uid}{S}")
    print(f"{B}[+] Grabbing tokens...{S}")
    s1 = step1(cookie, uid)
    if s1["status"] != "success":
        print(f"{B}[{R}x{B}] {s1['message']}{S}"); exit()
    DTSG, LSD, fbid_v2 = s1["DTSG"], s1["LSD"], s1["fbid_v2"]
    step2(cookie, uid, DTSG, LSD)
    print(f"{B}[+] Enabling SSO (FB to IG)...{S}")
    if enable_sso(cookie, uid, DTSG, LSD, fbid_v2, "FB2IG")["status"] != "success":
        print(f"{B}[{R}x{B}] SSO FB to IG failed – try manual linking{S}"); exit()
    print(f"{B}[+] Enabling SSO (IG to FB)...{S}")
    if enable_sso(cookie, uid, DTSG, LSD, fbid_v2, "IG2FB")["status"] != "success":
        print(f"{B}[{R}x{B}] SSO IG to FB failed – try manual linking{S}"); exit()
    while True:
        name = input(f"{B}({V}+{B}) New name (emoji OK): {C}").strip()
        if len(name) >= 1: break
        print(f"{B}[{R}x{B}] Minimum 1 character{S}")
    print(f"{B}[+] Updating Instagram name...{S}")
    if step5(cookie, uid, DTSG, LSD, fbid_v2, name)["status"] != "success":
        print(f"{B}[{R}x{B}] Instagram update failed{S}"); exit()
    print(f"{B}[+] Syncing name to Facebook...{S}")
    time.sleep(2)
    sync_res = step6(cookie, uid, DTSG, LSD, fbid_v2)
    if sync_res["status"] != "success":
        print(f"{B}[!] Sync didn’t confirm – forcing direct FB update...{S}")
        fb_res = step7(cookie, uid, DTSG, LSD, name)
        if fb_res["status"] != "success":
            print(f"{B}[{R}x{B}] Both sync & direct FB failed to {fb_res.get('message','unknown')}{S}"); exit()
    print(f"{v} Name changed successfully!{S}")
    print(f"{B}[{V}Success{B}] Current name: {name}{S}")

if __name__ == "__main__":
    main()
