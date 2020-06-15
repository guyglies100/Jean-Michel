from requests import Request, Session
import json
from time import sleep
import functions as fct
refresh_time_in_sec =120

#Étienne Lepage-Lepitre

def get_grille_de_note(username, password):
  login_url = "https://cas.usherbrooke.ca/login"
  login_payload = '_eventId=submit&execution=75731e30-8af8-40e8-8c78-ac5d0b28f7a4_ZXlKbGJtTWlPaUpCTVRJNFIwTk5JaXdpWVd4bklqb2laR2x5SW4wLi5fdUFZWXNxMGtsX284WVdrLkgzMG00ZUlTNHBFX1VhX2dNcTZwOXA4YmFuMVhWLXFmOFEteU9iTTdjZDAtZFZZSXF0c3pBVGJOSER0OHc3YnVlRFM0cG81RDhkY0tVd2xWTk5lWG4wdXI5RHczZlRFUkF3aGxUZnkwdkxTS0xTODNiZloyN2tadmlfRU9qdjRPUHpCWVFWM1QzQ2J2Tm8wUFRsd0N4QnZIZlJreTI2aG85WVp2a09MbWt1WjFERldpSG1VLV9xcnV0bk9xeEJIRG1aREFfYkJhUFF1eHJaMkVhb1oxX3lWNXdGZDRab2pWUlhfSm8yNVpvLVY1bHhCdzYtbDFDWEVOVlRUYm8xbm8yeWZUM1VBZnE5RTNQMm0xMkE4cDZ3b19pTUxzdnhoWHVtcDdJa2EzTXdUZEhvcWYxSGc3NzFsZ1FjVjdTUlllQlp6X3hrSXBQcTlBcl8xM0dnU184blpjNm1qbE1TbEVNN241U2w4VjNMWnY4dG5XUkVQa3Q0SHZ2OW5XazllZU5LNDZfX3NhQ2FTanU2aVNzV0tTcngwSy1zRlc0SnZXRDEtVjFEa0gwYW9qT0ZiNzRIMjZBU1h4c3NMRC1PLThFVU00Z0pJd3ZTT1RPVXNCZzNoTk9hX1JuY1pmU1BwRHdOX1dFNEJKNnpGM1F2UEpIbnhuVG5adTFRaXlSSWxaRklDTlhMcFJYdWlnT3dlRXVhY195ZHdNbl9hVHVCQnVjb1RJU0w2RjFSVVhqeXgwNmgtSGdubDdjUEY4UzQwdW5zOUg4QkxHWlpTelczVWxvWjNtajl0Wk8yS19rWnowYkhaOExxQ3FnU3REOTdJVWp5bjM4THlqYkVEaGNpLWlRdGJjZUtvVHpZX1J2M3NYWWNNM090X0Z5eUtOT25ydDdPSlQ5NXNYc0ppRUxDQWU3cVF3RWdxamUxMDZ0SDgzTDVPbzdyRktXQ3NNbW5IOV9MQzlDcnpFVzB5QTlXeGlQNUo1dkpEZXpqc1V1MGM0Um0xSzhsVENpQ1pGelFqY2gxV0VhT0xzcFFXdndRSlpSLWlwT0lHTVJreUItd0diVjB2ZFJIb1JwVWZrRmJiZXpTd094OWhuU2NtbDB3YmUtMUNLelhOSmlhVHVLbkpZLUxwTTZGMGZ5ekhZQVFJdmQtNENWWGpOSFk5My03SEtMZXdaX0lXNGhDUEthU1pHZVJCSzBWSHdRWEl4ZG1LVmF3MjVBV2gyOEtXZnZyeVR1SXlnaHFRV3lLcmVodGVZaTJHOG5RbFdTNzV4X1o4bnMySnd1ZnVWaktnM0NGbW1CZHhJczRtZzBFZFIxUHYtc0tCeWp4U3AycERNVlNhUlgyYzNfS1llRTFGTnFjX0xVNU9kaVIzblowVnhFMHpwYmdDME1pSEw3Y3NrVjZPSklzUS5oaVp1RjI5M1dybW9HRDdyMTRVTC13&lt=LT-11165-IpmazbRvxP4RB5bpI7Tn2grJRkipi3-n3&password='+password+'&submit=&username='+username
  login_headers = {
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://cas.usherbrooke.ca',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  note_url = "https://www.gel.usherbrooke.ca/grille-notes/?trimestre=e20"
  note_payload = {}
  note_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Accept': '*/*'
  }
  s = Session()
  login_req = Request("POST", login_url, headers=login_headers, data = login_payload)
  login_prepped = s.prepare_request(login_req)
  login_resp = s.send(login_prepped)
  note_req = Request("POST", note_url, headers=note_headers, data = note_payload)
  note_prepped = s.prepare_request(note_req)
  note_resp = s.send(note_prepped)
  return json.loads(note_resp.text.encode('utf8'))

def check_for_nouvelles_notes(grille_actuelle, grille_ancienne):
  fct.log(grille_actuelle)
  fct.log(grille_ancienne)
  nouvelles_notes = []
  for index_cours, cours in enumerate(grille_actuelle):
    for index_evaluation, evaluation in enumerate(cours["evaluations"]):
      if(evaluation["avg"] != None and grille_ancienne[index_cours]["evaluations"][index_evaluation]["avg"] == None):
        nouvelles_notes.append(cours["ap"])
  return nouvelles_notes