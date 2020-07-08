# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http.request import Request
from datetime import datetime
from superbet_speciale.items import DaNuItem, InainteDupaItem, F1x2Item, TotaluriItem

class SuperbetSpider(scrapy.Spider):
	name = 'spec'
	allowed_domains = ['superbet.ro']

	current_date  = datetime.today().strftime('%Y-%m-%d')
	current_time = '00:00:01'
	current_date_time = current_date + '+' + current_time
	url = 'https://offer1.superbet.ro/offer/getOfferByDate?compression=true&langId=2&controller=offer&method=getOfferByDate&preselected=true&offerState=prematch&startDate={}&endDate='
	start_urls = [url.format(current_date_time)]
	
	def parse(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		all_matches = jsonresponse.get('data')
		for x in all_matches:
			match_id = x.get('soi')
			try:
				match_id = match_id.replace('S','')
			except:
				pass
			if match_id:
				relative_url = 'https://offer-2.betting.superbet.ro/specials/getSpecialsById?specialIds={}'
				complete_url = relative_url.format(match_id)
				yield Request(complete_url, callback=self.parse_odds)
			else:
				pass
	
	def parse_odds(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		all_matches = jsonresponse.get('data')
		match_id = all_matches[0].get('matchId')
		bet_groups = all_matches[0].get('betGroups')
		for x in bet_groups:			
			# marcatori in meci
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Marcatori în meci':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					nu = odd.get('odds')[1].get('value')

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# marcatori in meci si rezultat final
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Marcatori în meci si rezultat final':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# jucatorul primeste primul cartonas galben
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Jucătorul primește cartonaș galben':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# Intervalul primului gol
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			group_name = group_name.lstrip()
			if group_name == 'Intervalul primului gol':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					minutul = odd.get('sbVal')
					inainte = odd.get('odds')[0].get('value')
					dupa = odd.get('odds')[1].get('value')

					interval_pg = InainteDupaItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						minutul = minutul,
						inainte = inainte,
						dupa = dupa
					)
					yield interval_pg

			# Final 1x2 după primele 10 minute
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Final 1x2 după primele 10 minute':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					_1 = odd.get('odds')[0].get('value')
					_x = odd.get('odds')[1].get('value')
					_2 = odd.get('odds')[2].get('value')

					_1x2 = F1x2Item(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						_1 = _1,
						_x = _x,
						_2 = _2
					)
					yield _1x2

			# Cum se marchează primul gol
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Cum se marchează primul gol':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# Primul eveniment in meci
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Primul eveniment în meci':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu


			# Condusă / Câștigă
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Condusă / Câștigă':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					_1 = odd.get('odds')[0].get('value')
					_2 = odd.get('odds')[1].get('value')


					_1x2 = F1x2Item(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						_1 = _1,
						_2 = _2
					)
					yield _1x2

			# Cine va avea
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Cine va avea':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					_1 = odd.get('odds')[0].get('value')
					try:
						_x = odd.get('odds')[1].get('value')
					except:
						_x = None
					try:
						_2 = odd.get('odds')[2].get('value')
					except:
						_2 = None

					_1x2 = F1x2Item(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						_1 = _1,
						_x = _x,
						_2 = _2
					)
					yield _1x2

			# Totaluri
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Totaluri':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					sbval = odd.get('sbVal')
					sub = odd.get('odds')[0].get('value')
					peste = odd.get('odds')[1].get('value')

					total = TotaluriItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						sbval = sbval,
						sub = sub,
						peste = peste
					)
					yield total

			# Echipa cu mai multe
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Echipa cu mai multe':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					_1 = odd.get('odds')[0].get('value')
					try:
						_x = odd.get('odds')[1].get('value')
					except:
						_x = None
					try:
						_2 = odd.get('odds')[2].get('value')
					except:
						_2 = None

					_1x2 = F1x2Item(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						_1 = _1,
						_x = _x,
						_2 = _2
					)
					yield _1x2

			# Succ.eveni. goluri / cartonașe galbene
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Succ.eveni. goluri / cartonașe galbene':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# Succ.eveni. goluri / cornere
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Succ.eveni. goluri / cornere':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# Penalti - cartonaș roșu
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Penalti - cartonaș roșu':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# Echipa marcheaza
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Echipa marcheaza':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# Posesia mingii
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Posesia mingii':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					sbval = odd.get('sbVal')
					sub = odd.get('odds')[0].get('value')
					peste = odd.get('odds')[1].get('value')

					total = TotaluriItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						sbval = sbval,
						sub = sub,
						peste = peste
					)
				yield total

			# Scor corect oricând
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'Scor corect oricând':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

			# SuperPariuri
			group_name = x.get('betGroupName')
			group_name = group_name.split('|', 1)[1]
			group_name = group_name.split('|', 1)[0]
			if group_name == 'SuperPariuri':
				odd_types = x.get('oddTypes')

				for odd in odd_types:
					odd_name = odd.get('oddTypeName')
					odd_name = odd_name.split('|', 1)[1]
					odd_name = odd_name.split('|', 1)[0]

					da = odd.get('odds')[0].get('value')
					try:
						nu = odd.get('odds')[1].get('value')
					except:
						nu = None

					danu = DaNuItem(
						s_id = match_id,
						group_name = group_name,
						odd_name = odd_name,
						da = da,
						nu = nu
					)
					yield danu

	# def parse_odds(self, response):
	# 	jsonresponse = json.loads(response.body_as_unicode())
	# 	all_matches = jsonresponse.get('data')
	# 	match_id = all_matches[0].get('matchId')
	# 	bet_groups = all_matches[0].get('betGroups')
	# 	for x in bet_groups:			
	# 		# marcatori in meci
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Marcatori în meci':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				nu = odd.get('odds')[1].get('value')

	# 				marcatori_meci = SpecMarcatoriInMeci(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield marcatori_meci

	# 		# marcatori in meci si rezultat final
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Marcatori în meci si rezultat final':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				marcatori_rez_final = SpecMarcatoriInMeciSiRezultatFinal(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield marcatori_rez_final

	# 		# jucatorul primeste primul cartonas galben
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Jucătorul primește cartonaș galben':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				jucator_pgalben = SpecJucatorPrimulGalben(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield jucator_pgalben

	# 		# Intervalul primului gol
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		group_name = group_name.lstrip()
	# 		if group_name == 'Intervalul primului gol':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				minutul = odd.get('sbVal')
	# 				inainte = odd.get('odds')[0].get('value')
	# 				dupa = odd.get('odds')[1].get('value')

	# 				interval_pg = SpecIntervalPrimulGol(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					minutul = minutul,
	# 					inainte = inainte,
	# 					dupa = dupa
	# 				)
	# 				yield interval_pg

	# 		# Final 1x2 după primele 10 minute
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Final 1x2 după primele 10 minute':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				_1 = odd.get('odds')[0].get('value')
	# 				_x = odd.get('odds')[1].get('value')
	# 				_2 = odd.get('odds')[2].get('value')

	# 				_1x210min = Spec1x210min(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					_1 = _1,
	# 					_x = _x,
	# 					_2 = _2
	# 				)
	# 				yield _1x210min

	# 		# Cum se marchează primul gol
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Cum se marchează primul gol':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				cum_pg = SpecCumSeMarcheazaPg(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield cum_pg

	# 		# Primul eveniment in meci
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Primul eveniment în meci':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				prim_eveniment = SpecPrimulEveniment(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield prim_eveniment


	# 		# Condusă / Câștigă
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Condusă / Câștigă':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				_1 = odd.get('odds')[0].get('value')
	# 				_2 = odd.get('odds')[1].get('value')


	# 				condusa_castiga = SpecCondusaCastiga(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					_1 = _1,
	# 					_2 = _2
	# 				)
	# 				yield condusa_castiga

	# 		# Cine va avea
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Cine va avea':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				_1 = odd.get('odds')[0].get('value')
	# 				try:
	# 					_x = odd.get('odds')[1].get('value')
	# 				except:
	# 					_x = None
	# 				try:
	# 					_2 = odd.get('odds')[2].get('value')
	# 				except:
	# 					_2 = None

	# 				cine_avea = SpecCineVaAvea(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					_1 = _1,
	# 					_x = _x,
	# 					_2 = _2
	# 				)
	# 				yield cine_avea

	# 		# Totaluri
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Totaluri':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				sbval = odd.get('sbVal')
	# 				sub = odd.get('odds')[0].get('value')
	# 				peste = odd.get('odds')[1].get('value')

	# 				totaluri = SpecTotaluri(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					sbval = sbval,
	# 					sub = sub,
	# 					peste = peste
	# 				)
	# 				yield totaluri

	# 		# Echipa cu mai multe
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Echipa cu mai multe':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				_1 = odd.get('odds')[0].get('value')
	# 				try:
	# 					_x = odd.get('odds')[1].get('value')
	# 				except:
	# 					_x = None
	# 				try:
	# 					_2 = odd.get('odds')[2].get('value')
	# 				except:
	# 					_2 = None

	# 				mai_multe = SpecEchipaCuMaiMulte(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					_1 = _1,
	# 					_x = _x,
	# 					_2 = _2
	# 				)
	# 				yield mai_multe

	# 		# Succ.eveni. goluri / cartonașe galbene
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Succ.eveni. goluri / cartonașe galbene':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				gol_cartonas = SpecSucGoluriCartonase(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield gol_cartonas

	# 		# Succ.eveni. goluri / cornere
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Succ.eveni. goluri / cornere':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				gol_corner = SpecSucGoluriCornere(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield gol_corner

	# 		# Penalti - cartonaș roșu
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Penalti - cartonaș roșu':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				penalty_rosu = SpecPenaltyRosu(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield penalty_rosu

	# 		# Echipa marcheaza
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Echipa marcheaza':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				echipa_marcheaza = SpecEchipaMarcheaza(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield echipa_marcheaza

	# 		# Posesia mingii
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Posesia mingii':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				sbval = odd.get('sbVal')
	# 				sub = odd.get('odds')[0].get('value')
	# 				peste = odd.get('odds')[1].get('value')

	# 				posesie = SpecPosesie(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					sbval = sbval,
	# 					sub = sub,
	# 					peste = peste
	# 				)
	# 				yield posesie

	# 		# Scor corect oricând
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'Scor corect oricând':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				sc_oricand = SpecScorCorectOricand(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield sc_oricand

	# 		# SuperPariuri
	# 		group_name = x.get('betGroupName')
	# 		group_name = group_name.split('|', 1)[1]
	# 		group_name = group_name.split('|', 1)[0]
	# 		if group_name == 'SuperPariuri':
	# 			odd_types = x.get('oddTypes')

	# 			for odd in odd_types:
	# 				odd_name = odd.get('oddTypeName')
	# 				odd_name = odd_name.split('|', 1)[1]
	# 				odd_name = odd_name.split('|', 1)[0]

	# 				da = odd.get('odds')[0].get('value')
	# 				try:
	# 					nu = odd.get('odds')[1].get('value')
	# 				except:
	# 					nu = None

	# 				superpariuri = SpecSuperPariuri(
	# 					s_id = match_id,
	# 					group_name = group_name,
	# 					odd_name = odd_name,
	# 					da = da,
	# 					nu = nu
	# 				)
	# 				yield superpariuri
