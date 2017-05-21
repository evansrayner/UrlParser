from urlparser import urlparser
import json


def test_validate_image():
	assert urlparser.validate_image('aksbfkjsbd.jpg') == False
	assert urlparser.validate_image(
		'http://ichef.bbci.co.uk/onesport/cps/800/cpsprodpb'
		'/E13E/production/_96126675_kane2.jpg'
		) == True


def test_find_from_srcset():
	assert urlparser.find_from_srcset(
		'images/space-needle.jpg 200w, images/space-needle-2x.jpg'
		'400w, images/space-needle-hd.jpg 600w'
		) == 'images/space-needle-hd.jpg'
	assert urlparser.find_from_srcset(None) == None


def test_find_images():
	pass


def test_generate_content():
	assert urlparser.generate_content([
		'http://www.bbc.co.uk/sport/football/39981950'
		]) == json.dumps([
			{
				'url': 'http://www.bbc.co.uk/sport/football/39981950',
				'headline': 'Harry Kane: Tottenham striker targets 100'
				' league goals by end of 2017-18 - BBC Sport',
				'images': [{
					'http://ichef.bbci.co.uk/onesport/cps/480/cpsprodpb'
					'/E13E/production/_96126675_kane2.jpg': {
						'url': 'http://ichef.bbci.co.uk/onesport/cps/480'
						'/cpsprodpb/E13E/production/_96126675_kane2.jpg',
						'caption': 'Harry Kane is aiming to win the golden'
						' boot for the second time in succession this season'
					}
				}]
			}
		])