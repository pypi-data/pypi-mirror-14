from cantools.web import respond, succeed, fail, cgi_get
from cantools.db import get, get_multi, get_schema, get_page, edit
from cantools import config
import model # load up all models (for schema)

def response():
	action = cgi_get("action", choices=["schema", "get", "edit", "delete"])

	# edit/delete always require credentials; getters do configurably
	if not config.db.public or action in ["edit", "delete"]:
		if cgi_get("pw") != config.admin.pw:
			fail("wrong")

	if action == "schema":
		succeed(get_schema())
	elif action == "get":
		mname = cgi_get("modelName", required=False)
		keys = cgi_get("keys", required=False)
		if mname:
			succeed(get_page(mname, cgi_get("limit"), cgi_get("offset"),
				cgi_get("order", default="index"), cgi_get("filters", default={})))
		elif keys:
			succeed([d.data() for d in get_multi(keys)])
		else:
			succeed(get(cgi_get("key")).data())
	elif action == "edit":
		succeed(edit(cgi_get("data")).data())
	elif action == "delete":
		get(cgi_get("key")).rm()
		succeed()

respond(response)