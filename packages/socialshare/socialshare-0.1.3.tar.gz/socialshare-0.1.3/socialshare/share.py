import requests
import json
import webbrowser
from twython import *

linkedin_share_url = 'https://api.linkedin.com/v1/people/~/shares' ## https://developer.linkedin.com/docs/share-on-linkedin


def linkedin_makerequest(method, url, access_token ,data=None, params=None, headers=None, timeout=60):
	headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
	params = {}
	kw = dict(data=data, params=params, headers=headers, timeout=timeout)
	params.update({'oauth2_access_token': access_token})
	return requests.request(method.upper(), url, **kw)   

'''
Linkedin share done with user accesstoken 

  params = {
		'comment':comment,
		'content': {
		'title': title,
		'submitted-url':submitted_url,
		'submitted-image-url':image_url,
		'description': description,
	},
	'visibility': {
		'code': 'anyone'
	}
	}

'''
def linkedin_share(params=None,access_token=None):
	response = {}
	if not access_token:
		response['status'] = "error" 
		response['reason'] = " Access Token Is Missing"
		return response
	try:
		response = linkedin_makerequest('POST', linkedin_share_url, access_token,data=json.dumps(params))
		response = response.json()
		return response
	except Exception, e:
		return str(e)


def facebook_share(params=None,access_token=None):

	'''
	reffer this url for more :https://developers.facebook.com/docs/graph-api/reference/v2.5/post
	params = {'message':'your own message','link':'image link[make sure the url]',
	'caption':'Caption','description':'Description','created_time'://current date}

	example:

	 params = {'message':'testingsdaasdsas dpurposesadasdasd cxzdxccz',
	 'link':'https://www.google.co.in/search?q=image+urls&client=ubuntu&espv=2&biw=
	 1321&bih=659&tbm=isch&imgil=txwjc-7_VXgu6M%253A%253BqBUqJmC01s01SM%253B
	 http%25253A%25252F%25252Fwww.them.pro%25252Furls&source=iu&pf=m&fir=txwjc-7_V
	 Xgu6M%253A%252CqBUqJmC01s01SM%252C_&usg=__XvufNGLhjxR9fdMfkXoBTSsPPQE%3D&ved=
	 0ahUKEwjxnpi8prXLAhWKkI4KHQqnApsQyjcIJA&ei=lPrgVvGEBYqhugSKzorYCQ#imgrc=txwjc-7_VXgu6M%3A',
	'caption':'sadtestin caption','description':'testcaption','created_time':datetime.datetime.now()}

	'''
	response = {}
	if not access_token:
		response['status'] = "error"
		response['reason'] = " Access Token Is Missing"
		return response

	facebook_share_url = ( "https://graph.facebook.com/me/feed?" +"access_token=" + access_token )
	try:
		response = requests.post(facebook_share_url,params=params)
		response = response.json()
		return response
	except Exception, e:
		return str(e)

'''
google will not provideing API for share the content into user stream(wall) 

read more:http://stackoverflow.com/questions/7570327/how-to-post-in-google-plus-wall

'''
def google_share(share_url=None):
	response = {}
	try:
		request = requests.get(share_url)
		if request.status_code == 200:
			google_url = 'https://plus.google.com/share?url={0}&hl=en'.format(share_url)
			new = 2
			webbrowser.open(google_url,new=new)
	except Exception, e:
		return str(e)

'''
Now days twitter is not accepting the tweets from the outside the twitter server due to malicious
activities
Error Message : " Twitter API returned a 403 (Forbidden), This request looks like it might be 
automated. To protect our users from spam and other malicious activity, we can't 
complete this action right now. Please try again later."
cfg = { 
	"consumer_key"        : "*******************************************",
	"consumer_secret"     : "*******************************************",
	"access_token"        : "*******************************************",
	"access_token_secret" : "********************************************" 
	}
'''
def twitter_share(params=None):
	cfg = params
	if cfg['consumer_key'] and cfg['consumer_secret'] and cfg['access_token'] and cfg['access_token_secret'] and cfg['status'] is not None:
		twitter = Twython(app_key= cfg['consumer_key'],
			app_secret= cfg['consumer_secret'],
			oauth_token= cfg['access_token'],
			oauth_token_secret= cfg['access_token_secret'])
		try:
			twitter_res = twitter.update_status(status=cfg['status'])
		except TwythonError,e:
			return (str(e))
	else:
		response = {}
		response['error'] = [' parameter Missing '] 
		return response







