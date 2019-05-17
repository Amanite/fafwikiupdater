# faf wiki unit page generator

import json, re, io
from urllib.request import urlopen


def process_url_data(url):
	# This processes the url specified and returns a dictionary with the data
	response = urlopen(url)
	# Converts bytes to string type and string type to dict
	response_string = response.read().decode('utf-8')
	json_obj = json.loads(response_string)
	return json_obj


def unit_data(unit_id):
	# gets unit data, parameter is the unit ID like URL0001 for cybran acu
	unit_url = "http://direct.faforever.com/faf/unitsDB/api.php?searchunit="+unit_id
	unit_json_object = process_url_data(unit_url)
	return unit_json_object


f = open("myfile.txt", "w", encoding="utf-8")


def process_unit_data(unit_id):
	data = unit_data(unit_id)
	description = data["Interface"]["HelpText"]

	# description comes out messed up from the db so we need to clean it up

	def clean_string (s):
		a, b = s.split(">")
		return b

	faction = data["Categories"][2]
	abilities = data["Display"]["Abilities"]
	veterancy_regen = data["Buffs"]["Regen"]
	hp = data["Defense"]["Health"]
	regen_rate = data["Defense"]["RegenRate"]
	economy = data["Economy"]
	name = clean_string(data["ApiName"])
	enhancements = data["Enhancements"]
	categories = data["Categories"]

	# tech level comes out messed up too so it needs to be cleaned up

	def clean_tech_level(s):
		matches = re.findall("`d", s)
		return "Tech"+ str(matches)

	tech_level = clean_tech_level(data["General"]["TechLevel"])

	intel = data["Intel"]
	strategic_icon_name = data["StrategicIconName"]
	transport = data["Transport"]
	veterancy = data["Veteran"]
	weapons = data["Weapon"]

	def make_intro():
		f.write(("HEADER" + "The" + faction + name + "is a" + tech_level + clean_string(description)+". It has "+ hp + "health points."))


	def make_body():

		def print_economy():
			for value in economy:
				f.write((str(value) + "\n separator \n"))


		def print_weapons():
			for value in weapons:
				f.write((str(value) + "\n separator \n"))


		def print_abilities():
			for value in abilities:
				f.write(str(value) + "\n separator \n")


		def print_categories():
			for value in categories:
				f.write((str(value) + "\n separator \n"))

		print_economy()
		print_weapons()
		print_abilities()
		print_categories()
	make_intro()
	make_body()

process_unit_data("URL0001")
