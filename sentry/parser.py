
import re, sys, logging
from sentry import rules

log = logging.getLogger(__name__)

# block ^(.*)exmaple.xxx
RE_BLOCK = re.compile(r'^block (?P<domain>.*)$',flags=re.MULTILINE)

# log ^(.*)example.com
RE_LOG = re.compile(r'^log (?P<domain>.*)$',flags=re.MULTILINE)

# redirect ^(.*)google.com to nytimes.com
RE_REDIRECT = re.compile(r'^redirect (?P<domain>.*) to (?P<destination>.*)$',flags=re.MULTILINE)

## future ideas (not yet implemented in the rule language)

# redirect ^(.*)example.com to nytimes.com using A
# redirect ^(.*)example.com to nytimes.com using CNAME
# rewrite ^(.*)example.com using REGEX
# resolve ^(.*)example.com using 1.1.1.1

def parse(settings):
	ruleset = []	
	
	for line in settings['rules']:
		log.debug('parsing: %s' % line)
		
		# block
		match = RE_BLOCK.search(line)		
		if match is not None:
			try:
				log.debug('found block rule, processing it')
				domain = match.group('domain').strip()
				ruleset.append(rules.BlockRule(settings,domain))
			except Exception as e:
				log.error('syntax error in line: %s - skipping' % line)	
				log.exception(e)
		# log
		match = RE_LOG.search(line)		
		if match is not None:
			try:
				log.debug('found logging rule, processing it')
				domain = match.group('domain').strip()
				ruleset.append(rules.LoggingRule(settings, domain))
			except Exception as e:
				log.error('syntax error in line: %s - skipping' % line)	
				log.exception(e)

		# redirect
		match = RE_REDIRECT.search(line)		
		if match is not None:
			try:
				log.debug('found redirect rule, processing it')
				domain = match.group('domain').strip()
				destination = match.group('destination').strip()
				ruleset.append(rules.RedirectRule(settings, domain,destination))
			except Exception as e:
				log.error('syntax error in line: %s - skipping' % line)	
				log.exception(e)

	return ruleset

